#!/usr/bin/env python3
"""Run the frozen V3.3 RC game invariants for a newer Expansion SWF.

The V3.3 validator ends with two release-surface assertions that intentionally
pin the browser HTML to the V3.3 filename/label. Those assertions are not SWF
invariants and must change for V3.4. This wrapper executes an in-memory copy of
the frozen validator with only that launcher-freeze section removed; every
progression, save/load, stage-routing, reward, balance and performance check is
left unchanged.
"""
from pathlib import Path
import subprocess
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: validate_v34_invariants.py <ffdec-export-root>')

source_path = Path(__file__).with_name('validate_v33_rc.py')
source = source_path.read_text(encoding='utf-8')
start_marker = '# ---- Launcher/release freeze ------------------------------------------------'
report_marker = 'report = {'
start = source.find(start_marker)
report = source.find(report_marker, start)
if start < 0 or report < 0:
    raise SystemExit('V3.3 validator layout changed; refusing to skip an unknown section')

patched = source[:start]
patched += "# V3.4: launcher filename/label freeze intentionally omitted.\n"
patched += "ok('V3.3 SWF invariant suite reused by V3.4', 'launcher freeze excluded')\n\n"
patched += source[report:]

tmp = Path('/tmp/validate_epicwar5_v34_invariants.py')
tmp.write_text(patched, encoding='utf-8')
subprocess.run([sys.executable, str(tmp), sys.argv[1]], check=True)
print('V3.4 PASS: frozen V3.3 gameplay/save/performance invariants passed')
