#!/usr/bin/env python3
import subprocess

BASE = 'f01ad606ffa1ea0a63d8875656e1d30d5b2e6486'
code = subprocess.check_output(
    ['git', 'show', f'{BASE}:.github/v4-finalize.py'],
    text=True,
    encoding='utf-8',
)
old = "t = get(name).replace('MouseEvent.CLICK,this.clickEvent', 'MouseEvent.MOUSE_DOWN,this.clickEvent')"
new = "t = get(name).replace('MouseEvent.CLICK,this.clickEvent', 'MouseEvent.MOUSE_DOWN,this.clickEvent').replace('MouseEvent.CLICK,clickEvent', 'MouseEvent.MOUSE_DOWN,this.clickEvent')"
if code.count(old) != 1:
    raise SystemExit(f'touch normalization anchor count: {code.count(old)}')
code = code.replace(old, new, 1)
exec(compile(code, '<v4-finalizer>', 'exec'), globals(), globals())
