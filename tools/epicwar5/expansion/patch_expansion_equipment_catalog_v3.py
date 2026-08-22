#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_expansion_equipment_catalog_v3.py <exported-scripts-root>')
root = Path(sys.argv[1])
base = root / 'scripts' / 'Game'


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

# ------------------------------------------------------------------
# DataManager: make the inventory array large enough for items 31..55.
# ------------------------------------------------------------------
p = base / 'Manager' / 'DataManager.as'
t = p.read_text(encoding='utf-8-sig')
t = once(t,
'''      private function expansionEnsureData() : void
      {
         var ids:Array =''',
'''      private function expansionEnsureData() : void
      {
         while(this.dat_item_inv.length < 55) this.dat_item_inv.push(0);
         var ids:Array =''',
'expansion inventory padding')
p.write_text(t, encoding='utf-8', newline='\n')

# ------------------------------------------------------------------
# CharAbilityStat: 25 new composite gear abilities (81..105).
# ------------------------------------------------------------------
p = base / 'System' / 'StatDef' / 'CharAbilityStat.as'
t = p.read_text(encoding='utf-8-sig')
anchor = '''            case 77:
               this.name_id = "b_castle";
               this.name_str = "Castle Defense";
               this.desc = "Build Castle Defense (Attack+Healing)";
               this.spell_manacost = 80;
               this.rank = 25;
'''
cases = r'''            case 77:
               this.name_id = "b_castle";
               this.name_str = "Castle Defense";
               this.desc = "Build Castle Defense (Attack+Healing)";
               this.spell_manacost = 80;
               this.rank = 25;
               break;
            case 81:
               this.name_id = "x_vanguard"; this.name_str = "Vanguard"; this.desc = "Damage +30%, health +10%"; this.damage_mult = 0.30; this.health_boost = 0.10; this.rank = 50; break;
            case 82:
               this.name_id = "x_bastion"; this.name_str = "Bastion"; this.desc = "Health +40%, defense +15%"; this.health_boost = 0.40; this.defense_mult = 0.15; this.rank = 55; break;
            case 83:
               this.name_id = "x_windstep"; this.name_str = "Windstep"; this.desc = "Speed +1.5, damage +10%"; this.speed = 1.5; this.damage_mult = 0.10; this.rank = 52; break;
            case 84:
               this.name_id = "x_bloodsigil"; this.name_str = "Blood Sigil"; this.desc = "Damage +35%, regen +40, health -10%"; this.damage_mult = 0.35; this.health_regen = 40; this.health_boost = -0.10; this.rank = 58; break;
            case 85:
               this.name_id = "x_titanbelt"; this.name_str = "Titan Belt"; this.desc = "Population +3, health +20%"; this.pop = 3; this.health_boost = 0.20; this.rank = 60; break;
            case 86:
               this.name_id = "x_arcaneguard"; this.name_str = "Arcane Guard"; this.desc = "Magic resistance, health +15%"; this.resist_magic = 1; this.health_boost = 0.15; this.rank = 62; break;
            case 87:
               this.name_id = "x_spearbreaker"; this.name_str = "Spearbreaker"; this.desc = "Pierce resistance, defense +15%"; this.resist_pierce = 1; this.defense_mult = 0.15; this.rank = 62; break;
            case 88:
               this.name_id = "x_bladebreaker"; this.name_str = "Bladebreaker"; this.desc = "Slash resistance, defense +15%"; this.resist_slash = 1; this.defense_mult = 0.15; this.rank = 62; break;
            case 89:
               this.name_id = "x_hammerbreaker"; this.name_str = "Hammerbreaker"; this.desc = "Strike resistance, defense +15%"; this.resist_strike = 1; this.defense_mult = 0.15; this.rank = 62; break;
            case 90:
               this.name_id = "x_phoenixcore"; this.name_str = "Phoenix Core"; this.desc = "Regen +250, health +20%"; this.health_regen = 250; this.health_boost = 0.20; this.rank = 68; break;
            case 91:
               this.name_id = "x_hellfire"; this.name_str = "Hellfire Brand"; this.desc = "Fire attack, damage +25%"; this.attack_elemental = "fire"; this.damage_mult = 0.25; this.rank = 70; break;
            case 92:
               this.name_id = "x_frostbite"; this.name_str = "Frostbite Seal"; this.desc = "Ice attack, defense +20%"; this.attack_elemental = "ice"; this.defense_mult = 0.20; this.rank = 70; break;
            case 93:
               this.name_id = "x_stormcrown"; this.name_str = "Storm Crown"; this.desc = "Thunder attack, damage +20%, speed +0.5"; this.attack_elemental = "thunder"; this.damage_mult = 0.20; this.speed = 0.5; this.rank = 72; break;
            case 94:
               this.name_id = "x_venomfang"; this.name_str = "Venom Fang"; this.desc = "Poison attack, damage +25%"; this.attack_elemental = "poison"; this.damage_mult = 0.25; this.rank = 72; break;
            case 95:
               this.name_id = "x_abysslens"; this.name_str = "Abyss Lens"; this.desc = "Dark attack, damage +25%"; this.attack_elemental = "dark"; this.damage_mult = 0.25; this.rank = 74; break;
            case 96:
               this.name_id = "x_siegegauntlet"; this.name_str = "Siege Gauntlet"; this.desc = "Building damage +1000, damage +15%"; this.attack_building = 1000; this.damage_mult = 0.15; this.rank = 76; break;
            case 97:
               this.name_id = "x_warlord"; this.name_str = "Warlord Crest"; this.desc = "Damage +20%, defense +15%, population +1"; this.damage_mult = 0.20; this.defense_mult = 0.15; this.pop = 1; this.rank = 78; break;
            case 98:
               this.name_id = "x_colossus"; this.name_str = "Colossus Heart"; this.desc = "Health +50%, speed -0.3"; this.health_boost = 0.50; this.speed = -0.3; this.rank = 80; break;
            case 99:
               this.name_id = "x_duelist"; this.name_str = "Duelist Charm"; this.desc = "Damage +30%, speed +0.8, health -10%"; this.damage_mult = 0.30; this.speed = 0.8; this.health_boost = -0.10; this.rank = 82; break;
            case 100:
               this.name_id = "x_paladin"; this.name_str = "Paladin Reliquary"; this.desc = "Health +30%, defense +20%, regen +50"; this.health_boost = 0.30; this.defense_mult = 0.20; this.health_regen = 50; this.rank = 84; break;
            case 101:
               this.name_id = "x_sorcerer"; this.name_str = "Sorcerer Prism"; this.desc = "Magic resistance, speed +0.5, health +10%"; this.resist_magic = 1; this.speed = 0.5; this.health_boost = 0.10; this.rank = 86; break;
            case 102:
               this.name_id = "x_beasttotem"; this.name_str = "Beast Totem"; this.desc = "Population +2, damage +20%"; this.pop = 2; this.damage_mult = 0.20; this.rank = 88; break;
            case 103:
               this.name_id = "x_guardianhalo"; this.name_str = "Guardian Halo"; this.desc = "All physical/magic resistance, health +15%"; this.resist_strike = 1; this.resist_slash = 1; this.resist_pierce = 1; this.resist_magic = 1; this.health_boost = 0.15; this.rank = 92; break;
            case 104:
               this.name_id = "x_berserkercrown"; this.name_str = "Berserker Crown"; this.desc = "Damage +60%, health -15%"; this.damage_mult = 0.60; this.health_boost = -0.15; this.rank = 96; break;
            case 105:
               this.name_id = "x_artlogicprime"; this.name_str = "Artlogic Prime"; this.desc = "Damage +35%, health +35%, defense +20%, regen +100"; this.damage_mult = 0.35; this.health_boost = 0.35; this.defense_mult = 0.20; this.health_regen = 100; this.rank = 110;
'''
t = once(t, anchor, cases, 'new equipment abilities')
t = once(t, '         for(i = 1; i <= 80; i++)\n', '         for(i = 1; i <= 105; i++)\n', 'ability name lookup range')
p.write_text(t, encoding='utf-8', newline='\n')

