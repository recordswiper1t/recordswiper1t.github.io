#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build-v10-map-specials.py <exported-v9-scripts-dir>')

p = Path(sys.argv[1]) / 'TowerHolder.as'
text = p.read_text(encoding='utf-8-sig')

start = text.index('         if(param1 == "qol_specials")')
end = text.index('         if(param1 == "qol_dwarf")', start)

new = r'''         if(param1 == "qol_specials")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_legion_archer","tw_archer",0,false,0,0,0,1,"TooltipBasic",{
               "title":"Legion Archer",
               "text":"Place the early-stage special archer tower."
            }),new Array("qol_mercenary","tw_soldier",0,false,0,0,0,2,"TooltipBasic",{
               "title":"Mercenary / Genie Camp",
               "text":"Place the Dunes special mercenary shop; recruits keep their normal hire costs."
            }),new Array("qol_amazona","tw_soldier",0,false,0,0,0,3,"TooltipBasic",{
               "title":"Spear Maiden Hut",
               "text":"Place the Crimson Valley jungle handmaiden / spear-maiden hut."
            }),new Array("qol_piratecamp","tw_archer",0,false,0,0,0,4,"TooltipBasic",{
               "title":"Pirate Cannon Camp",
               "text":"Place the map-special pirate cannon battery."
            }),new Array("qol_dwarf","tw_archer",250,false,0,0,0,5,"TooltipBasic",{
               "title":"Dwarf Riflemen — 250",
               "text":"Place the level-only Dwarf Riflemen tower."
            }),new Array("qol_pirates","tw_soldier",180,false,0,0,0,6,"TooltipBasic",{
               "title":"Pirate Barracks — 180",
               "text":"Place the level-only Pirate Barracks."
            }),new Array("qol_hall","tw_soldier",225,false,0,0,0,7,"TooltipBasic",{
               "title":"Dwarf Hall — 225",
               "text":"Place the map-special Dwarf Hall barracks."
            }),new Array("qol_specials2","tw_clean",0,false,0,0,0,8,"TooltipBasic",{
               "title":"Advanced normal towers →",
               "text":"Crossbow, Totem, Archmage, Necromancer, DWAARP and Battle-Mecha."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_specials2")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"Crossbow Fort",
               "text":"Build the Crossbow specialization directly."
            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Tribal Axethrowers",
               "text":"Build the Totem specialization directly."
            }),new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,3,"TooltipBasic",{
               "title":"Archmage",
               "text":"Build the Archmage specialization directly."
            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,4,"TooltipBasic",{
               "title":"Necromancer",
               "text":"Build the Necromancer specialization directly."
            }),new Array("qol_specials3","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"More advanced towers →",
               "text":"Open DWAARP and Battle-Mecha."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,8,"TooltipBasic",{
               "title":"← Map-special buildings",
               "text":"Return to the real map-special building page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_specials3")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Map-special buildings",
               "text":"Return to the real map-special building page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
'''

text = text[:start] + new + text[end:]

# Remove V9's mistaken bespoke Assassin/Templar map-special actions. They remain
# available through the game's normal barracks upgrade path.
for action in ('qol_assassin', 'qol_templar'):
    marker = f'         if(param1 == "{action}")\n'
    i = text.find(marker)
    if i >= 0:
        brace = text.find('{', i)
        depth = 0
        j = brace
        while j < len(text):
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    j += 1
                    while j < len(text) and text[j] in '\r\n': j += 1
                    break
            j += 1
        text = text[:i] + text[j:]

for needle in [
    '"title":"Legion Archer"',
    '"title":"Mercenary / Genie Camp"',
    '"title":"Spear Maiden Hut"',
    '"title":"Advanced normal towers →"',
    'if(param1 == "qol_legion_archer")',
    'if(param1 == "qol_mercenary")',
    'if(param1 == "qol_amazona")',
]:
    if needle not in text:
        raise SystemExit(f'validation failed: {needle}')

p.write_text(text, encoding='utf-8', newline='\n')
print('V10 real map-special menu applied')
