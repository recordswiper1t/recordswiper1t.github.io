#!/usr/bin/env python3
"""Probe FFDec internal SWF XML structure without retaining game assets."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inspect(path: Path) -> dict:
    tag_counts: Counter[str] = Counter()
    attrs_by_tag: dict[str, set[str]] = defaultdict(set)
    idish_attrs: Counter[str] = Counter()
    examples: dict[str, dict] = {}
    root_name = None
    root_attrs = None

    for event, elem in ET.iterparse(path, events=("start", "end")):
        if event == "start":
            name = local(elem.tag)
            if root_name is None:
                root_name = name
                root_attrs = dict(elem.attrib)
            tag_counts[name] += 1
            attrs_by_tag[name].update(elem.attrib)
            for key in elem.attrib:
                kl = key.lower()
                if "id" in kl or "class" in kl or "name" in kl:
                    idish_attrs[key] += 1
            if name not in examples and elem.attrib:
                # Attribute names and short scalar examples are enough to design
                # a remapper; never retain XML bodies or asset data.
                examples[name] = {
                    k: (v[:80] if len(v) > 80 else v)
                    for k, v in list(elem.attrib.items())[:12]
                }
        else:
            elem.clear()

    interesting = {}
    needles = ("Define", "PlaceObject", "SymbolClass", "ExportAssets", "DoABC", "ImportAssets")
    for name in sorted(tag_counts):
        if name.startswith(needles) or name in {"item", "tag", "SWF"}:
            interesting[name] = {
                "count": tag_counts[name],
                "attributes": sorted(attrs_by_tag[name]),
                "example": examples.get(name, {}),
            }

    return {
        "path": str(path),
        "root": root_name,
        "root_attributes": root_attrs,
        "tag_type_count": len(tag_counts),
        "top_tags": tag_counts.most_common(50),
        "idish_attributes": idish_attrs.most_common(80),
        "interesting_tags": interesting,
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