# ------------------------------------------------------------------
# CharItemStat: item IDs 31..55, one unique reward per expansion stage.
# ------------------------------------------------------------------
p = base / 'System' / 'StatDef' / 'CharItemStat.as'
t = p.read_text(encoding='utf-8-sig')
anchor = '''            case 30:
               this.name_id = "itm_special";
               this.name_str = "Artlogic\'s Badge";
               this.desc = "Grants awesome skill!?";
               this.rank = 3;
               this.ability_name_id = "p_special";
'''
items = [
('exp_vanguard','Vanguard Edge','Damage +30%, health +10%','x_vanguard'),
('exp_bastion','Bastion Plate','Health +40%, defense +15%','x_bastion'),
('exp_windstep','Windstep Boots','Speed +1.5, damage +10%','x_windstep'),
('exp_bloodsigil','Blood Sigil','Damage +35%, regen +40, health -10%','x_bloodsigil'),
('exp_titanbelt','Titan Belt','Population +3, health +20%','x_titanbelt'),
('exp_arcaneguard','Arcane Guard','Magic resistance, health +15%','x_arcaneguard'),
('exp_spearbreaker','Spearbreaker Ring','Pierce resistance, defense +15%','x_spearbreaker'),
('exp_bladebreaker','Bladebreaker Ring','Slash resistance, defense +15%','x_bladebreaker'),
('exp_hammerbreaker','Hammerbreaker Ring','Strike resistance, defense +15%','x_hammerbreaker'),
('exp_phoenixcore','Phoenix Core','Regen +250, health +20%','x_phoenixcore'),
('exp_hellfire','Hellfire Brand','Fire attack, damage +25%','x_hellfire'),
('exp_frostbite','Frostbite Seal','Ice attack, defense +20%','x_frostbite'),
('exp_stormcrown','Storm Crown','Thunder attack, damage +20%, speed +0.5','x_stormcrown'),
('exp_venomfang','Venom Fang','Poison attack, damage +25%','x_venomfang'),
('exp_abysslens','Abyss Lens','Dark attack, damage +25%','x_abysslens'),
('exp_siegegauntlet','Siege Gauntlet','Building damage +1000, damage +15%','x_siegegauntlet'),
('exp_warlord','Warlord Crest','Damage +20%, defense +15%, population +1','x_warlord'),
('exp_colossus','Colossus Heart','Health +50%, speed -0.3','x_colossus'),
('exp_duelist','Duelist Charm','Damage +30%, speed +0.8, health -10%','x_duelist'),
('exp_paladin','Paladin Reliquary','Health +30%, defense +20%, regen +50','x_paladin'),
('exp_sorcerer','Sorcerer Prism','Magic resistance, speed +0.5, health +10%','x_sorcerer'),
('exp_beasttotem','Beast Totem','Population +2, damage +20%','x_beasttotem'),
('exp_guardianhalo','Guardian Halo','All resistance, health +15%','x_guardianhalo'),
('exp_berserkercrown','Berserker Crown','Damage +60%, health -15%','x_berserkercrown'),
('exp_artlogicprime','Artlogic Prime','Damage +35%, health +35%, defense +20%, regen +100','x_artlogicprime')]
block = anchor + '               break;\n'
for idx,(nid,name,desc,ability) in enumerate(items,31):
    block += f'''            case {idx}:\n               this.name_id = "{nid}";\n               this.name_str = "{name}";\n               this.desc = "{desc}";\n               this.rank = {4 + (idx-31)//5};\n               this.ability_name_id = "{ability}";\n               break;\n'''
