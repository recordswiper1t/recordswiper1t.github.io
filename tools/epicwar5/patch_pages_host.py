#!/usr/bin/env python3
"""Authorize the stable Epic War 5 build on this GitHub Pages host.

This patch is intentionally separate from the experimental expansion pipeline.
It only changes the original V1.05 HostManager domain branch after the stable
Sandbox V2 source patches have been applied.
"""
from pathlib import Path
import sys

# Stable release hotfix revision 1. Keep this script expansion-independent.
if len(sys.argv) != 2:
    raise SystemExit('usage: patch_pages_host.py <ffdec-export-root>')

p = Path(sys.argv[1]) / 'scripts' / 'Game' / 'Manager' / 'HostManager.as'
if not p.exists():
    raise SystemExit(f'missing {p}')
t = p.read_text(encoding='utf-8-sig')

old = '''         else if(this._host_address.lastIndexOf("armorgames.com") > -1)\n         {\n            this._host_name = "armorgames";\n            this._block_site = false;\n            this._enable_mochibot = false;\n            this._ad_type = "kong";\n            this._link_sponsor = "http://www.armorgames.com";\n         }\n         else\n'''
new = '''         else if(this._host_address.lastIndexOf("armorgames.com") > -1)\n         {\n            this._host_name = "armorgames";\n            this._block_site = false;\n            this._enable_mochibot = false;\n            this._ad_type = "kong";\n            this._link_sponsor = "http://www.armorgames.com";\n         }\n         else if(this._host_address.lastIndexOf("recordswiper1t.github.io") > -1)\n         {\n            this._host_name = "github-pages";\n            this._block_site = false;\n            this._enable_mochibot = false;\n            this._enable_ads = false;\n            this._ad_type = "";\n         }\n         else\n'''

count = t.count(old)
if count != 1:
    raise SystemExit(f'HostManager Armor Games anchor expected once, got {count}')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8', newline='\n')

for needle in [
    'lastIndexOf("recordswiper1t.github.io") > -1',
    'this._host_name = "github-pages";',
    'this._block_site = false;',
    'this._enable_mochibot = false;',
    'this._enable_ads = false;'
]:
    if needle not in t:
        raise SystemExit('stable host hotfix validation failed: ' + needle)

print('Epic War 5 stable GitHub Pages HostManager hotfix applied')
