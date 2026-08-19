#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: normalize-v5-perf-anchors.py <Level.as>")

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8-sig")

threshold_pattern = re.compile(
    r"var heavy:Boolean = this\.entities\.numChildren > \d+ \|\| this\.bullets\.numChildren > \d+;\s*"
    r"var extreme:Boolean = this\.entities\.numChildren > \d+ \|\| this\.bullets\.numChildren > \d+;"
)
text, n = threshold_pattern.subn(
    "var heavy:Boolean = this.entities.numChildren > 180 || this.bullets.numChildren > 220;\n"
    "         var extreme:Boolean = this.entities.numChildren > 300 || this.bullets.numChildren > 380;",
    text,
    count=1,
)
if n != 1:
    raise SystemExit(f"performance threshold structure: expected 1 match, found {n}")

cadence_pattern = re.compile(
    r"if\(!heavy \|\| !extreme && \(this\.qolPerfFrame & 1\) == 0 \|\| extreme && this\.qolPerfFrame % \d+ == 0\)"
)
text, n = cadence_pattern.subn(
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && this.qolPerfFrame % 4 == 0)",
    text,
    count=1,
)
if n != 1:
    raise SystemExit(f"performance cadence structure: expected 1 match, found {n}")

path.write_text(text, encoding="utf-8", newline="\n")
print("Normalized V5 performance anchors for deterministic V6 patching")