# Remove final break for last case is harmless; leave it.
t = once(t, anchor, block, 'new equipment items')
t = once(t, '         for(i = 1; i <= 30; i++)\n', '         for(i = 1; i <= 55; i++)\n', 'item name lookup range')
p.write_text(t, encoding='utf-8', newline='\n')

# ------------------------------------------------------------------
# Equipment inventory UI: five pages and recycled icon frames for new items.
# Runs after patch_equipment_slots_v3.py.
# ------------------------------------------------------------------
p = base / 'Interface' / 'WorldMapFormationAcc.as'
t = p.read_text(encoding='utf-8-sig')
helper = r'''      private function expansionItemIconFrame(ID:int) : int
      {
         if(ID <= 0) return 1;
         return (ID - 1) % 30 + 1;
      }
      
'''
t = once(t, '      private function itemSlotParsing(', helper + '      private function itemSlotParsing(', 'item icon helper')
t = t.replace('CLIP.icon.gotoAndStop(ID);', 'CLIP.icon.gotoAndStop(this.expansionItemIconFrame(ID));')
t = t.replace('this.equip1.icon.gotoAndStop(itemEquip);', 'this.equip1.icon.gotoAndStop(this.expansionItemIconFrame(itemEquip));')
t = once(t, '         this.page.htmlText = String("Page " + this.pageNum + " / " + "3");\n', '         this.page.htmlText = String("Page " + this.pageNum + " / " + "5");\n', 'five inventory pages label')
t = once(t, '            this.pageNum = 3;\n', '            this.pageNum = 5;\n', 'previous wrap to page five')
t = once(t, '         if(this.pageNum > 3)\n', '         if(this.pageNum > 5)\n', 'next wrap after page five')
t = once(t, '         var itemSlot:int = int(CLIP.icon.currentFrame);\n', '         var itemSlot:int = (this.pageNum - 1) * 12 + NUM;\n         if(itemSlot > 55) return;\n', 'real item ID selection')
p.write_text(t, encoding='utf-8', newline='\n')

for rel, needles in {
    'Manager/DataManager.as':['dat_item_inv.length < 55'],
    'System/StatDef/CharAbilityStat.as':['case 105:','x_artlogicprime','i <= 105'],
    'System/StatDef/CharItemStat.as':['case 55:','Artlogic Prime','i <= 55'],
    'Interface/WorldMapFormationAcc.as':['expansionItemIconFrame','Page " + this.pageNum + " / " + "5"','itemSlot > 55']
}.items():
    z = (base / rel).read_text(encoding='utf-8-sig')
    for needle in needles:
        if needle not in z:
            raise SystemExit(f'{rel} missing {needle}')

print('Expansion V3 25-item equipment catalog and five-page inventory applied')
