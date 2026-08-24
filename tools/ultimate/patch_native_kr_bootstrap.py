#!/usr/bin/env python3
"""Make the namespaced KR document controller safe to create as a sub-runtime.

The original Defense constructor initializes fields, calls MovieClip's
constructor, then immediately drives its root-timeline preloader.  A merged SWF
has no second document timeline, so only that final preloader section is
invalid.  This tool truncates the constructor immediately after constructsuper
and leaves every field initializer and every other KR method byte-for-byte
untouched.
"""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from reorder_abc_scripts import DOABC, class_name_tables, items


TARGET = "KR1__Defense"
CONSTRUCTSUPER_ZERO = "d04900"


def patch_fragment(fragment: bytes) -> tuple[bytes, dict | None]:
    root = ET.fromstring(fragment)
    abc = root.find("abc")
    if abc is None:
        return fragment, None
    _strings, multinames = class_name_tables(abc)
    target = None
    for index, instance in enumerate(items(abc.find("instance_info"))):
        name_index = int(instance.attrib.get("name_index", "0"))
        name = multinames[name_index] if 0 <= name_index < len(multinames) else ""
        if name == TARGET:
            target = (index, instance)
            break
    if target is None:
        return fragment, None
    class_index, instance = target
    method_index = instance.attrib.get("iinit_index")
    body = next(
        (node for node in items(abc.find("bodies")) if node.attrib.get("method_info") == method_index),
        None,
    )
    if body is None:
        raise SystemExit(f"{TARGET}: constructor body {method_index} not found")
    original = body.attrib.get("codeBytes", "")
    marker = original.find(CONSTRUCTSUPER_ZERO)
    if marker < 0 or original.find(CONSTRUCTSUPER_ZERO, marker + 1) >= 0:
        raise SystemExit(f"{TARGET}: expected one constructsuper(0) marker")
    patched = original[: marker + len(CONSTRUCTSUPER_ZERO)] + "47"
    body.attrib["codeBytes"] = patched
    return ET.tostring(root, encoding="utf-8", short_empty_elements=True) + b"\n", {
        "class": TARGET,
        "class_index": class_index,
        "constructor_method": int(method_index or 0),
        "original_code_bytes": len(original) // 2,
        "patched_code_bytes": len(patched) // 2,
        "field_initializers_preserved": True,
        "preloader_tail_removed": True,
    }


def process(source: Path, output: Path) -> dict:
    data = source.read_bytes()
    cursor = 0
    patches = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        for match in DOABC.finditer(data):
            handle.write(data[cursor:match.start()])
            transformed, report = patch_fragment(match.group(0))
            handle.write(transformed)
            if report:
                patches.append(report)
            cursor = match.end()
        handle.write(data[cursor:])
    if len(patches) != 1:
        raise SystemExit(f"expected one {TARGET} constructor, patched {len(patches)}")
    return {"source": str(source), "output": str(output), "patches": patches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = process(args.source, args.output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
