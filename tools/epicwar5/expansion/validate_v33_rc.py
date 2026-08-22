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


def ok(name, detail=''):
    checks.append({'check': name, 'status': 'PASS', 'detail': detail})


def require(text, needle, name):
    if needle not in text:
        raise SystemExit(f'RC FAIL [{name}]: missing {needle!r}')
    ok(name, needle)


def forbid(text, needle, name):
    if needle in text:
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
    return [(int(a), int(b)) for a,b in re.findall(
        r'if\s*\(\s*CLEARS\s*>=\s*(\d+)\s*\)\s*return\s+(\d+)\s*;', body, re.S)]


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

require(dm, 'return this.expansionProgressCount() >= 18;', 'advanced upgrades unlock at 18')
require(dm, 'return this.getStageNormalClear() >= 12 && this.getStageExtraClear() >= 8;', 'Expansion gate excludes mandatory trials')
require(dm, 'for(i = 1; i <= 25; i++) if(this.stageGetValue("expansion",i) >= 1) total++;', 'progress counts all 25 Expansion clears')

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
require(dm, 'while(this.dat_stage_expansion_stat.length < 25)', 'Expansion clear bank self-repairs short saves')
require(dm, 'this.dat_stage_expansion_stat.length = 25;', 'Expansion clear bank trims malformed long saves')
require(dm, 'while(this.dat_item_inv.length < 57)', '57-item inventory migration')

for i in range(7,13):
    require(dm, f'so.data.unit_equip{i}_id', f'army slot {i} saved')
    require(dm, f'this.unit_equip{i}_id = int(so.data.unit_equip{i}_id)', f'army slot {i} loaded')
for field in ['item2','item3'] + [f'ability{i}' for i in range(10,19)]:
    require(dm, f'case "{field}"', f'{field} persistence mapping')
ok('extended character state', 'item2/item3 + ability10..18 have persistent row mappings')

# ---- Stage sequencing / softlock-oriented static checks --------------------
case_ids = sorted(set(int(x) for x in re.findall(r'case (1\d\d):\s*\n\s*this\.initExpansion\(', be)))
if case_ids != list(range(101,126)):
    raise SystemExit(f'RC FAIL [Expansion battle inputs]: expected 101..125, got {case_ids}')
ok('25 Expansion battle inputs', 'battle inputs 101..125 are all present')
require(be, 'this.bSys.battle_stage = 25 + tier;', 'Expansion battle stage IDs map to 26..50')
require(br, 'this.bSys.battle_stage >= 26 && this.bSys.battle_stage <= 50', 'all Expansion wins persist')
require(br, 'this.mGF.datMgr.stageSetValue("expansion",expansionStage', 'Expansion result writes clear bank')
require(br, 'this.mGF.datMgr.saveData();', 'battle result flushes save immediately')
require(wm, 'i == 1 || this.mGF.datMgr.stageGetValue("expansion",i - 1) >= 1', 'Expansion stages unlock sequentially')

# Every Expansion stage must have a named first-clear reward entry.
m = re.search(r'var rewardNames:Array = \[([^\]]+)\];', be)
if not m:
    raise SystemExit('RC FAIL [rewardNames]: array not found')
rewards = re.findall(r'"([^"]+)"', m.group(1))
if len(rewards) != 25 or len(set(rewards)) != 25:
    raise SystemExit(f'RC FAIL [first-clear reward map]: expected 25 unique rewards, got {len(rewards)}/{len(set(rewards))}')
ok('first-clear reward map', '25 unique stage relic rewards')
require(be, 'firstClear ? String(rewardNames[index]) : ""', 'stage relics are first-clear only')
require(br, 'Math.max(this.mGF.datMgr.itemGetValue(itemReward),2)', 'first-clear relic ownership uses usable value')

# ---- V3.3 migration + milestone rewards ------------------------------------
require(dm, 'itemGetValue(30 + relicStage) == 1', 'legacy V3/V3.2 relic ownership repair')
require(dm, 'itemGetValue(57) < 2', '50-clear milestone reward migration')
require(ca, 'x_fieldstandard', 'Field Standard ability exists')
require(ca, 'x_conquerormedal', 'Conqueror Medal ability exists')
require(ci, 'Field Standard', 'Field Standard item exists')
require(ci, 'Conqueror Medal', 'Conqueror Medal item exists')
require(acc, 'if(itemSlot > 57)', 'equipment UI exposes exactly 57 items')

# ---- V3.2 identity/balance regression --------------------------------------
require(cts, 'case 10: return [20,46,52,15,47,39,37,48,35]', 'role-specific Hobbit advanced tree retained')
require(cts, 'case 25: return [20,46,71,15,47,72,42,48,73]', 'role-specific Engineer advanced tree retained')
require(dm, 'expansionUpgradeCostMultiplier', 'depth-aware advanced upgrade pricing retained')
require(wm, 'var threat:int = 1', 'T1-T5 threat display retained')

# ---- Performance regression guards -----------------------------------------
require(cb, 'Math.abs(myClip.x - child.x) <= 900', 'character broad-phase collision/target filter')
require(cb, 'var myDepth:int = this.getZDepth()', 'incremental display-depth insertion')
forbid(cb, 'children.sort(this.zSorting)', 'legacy full battlefield sort removed')
require(cb, 'this._healthbar_refresh = 3', 'health bar refresh throttled')
require(pu, 'this._count_refresh = 8', 'player population scan throttled')
require(pu, 'this._ui_refresh = 3', 'player UI refresh throttled')
require(ew, 'countEnemyWave(COMMAND:Boolean = false)', 'wave count no longer implies command refresh')
require(ew, 'setMaxUnit(VAL:int = 25)', 'wave controller cap API retained')
require(be, 'var waveCap:int = Math.min(22,16 + int(tier / 4))', 'Expansion disposable-wave cap')
require(bg, 'burst = this.mGF.stageRoot.stage.quality == "low" ? 18 : 36', 'weather particle budget')
require(fx, 'isWorldXVisible(X:Number = 0, MARGIN:Number = 250)', 'offscreen effect culling')
require(fx, 'contBLOODSPLAT.numChildren >= 60', 'blood splat cap')
require(bs, 'load >= 175', 'adaptive heavy-load threshold')
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
