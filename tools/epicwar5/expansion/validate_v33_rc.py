#!/usr/bin/env python3
from pathlib import Path
import re, sys, json

if len(sys.argv) != 2:
    raise SystemExit('usage: validate_v33_rc.py <ffdec-export-root>')

root = Path(sys.argv[1]) / 'scripts' / 'Game'
repo = Path.cwd()
checks = []


def read(rel):
    p = root / rel
    if not p.is_file():
        raise SystemExit(f'RC FAIL: missing decompiled file {rel}')
    return p.read_text(encoding='utf-8-sig')


def squash(s):
    return re.sub(r'\s+', ' ', s).strip()


def ok(name, detail=''):
    checks.append({'check': name, 'status': 'PASS', 'detail': detail})


def require(text, needle, name):
    if needle not in text and squash(needle) not in squash(text):
        raise SystemExit(f'RC FAIL [{name}]: missing {needle!r}')
    ok(name, needle)


def require_re(text, pattern, name, detail=''):
    if not re.search(pattern, text, re.S):
        raise SystemExit(f'RC FAIL [{name}]: pattern not found: {pattern}')
    ok(name, detail or pattern)


def forbid(text, needle, name):
    if needle in text or squash(needle) in squash(text):
        raise SystemExit(f'RC FAIL [{name}]: forbidden legacy marker {needle!r}')
    ok(name, f'absent: {needle}')


def method(text, name, next_name=None):
    start = text.find('      public function ' + name + '(')
    if start < 0:
        start = text.find('      private function ' + name + '(')
    if start < 0:
        raise SystemExit(f'RC FAIL: method {name} not found')
    if next_name:
        end = text.find('      public function ' + next_name + '(', start + 1)
        if end < 0:
            end = text.find('      private function ' + next_name + '(', start + 1)
    else:
        m = re.search(r'^      (?:public|private|protected) function ', text[start + 10:], re.M)
        end = start + 10 + m.start() if m else len(text)
    if end < 0:
        end = len(text)
    return text[start:end]


def threshold_pairs(body):
    # FFDec may emit either `if (...) return N;` or `if (...) { return N; }`.
    return [(int(a), int(b)) for a,b in re.findall(
        r'if\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*>=\s*(\d+)\s*\)\s*(?:\{\s*)?return\s+(\d+)\s*;', body, re.S)]


dm = read('Manager/DataManager.as')
br = read('Interface/BattleResult.as')
wm = read('Interface/WorldMap.as')
be = read('System/Battle/BattleControlEnemy.as')
cts = read('System/StatDef/CharTotalStat.as')
ca = read('System/StatDef/CharAbilityStat.as')
ci = read('System/StatDef/CharItemStat.as')
acc = read('Interface/WorldMapFormationAcc.as')
cb = read('System/GameObject/Character/CharacterBase.as')
pu = read('System/Battle/PlayerUnit.as')
ew = read('System/Battle/EnemyWave.as')
bg = read('System/Background/BackgroundMgr.as')
fx = read('Manager/EffectManager.as')
bs = read('System/Battle/BattleSystem.as')

# ---- Progression invariants -------------------------------------------------
army = method(dm, 'expansionArmySlotsForClears', 'expansionEquipmentSlotsForClears')
pairs = threshold_pairs(army)
expected = [(45,12),(38,11),(31,10),(25,9),(20,8),(14,7),(9,6),(5,5),(2,4)]
if pairs != expected or not re.search(r'return\s+3\s*;', army):
    raise SystemExit(f'RC FAIL [army progression]: got {pairs}, expected {expected}')
ok('army progression', '3 slots at 0 clears; 12 slots at 45 clears')

equip = method(dm, 'expansionEquipmentSlotsForClears', 'expansionUpgradeCostMultiplier')
if threshold_pairs(equip) != [(35,3),(15,2)] or not re.search(r'return\s+1\s*;', equip):
    raise SystemExit('RC FAIL [equipment progression]: expected 1 -> 2@15 -> 3@35')
ok('equipment progression', '1 slot -> 2 at 15 -> 3 at 35')

