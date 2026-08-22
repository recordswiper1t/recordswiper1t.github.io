#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('usage: patch_mastery_v1.py <scripts-root>')
root=Path(sys.argv[1])

def one(rel, old, new, label):
    p=root/rel; t=p.read_text(encoding='utf-8-sig'); n=t.count(old)
    if n!=1: raise SystemExit(f'{rel} {label}: expected 1 match, got {n}')
    p.write_text(t.replace(old,new,1),encoding='utf-8',newline='\n')

C='com/brockw/stickwar/campaign/Campaign.as'
one(C,'   import com.brockw.stickwar.engine.Team.Tech;\n','   import com.brockw.stickwar.engine.Team.Tech;\n   import com.brockw.stickwar.engine.Team.Team;\n   import com.brockw.stickwar.engine.units.Unit;\n','imports')
one(C,'      public var isAutoSaveEnabled:Boolean;\n','      public var isAutoSaveEnabled:Boolean;\n      \n      private var _superRanks:Array;\n      public static const SUPER_MAX_RANK:int = 6;\n','fields')
one(C,'         this.campaignPoints = 0;\n','         this.campaignPoints = 0;\n         this._superRanks = new Array(22);\n         for(var superI:int = 0; superI < this._superRanks.length; superI++) this._superRanks[superI] = 0;\n','init')
one(C,'         cookie.data.techAllowed = tech;\n         cookie.flush();\n','         cookie.data.techAllowed = tech;\n         cookie.data.superRanks = this._superRanks.slice();\n         cookie.flush();\n','save')
one(C,'         var tech:Array = new Array();\n         for each(t in cookie.data.techAllowed)\n','         var tech:Array = new Array();\n         if(cookie.data.superRanks != undefined)\n         {\n            for(i = 0; i < this._superRanks.length && i < cookie.data.superRanks.length; i++) this._superRanks[i] = int(cookie.data.superRanks[i]);\n         }\n         for each(t in cookie.data.techAllowed)\n','load')
methods=r'''      public function getSuperRank(type:int) : int
      {
         return type >= 0 && type < this._superRanks.length ? int(this._superRanks[type]) : 0;
      }
      
      public function getSuperCost(type:int) : int
      {
         var r:int = this.getSuperRank(type) + 1;
         return r <= SUPER_MAX_RANK ? r : 0;
      }
      
      public function buySuperRank(type:int) : Boolean
      {
         var cost:int = this.getSuperCost(type);
         if(cost <= 0 || this.campaignPoints < cost) return false;
         this.campaignPoints -= cost;
         this._superRanks[type] = this.getSuperRank(type) + 1;
         return true;
      }
      
      public function getSuperTechName(type:int, rank:int) : String
      {
         var names:Array = null;
         switch(type)
         {
            case Unit.U_MINER: names="Deep Bag|Efficient Pick|Miner Hustle|Emergency Wall|Guild Logistics|Industrial Extraction".split("|"); break;
            case Unit.U_SWORDWRATH: names="Forged Blade|Footwork|Rage|Cleave|Berserker Blood|Captain's Rally".split("|"); break;
            case Unit.U_ARCHER: names="Composite Bow|Quiver Drill|Fire Arrows|Piercing Shot|Volley Doctrine|Deadeye".split("|"); break;
            case Unit.U_SPEARTON: names="Tempered Spear|Tower Shield|Shield Wall|Shield Bash|Phalanx|Javelin Mastery".split("|"); break;
            case Unit.U_MAGIKILL: names="Arcane Bolt|Summon|Electric Wall|Chain Blast|Summoner Circle|Storm Capstone".split("|"); break;
            case Unit.U_MONK: names="Mend|Purify|Sanctuary|Battle Prayer|Mass Heal|Resurrection".split("|"); break;
            case Unit.U_NINJA: names="Backstab|Sprint|Cloak|Poison Edge|Assassin Mark|Execution".split("|"); break;
            case Unit.U_FLYING_CROSSBOWMAN: names="Wing Drill|Bomb Satchel|Dive|Shrapnel|Sky Guard|Siege Flight".split("|"); break;
            case Unit.U_ENSLAVED_GIANT: names="Stone Fists|Thick Hide|Ground Slam|Siege Grip|Titan Blood|Earthshaker".split("|"); break;
            case Unit.U_CHAOS_MINER: names="Blood Pick|Forced Labor|Frenzy|Bone Cache|Dark Logistics|Abyssal Extraction".split("|"); break;
            case Unit.U_CAT: names="Fangs|Pack Speed|Leap|Blood Scent|Brood|Alpha".split("|"); break;
            case Unit.U_BOMBER: names="Dense Charge|Fast Fuse|Shrapnel|Chain Bomb|Martyr|Cataclysm".split("|"); break;
            case Unit.U_KNIGHT: names="Black Plate|Crushing Mace|Charge|Guard Break|Dread Aura|Juggernaut".split("|"); break;
            case Unit.U_DEAD: names="Rot Claw|Grave Flesh|Reanimate|Plague Bite|Bone Horde|Undying".split("|"); break;
            case Unit.U_WINGIDON: names="Wing Blade|Dark Bolt|Dive|Shadow Volley|Night Swarm|Matriarch's Favor".split("|"); break;
            case Unit.U_SKELATOR: names="Bone Staff|Summon Dead|Curse|Soul Drain|Mass Raise|Death Oracle".split("|"); break;
            case Unit.U_MEDUSA: names="Serpent Bolt|Stone Glare|Petrify|Venom Field|Gorgon Guard|Queen's Wrath".split("|"); break;
            case Unit.U_GIANT: names="Grave Fist|Rotten Hide|Corpse Toss|Terror Slam|Graveborn|World Breaker".split("|"); break;
         }
         return names != null && rank >= 1 && rank <= names.length ? String(names[rank - 1]) : "MAX";
      }
      
      public function applySuperResearch(team:Team, type:int) : void
      {
         if(team == null || team.tech == null) return;
         var r:int = this.getSuperRank(type);
         if(type == Unit.U_MINER) { if(r>=2) team.tech.isResearchedMap[Tech.MINER_SPEED]=1; if(r>=4) team.tech.isResearchedMap[Tech.MINER_WALL]=1; }
         else if(type == Unit.U_SWORDWRATH && r>=3) team.tech.isResearchedMap[Tech.SWORDWRATH_RAGE]=1;
         else if(type == Unit.U_ARCHER && r>=3) team.tech.isResearchedMap[Tech.ARCHIDON_FIRE]=1;
         else if(type == Unit.U_SPEARTON) { if(r>=2) team.tech.isResearchedMap[Tech.BLOCK]=1; if(r>=4) team.tech.isResearchedMap[Tech.SHIELD_BASH]=1; }
         else if(type == Unit.U_NINJA) { if(r>=3) team.tech.isResearchedMap[Tech.CLOAK]=1; if(r>=6) team.tech.isResearchedMap[Tech.CLOAK_II]=1; }
         else if(type == Unit.U_FLYING_CROSSBOWMAN && r>=3) team.tech.isResearchedMap[Tech.CROSSBOW_FIRE]=1;
         else if(type == Unit.U_MONK && r>=2) team.tech.isResearchedMap[Tech.MONK_CURE]=1;
         else if(type == Unit.U_MAGIKILL) { if(r>=2) team.tech.isResearchedMap[Tech.MAGIKILL_NUKE]=1; if(r>=3) team.tech.isResearchedMap[Tech.MAGIKILL_WALL]=1; if(r>=5) team.tech.isResearchedMap[Tech.MAGIKILL_POISON]=1; }
         else if(type == Unit.U_ENSLAVED_GIANT) { if(r>=3) team.tech.isResearchedMap[Tech.GIANT_GROWTH_I]=1; if(r>=5) team.tech.isResearchedMap[Tech.GIANT_GROWTH_II]=1; }
         else if(type == Unit.U_CHAOS_MINER) { if(r>=2) team.tech.isResearchedMap[Tech.MINER_SPEED]=1; if(r>=4) team.tech.isResearchedMap[Tech.MINER_TOWER]=1; }
         else if(type == Unit.U_CAT) { if(r>=2) team.tech.isResearchedMap[Tech.CAT_SPEED]=1; if(r>=4) team.tech.isResearchedMap[Tech.CAT_PACK]=1; }
         else if(type == Unit.U_KNIGHT && r>=3) team.tech.isResearchedMap[Tech.KNIGHT_CHARGE]=1;
         else if(type == Unit.U_DEAD && r>=3) team.tech.isResearchedMap[Tech.DEAD_POISON]=1;
         else if(type == Unit.U_WINGIDON && r>=3) team.tech.isResearchedMap[Tech.WINGIDON_SPEED]=1;
         else if(type == Unit.U_SKELATOR && r>=3) team.tech.isResearchedMap[Tech.SKELETON_FIST_ATTACK]=1;
         else if(type == Unit.U_MEDUSA && r>=4) team.tech.isResearchedMap[Tech.MEDUSA_POISON]=1;
         else if(type == Unit.U_GIANT) { if(r>=3) team.tech.isResearchedMap[Tech.CHAOS_GIANT_GROWTH_I]=1; if(r>=5) team.tech.isResearchedMap[Tech.CHAOS_GIANT_GROWTH_II]=1; }
      }
      
      public function getHybridSlots() : int
      {
         if(this.currentLevel >= 60) return 3;
         if(this.currentLevel >= 55) return 2;
         if(this.currentLevel >= 47) return 1;
         return 0;
      }
      
'''
one(C,'      public function get justTutorial() : Boolean\n',methods+'      public function get justTutorial() : Boolean\n','methods')

