#!/usr/bin/env python3
from pathlib import Path
import io
import sys
import tokenize

source_path = Path(__file__).with_name('build-v12.py')
src = source_path.read_text(encoding='utf-8')

scripts = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if scripts is None:
    raise SystemExit('usage: run-build-v12.py <exported-v11-scripts-dir>')

# Normalize two small source-shape differences between the final verified V11
# decompile and the earlier V12 prototype anchors. These changes are only to
# make the strict patcher match; the V12 replacement then writes the intended
# final code.
level_path = scripts / 'Level.as'
level_text = level_path.read_text(encoding='utf-8-sig')
current_footer = '            this.qolSettings.addChild(this.qolButton("← Dashboard",165,414,250,"page_main"));'
legacy_footer = ('            this.qolSettings.addChild(this.qolLabel("Adjusts only cosmetic cadence/back-pressure; attacks and movement stay full-rate.",28,334,14));\n'
                 '            this.qolSettings.addChild(this.qolButton("← Dashboard",165,408,250,"page_main"));')
if current_footer in level_text:
    level_text = level_text.replace(current_footer, legacy_footer, 1)
elif legacy_footer not in level_text:
    raise SystemExit('V12 runner could not locate the V11 performance footer')

current_action = '            else if(action == "perf_aggressive")\n            {'
legacy_action = '         else if(action == "perf_aggressive")\n         {'
if current_action in level_text:
    level_text = level_text.replace(current_action, legacy_action, 1)
elif legacy_action not in level_text:
    raise SystemExit('V12 runner could not locate the V11 aggressive-performance action')
level_path.write_text(level_text, encoding='utf-8', newline='\n')

# build-v12.py embeds exact ActionScript snippets in triple-quoted Python
# strings. Preserve literal ActionScript escape sequences such as "\\n" by
# turning only affected triple-quoted tokens into raw strings.
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

namespace = {'__name__': '__main__', '__file__': str(source_path)}
exec(compile(normalized, str(source_path), 'exec'), namespace, namespace)

# Final polish after the core transform: recycle-only runs show a real elapsed
# timer, and the post-boss controller avoids a full enemy scan every frame and
# temporary Point allocations in its periodic ally pulses.
level_text = level_path.read_text(encoding='utf-8')
old_timer = '         var currentText:String = this.qolTimeAttackLaunched ? this.qolTimeText(current) : "ARMED";'
new_timer = ('         if(!Level.qolTimeAttackEnabled && Level.qolRecycleEnemies)\n'
             '         {\n'
             '            current = this.qolCurrentRunSeconds();\n'
             '         }\n'
             '         var currentText:String = Level.qolTimeAttackEnabled ? (this.qolTimeAttackLaunched ? this.qolTimeText(current) : "ARMED") : this.qolTimeText(current);')
if old_timer not in level_text:
    raise SystemExit('V12 polish could not locate timer text logic')
level_text = level_text.replace(old_timer, new_timer, 1)
level_path.write_text(level_text, encoding='utf-8', newline='\n')

l15_path = scripts / 'Level15.as'
l15 = l15_path.read_text(encoding='utf-8')
old_scan = '''         var e:Enemy = null;
         for each(e in this.enemies)
         {
            this.qolV12TuneEnemy(e);
            if(!e.isDead && getQualifiedClassName(e) == "EnemySaurianNightscale" && e.health < e.initHealth / 2 && !this.qolV12Raged[e])
            {
               this.qolV12Raged[e] = true;
               e.speed *= 1.35;
               e.transform.colorTransform = new ColorTransform(1.05,0.28,1.20,1,35,0,45,0);
            }
         }
         this.qolV12Milestone();'''
new_scan = '''         var e:Enemy = null;
         if(this.qolV12Tick % 3 == 0)
         {
            for each(e in this.enemies)
            {
               this.qolV12TuneEnemy(e);
               if(!e.isDead && getQualifiedClassName(e) == "EnemySaurianNightscale" && e.health < e.initHealth / 2 && !this.qolV12Raged[e])
               {
                  this.qolV12Raged[e] = true;
                  e.speed *= 1.35;
                  e.transform.colorTransform = new ColorTransform(1.05,0.28,1.20,1,35,0,45,0);
               }
            }
         }
         this.qolV12Milestone();'''
if old_scan not in l15:
    raise SystemExit('V12 polish could not locate post-boss enemy scan')
l15 = l15.replace(old_scan, new_scan, 1)
old_tower_dist = 'Point.distance(new Point(e.x,e.y),new Point(this.qolV12Tower.x,this.qolV12Tower.y)) < 245'
new_tower_dist = '(e.x - this.qolV12Tower.x) * (e.x - this.qolV12Tower.x) + (e.y - this.qolV12Tower.y) * (e.y - this.qolV12Tower.y) < 60025'
old_hero_dist = 'Point.distance(new Point(e.x,e.y),new Point(this.qolV12Hero.x,this.qolV12Hero.y)) < 135'
new_hero_dist = '(e.x - this.qolV12Hero.x) * (e.x - this.qolV12Hero.x) + (e.y - this.qolV12Hero.y) * (e.y - this.qolV12Hero.y) < 18225'
if old_tower_dist not in l15 or old_hero_dist not in l15:
    raise SystemExit('V12 polish could not locate ally pulse distance checks')
l15 = l15.replace(old_tower_dist, new_tower_dist, 1).replace(old_hero_dist, new_hero_dist, 1)
l15_path.write_text(l15, encoding='utf-8', newline='\n')

print('V12 compatibility and polish pass applied successfully')
