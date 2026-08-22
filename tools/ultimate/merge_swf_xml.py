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


# Character IDs/references used by FFDec's SWF XML model. Deliberately exclude
# ABC/method indices (`id`, `slot_id`, `disp_id`, `name_index`, etc.).
CHARACTER_ID_ATTRS = {
    "characterId", "characterID", "spriteId", "shapeId", "bitmapId",
    "fontId", "fontID", "textID", "soundId", "tagId", "buttonId",
    "videoId",
}

# Top-level source tags that define reusable assets/code. Timeline control tags
# such as PlaceObject/ShowFrame/RemoveObject are intentionally excluded here;
# they remain nested inside imported DefineSprite tags where appropriate.
EXACT_IMPORT_TYPES = {
    "DoABC2Tag", "DoABCTag", "SymbolClassTag", "ExportAssetsTag",
    "DefineScalingGridTag", "CSMTextSettingsTag", "DefineSceneAndFrameLabelDataTag",
}
IMPORT_PREFIXES = ("Define",)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_swf_tag_item(elem: ET.Element) -> bool:
    return local(elem.tag) == "item" and elem.attrib.get("type", "").endswith("Tag")


def should_import(tag_type: str) -> bool:
    return tag_type in EXACT_IMPORT_TYPES or tag_type.startswith(IMPORT_PREFIXES)


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


def max_character_id(path: Path) -> int:
    maximum = 0
    for _event, elem in ET.iterparse(path, events=("start",)):
        for key, value in elem.attrib.items():
            if key not in CHARACTER_ID_ATTRS:
                continue
            try:
                number = int(value)
            except ValueError:
                continue
            if number > maximum:
                maximum = number
    return maximum


def load_class_map(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = data.get("classes") if isinstance(data, dict) else None
    if not isinstance(mapping, dict) or not mapping:
        raise SystemExit(f"invalid/empty class map: {path}")
    return {str(k): str(v) for k, v in mapping.items()}


def replace_class_tokens(value: str, class_map: dict[str, str]) -> tuple[str, int]:
    """Rename exact/qualified class tokens while avoiding arbitrary substrings."""
    if value in class_map:
        return class_map[value], 1
    # Most game classes are in the global package. Also cover reflection strings
    # and qualified values while requiring identifier boundaries.
    changed = 0
    out = value
    for old, new in class_map.items():
        if old not in out:
            continue
        pattern = rf"(?<![A-Za-z0-9_$]){re.escape(old)}(?![A-Za-z0-9_$])"
        out2, count = re.subn(pattern, new, out)
        if count:
            out = out2
            changed += count
    return out, changed


def transform_tree(elem: ET.Element, offset: int, class_map: dict[str, str], stats: Counter) -> None:
    for node in elem.iter():
        for key, value in list(node.attrib.items()):
            if key in CHARACTER_ID_ATTRS:
                try:
                    number = int(value)
                except ValueError:
                    number = 0
                if number > 0:
                    node.attrib[key] = str(number + offset)
                    stats["id_references_shifted"] += 1
                    continue
            new_value, count = replace_class_tokens(value, class_map)
            if count:
                node.attrib[key] = new_value
                stats["class_tokens_renamed"] += count
        if node.text:
            new_text, count = replace_class_tokens(node.text, class_map)
            if count:
                node.text = new_text
                stats["class_tokens_renamed"] += count
        if node.tail:
            new_tail, count = replace_class_tokens(node.tail, class_map)
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


def find_tags_close(path: Path) -> int:
    needle = b"</tags>"
    with path.open("rb") as fh:
        with mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            pos = mm.rfind(needle)
            if pos < 0:
                raise SystemExit(f"could not find </tags> in {path}")
            return pos


def copy_prefix_and_suffix(base: Path, output: Path, insert_file: Path) -> None:
    pos = find_tags_close(base)
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
    parser.add_argument("--gap", type=int, default=1000)
    args = parser.parse_args()

    base = Path(args.base)
    source = Path(args.source)
    output = Path(args.output)
    report_path = Path(args.report)
    class_map = load_class_map(Path(args.class_map))

    base_max = max_character_id(base)
    source_max = max_character_id(source)
    # Offset every positive KR1 character ID above Frontiers' namespace. A gap
    # keeps room for future Frontiers-only generated definitions.
    offset = base_max + max(1, args.gap)
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
            transform_tree(elem, offset, class_map, stats)
            tf.write(serialize_fragment(elem))
            tf.write(b"\n")
            stats["top_level_tags_imported"] += 1
            imported_types[tag_type] += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    copy_prefix_and_suffix(base, output, fragment_path)
    fragment_path.unlink(missing_ok=True)

    report = {
        "base_max_character_id": base_max,
        "source_max_character_id": source_max,
        "character_id_offset": offset,
        "imported_character_id_range": [offset + 1, offset + source_max],
        "source_class_count": len(class_map),
        "stats": dict(stats),
        "imported_tag_types": dict(imported_types.most_common()),
        "policy": {
            "base_document_class_retained": True,
            "source_document_class_binding_removed": True,
            "top_level_source_timeline_control_imported": False,
            "nested_define_sprite_timeline_control_retained": True,
        },
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
