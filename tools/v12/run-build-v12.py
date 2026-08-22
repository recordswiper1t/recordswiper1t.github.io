#!/usr/bin/env python3
from pathlib import Path
import io
import sys
import tokenize

source_path = Path(__file__).with_name('build-v12.py')
src = source_path.read_text(encoding='utf-8')

# V12 was authored against the exact verified V11 source, but two compatibility
# details need normalization before the strict patcher runs:
# 1) ActionScript string literals like "...\\n..." inside Python triple strings
#    must retain the backslash+n characters.
# 2) The final V11 performance page retained its threshold buttons and used a
#    later dashboard footer than the original V12 prototype expected.  Convert
#    just that footer to the legacy two-line anchor; build-v12.py then replaces
#    it with the adaptive-quality footer while leaving all threshold controls.
scripts = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if scripts is None:
    raise SystemExit('usage: run-build-v12.py <exported-v11-scripts-dir>')
level_path = scripts / 'Level.as'
level_text = level_path.read_text(encoding='utf-8-sig')
current_footer = '            this.qolSettings.addChild(this.qolButton("← Dashboard",165,414,250,"page_main"));'
legacy_footer = ('            this.qolSettings.addChild(this.qolLabel("Adjusts only cosmetic cadence/back-pressure; attacks and movement stay full-rate.",28,334,14));\n'
                 '            this.qolSettings.addChild(this.qolButton("← Dashboard",165,408,250,"page_main"));')
if current_footer in level_text:
    level_text = level_text.replace(current_footer, legacy_footer, 1)
elif legacy_footer not in level_text:
    raise SystemExit('V12 runner could not locate the V11 performance footer')
level_path.write_text(level_text, encoding='utf-8', newline='\n')

out = []
last = (1, 0)
lines = src.splitlines(keepends=True)

def between(start, end):
    (sl, sc), (el, ec) = start, end
    if sl == el:
        return lines[sl - 1][sc:ec]
    parts = [lines[sl - 1][sc:]]
    parts.extend(lines[sl:el - 1])
    parts.append(lines[el - 1][:ec])
    return ''.join(parts)

def prefix_raw_string(token_text: str) -> str:
    lower = token_text.lower()
    i = 0
    while i < len(token_text) and token_text[i].lower() in 'rubf':
        i += 1
    body = token_text[i:]
    if not (body.startswith("'''") or body.startswith('"""')):
        return token_text
    if 'r' in lower[:i]:
        return token_text
    if '\\n' not in body and '\\t' not in body and '\\r' not in body:
        return token_text
    if 'f' in lower[:i]:
        raise SystemExit('unexpected f-string triple literal with ActionScript escapes')
    return token_text[:i] + 'r' + token_text[i:]

reader = io.StringIO(src).readline
for tok in tokenize.generate_tokens(reader):
    if tok.type == tokenize.ENDMARKER:
        break
    out.append(between(last, tok.start))
    text = tok.string
    if tok.type == tokenize.STRING:
        text = prefix_raw_string(text)
    out.append(text)
    last = tok.end
out.append(between(last, (len(lines), len(lines[-1]) if lines else 0)))
normalized = ''.join(out)

namespace = {
    '__name__': '__main__',
    '__file__': str(source_path),
}
exec(compile(normalized, str(source_path), 'exec'), namespace, namespace)
