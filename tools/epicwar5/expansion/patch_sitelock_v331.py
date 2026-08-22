#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_sitelock_v331.py <ffdec-export-root>')

p = Path(sys.argv[1]) / 'scripts' / 'Game' / 'Manager' / 'HostManager.as'
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
        raise SystemExit('hotfix validation failed: ' + needle)

print('Epic War 5 V3.3.1 GitHub Pages sitelock hotfix applied')
