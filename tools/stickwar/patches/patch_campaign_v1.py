#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape
import sys

if len(sys.argv)!=2:
    raise SystemExit('usage: patch_campaign_v1.py <scripts-root>')
root=Path(sys.argv[1])

ORDER=['Miner','Swordwrath','Archidon','Spearton','Magikill','Monk','Ninja','FlyingCrossbowman','EnslavedGiant']
CHAOS=['ChaosMiner','Cat','Bomber','Knight','Dead','Wingadon','SkelatalMage','Medusa','Giant']

SW1=[
 ('Archidon Border',4,'The first Archidon nation blocks the conquest. Break the statue and take the bow.', ['Miner','Swordwrath'], ['Miner','Archidon'], 'Archidon'),
 ('Swordwrath Uprising',3,'Swordwrath legions counterattack before the new empire can stabilize.', ['Miner','Swordwrath','Archidon'], ['Miner','Swordwrath'], 'Swordwrath'),
 ('Spearton Pass',6,'A shield wall seals the mountain pass.', ['Miner','Swordwrath','Archidon'], ['Miner','Spearton'], 'Spearton'),
 ('Magikill Dominion',2,'The Magikill answer steel with summons and magic.', ['Miner','Swordwrath','Archidon','Spearton'], ['Miner','Magikill'], 'Magikill'),
 ('Giants of the West',5,'The giant tribes turn the western plains into a killing field.', ['Miner','Swordwrath','Archidon','Spearton','Magikill'], ['Miner','EnslavedGiant'], 'EnslavedGiant'),
 ('No Man\'s Land',1,'Cross open ground against a mixed army with no safe flank.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Swordwrath','Archidon','Spearton'], None),
 ('Ambush at Dusk',4,'The conquered tribes attack together at dusk.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Swordwrath','Archidon','Spearton','Magikill'], None),
 ('Ice Hills',0,'Push the conquest through the frozen north.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Archidon','Spearton','Magikill'], None),
 ('Castle Approach',7,'A fortified coalition makes its last stand before the capital.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], None),
 ('The Last Giant',3,'An ancient giant towers over the final tribal army.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','EnslavedGiant'], None),
 ('United Front',5,'The surviving nations unite against Order for one final field battle.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], None),
 ('Birth of the Empire',7,'Destroy the last coalition statue and complete the first conquest of Inamorta.', ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], ['Miner','Swordwrath','Archidon','Spearton','Magikill','EnslavedGiant'], None),
]

# Exactly 39 post-SW2 encounters. Together with 12 SW1 remasters + SW2's original
# 14 authored stages this produces the 65-stage Stick War Complete campaign.
POST=[
 ('Ashes of Order','Chaos',3),('Hollow Legion','Chaos',2),('Twin Fortresses','Order',7),('Black River','Chaos',4),
 ('Skyfall','Chaos',5),('Ritual Ground','Chaos',1),('Broken Phalanx','Order',6),('Stone and Bone','Chaos',5),
 ('Night of Knives','Order',3),('Second Crown','Chaos',7),('Frozen Frontier','Order',0),('Rifle Line','Order',6),
 ('Titan Spearton','Order',5),('War Mammoths','Chaos',1),('Whiteout','Order',0),('Siege Albowtross','Order',7),
 ('Iron Camp','Order',6),('Three Banners','Order',5),('Frozen King','Order',0),('Chaos Reborn','Chaos',2),
 ('Order\'s Shadow','Order',3),('Eclipsor Matriarch','Chaos',5),('Marrowkai Prime','Chaos',2),('Grave of Giants','Chaos',1),
 ('Medusa Ascendant','Chaos',7),('Twin Empires','Chaos',6),('Long Night','Chaos',4),('Last Conquest','Chaos',3),
 ('New Empire','Order',5),('Swordwrath Crucible','Order',3),('Archidon Gauntlet','Order',4),('Spearton Stand','Order',6),
 ('Magikill Trial','Order',2),('Giant Rampage','Order',5),('Miner\'s Fortune','Order',1),('Chaos Ascendant','Order',7),
 ('Order Ascendant','Chaos',7),('Hundred Unit War','Chaos',6),('Inamorta Benchmark','Chaos',5),
]