require_re(dm, r'return\s+this\.expansionProgressCount\(\)\s*>=\s*18\s*;', 'advanced upgrades unlock at 18')
require_re(dm, r'return\s+this\.getStageNormalClear\(\)\s*>=\s*12\s*&&\s*this\.getStageExtraClear\(\)\s*>=\s*8\s*;', 'Expansion gate excludes mandatory trials')
progress = method(dm, 'expansionProgressCount', 'expansionOriginalCampaignComplete')
require(progress, 'stageGetValue("normal",i)', 'progress includes story clears')
require(progress, 'stageGetValue("extra",i)', 'progress includes extra clears')
require(progress, 'stageGetValue("trial",i)', 'progress includes optional trial clears')
require(progress, 'stageGetValue("expansion",i)', 'progress includes Expansion clears')
require_re(progress, r'i\s*<=\s*25', 'progress loops through all 25 Expansion stages')

# Simulate the parsed progression curve to ensure no dead endpoint.
def army_slots(c):
    for threshold, slots in expected:
        if c >= threshold:
            return slots
    return 3
for c in range(51):
    if c and army_slots(c) < army_slots(c-1):
        raise SystemExit('RC FAIL [monotonic army progression]')
if army_slots(0) != 3 or army_slots(20) != 8 or army_slots(45) != 12 or army_slots(50) != 12:
    raise SystemExit('RC FAIL [army progression samples]')
ok('progression simulation', '0=3, 20=8, 45=12, 50=12; monotonic')

# ---- Save/load round-trip structure ----------------------------------------
require(dm, 'so.data.stage_expansion_stat = new String(this.stage_expansion_stat);', 'Expansion clear bank is saved')
require(dm, 'this.stage_expansion_stat = so.data.stage_expansion_stat == undefined', 'old-save Expansion bank migration')
require(dm, 'this.dat_stage_expansion_stat = this.stage_expansion_stat.split(",");', 'Expansion clear bank is loaded')
require(dm, 'this.stage_expansion_stat = this.mergeArrayString(this.dat_stage_expansion_stat);', 'Expansion clear bank is serialized')
require_re(dm, r'while\s*\(\s*this\.dat_stage_expansion_stat\.length\s*<\s*25\s*\)', 'Expansion clear bank self-repairs short saves')
require(dm, 'this.dat_stage_expansion_stat.length = 25;', 'Expansion clear bank trims malformed long saves')
require_re(dm, r'while\s*\(\s*this\.dat_item_inv\.length\s*<\s*57\s*\)', '57-item inventory migration')

for i in range(7,13):
    require(dm, f'so.data.unit_equip{i}_id', f'army slot {i} saved')
    require_re(dm, rf'this\.unit_equip{i}_id\s*=\s*int\s*\(\s*so\.data\.unit_equip{i}_id\s*\)', f'army slot {i} loaded')
for field in ['item2','item3'] + [f'ability{i}' for i in range(10,19)]:
    require(dm, f'case "{field}"', f'{field} persistence mapping')
ok('extended character state', 'item2/item3 + ability10..18 have persistent row mappings')

# ---- Stage sequencing / softlock-oriented static checks --------------------
case_ids = sorted(set(int(x) for x in re.findall(r'case\s+(1\d\d)\s*:', be)))
exp_cases = [x for x in case_ids if 101 <= x <= 125]
if exp_cases != list(range(101,126)):
    raise SystemExit(f'RC FAIL [Expansion battle inputs]: expected 101..125, got {exp_cases}')
for n in range(1,26):
    require_re(be, rf'case\s+{100+n}\s*:.*?initExpansion\s*\(\s*{n}\s*\)', f'Expansion battle input {100+n} routes to stage {n}')
ok('25 Expansion battle inputs', 'battle inputs 101..125 all route to initExpansion(1..25)')
require_re(be, r'this\.bSys\.battle_stage\s*=\s*25\s*\+\s*tier\s*;', 'Expansion battle stage IDs map to 26..50')
require_re(br, r'this\.bSys\.battle_stage\s*>=\s*26\s*&&\s*this\.bSys\.battle_stage\s*<=\s*50', 'all Expansion wins persist')
require(br, 'stageSetValue("expansion",expansionStage', 'Expansion result writes clear bank')
require(br, 'this.mGF.datMgr.saveData();', 'battle result flushes save immediately')
require_re(wm, r'i\s*==\s*1\s*\|\|\s*this\.mGF\.datMgr\.stageGetValue\("expansion",\s*i\s*-\s*1\)\s*>=\s*1', 'Expansion stages unlock sequentially')

# Every Expansion stage must have a named first-clear reward entry.
m = re.search(r'var\s+rewardNames\s*:\s*Array\s*=\s*\[([^\]]+)\]\s*;', be, re.S)
if not m:
    raise SystemExit('RC FAIL [rewardNames]: array not found')
