#!/usr/bin/env python3
"""Probe FFDec internal SWF XML without retaining copyrighted binary/XML payloads.

The report is intentionally structural: tag counts, character ids, linkage-like
name/id pairs, and a conservative numeric dependency closure around requested
symbols. It is used to design the KR1 -> KRF transplant pipeline.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ID_KEYS = {
    "characterid", "character_id", "character", "tagid", "tag_id", "spriteid",
    "sprite_id", "fontid", "font_id", "soundid", "sound_id", "bitmapid",
    "bitmap_id", "buttonid", "button_id", "sourceid", "source_id", "id",
}
NAME_KEYS = {"name", "classname", "class_name", "symbol", "exportname", "export_name"}
REF_HINTS = ("id", "character", "sprite", "font", "sound", "bitmap", "button", "source")
NUM_RE = re.compile(r"^-?\d+$")


def lname(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def attr_key(k: str) -> str:
    return lname(k).replace("-", "_").lower()


def first_int(attrs: dict[str, str], keys=ID_KEYS):
    for k, v in attrs.items():
        if attr_key(k) in keys and NUM_RE.match(v or ""):
            try:
                return int(v)
            except ValueError:
                pass
    return None


def numeric_refs(elem: ET.Element) -> set[int]:
    out: set[int] = set()
    for node in elem.iter():
        for k, v in node.attrib.items():
            kk = attr_key(k)
            if any(h in kk for h in REF_HINTS) and NUM_RE.match(v or ""):
                try:
                    n = int(v)
                except ValueError:
                    continue
                if n >= 0:
                    out.add(n)
    return out


def node_names(elem: ET.Element) -> set[str]:
    out: set[str] = set()
    for node in elem.iter():
        for k, v in node.attrib.items():
            if attr_key(k) in NAME_KEYS and v:
                out.add(v)
        if node.text:
            t = node.text.strip()
            if 0 < len(t) <= 160:
                out.add(t)
    return out


def analyse(path: Path, targets: list[str]) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()

    counts = collections.Counter()
    definitions: dict[int, dict] = {}
    occurrences: list[dict] = []
    linkage_pairs: list[dict] = []

    for elem in root.iter():
        tag = lname(elem.tag)
        counts[tag] += 1
        cid = first_int(elem.attrib)
        if cid is not None and cid >= 0:
            # Keep the first outer definition we see for an id; later nested
            # references are still captured by numeric_refs.
            definitions.setdefault(cid, {
                "tag": tag,
                "attrs": dict(elem.attrib),
                "refs": sorted(numeric_refs(elem) - {cid}),
            })

        names = node_names(elem)
        if names and cid is not None:
            for n in sorted(names):
                if len(n) <= 160 and not NUM_RE.match(n):
                    linkage_pairs.append({"name": n, "id": cid, "tag": tag})

        hay = " ".join([tag, *map(str, elem.attrib.values()), elem.text or ""])
        hit = [t for t in targets if t.lower() in hay.lower()]
        if hit:
            occurrences.append({
                "tag": tag,
                "attrs": dict(elem.attrib),
                "targets": hit,
                "id": cid,
                "refs": sorted(numeric_refs(elem) - ({cid} if cid is not None else set())),
            })

    # De-duplicate linkage records while preserving useful order.
    seen = set()
    links = []
    for row in linkage_pairs:
        key = (row["name"], row["id"], row["tag"])
        if key not in seen:
            seen.add(key)
            links.append(row)

    # Seed dependency closure from target occurrences. This is deliberately
    # conservative: every numeric id-like reference in a matched subtree is a seed.
    seeds: set[int] = set()
    for row in occurrences:
        if row["id"] is not None:
            seeds.add(row["id"])
        seeds.update(row["refs"])

    closure = set(seeds)
    queue = collections.deque(seeds)
    while queue:
        cur = queue.popleft()
        d = definitions.get(cur)
        if not d:
            continue
        for nxt in d["refs"]:
            if nxt not in closure:
                closure.add(nxt)
                queue.append(nxt)

    closure_rows = []
    for cid in sorted(closure):
        d = definitions.get(cid)
        closure_rows.append({
            "id": cid,
            "defined": d is not None,
            "tag": d["tag"] if d else None,
            "refs": d["refs"] if d else [],
        })

    target_links = [
        row for row in links
        if any(t.lower() in row["name"].lower() for t in targets)
    ]

    return {
        "xml": str(path),
        "root_tag": lname(root.tag),
        "element_count": sum(counts.values()),
        "tag_counts_top": counts.most_common(80),
        "character_definition_count": len(definitions),
        "max_character_id": max(definitions) if definitions else None,
        "targets": targets,
        "target_occurrences": occurrences[:250],
        "target_linkages": target_links[:250],
        "dependency_seed_ids": sorted(seeds),
        "dependency_closure_count": len(closure),
        "dependency_closure": closure_rows[:5000],
        "linkage_sample": links[:1000],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("xml", type=Path)
    ap.add_argument("--target", action="append", default=[])
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    targets = args.target or ["Level1", "GLevel1"]
    report = analyse(args.xml, targets)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
