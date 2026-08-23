#!/usr/bin/env python3
"""Merge a namespaced source SWF XML definition set into a base SWF XML.

Designed for FFDec `-swf2xml` output. The base timeline/document class remains
untouched. Source definition tags, ABC and linkage metadata are imported with a
collision-free character-ID remap and ActionScript/linkage namespace prefix.

SWF character IDs are UI16 but are not guaranteed to be dense. A simple
`base_max + offset` strategy is therefore wrong: real files contain sparse IDs,
65535 sentinels and linkage/reference fields whose numeric maxima do not describe
available character namespace. This merger instead reserves every character-like
ID used by the base and maps every source ID into unused UI16 slots.

This is a structural merge primitive, not the final campaign integration layer.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import mmap
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET


# FFDec uses several names for SWF character-definition/reference fields.
CHARACTER_ID_ATTRS = {
    "characterId", "characterID", "characterid",
    "spriteId", "spriteID",
    "shapeId", "shapeID",
    "bitmapId", "bitmapID",
    "fontId", "fontID",
    "textId", "textID",
    "soundId", "soundID",
    "buttonId", "buttonID",
    "videoId", "videoID",
    "morphShapeId", "morphShapeID",
    "binaryDataId", "binaryDataID",
}

# `tagId` is context-sensitive in FFDec XML. UnknownTag.tagId is the SWF tag
# code, not a character ID. In known tags/linkage entries (notably SymbolClass
# and ExportAssets children) it is a character reference and must be remapped.
CONTEXTUAL_CHARACTER_ID_ATTR = "tagId"

# Bitmap fill styles use UI16 65535 as a sentinel meaning "no bitmap".
CHARACTER_ID_SENTINELS = {
    "bitmapId": {65535},
    "bitmapID": {65535},
}

EXACT_IMPORT_TYPES = {
    "DoABC2Tag", "DoABCTag", "SymbolClassTag", "ExportAssetsTag",
    "DefineScalingGridTag", "CSMTextSettingsTag", "JPEGTablesTag",
}
IMPORT_PREFIXES = ("Define",)
MAX_SWF_CHARACTER_ID = 65535
# Avoid allocating 65535 even though it can be a numeric UI16 value because
# several SWF structures reserve it as a sentinel.
MAX_ALLOCATED_CHARACTER_ID = 65534


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_swf_tag_item(elem: ET.Element) -> bool:
    return local(elem.tag) == "item" and elem.attrib.get("type", "").endswith("Tag")


def should_import(tag_type: str) -> bool:
    return tag_type in EXACT_IMPORT_TYPES or tag_type.startswith(IMPORT_PREFIXES)


def is_character_sentinel(key: str, number: int) -> bool:
    return number in CHARACTER_ID_SENTINELS.get(key, set())


def is_character_id_field(elem: ET.Element, key: str) -> bool:
    if key in CHARACTER_ID_ATTRS:
        return True
    if key != CONTEXTUAL_CHARACTER_ID_ATTR:
        return False
    # UnknownTag.tagId is the numeric SWF tag code. Do not reinterpret it.
    if elem.attrib.get("type") == "UnknownTag":
        return False
    return True


def iter_top_level_tag_elements(path: Path):
    """Yield complete direct children of FFDec's `<tags>` container one at a time."""
    stack: list[str] = []
    capture_depth = 0
    context = ET.iterparse(path, events=("start", "end"))
    for event, elem in context:
        name = local(elem.tag)
        if event == "start":
            parent = stack[-1] if stack else None
            stack.append(name)
            if name == "item" and parent == "tags" and is_swf_tag_item(elem):
                capture_depth = len(stack)
        else:
            parent = stack[-2] if len(stack) >= 2 else None
            is_top = name == "item" and parent == "tags" and is_swf_tag_item(elem)
            if is_top:
                yield elem
                elem.clear()
                capture_depth = 0
            elif not capture_depth:
                elem.clear()
            stack.pop()