rewards = re.findall(r'"([^"]+)"', m.group(1))
if len(rewards) != 25 or len(set(rewards)) != 25:
    raise SystemExit(f'RC FAIL [first-clear reward map]: expected 25 unique rewards, got {len(rewards)}/{len(set(rewards))}')
ok('first-clear reward map', '25 unique stage relic rewards')
require_re(be, r'firstClear\s*\?\s*String\s*\(\s*rewardNames\[index\]\s*\)\s*:\s*""', 'stage relics are first-clear only')
require_re(br, r'Math\.max\s*\(\s*this\.mGF\.datMgr\.itemGetValue\(itemReward\)\s*,\s*2\s*\)', 'first-clear relic ownership uses usable value')

# ---- V3.3 migration + milestone rewards ------------------------------------
require_re(dm, r'itemGetValue\s*\(\s*30\s*\+\s*relicStage\s*\)\s*==\s*1', 'legacy V3/V3.2 relic ownership repair')
require_re(dm, r'itemGetValue\s*\(\s*57\s*\)\s*<\s*2', '50-clear milestone reward migration')
require(ca, 'x_fieldstandard', 'Field Standard ability exists')
require(ca, 'x_conquerormedal', 'Conqueror Medal ability exists')
require(ci, 'Field Standard', 'Field Standard item exists')
require(ci, 'Conqueror Medal', 'Conqueror Medal item exists')
require_re(acc, r'if\s*\(\s*itemSlot\s*>\s*57\s*\)', 'equipment UI exposes exactly 57 items')

# ---- V3.2 identity/balance regression --------------------------------------
require(cts, 'case 10: return [20,46,52,15,47,39,37,48,35]', 'role-specific Hobbit advanced tree retained')
require(cts, 'case 25: return [20,46,71,15,47,72,42,48,73]', 'role-specific Engineer advanced tree retained')
require(dm, 'expansionUpgradeCostMultiplier', 'depth-aware advanced upgrade pricing retained')
require(wm, 'var threat:int = 1', 'T1-T5 threat display retained')

# ---- Performance regression guards -----------------------------------------
require_re(cb, r'Math\.abs\s*\(\s*myClip\.x\s*-\s*child\.x\s*\)\s*<=\s*900', 'character broad-phase collision/target filter')
require(cb, 'var myDepth:int = this.getZDepth()', 'incremental display-depth insertion')
forbid(cb, 'children.sort(this.zSorting)', 'legacy full battlefield sort removed')
require_re(cb, r'this\._healthbar_refresh\s*=\s*3', 'health bar refresh throttled')
require_re(pu, r'this\._count_refresh\s*=\s*8', 'player population scan throttled')
require_re(pu, r'this\._ui_refresh\s*=\s*3', 'player UI refresh throttled')
require(ew, 'countEnemyWave(COMMAND:Boolean = false)', 'wave count no longer implies command refresh')
require(ew, 'setMaxUnit(VAL:int = 25)', 'wave controller cap API retained')
require_re(be, r'var\s+waveCap\s*:\s*int\s*=\s*Math\.min\s*\(\s*22\s*,\s*16\s*\+\s*int\s*\(\s*tier\s*/\s*4\s*\)\s*\)', 'Expansion disposable-wave cap')
require_re(bg, r'burst\s*=\s*this\.mGF\.stageRoot\.stage\.quality\s*==\s*"low"\s*\?\s*18\s*:\s*36', 'weather particle budget')
require(fx, 'isWorldXVisible(X:Number = 0, MARGIN:Number = 250)', 'offscreen effect culling')
require_re(fx, r'contBLOODSPLAT\.numChildren\s*>=\s*60', 'blood splat cap')
require_re(bs, r'load\s*>=\s*175', 'adaptive heavy-load threshold')
require(bs, 'updateAdaptivePerformance()', 'adaptive quality update enabled')

# ---- Launcher/release freeze ------------------------------------------------
launcher = (repo / 'epicwar5-expansion' / 'index.html').read_text(encoding='utf-8')
require(launcher, '/assets/epic-war-5-expansion-v33.swf?v=33-performance', 'launcher pinned to V3.3')
require(launcher, 'Play Expansion V3.3', 'launcher visibly identifies V3.3')

report = {
    'release': 'Epic War 5 Expansion V3.3 RC',
    'status': 'PASS',
    'checks_passed': len(checks),
    'checks': checks,
}
out = Path('/tmp/EPICWAR5-V33-RC-REPORT.json')
out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'RC PASS: {len(checks)} invariant checks passed')
print(out)
