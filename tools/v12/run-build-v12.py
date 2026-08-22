#!/usr/bin/env python3
from pathlib import Path
import io
import sys
import tokenize

source_path = Path(__file__).with_name('build-v12.py')
src = source_path.read_text(encoding='utf-8')

# build-v12.py embeds exact ActionScript snippets in triple-quoted Python
# strings.  ActionScript string literals such as "...\\n..." must retain the
# backslash+n characters; normal Python triple strings would turn those into an
# actual newline and make the exact-source matcher fail.  Prefix only affected
# triple-quoted string tokens with r, leaving ordinary Python strings alone.
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
    # Find the quote after optional Python string prefixes.
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
    # These snippets are source-code matchers/replacements, not format strings.
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
