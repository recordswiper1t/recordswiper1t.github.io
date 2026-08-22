#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_advanced_identity_v32.py <exported-scripts-root>')
p = Path(sys.argv[1])/'scripts'/'Game'/'System'/'StatDef'/'CharTotalStat.as'
t = p.read_text(encoding='utf-8-sig')
start = t.find('      private function expansionAdvancedTree() : Array\n')
end = t.find('      private function expansionAdvancedAbility(SLOT:int) : int\n', start)
if start < 0 or end < 0:
    raise SystemExit('V3.2 advanced identity region not found')

# Existing ability IDs only. No new ability/content count is introduced.
# Each row is the 9-node advanced half (slots 10..18), organized as three
# three-node continuations of the original tree branches.
method = r'''      private function expansionAdvancedTree() : Array
      {
         switch(this.id)
         {
            // Heroes
            case 1: return [20,25,58,35,37,66,36,38,43]; // Viegraf: guard / command / special
            case 2: return [20,29,65,15,39,56,36,38,75]; // Etheriea: ice / sustain / altar
            case 3: return [20,25,57,35,30,63,40,38,77]; // Skull Knight: rage / fire / castle

            // Haven / Necropolis / Underworld regular units
            case 10: return [20,46,52,15,47,39,37,48,35]; // Little Hobbit: swarm support
            case 11: return [15,25,58,36,39,26,41,38,76]; // Dwarf Defender: fortress tank
            case 12: return [20,37,60,15,28,71,35,39,32]; // Elf Hunter: ranged pressure
            case 13: return [20,29,69,15,39,53,37,38,75]; // Elderly Wizard: magic/support
            case 14: return [20,37,57,15,27,39,35,40,52]; // Amazon: fast melee
            case 15: return [15,25,58,36,39,55,41,38,76]; // Paladin: defense/healing
            case 16: return [20,37,60,15,28,71,35,39,48]; // Centaurion: mobile ranged
            case 17: return [20,34,68,15,29,66,39,38,75]; // Witch: poison/magic
            case 18: return [20,37,57,15,39,59,35,38,40]; // Vampire: sustain offense
            case 19: return [20,28,57,15,26,39,35,38,42]; // Anubis: durable assault
            case 20: return [20,46,57,15,47,37,35,48,39]; // Goblin: swarm aggression
            case 21: return [20,30,63,15,29,69,37,39,38]; // Succubus: fire caster
            case 22: return [15,25,76,36,39,26,41,38,57]; // Troll: wall/tank
            case 23: return [20,25,72,35,39,26,40,38,36]; // Gorilla: bruiser/fire tower
            case 24: return [20,29,68,15,37,76,35,39,38]; // Hell Raider: magic bruiser
            case 25: return [20,46,71,15,47,72,42,48,73]; // Dwarf Engineer: siege/towers
            case 26: return [20,37,42,40,46,57,35,47,48]; // Bomber: speed/demolition
            case 27: return [15,25,57,36,39,26,41,38,47]; // Taurus: frontline swarm
            case 28: return [15,25,58,36,39,42,41,38,76]; // Tank: armored siege

            // Elite / titan units
            case 50: return [20,28,53,35,37,66,39,38,67]; // Lamia
            case 51: return [15,25,58,36,39,76,41,38,42]; // Golem
            case 52: return [20,29,69,35,39,67,40,38,70]; // Death/Lich
            case 53: return [20,37,57,35,39,31,40,38,15]; // White Tiger
            case 54: return [20,30,63,35,39,56,40,38,69]; // Phoenix
            case 55: return [15,25,56,36,39,67,41,38,70]; // Divine Angel
            case 56: return [15,25,71,36,72,73,38,74,77]; // Iron Fortress
            case 57: return [20,25,58,35,39,66,40,38,53]; // Earth Dragon
            case 58: return [20,30,63,35,37,57,40,38,69]; // Black Dragon
            case 59: return [20,30,63,35,37,57,40,42,72]; // Inferno
            case 60: return [20,25,35,36,38,39,40,41,43]; // Lord of Hell
            default: return [20,15,25,35,36,37,38,39,42];
         }
      }
      
'''
t = t[:start] + method + t[end:]
p.write_text(t,encoding='utf-8',newline='\n')

for needle in [
    'case 10: return [20,46,52,15,47,39,37,48,35]',
    'case 13: return [20,29,69,15,39,53,37,38,75]',
    'case 25: return [20,46,71,15,47,72,42,48,73]',
    'case 51: return [15,25,58,36,39,76,41,38,42]',
    'case 56: return [15,25,71,36,72,73,38,74,77]',
    'case 60: return [20,25,35,36,38,39,40,41,43]'
]:
    if needle not in t:
        raise SystemExit('V3.2 advanced identity validation failed: '+needle)
if 'expansionPolishTree' in t:
    raise SystemExit('generic V3.2 dedupe helper remained after role-specific tree replacement')
print('Epic War 5 V3.2 role-specific advanced trees applied')
