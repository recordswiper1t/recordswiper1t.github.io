#!/usr/bin/env python3
"""Merge a namespaced source SWF XML definition set into a base SWF XML.

Designed for FFDec `-swf2xml` output. The base timeline/document class remains
untouched. Source definition tags, ABC and linkage metadata are imported with a
character-ID offset and ActionScript/linkage namespace prefix.

This is a structural merge primitive, not the final campaign integration layer.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import mmap
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET


# FFDec uses several different names for SWF character-definition/reference
# fields. `tagId` is deliberately NOT here: UnknownTag.tagId is the SWF tag code
# (for example 255), not a character ID.
CHARACTER_ID_ATTRS = {
    "characterId", "characterID", "spriteId", "shapeId", "bitmapId",
    "fontId", "fontID", "textID", "soundId", "buttonId", "videoId",
}

# SWF bitmap fill styles use UI16 65535 as a sentinel meaning no bitmap. It is
# not a real character ID and must survive remapping unchanged. The first merge
# proof exposed this because a naive max scan falsely reported both SWFs as
# already consuming character ID 65535.
CHARACTER_ID_SENTINELS = {
    "bitmapId": {65535},
}

EXACT_IMPORT_TYPES = {
    "DoABC2Tag", "DoABCTag", "SymbolClassTag", "ExportAssetsTag",
    "DefineScalingGridTag", "CSMTextSettingsTag", "JPEGTablesTag",
}
IMPORT_PREFIXES = ("Define",)
MAX_SWF_CHARACTER_ID = 65535


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_swf_tag_item(elem: ET.Element) -> bool:
    return local(elem.tag) == "item" and elem.attrib.get("type", "").endswith("Tag")


def should_import(tag_type: str) -> bool:
    return tag_type in EXACT_IMPORT_TYPES or tag_type.startswith(IMPORT_PREFIXES)


def is_character_sentinel(key: str, number: int) -> bool:
    return number in CHARACTER_ID_SENTINELS.get(key, set())


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


def character_id_extents(path: Path) -> dict:
    maximum = 0
    max_attr = None
    max_element = None
    by_attr: dict[str, int] = {}
    sentinel_counts: Counter = Counter()
    for _event, elem in ET.iterparse(path, events=("start",)):
        for key, value in elem.attrib.items():
            if key not in CHARACTER_ID_ATTRS:
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
            if number > by_attr.get(key, 0):
                by_attr[key] = number
            if number > maximum:
                maximum = number
                max_attr = key
                max_element = local(elem.tag)
    return {
        "max": maximum,
        "max_attribute": max_attr,
        "max_element": max_element,
        "max_by_attribute": dict(sorted(by_attr.items())),
        "sentinels_ignored": dict(sentinel_counts),
    }


def max_character_id(path: Path) -> int:
    return int(character_id_extents(path)["max"])


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
        # Binary/base64 payloads are opaque and cannot contain meaningful XML
        # class tokens. Avoid regex-scanning megabyte-sized image/audio attrs.
        if len(value) > 8192:
            return value, 0
        count = 0

        def sub(match: re.Match[str]) -> str:
            nonlocal count
            count += 1
            return self.mapping[match.group(1)]

        return self.pattern.sub(sub, value), count


def transform_tree(elem: ET.Element, offset: int, renamer: ClassRenamer, stats: Counter) -> None:
    for node in elem.iter():
        for key, value in list(node.attrib.items()):
            if key in CHARACTER_ID_ATTRS:
                try:
                    number = int(value)
                except ValueError:
                    number = 0
                if number > 0 and not is_character_sentinel(key, number):
                    node.attrib[key] = str(number + offset)
                    stats["id_references_shifted"] += 1
                    continue
                if is_character_sentinel(key, number):
                    stats["id_sentinels_preserved"] += 1
            new_value, count = renamer.replace(value)
            if count:
                node.attrib[key] = new_value
                stats["class_tokens_renamed"] += count
        if node.text and len(node.text) <= 8192:
            new_text, count = renamer.replace(node.text)
            if count:
                node.text = new_text
                stats["class_tokens_renamed"] += count
        if node.tail and len(node.tail) <= 8192:
            new_tail, count = renamer.replace(node.tail)
            if count:
                node.tail = new_tail
                stats["class_tokens_renamed"] += count


def drop_source_document_class(symbol_tag: ET.Element, stats: Counter) -> None:
    """Remove SymbolClass entries bound to character/tag 0 (source document class)."""
    for parent in list(symbol_tag.iter()):
        for child in list(parent):
            attrs = child.attrib
            if attrs.get("tagId") == "0" or attrs.get("characterId") == "0" or attrs.get("characterID") == "0":
                parent.remove(child)
                stats["document_class_entries_removed"] += 1


def serialize_fragment(elem: ET.Element) -> bytes:
    return ET.tostring(elem, encoding="utf-8", short_empty_elements=True)


def find_insertion_point(path: Path) -> int:
    """Insert before the base SWF EndTag; tags after EndTag are not executable."""
    with path.open("rb") as fh:
        with mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            marker = b'type="EndTag"'
            hit = mm.rfind(marker)
            if hit >= 0:
                start = mm.rfind(b"<item", 0, hit)
                if start >= 0:
                    return start
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
        dst.write(b"\n<!-- KR1 namespaced imported definitions/code -->\n")
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
    parser.add_argument("--gap", type=int, default=64)
    args = parser.parse_args()

    base = Path(args.base)
    source = Path(args.source)
    output = Path(args.output)
    report_path = Path(args.report)
    class_map = load_class_map(Path(args.class_map))
    renamer = ClassRenamer(class_map)

    base_extents = character_id_extents(base)
    source_extents = character_id_extents(source)
    base_max = int(base_extents["max"])
    source_max = int(source_extents["max"])
    offset = base_max + max(1, args.gap)
    imported_max = offset + source_max
    if imported_max > MAX_SWF_CHARACTER_ID:
        raise SystemExit(
            f"character-ID namespaces do not fit UI16: base max {base_max} "
            f"({base_extents['max_attribute']}), source max {source_max} "
            f"({source_extents['max_attribute']}), offset {offset}, imported max {imported_max}"
        )

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
            transform_tree(elem, offset, renamer, stats)
            tf.write(serialize_fragment(elem))
            tf.write(b"\n")
            stats["top_level_tags_imported"] += 1
            imported_types[tag_type] += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    copy_with_insert(base, output, fragment_path)
    fragment_path.unlink(missing_ok=True)

    report = {
        "base_character_id_extents": base_extents,
        "source_character_id_extents": source_extents,
        "base_max_character_id": base_max,
        "source_max_character_id": source_max,
        "character_id_offset": offset,
        "imported_character_id_range": [offset + 1, imported_max],
        "source_class_count": len(class_map),
        "stats": dict(stats),
        "imported_tag_types": dict(imported_types.most_common()),
        "policy": {
            "base_document_class_retained": True,
            "source_document_class_binding_removed": True,
            "inserted_before_base_end_tag": True,
            "top_level_source_timeline_control_imported": False,
            "nested_define_sprite_timeline_control_retained": True,
            "bitmap_id_65535_sentinel_preserved": True,
            "unknown_tag_code_not_treated_as_character_id": True,
        },
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
