#!/usr/bin/env python3
"""Probe FFDec internal SWF XML structure without retaining game assets.

FFDec represents actual SWF tags as generic `<item type="...Tag">` nodes, so
this probe groups those item types and records only schema/reference metadata.
No image/audio/ABC payloads or decompiled method bodies are retained.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


IDISH = re.compile(r"(?:^id$|id$|Id$|ID$|character|font|sound|sprite|shape|bitmap|textID|tagId)")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def scalar(value: str) -> str:
    if len(value) > 80:
        return f"<{len(value)} chars>"
    return value


def inspect(path: Path) -> dict:
    element_counts: Counter[str] = Counter()
    attrs_by_element: dict[str, set[str]] = defaultdict(set)
    global_idish: Counter[str] = Counter()
    root_name = None
    root_attrs = None

    swf_tag_counts: Counter[str] = Counter()
    swf_tag_attrs: dict[str, set[str]] = defaultdict(set)
    swf_tag_idish: dict[str, Counter[str]] = defaultdict(Counter)
    swf_tag_examples: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    swf_tag_stack: list[str] = []
    top_level_tag_sequence: list[str] = []
    seen_tag_depth = 0

    numeric_id_values: dict[str, list[int]] = defaultdict(list)

    for event, elem in ET.iterparse(path, events=("start", "end")):
        if event == "start":
            name = local(elem.tag)
            if root_name is None:
                root_name = name
                root_attrs = dict(elem.attrib)
            element_counts[name] += 1
            attrs_by_element[name].update(elem.attrib)

            is_tag_item = name == "item" and elem.attrib.get("type", "").endswith("Tag")
            if is_tag_item:
                tag_type = elem.attrib["type"]
                swf_tag_stack.append(tag_type)
                swf_tag_counts[tag_type] += 1
                if seen_tag_depth == 0:
                    top_level_tag_sequence.append(tag_type)
                seen_tag_depth += 1

            active = swf_tag_stack[-1] if swf_tag_stack else None
            if active:
                swf_tag_attrs[active].update(elem.attrib)

            for key, value in elem.attrib.items():
                if IDISH.search(key):
                    global_idish[key] += 1
                    if active:
                        swf_tag_idish[active][key] += 1
                        examples = swf_tag_examples[active][key]
                        sv = scalar(value)
                        if sv not in examples and len(examples) < 5:
                            examples.append(sv)
                    try:
                        numeric_id_values[key].append(int(value))
                    except (TypeError, ValueError):
                        pass
        else:
            name = local(elem.tag)
            is_tag_item = name == "item" and elem.attrib.get("type", "").endswith("Tag")
            if is_tag_item:
                seen_tag_depth -= 1
                if swf_tag_stack:
                    swf_tag_stack.pop()
            elem.clear()

    tag_schema = {}
    for tag_type in sorted(swf_tag_counts):
        tag_schema[tag_type] = {
            "count": swf_tag_counts[tag_type],
            "attributes_seen_in_subtree": sorted(swf_tag_attrs[tag_type]),
            "id_reference_counts": dict(swf_tag_idish[tag_type].most_common()),
            "id_reference_examples": dict(swf_tag_examples[tag_type]),
        }

    numeric_ranges = {}
    for key, values in numeric_id_values.items():
        if values:
            numeric_ranges[key] = {"min": min(values), "max": max(values), "count": len(values)}

    return {
        "path": str(path),
        "root": root_name,
        "root_attributes": root_attrs,
        "xml_element_type_count": len(element_counts),
        "top_xml_elements": element_counts.most_common(50),
        "global_idish_attributes": global_idish.most_common(100),
        "numeric_id_ranges": numeric_ranges,
        "swf_tag_type_count": len(swf_tag_counts),
        "swf_tag_counts": swf_tag_counts.most_common(),
        "top_level_tag_sequence_head": top_level_tag_sequence[:80],
        "top_level_tag_sequence_tail": top_level_tag_sequence[-40:],
        "swf_tag_schema": tag_schema,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kr1", required=True)
    parser.add_argument("--krf", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = {
        "kr1": inspect(Path(args.kr1)),
        "krf": inspect(Path(args.krf)),
        "purpose": "FFDec XML schema probe for safe character-ID/linkage/tag merging",
    }
    Path(args.output).write_text(json.dumps(out, indent=2), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