def character_id_inventory(path: Path) -> dict:
    """Collect all character-like IDs/references without assuming density.

    Over-reserving a harmless reference is safe; failing to reserve a real base
    reference is not. The inventory therefore scans all known character fields
    plus contextual tagId values, excluding documented sentinels/tag codes.
    """
    ids: set[int] = set()
    by_attr: dict[str, set[int]] = defaultdict(set)
    sentinel_counts: Counter = Counter()
    unknown_tag_codes: Counter = Counter()

    for _event, elem in ET.iterparse(path, events=("start",)):
        for key, value in elem.attrib.items():
            if key == CONTEXTUAL_CHARACTER_ID_ATTR and elem.attrib.get("type") == "UnknownTag":
                try:
                    unknown_tag_codes[int(value)] += 1
                except ValueError:
                    pass
                continue
            if not is_character_id_field(elem, key):
                continue
            try:
                number = int(value)
            except ValueError:
                continue
            if is_character_sentinel(key, number):
                sentinel_counts[key] += 1
                continue
            if number <= 0:
                continue
            if number > MAX_SWF_CHARACTER_ID:
                # A value larger than UI16 cannot be a valid SWF character ID.
                continue
            ids.add(number)
            by_attr[key].add(number)

    return {
        "ids": ids,
        "count": len(ids),
        "min": min(ids) if ids else None,
        "max": max(ids) if ids else None,
        "unique_by_attribute": {k: len(v) for k, v in sorted(by_attr.items())},
        "max_by_attribute": {k: max(v) for k, v in sorted(by_attr.items()) if v},
        "sentinels_ignored": dict(sentinel_counts),
        "unknown_tag_codes_ignored": dict(unknown_tag_codes),
    }


def inventory_report(inv: dict) -> dict:
    return {k: v for k, v in inv.items() if k != "ids"}


def allocate_character_id_map(base_ids: set[int], source_ids: set[int]) -> dict[int, int]:
    """Map every source ID to an unused base slot, compactly and deterministically."""
    reserved = {x for x in base_ids if 0 < x <= MAX_ALLOCATED_CHARACTER_ID}
    available = (x for x in range(1, MAX_ALLOCATED_CHARACTER_ID + 1) if x not in reserved)
    mapping: dict[int, int] = {}
    try:
        for old in sorted(source_ids):
            mapping[old] = next(available)
    except StopIteration:
        free = MAX_ALLOCATED_CHARACTER_ID - len(reserved)
        raise SystemExit(
            f"character-ID namespaces do not fit UI16: base reserves {len(reserved)} IDs, "
            f"source uses {len(source_ids)} IDs, only {free} safe slots remain"
        )
    return mapping


