#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_campaign_v2.py <scripts-root>')
root = Path(sys.argv[1])

ORDER = ['Miner','Swordwrath','Archidon','Spearton','Ninja','FlyingCrossbowman','Monk','Magikill','EnslavedGiant']
CHAOS = ['ChaosMiner','Cat','Bomber','Knight','Dead','Wingadon','SkelatalMage','Medusa','Giant']

SW1 = [
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

# title, player race, opponent race, map. These are post-SW2 stages 27..65.
# Several late-game missions deliberately switch the playable side to Chaos.
POST = [
 ('Ashes of Order','Order','Chaos',3),('Hollow Legion','Order','Chaos',2),('Twin Fortresses','Order','Order',7),('Black River','Order','Chaos',4),
 ('Skyfall','Order','Chaos',5),('Ritual Ground','Order','Chaos',1),('Broken Phalanx','Order','Order',6),('Stone and Bone','Order','Chaos',5),
 ('Night of Knives','Order','Order',3),('Second Crown','Order','Chaos',7),('Frozen Frontier','Order','Order',0),('Rifle Line','Order','Order',6),
 ('Titan Spearton','Order','Order',5),('War Mammoths','Order','Chaos',1),('Whiteout','Order','Order',0),('Siege Albowtross','Order','Order',7),
 ('Iron Camp','Order','Order',6),('Three Banners','Order','Order',5),('Frozen King','Order','Order',0),
 ('Chaos Reborn','Chaos','Order',2),('Order\'s Shadow','Chaos','Order',3),('Eclipsor Matriarch','Order','Chaos',5),
 ('Marrowkai Prime','Order','Chaos',2),('Grave of Giants','Chaos','Order',1),('Medusa Ascendant','Chaos','Order',7),
 ('Twin Empires','Order','Chaos',6),('Long Night','Order','Chaos',4),('Last Conquest','Chaos','Order',3),('New Empire','Order','Chaos',5),
 ('Swordwrath Crucible','Order','Order',3),('Archidon Gauntlet','Order','Order',4),('Spearton Stand','Order','Order',6),
 ('Magikill Trial','Order','Order',2),('Giant Rampage','Order','Chaos',5),('Miner\'s Fortune','Order','Chaos',1),
 ('Chaos Ascendant','Chaos','Order',7),('Order Ascendant','Order','Chaos',7),('Hundred Unit War','Order','Chaos',6),('Inamorta Benchmark','Order','Chaos',5),
]

def roster_for(race, depth):
    src = CHAOS if race == 'Chaos' else ORDER
    start = 3 if race == 'Chaos' else 4
    return src[:min(len(src), start + depth // 4)]

def xml_player(race, units, stage, enemy=False):
    miner = 'ChaosMiner' if race == 'Chaos' else 'Miner'
    combat = [u for u in units if u != miner]
    start = [miner, miner]
    if combat:
        start.append(combat[min(stage // 3, len(combat)-1)])
    if stage > 10 and combat:
        start.append(combat[min(stage // 5, len(combat)-1)])
    statue = 1000 + (stage * 55 if enemy else min(stage,25)*12)
    gold = (650 + min(stage,20)*20) if not enemy else (450 + stage*45)
    mana = (150 + min(stage,20)*20) if not enemy else (100 + stage*30)
    tag = 'oponent' if enemy else 'player'
    body = [f'<{tag} race="{race}" statueHealth="{statue}">']
    for u in start:
        body.append(f'<startingUnit>{u}</startingUnit>')
    for u in units:
        body.append(f'<unit>{u}</unit>')
    body += [f'<gold>{gold}</gold>', f'<mana>{mana}</mana>', f'<raceName>{race}</raceName>', f'</{tag}>']
    return ''.join(body)

def level_xml(title,map_id,story,player_race,player_units,enemy_race,enemy_units,stage,unlock=None,points=8):
    parts = [f'<level title="{escape(title)}" map="{map_id}" story="{escape(story)}" points="{points}">']
    if unlock:
        parts.append(f'<unlock>{unlock}</unlock>')
    parts.append(xml_player(player_race,player_units,stage,False))
    parts.append(xml_player(enemy_race,enemy_units,stage,True))
    # Smooth stat growth. Bespoke objective logic is layered by patch_super_systems_v1.py.
    normal = 1.0 + max(0,stage-12)*0.012
    hard = 1.15 + max(0,stage-12)*0.016
    insane = 1.35 + max(0,stage-12)*0.022
    health = 1.0 + max(0,stage-12)*0.010
    damage = 1.0 + max(0,stage-12)*0.008
    parts += [f'<normal>{normal:.3f}</normal>', f'<hard>{hard:.3f}</hard>', f'<insane>{insane:.3f}</insane>',
              f'<normalHealthScale>{health:.3f}</normalHealthScale>', f'<normalDamageScale>{damage:.3f}</normalDamageScale>',
              '<tip>Super Stick War: scout the composition, preserve the economy, use combined arms, and exploit direct control when needed.</tip>', '</level>']
    return ''.join(parts)

sw1_levels = []
for idx,(title,map_id,story,punits,eunits,unlock) in enumerate(SW1,1):
    sw1_levels.append(level_xml(title,map_id,story,'Order',punits,'Order',eunits,idx,unlock,8))

post_levels = []
for j,(title,player_race,enemy_race,map_id) in enumerate(POST,1):
    stage = 26 + j
    post_levels.append(level_xml(title,map_id,
        'The second conquest has ended, but a larger war now decides the future of Inamorta.',
        player_race, roster_for(player_race,j), enemy_race, roster_for(enemy_race,j+2), stage, None, 8))

SW1_XML = '<campaign>' + ''.join(sw1_levels) + '</campaign>'
POST_XML = '<campaign>' + ''.join(post_levels) + '</campaign>'

p = root/'com/brockw/stickwar/campaign/Campaign.as'
t = p.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n != 1:
        raise SystemExit(f'Campaign.as {label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

one('''         var x:* = undefined;\n         super();\n''','''         var x:* = undefined;\n         var sw1Xml:XML = null;\n         var postXml:XML = null;\n         super();\n''','constructor locals')
one('''         this.xml = new XML(str);\n         for each(x in this.xml.level)\n         {\n            this.levels.push(new Level(x));\n         }\n''',f'''         this.xml = new XML(str);\n         // SUPER STICK WAR CAMPAIGN V1: 12 SW1 remasters, 14 canonical SW2 stages, 39 postgame stages.\n         sw1Xml = new XML({SW1_XML!r});\n         postXml = new XML({POST_XML!r});\n         for each(x in sw1Xml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n         for each(x in this.xml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n         for each(x in postXml.level)\n         {{\n            this.levels.push(new Level(x));\n         }}\n''','campaign assembly')
# Separate expansion saves from canonical SW2.
t=t.replace('SharedObject.getLocal("stickempiresSave")','SharedObject.getLocal("stickwarCompleteSaveV1")')
if t.count('stickwarCompleteSaveV1') != 3:
    raise SystemExit('Campaign.as save namespace: expected 3 SharedObject sites')
p.write_text(t,encoding='utf-8',newline='\n')
print('patched',p)

# Expansion population ceiling. This is a floor: Battle Lab may raise it further before initTeams.
p = root/'com/brockw/stickwar/engine/Team/Team.as'
t = p.read_text(encoding='utf-8-sig')
old = '''         this.populationLimit = game.xml.xml.populationLimit;\n'''
new = '''         this.populationLimit = Math.max(int(game.xml.xml.populationLimit),120);\n'''
if t.count(old) != 1:
    raise SystemExit('Team population limit anchor mismatch')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('patched',p)
print('Super Stick War campaign V2: 12 SW1 + 14 canonical SW2 + 39 postgame = 65 stages; Order + Chaos player missions; 8 mastery points per new stage')
