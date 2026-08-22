#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('usage: patch_objectives_lab_v1.py <scripts-root>')
root=Path(sys.argv[1])

def one(rel, old, new, label):
    p=root/rel; t=p.read_text(encoding='utf-8-sig'); n=t.count(old)
    if n!=1: raise SystemExit(f'{rel} {label}: expected 1 match, got {n}')
    p.write_text(t.replace(old,new,1),encoding='utf-8',newline='\n')

C='com/brockw/stickwar/campaign/CampaignGameScreen.as'
one(C,'   import flash.events.*;\n','   import flash.events.*;\n   import flash.net.SharedObject;\n   import flash.utils.Dictionary;\n','imports')
one(C,'      public var doAiUpdates:Boolean;\n','''      public var doAiUpdates:Boolean;
      
      private var _superObjective:String;
      private var _superObjectiveStart:int;
      private var _superBoss:Unit;
      private var _superBossResolved:Boolean;
      private var _superNextWave:int;
      private var _superEconomyTarget:int;
      private var _superLabParams:Object;
      private var _superTimeAttack:Boolean;
      private var _superTimeRecorded:Boolean;
''','fields')
params='''         this._superLabParams = main.loaderInfo != null ? main.loaderInfo.parameters : null;\n         if(this._superLabParams != null && String(this._superLabParams.swcLab) == "1")\n         {\n            var pf:String=String(this._superLabParams.swcFaction); var ef:String=String(this._superLabParams.swcEnemy);\n            level.player.race = pf == "Chaos" ? "Chaos" : "Order";\n            level.oponent.race = ef == "Order" || ef == "Northern" ? "Order" : "Chaos";\n            if(int(this._superLabParams.swcGold)>0) level.player.gold=int(this._superLabParams.swcGold);\n            if(int(this._superLabParams.swcMana)>=0) level.player.mana=int(this._superLabParams.swcMana);\n         }\n'''
one(C,'         var level:Level = main.campaign.getCurrentLevel();\n','         var level:Level = main.campaign.getCurrentLevel();\n'+params,'params')
one(C,'         game.initGame(main,this,level.mapName);\n','         game.initGame(main,this,level.mapName);\n         if(this._superLabParams != null && String(this._superLabParams.swcLab)=="1" && int(this._superLabParams.swcPop)>=10) game.xml.xml.populationLimit=Math.min(500,int(this._superLabParams.swcPop));\n','population')
roster='''         if(this._superLabParams != null && String(this._superLabParams.swcLab)=="1")\n         {\n            var labUnits:Dictionary=new Dictionary();\n            if(level.player.race=="Chaos")\n            {\n               labUnits[Unit.U_CHAOS_MINER]=1; labUnits[Unit.U_CAT]=1; labUnits[Unit.U_BOMBER]=1; labUnits[Unit.U_KNIGHT]=1; labUnits[Unit.U_DEAD]=1; labUnits[Unit.U_WINGIDON]=1; labUnits[Unit.U_SKELATOR]=1; labUnits[Unit.U_MEDUSA]=1; labUnits[Unit.U_GIANT]=1;\n            }\n            else\n            {\n               labUnits[Unit.U_MINER]=1; labUnits[Unit.U_SWORDWRATH]=1; labUnits[Unit.U_ARCHER]=1; labUnits[Unit.U_SPEARTON]=1; labUnits[Unit.U_NINJA]=1; labUnits[Unit.U_FLYING_CROSSBOWMAN]=1; labUnits[Unit.U_MONK]=1; labUnits[Unit.U_MAGIKILL]=1; labUnits[Unit.U_ENSLAVED_GIANT]=1;\n            }\n            game.teamA.unitsAvailable=labUnits;\n         }\n'''
one(C,'         game.teamA.unitsAvailable = level.player.unitsAvailable;\n         game.teamB.unitsAvailable = level.oponent.unitsAvailable;\n','         game.teamA.unitsAvailable = level.player.unitsAvailable;\n         game.teamB.unitsAvailable = level.oponent.unitsAvailable;\n'+roster,'roster')
init='''         this.initSuperObjective();\n         if(this._superLabParams != null && String(this._superLabParams.swcLab)=="1")\n         {\n            userInterface.enableDiagnostics();\n            this.applyBattleLabPreset(String(this._superLabParams.swcPreset));\n            if(String(this._superLabParams.swcFaction)=="Hybrid")\n            {\n               this.spawnSuperUnit(this.team,Unit.U_KNIGHT); this.spawnSuperUnit(this.team,Unit.U_DEAD); this.spawnSuperUnit(this.team,Unit.U_CAT);\n            }\n            if(String(this._superLabParams.swcEnemy)=="Mixed")\n            {\n               this.spawnSuperUnit(this.team.enemyTeam,Unit.U_SPEARTON); this.spawnSuperUnit(this.team.enemyTeam,Unit.U_ARCHER);\n            }\n            else if(String(this._superLabParams.swcEnemy)=="Northern")\n            {\n               this.spawnSuperUnit(this.team.enemyTeam,Unit.U_SPEARTON,1.8,1.2); this.spawnSuperUnit(this.team.enemyTeam,Unit.U_ARCHER,1.5,1.25); this.spawnSuperUnit(this.team.enemyTeam,Unit.U_ENSLAVED_GIANT,1.5,1.15);\n            }\n         }\n'''
one(C,'         this.doAiUpdates = true;\n','         this.doAiUpdates = true;\n'+init,'objective init')
one(C,'         if(this.controller != null)\n         {\n            this.controller.update(this);\n         }\n         super.update(evt,timeDiff);\n','         if(this.controller != null)\n         {\n            this.controller.update(this);\n         }\n         this.updateSuperObjective();\n         super.update(evt,timeDiff);\n','update hook')
methods=r'''      private function objectiveForTitle(title:String) : String
      {
         if(title.indexOf("Benchmark")>=0 || title=="Hundred Unit War") return "benchmark";
         if(title.indexOf("Crucible")>=0 || title.indexOf("Gauntlet")>=0 || title.indexOf("Stand")>=0 || title.indexOf("Trial")>=0 || title.indexOf("Rampage")>=0) return "possession";
         if(title=="Miner's Fortune") return "economy";
         if(title.indexOf("Giant")>=0 || title.indexOf("King")>=0 || title.indexOf("Matriarch")>=0 || title.indexOf("Prime")>=0 || title.indexOf("Medusa")>=0 || title=="Last Conquest" || title=="Second Crown") return "boss";
         if(title=="No Man's Land" || title.indexOf("Night")>=0 || title=="Skyfall" || title=="Hollow Legion" || title=="War Mammoths") return "survive";
         return "destroy";
      }
      
      private function bossTypeForTitle(title:String) : int
      {
         if(title.indexOf("Spearton")>=0) return Unit.U_SPEARTON;
         if(title.indexOf("Albowtross")>=0) return Unit.U_FLYING_CROSSBOWMAN;
         if(title.indexOf("Matriarch")>=0) return Unit.U_WINGIDON;
         if(title.indexOf("Medusa")>=0) return Unit.U_MEDUSA;
         if(title.indexOf("Marrowkai")>=0 || title.indexOf("Bone")>=0) return Unit.U_SKELATOR;
         if(title.indexOf("Shadow")>=0 || title.indexOf("Knives")>=0) return Unit.U_NINJA;
         if(title.indexOf("Giant")>=0 || title.indexOf("King")>=0 || title=="Last Conquest") return this.team.enemyTeam.type==Team.T_CHAOS?Unit.U_GIANT:Unit.U_ENSLAVED_GIANT;
         return this.team.enemyTeam.type==Team.T_CHAOS?Unit.U_KNIGHT:Unit.U_SPEARTON;
      }
      
      private function spawnSuperUnit(target:Team,type:int,healthMul:Number=1,damageMul:Number=1) : Unit
      {
         var u:Unit=game.unitFactory.getUnit(type); target.spawn(u,game); u.x=u.px=target.homeX+target.direction*900; u.y=u.py=game.map.height/2; target.population+=u.population;
         if(healthMul!=1) { u.maxHealth=int(u.maxHealth*healthMul); u.health=u.maxHealth; }
         if(damageMul!=1) u.damageToDeal*=damageMul;
         return u;
      }
      
      private function initSuperObjective() : void
      {
         this._superObjective=this.objectiveForTitle(main.campaign.getCurrentLevel().title); this._superObjectiveStart=game.frame; this._superBoss=null; this._superBossResolved=false; this._superNextWave=game.frame+300; this._superEconomyTarget=5000; this._superTimeAttack=false; this._superTimeRecorded=false;
         if(this._superObjective=="boss")
         {
            var depth:Number=1+Math.max(0,main.campaign.currentLevel-20)*0.055; this._superBoss=this.spawnSuperUnit(this.team.enemyTeam,this.bossTypeForTitle(main.campaign.getCurrentLevel().title),3.5*depth,1.35+depth*0.25); this.team.enemyTeam.statue.maxHealth=Math.max(this.team.enemyTeam.statue.maxHealth,25000); this.team.enemyTeam.statue.health=this.team.enemyTeam.statue.maxHealth; userInterface.helpMessage.showMessage("BOSS — defeat the champion to break the enemy army");
         }
         else if(this._superObjective=="survive") userInterface.helpMessage.showMessage("SURVIVE — hold until the timer expires");
         else if(this._superObjective=="economy") userInterface.helpMessage.showMessage("ECONOMY — reach 5000 gold to win");
         else if(this._superObjective=="possession") userInterface.helpMessage.showMessage("POSSESSION TRIAL — select one unit and press F");
         else if(this._superObjective=="benchmark") { userInterface.enableDiagnostics(); this.applyBattleLabPreset(main.campaign.getCurrentLevel().title=="Inamorta Benchmark"?"Benchmark":"Massive Battle"); }
      }
      
      private function livingEnemyCombat() : int
      {
         var u:Unit=null; var count:int=0;
         for each(u in this.team.enemyTeam.units) if(u.isAlive() && u.type!=Unit.U_MINER && u.type!=Unit.U_CHAOS_MINER) ++count;
         return count;
      }
      
      private function recordTimeAttack() : void
      {
         if(this._superTimeRecorded) return; this._superTimeRecorded=true;
         var seconds:Number=(game.frame-this._superObjectiveStart)/30; var so:SharedObject=SharedObject.getLocal("superStickWarLabTimesV1"); var key:String="best_"+String(this._superLabParams.swcPreset)+"_"+main.campaign.getCurrentLevel().mapName;
         var old:Number=Number(so.data[key]); if(isNaN(old) || old<=0 || seconds<old) { so.data[key]=seconds; so.flush(); userInterface.helpMessage.showMessage("NEW BEST TIME: "+seconds.toFixed(2)+"s"); } else userInterface.helpMessage.showMessage("Time: "+seconds.toFixed(2)+"s  Best: "+old.toFixed(2)+"s");
      }
      
      private function updateSuperObjective() : void
      {
         var w:int=0; var duration:int=0;
         if(this._superTimeAttack && game.frame-this._superObjectiveStart>30 && this.livingEnemyCombat()==0) { this.recordTimeAttack(); this.team.enemyTeam.statue.damage(0,100000000,null); this._superTimeAttack=false; }
         if(this._superObjective=="boss" && !this._superBossResolved && (this._superBoss==null || !this._superBoss.isAlive())) { this._superBossResolved=true; this.team.enemyTeam.statue.damage(0,100000000,null); }
         else if(this._superObjective=="survive")
         {
            duration=main.campaign.getCurrentLevel().title=="Long Night"?3600:1800;
            if(game.frame-this._superObjectiveStart>=duration) this.team.enemyTeam.statue.damage(0,100000000,null);
            else if(game.frame>=this._superNextWave) { this._superNextWave+=300; for(w=0;w<4+int((game.frame-this._superObjectiveStart)/600);w++) this.spawnSuperUnit(this.team.enemyTeam,this.team.enemyTeam.type==Team.T_CHAOS?(w%2==0?Unit.U_CAT:Unit.U_DEAD):(w%2==0?Unit.U_SWORDWRATH:Unit.U_ARCHER)); }
         }
         else if(this._superObjective=="economy" && this.team.gold>=this._superEconomyTarget) this.team.enemyTeam.statue.damage(0,100000000,null);
         else if(this._superObjective=="possession" && game.frame-this._superObjectiveStart>180 && !userInterface.possessMode && (game.frame-this._superObjectiveStart)%300==0) userInterface.helpMessage.showMessage("Press F on one selected unit for direct control");
         else if(this._superObjective=="benchmark" && game.frame-this._superObjectiveStart>2700) this.team.enemyTeam.statue.damage(0,100000000,null);
      }
      
      private function applyBattleLabPreset(name:String) : void
      {
         var count:int=0; var i:int=0;
         if(name=="Massive Battle") count=35;
         else if(name=="Benchmark") count=100;
         else if(name=="Chaos") count=25;
         else if(name=="Possession") { count=30; userInterface.helpMessage.showMessage("Possession lab ready — select a unit and press F"); }
         else if(name=="Time Attack") { count=45; this.doAiUpdates=false; this._superTimeAttack=true; this._superObjectiveStart=game.frame; userInterface.helpMessage.showMessage("TIME ATTACK — destroy all combat units as fast as possible"); }
         else if(name=="Boss Rush") { this.doAiUpdates=false; for(i=0;i<5;i++) this.spawnSuperUnit(this.team.enemyTeam,i%2==0?(this.team.enemyTeam.type==Team.T_CHAOS?Unit.U_GIANT:Unit.U_ENSLAVED_GIANT):this.bossTypeForTitle("Medusa"),2.5,1.5); return; }
         for(i=0;i<count;i++) { this.spawnSuperUnit(this.team,i%3==0?this.team.getMinerType():(this.team.type==Team.T_CHAOS?Unit.U_CAT:Unit.U_SWORDWRATH)); this.spawnSuperUnit(this.team.enemyTeam,i%3==0?this.team.enemyTeam.getMinerType():(this.team.enemyTeam.type==Team.T_CHAOS?Unit.U_CAT:Unit.U_SWORDWRATH)); }
      }
      
'''
one(C,'      override public function leave() : void\n',methods+'      override public function leave() : void\n','methods')
print('Super objectives + Battle Lab V1 applied')
