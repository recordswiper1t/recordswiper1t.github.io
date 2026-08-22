#!/usr/bin/env python3
from pathlib import Path
import io
import subprocess
import sys
import tokenize

source_path = Path(__file__).with_name('build-v12.py')
src = source_path.read_text(encoding='utf-8')
scripts = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if scripts is None:
    raise SystemExit('usage: run-build-v12.py <exported-v11-scripts-dir>')

def replace_one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 got {count}')
    return text.replace(old, new, 1)

# Normalize two final-V11 UI shape differences so the strict V12 Level/Enemy
# patch can retain one-match safety checks.
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

# Preserve literal ActionScript escape sequences embedded in Python triple
# string source matchers. Ordinary Python strings are unchanged.
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

# The prototype Level15 transform targeted an older final-boss class. The final
# verified V11 Level15 is structurally different after boss-safety work, so its
# expansion transform is now maintained separately in level15-current.py.
marker = '# ---------------- Level15: The Last Rift ----------------'
if marker not in normalized:
    raise SystemExit('V12 runner could not locate legacy Level15 section')
normalized = normalized.split(marker, 1)[0] + "\nprint('V12 core Level/Enemy patch applied successfully')\n"
namespace = {'__name__': '__main__', '__file__': str(source_path)}
exec(compile(normalized, str(source_path), 'exec'), namespace, namespace)

# ---------------------------------------------------------------------------
# Full audit polish on the common Level class.
# ---------------------------------------------------------------------------
level_text = level_path.read_text(encoding='utf-8')
old_timer = '         var currentText:String = this.qolTimeAttackLaunched ? this.qolTimeText(current) : "ARMED";'
new_timer = ('         if(!Level.qolTimeAttackEnabled && Level.qolRecycleEnemies)\n'
             '         {\n'
             '            current = this.qolCurrentRunSeconds();\n'
             '         }\n'
             '         var currentText:String = Level.qolTimeAttackEnabled ? (this.qolTimeAttackLaunched ? this.qolTimeText(current) : "ARMED") : this.qolTimeText(current);')
level_text = replace_one(level_text, old_timer, new_timer, 'loop timer text')

# Only complete runs that began before wave 1 are eligible for persistent bests.
level_text = replace_one(level_text,'      private var qolRunStartMs:int = 0;\n','      private var qolRunStartMs:int = 0;\n      \n      private var qolRunStartedAtWave:int = 0;\n','run eligibility state')
level_text = replace_one(level_text,'         this.qolVirtualLivesLost = 0;\n         this.qolRunStartMs = getTimer();\n         this.qolTimerLast = -1;\n         this.qolBestTimeLoaded = false;','         this.qolVirtualLivesLost = 0;\n         this.qolRunStartMs = getTimer();\n         this.qolRunStartedAtWave = this.indexWaves;\n         this.qolTimerLast = -1;\n         this.qolBestTimeLoaded = false;','manual run eligibility start')
level_text = replace_one(level_text,'         this.qolTimeAttackLaunched = true;\n         this.qolVirtualLivesLost = 0;\n         this.qolRunStartMs = getTimer();\n         this.qolTimerRunning = true;','         this.qolTimeAttackLaunched = true;\n         this.qolVirtualLivesLost = 0;\n         this.qolRunStartMs = getTimer();\n         this.qolRunStartedAtWave = this.indexWaves;\n         this.qolTimerRunning = true;','time attack eligibility start')
level_text = replace_one(level_text,'      private function qolBankRun() : void\n      {\n         var elapsed:Number = this.qolCurrentRunSeconds();','      private function qolBankRun() : void\n      {\n         if(this.qolRunStartedAtWave != 0 || !this.qolTimeAttackDone())\n         {\n            this.qolUpdateTimerHud();\n            return;\n         }\n         var elapsed:Number = this.qolCurrentRunSeconds();','full-run bank guard')
level_text = replace_one(level_text,'      private function qolFinishTimeAttack() : void\n      {\n         if(!this.qolTimerRunning)\n         {\n            return;\n         }','      private function qolFinishTimeAttack() : void\n      {\n         if(!this.qolTimerRunning)\n         {\n            if(Level.qolRecycleEnemies)\n            {\n               this.qolBankRun();\n            }\n            return;\n         }','recycle-only completion bank')

# Public bridge used by the post-boss act to invoke the same safe Send-All path.
level_text = replace_one(level_text,'      private function qolGameTick() : void\n','      public function qolV12StartAllWaves() : void\n      {\n         this.qolSendAllWaves();\n      }\n      \n      private function qolGameTick() : void\n','postboss send-all bridge')

# Hero-owned summons should be removed immediately with their owner. Cronan was
# already covered; complete the lifecycle cleanup for Alric and Mirage too.
level_text = replace_one(level_text,'         if(param1 is SoldierHeroCronan)\n         {\n            SoldierHeroCronan(param1).qolCleanupCompanions();\n         }\n         if(param1.parent != null)','         if(param1 is SoldierHeroCronan)\n         {\n            SoldierHeroCronan(param1).qolCleanupCompanions();\n         }\n         var ownedIndex:int = 0;\n         var ownedUnit:Object = null;\n         if(param1 is SoldierHeroAlric)\n         {\n            ownedIndex = this.entities.numChildren - 1;\n            while(ownedIndex >= 0)\n            {\n               ownedUnit = this.entities.getChildAt(ownedIndex);\n               if(ownedUnit is SoldierSandWarrior)\n               {\n                  SoldierSandWarrior(ownedUnit).destroyThis();\n               }\n               ownedIndex--;\n            }\n         }\n         else if(param1 is SoldierHeroMirage)\n         {\n            ownedIndex = this.entities.numChildren - 1;\n            while(ownedIndex >= 0)\n            {\n               ownedUnit = this.entities.getChildAt(ownedIndex);\n               if(ownedUnit is SoldierMirageIllusion)\n               {\n                  SoldierMirageIllusion(ownedUnit).destroyThis();\n               }\n               ownedIndex--;\n            }\n         }\n         if(param1.parent != null)','hero owned summon cleanup')
level_path.write_text(level_text, encoding='utf-8', newline='\n')

# Apply the Last Rift against the actual final verified Level15 shape.
subprocess.check_call([sys.executable, str(Path(__file__).with_name('level15-current.py')), str(scripts)])

# Final structural markers before handing the source to FFDec.
checks = {
    'Level.as': ['qolVirtualLivesLost','qolBankRun','qolRunStartedAtWave','qolV12StartAllWaves','SoldierSandWarrior','SoldierMirageIllusion','Adaptive render quality'],
    'Level15.as': ['THE LAST RIFT','VORAK, THE RIFT SOVEREIGN','NYRA THE RIFTWARDEN','qolV12BuildPath','qolV12PostBossActive'],
    'Enemy.as': ['qolRecordVirtualLivesLost(this.cost)'],
    'EnemyCanibalBeast.as': ['qolRecordVirtualLivesLost(this.cost)'],
    'EnemyTremor.as': ['qolRecordVirtualLivesLost(this.cost)'],
}
for name, needles in checks.items():
    text = (scripts/name).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{name}: missing {needle}')
print('V12 compatibility and full audit polish pass applied successfully')
