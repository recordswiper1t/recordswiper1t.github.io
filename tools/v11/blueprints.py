#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: blueprints.py <scripts-dir>')
scripts = Path(sys.argv[1])

def read(name):
    p=scripts/name
    if not p.exists(): raise SystemExit(f'missing: {p}')
    return p.read_text(encoding='utf-8-sig')

def write(name,text):
    (scripts/name).write_text(text,encoding='utf-8',newline='\n')

def insert_before(text, needle, block, label):
    n=text.count(needle)
    if n!=1: raise SystemExit(f'{label}: expected 1 anchor, found {n}')
    return text.replace(needle,block+needle,1)

blueprints = {
'TowerArcherCrossbow.as': [('special_multishoot','this.§case const§'),('special_eagle','this.§_-C1§')],
'TowerArcherTotem.as': [('special_weakness','this.§in static§'),('special_silence','this.§_-5A§')],
'TowerMageArchmage.as': [('special_explosion','this.§native const return§'),('special_twister','this.§final for false§')],
'TowerMageNecromancer.as': [('special_death_rider','this.deathRiderCurrentLevel'),('special_pestilence','this.§_-3K§')],
'TowerEngineerDwaarp.as': [('special_drill','this.§_-lJ§'),('special_lava','this.§_-jI§')],
'TowerEngineerMech.as': [('special_missiles','this.missilesCurrentLevel'),('special_oil','this.oilCurrentLevel')],
'TowerSoldierAssassin.as': [('special_sneak','this.§true const get§'),('special_peak','this.§set const false§'),('special_counter','this.§do for false§')],
'TowerSoldierTemplar.as': [('special_holygrail','this.holygrailCurrentLevel'),('special_extralife','this.§_-vW§'),('special_blood','this.bloodCurrentLevel')],
'TowerDwarfRiflemen.as': [('special_barrel','this.§default const continue§'),('special_damage','this.§_-QL§')],
'§_-Zs§.as': [('special_hammer','this.§_-v5§'),('special_armor','this.§implements implements§'),('special_beer','this.§_-K8§')],
}
for name, pairs in blueprints.items():
    text=read(name)
    if 'public function qolBlueprintActions() : Array' in text:
        continue
    lines=['      public function qolBlueprintActions() : Array','      {','         var actions:Array = [];','         var i:int = 0;']
    for action,field in pairs:
        lines += ['         i = 0;',f'         while(i < {field})','         {',f'            actions.push("{action}");','            i++;','         }']
    lines += ['         return actions;','      }','      ','']
    text=insert_before(text,'      override public function upgradeTower(param1:String) : void\n','\n'.join(lines),'blueprint '+name)
    write(name,text)

print('V11 blueprint patches applied')