def xml_player(race, units, stage, enemy=False):
    miner='ChaosMiner' if race=='Chaos' else 'Miner'
    combat=[u for u in units if u!=miner]
    start=[miner,miner]
    if combat:
        start.append(combat[min((stage//3),len(combat)-1)])
    if stage>10 and combat:
        start.append(combat[min((stage//5),len(combat)-1)])
    statue=1000 + (stage*55 if enemy else min(stage,25)*12)
    gold=(650 + min(stage,20)*20) if not enemy else (450 + stage*45)
    mana=(150 + min(stage,20)*20) if not enemy else (100 + stage*30)
    body=[f'<player race="{race}" statueHealth="{statue}">']
    for u in start: body.append(f'<startingUnit>{u}</startingUnit>')
    for u in units: body.append(f'<unit>{u}</unit>')
    body += [f'<gold>{gold}</gold>',f'<mana>{mana}</mana>',f'<raceName>{race}</raceName>','</player>']
    return ''.join(body)

def level_xml(title,map_id,story,player_units,enemy_race,enemy_units,stage,unlock=None):
    # The vanilla campaign has scripted special controllers for its own 14 stages.
    # New levels intentionally use the generic normal victory condition so they are
    # robust while bespoke survival/boss controllers are layered on later.
    parts=[f'<level title="{escape(title)}" map="{map_id}" story="{escape(story)}" points="1">']
    if unlock: parts.append(f'<unlock>{unlock}</unlock>')
    p=xml_player('Order',player_units,stage,False)
    parts.append(p)
    o=xml_player(enemy_race,enemy_units,stage,True).replace('<player ','<oponent ',1).replace('</player>','</oponent>',1)
    parts.append(o)
    # Existing CampaignGameScreen reads these values; keep difficulty growth smooth.
    normal=1.0 + max(0,stage-12)*0.012
    hard=1.15 + max(0,stage-12)*0.016
    insane=1.35 + max(0,stage-12)*0.022
    health=1.0 + max(0,stage-12)*0.010
    damage=1.0 + max(0,stage-12)*0.008
    parts += [f'<normal>{normal:.3f}</normal>',f'<hard>{hard:.3f}</hard>',f'<insane>{insane:.3f}</insane>',
              f'<normalHealthScale>{health:.3f}</normalHealthScale>',f'<normalDamageScale>{damage:.3f}</normalDamageScale>',
              '<tip>Stick War Complete: build an economy, scout the composition, and use combined arms.</tip>','</level>']
    return ''.join(parts)

sw1_levels=[]
for idx,(title,map_id,story,punits,eunits,unlock) in enumerate(SW1,1):
    sw1_levels.append(level_xml(title,map_id,story,punits,'Order',eunits,idx,unlock))

post_levels=[]
for j,(title,race,map_id) in enumerate(POST,1):
    stage=26+j  # 12 SW1 + 14 original SW2 before postgame.
    if race=='Chaos':
        # Gradually widen Chaos's roster before the Omega stretch.
        count=min(len(CHAOS),3 + j//4)
        roster=CHAOS[:count]
    else:
        count=min(len(ORDER),4 + j//5)
        roster=ORDER[:count]
    post_levels.append(level_xml(title,map_id,
        'A new war reshapes Inamorta. This encounter is part of the Stick War Complete postgame campaign.',
        ORDER,race,roster,stage,None))

SW1_XML='<campaign>'+''.join(sw1_levels)+'</campaign>'
POST_XML='<campaign>'+''.join(post_levels)+'</campaign>'

p=root/'com/brockw/stickwar/campaign/Campaign.as'
t=p.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n!=1: raise SystemExit(f'Campaign.as {label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

one('''         var x:* = undefined;\n         super();\n''','''         var x:* = undefined;\n         var sw1Xml:XML = null;\n         var postXml:XML = null;\n         super();\n''','constructor locals')
one('''         this.xml = new XML(str);\n         for each(x in this.xml.level)\n         {\n            this.levels.push(new Level(x));\n         }\n''',f'''         this.xml = new XML(str);\n         // Stick War Complete: SW1 remaster -> all original SW2 authored stages -> postgame.\n         sw1Xml = new XML({SW1_XML!r});\n         postXml = new XML({POST_XML!r});\n         for each(x in sw1Xml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n         for each(x in this.xml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n         for each(x in postXml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n''','campaign assembly')
# Keep expansion saves completely separate from the vanilla Stick War 2 SharedObject.
t=t.replace('SharedObject.getLocal("stickempiresSave")','SharedObject.getLocal("stickwarCompleteSaveV1")')
if t.count('stickwarCompleteSaveV1') != 3:
    raise SystemExit('Campaign.as save namespace: expected 3 SharedObject sites')
p.write_text(t,encoding='utf-8',newline='\n')
print('patched',p)

# Raise the engine population ceiling for large expansion battles. The actual team
# population limit comes from global game XML, so clamp it upward without changing
# vanilla production costs or unit population values.
p=root/'com/brockw/stickwar/engine/Team/Team.as'
t=p.read_text(encoding='utf-8-sig')
old='''         this.populationLimit = game.xml.xml.populationLimit;\n'''
new='''         this.populationLimit = Math.max(int(game.xml.xml.populationLimit),120);\n'''
if t.count(old)!=1: raise SystemExit('Team population limit anchor mismatch')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('patched',p)
print('Stick War Complete campaign: 12 SW1 + 14 original SW2 + 39 postgame = 65 stages')