U='com/brockw/stickwar/engine/units/Unit.as'
one(U,'      private var _damageToDeal:Number;\n','      private var _damageToDeal:Number;\n      \n      private var _superMasteryApplied:int;\n','unit field')
one(U,'         this._health = 100;\n         this.stoned = false;\n','         this._health = 100;\n         this._superMasteryApplied = 0;\n         this.stoned = false;\n','unit reset')
unit_method=r'''      public function applySuperMastery(rank:int) : void
      {
         if(rank <= this._superMasteryApplied) return;
         if(rank > 6) rank = 6;
         for(var r:int=this._superMasteryApplied+1; r<=rank; r++)
         {
            if(r==1 || r==4 || r==6) { this.maxHealth=int(this.maxHealth*(r==6?1.15:(r==4?1.15:1.10))); this.health=this.maxHealth; }
            if(r==2 || r==5 || r==6) this.damageToDeal *= (r==6?1.15:(r==5?1.15:1.10));
            if(r==3 || r==6) { this._maxVelocity *= (r==6?1.12:1.08); this._maxForce *= (r==6?1.12:1.08); }
         }
         this._superMasteryApplied=rank;
      }
      
'''
one(U,'      public function setBuilding() : void\n',unit_method+'      public function setBuilding() : void\n','unit method')

T='com/brockw/stickwar/engine/Team/Team.as'
one(T,'         unit.init(game);\n         unit.healthBar.reset();\n','         unit.init(game);\n         if(game.main != null && game.main.campaign != null)\n         {\n            unit.applySuperMastery(game.main.campaign.getSuperRank(unit.type));\n            game.main.campaign.applySuperResearch(this,unit.type);\n         }\n         unit.healthBar.reset();\n','spawn mastery')
one(T,'         this.unitGroups[unit.type].push(unit);\n','         if(!(unit.type in this.unitGroups) || this.unitGroups[unit.type] == null) this.unitGroups[unit.type] = [];\n         this.unitGroups[unit.type].push(unit);\n','hybrid group')
print('Super mastery V1 applied')