def load_class_map(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = data.get("classes") if isinstance(data, dict) else None
    if not isinstance(mapping, dict) or not mapping:
        raise SystemExit(f"invalid/empty class map: {path}")
    return {str(k): str(v) for k, v in mapping.items()}


class ClassRenamer:
    """Fast identifier-boundary class rewriter for FFDec scalar XML values."""

    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping
        alternatives = "|".join(re.escape(x) for x in sorted(mapping, key=len, reverse=True))
        self.pattern = re.compile(rf"(?<![A-Za-z0-9_$])({alternatives})(?![A-Za-z0-9_$])")

    def replace(self, value: str) -> tuple[str, int]:
        if value in self.mapping:
            return self.mapping[value], 1
        if len(value) > 8192:
            return value, 0
        count = 0

        def sub(match: re.Match[str]) -> str:
            nonlocal count
            count += 1
            return self.mapping[match.group(1)]

        return self.pattern.sub(sub, value), count


def transform_tree(elem: ET.Element, id_map: dict[int, int], renamer: ClassRenamer, stats: Counter) -> None:
    # FFDec serializes SymbolClass/ExportAssets character references as a
    # parallel <tags><item>text array, not as tagId attributes. Leaving those
    # raw binds imported KR1 classes onto unrelated KRF character IDs at runtime.
    if elem.attrib.get("type") in {"SymbolClassTag", "ExportAssetsTag"}:
        tags = elem.find("tags")
        if tags is not None:
            for item in tags.findall("item"):
                if item.text is None:
                    continue
                try:
                    number = int(item.text)
                except ValueError:
                    continue
                if number == 0:
                    stats["linkage_document_ids_preserved"] += 1
                elif number in id_map:
                    item.text = str(id_map[number])
                    stats["linkage_text_ids_remapped"] += 1

    for node in elem.iter():
        for key, value in list(node.attrib.items()):
            if is_character_id_field(node, key):
                try:
                    number = int(value)
                except ValueError:
                    number = 0
                if is_character_sentinel(key, number):
                    stats["id_sentinels_preserved"] += 1
                elif number > 0 and number in id_map:
                    node.attrib[key] = str(id_map[number])
                    stats["id_values_remapped"] += 1
                    continue
            # Do not globally rewrite scalar attributes. Obfuscated AS3 class
            # names can be raw words such as "false" or "dynamic"; replacing
            # those values corrupts ordinary SWF XML flags. ABC/linkage names
            # live in element text constant/name arrays and are handled below.
        if node.text and len(node.text) <= 8192:
            new_text, count = renamer.replace(node.text)
            if count:
                node.text = new_text
                stats["class_tokens_renamed"] += count


def drop_source_document_class(symbol_tag: ET.Element, stats: Counter) -> None:
    """Remove SymbolClass entries bound to character/tag 0 (source document class)."""
    tags = symbol_tag.find("tags")
    names = symbol_tag.find("names")
    if tags is not None and names is not None:
        tag_items = list(tags.findall("item"))
        name_items = list(names.findall("item"))
        if len(tag_items) != len(name_items):
            raise SystemExit("source SymbolClass tag/name arrays have different lengths")
        if any((item.text or "").strip() == "0" for item in tag_items):
            # The document-class SymbolClass block also binds the source
            # preloader shell. None of those launch-only bindings belong in the
            # Frontiers runtime, and retaining them can instantiate KR1's sealed
            # preloader clips during KRF frame construction.
            removed = len(tag_items)
            tags.clear()
            names.clear()
            stats["document_preloader_linkage_entries_removed"] += removed
            stats["document_class_entries_removed"] += 1

    # Retain compatibility with FFDec variants that serialize bindings as
    # attribute-bearing child records rather than parallel arrays.
    for parent in list(symbol_tag.iter()):
        for child in list(parent):
            attrs = child.attrib
            if attrs.get("tagId") == "0" or attrs.get("characterId") == "0" or attrs.get("characterID") == "0":
                parent.remove(child)
                stats["document_class_entries_removed"] += 1


def serialize_fragment(elem: ET.Element) -> bytes:
    return ET.tostring(elem, encoding="utf-8", short_empty_elements=True)


def find_insertion_point(path: Path) -> int:
    """Insert definitions/code before the first rendered base timeline frame.

    DoABC tags appended only before EndTag are structurally present but may never
    initialize: they sit after the base timeline's final ShowFrame.  Imported
    classes then appear in FFDec exports while getDefinitionByName fails at
    runtime.  Definitions, linkages, and ABC must be registered before frame 1.
    """
    with path.open("rb") as fh:
        with mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            frame_marker = b'\n    <item type="ShowFrameTag"'
            frame_hit = mm.find(frame_marker)
            if frame_hit >= 0:
                return frame_hit + 1
            marker = b'\n    <item type="EndTag"'
            hit = mm.rfind(marker)
            if hit >= 0:
                return hit + 1
            close = mm.rfind(b"</tags>")
            if close < 0:
                raise SystemExit(f"could not find EndTag or </tags> in {path}")
            return close


def copy_with_insert(base: Path, output: Path, insert_file: Path) -> None:
    pos = find_insertion_point(base)
    with base.open("rb") as src, output.open("wb") as dst:
        remaining = pos
        while remaining:
            chunk = src.read(min(1024 * 1024, remaining))
            if not chunk:
                raise SystemExit("unexpected EOF copying base XML prefix")
            dst.write(chunk)
            remaining -= len(chunk)
        dst.write(b"\n<!-- KR1 namespaced imported definitions/code before frame 1 -->\n")
        with insert_file.open("rb") as add:
            while True:
                chunk = add.read(1024 * 1024)
                if not chunk:
                    break
                dst.write(chunk)
        dst.write(b"\n")
        src.seek(pos)
        while True:
            chunk = src.read(1024 * 1024)
            if not chunk:
                break
            dst.write(chunk)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Frontiers FFDec SWF XML")
    parser.add_argument("--source", required=True, help="KR1 FFDec SWF XML")
    parser.add_argument("--class-map", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    # Retained for CLI compatibility with early probes. Compact mapping no longer
    # needs or uses a numeric gap.
    parser.add_argument("--gap", type=int, default=64)
    args = parser.parse_args()

    base = Path(args.base)
    source = Path(args.source)
    output = Path(args.output)
    report_path = Path(args.report)
    class_map = load_class_map(Path(args.class_map))
    renamer = ClassRenamer(class_map)

    base_inv = character_id_inventory(base)
    source_inv = character_id_inventory(source)
    id_map = allocate_character_id_map(base_inv["ids"], source_inv["ids"])
    allocated_values = sorted(id_map.values())

    stats: Counter = Counter()
    imported_types: Counter = Counter()

    with tempfile.NamedTemporaryFile(prefix="kr1-import-", suffix=".xmlfrag", delete=False) as tf:
        fragment_path = Path(tf.name)
        for elem in iter_top_level_tag_elements(source):
            tag_type = elem.attrib.get("type", "")
            if not should_import(tag_type):
                stats["top_level_tags_skipped"] += 1
                continue
            if tag_type == "SymbolClassTag":
                drop_source_document_class(elem, stats)
            transform_tree(elem, id_map, renamer, stats)
            tf.write(serialize_fragment(elem))
            tf.write(b"\n")
            stats["top_level_tags_imported"] += 1
            imported_types[tag_type] += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    copy_with_insert(base, output, fragment_path)
    fragment_path.unlink(missing_ok=True)

    overlap = set(id_map.values()) & base_inv["ids"]
    if overlap:
        raise SystemExit(f"internal error: allocated character IDs collide with base: {sorted(overlap)[:20]}")

    report = {
        "base_character_id_inventory": inventory_report(base_inv),
        "source_character_id_inventory": inventory_report(source_inv),
        # Compatibility summary fields retained for older report readers.
        "base_max_character_id": base_inv["max"],
        "source_max_character_id": source_inv["max"],
        "character_id_offset": None,
        "character_id_mapping_count": len(id_map),
        "imported_character_id_range": [
            allocated_values[0] if allocated_values else None,
            allocated_values[-1] if allocated_values else None,
        ],
        "character_id_mapping_sample": [
            {"source": old, "target": id_map[old]}
            for old in sorted(id_map)[:100]
        ],
        "source_class_count": len(class_map),
        "stats": dict(stats),
        "imported_tag_types": dict(imported_types.most_common()),
        "policy": {
            "base_document_class_retained": True,
            "source_document_class_binding_removed": True,
            "inserted_before_base_first_show_frame": True,
            "top_level_source_timeline_control_imported": False,
            "nested_define_sprite_timeline_control_retained": True,
            "compact_collision_free_character_id_mapping": True,
            "bitmap_id_65535_sentinel_preserved": True,
            "unknown_tag_code_not_treated_as_character_id": True,
            "known_tag_and_linkage_tagId_references_remapped": True,
            "never_allocates_character_id_65535": True,
        },
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({
        "base_reserved_ids": base_inv["count"],
        "source_ids_remapped": source_inv["count"],
        "allocated_range": report["imported_character_id_range"],
        "top_level_tags_imported": stats["top_level_tags_imported"],
        "id_values_remapped": stats["id_values_remapped"],
        "class_tokens_renamed": stats["class_tokens_renamed"],
    }, indent=2))


if __name__ == "__main__":
    main()
