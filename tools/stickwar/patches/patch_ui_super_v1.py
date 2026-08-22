#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('usage: patch_ui_super_v1.py <scripts-root>')
root=Path(sys.argv[1])

def one(rel, old, new, label):
    p=root/rel; t=p.read_text(encoding='utf-8-sig'); n=t.count(old)
    if n!=1: raise SystemExit(f'{rel} {label}: expected 1 match, got {n}')
    p.write_text(t.replace(old,new,1),encoding='utf-8',newline='\n')

C='com/brockw/stickwar/campaign/CampaignScreen.as'
one(C,'         if(this.main.campaign.currentLevel != 0)\n         {\n            this.mc.gotoAndStop("level" + this.main.campaign.currentLevel);\n         }\n','         if(this.main.campaign.currentLevel != 0)\n         {\n            this.mc.gotoAndStop(this.main.campaign.currentLevel >= 14 ? "level14" : "level" + this.main.campaign.currentLevel);\n         }\n','map clamp')
one(C,'         if(evt.target == this.mc.map.playbuttonflag && this.mc.currentFrameLabel == "level" + (this.main.campaign.currentLevel + 1))\n','         if(evt.target == this.mc.map.playbuttonflag && (this.main.campaign.currentLevel >= 13 || this.mc.currentFrameLabel == "level" + (this.main.campaign.currentLevel + 1)))\n','play flag')
exp_update='''         if(this.main.campaign.currentLevel >= 14)\n         {\n            this.mc.stop();\n            if(this.main.campaign.getCurrentLevel() != null)\n            {\n               this.mc.text.text = this.main.campaign.getCurrentLevel().storyName + "  [" + (this.main.campaign.currentLevel + 1) + "/" + this.main.campaign.levels.length + "]";\n               this.mc.title.text = this.main.campaign.getCurrentLevel().title;\n            }\n            this.mc.bottomPanel.y = 1192.15;\n            MovieClip(this.mc.map.playbuttonflag).buttonMode = true;\n            return;\n         }\n'''
one(C,'      public function update(evt:Event) : void\n      {\n','      public function update(evt:Event) : void\n      {\n'+exp_update,'map update')

U='com/brockw/stickwar/engine/UserInterface.as'
one(U,'   import flash.ui.Keyboard;\n','   import flash.ui.Keyboard;\n   import flash.text.TextField;\n   import flash.text.TextFormat;\n','text imports')
one(U,'      private var lastButton:SimpleButton;\n','      private var lastButton:SimpleButton;\n      \n      private var _possessedUnit:Unit;\n      private var _possessMode:Boolean;\n      private var _masteryOpen:Boolean;\n      private var _sandboxMode:Boolean;\n      private var _diagnostics:Boolean;\n      private var _superText:TextField;\n      private var _diagText:TextField;\n      private var _lastDiagFrame:int;\n      private var _sandboxNoPop:Boolean;\n','fields')
init='''         this._possessedUnit=null; this._possessMode=false; this._masteryOpen=false; this._sandboxMode=false; this._diagnostics=false; this._sandboxNoPop=false; this._lastDiagFrame=0;\n         this._superText=new TextField(); this._superText.defaultTextFormat=new TextFormat("_sans",16,16777215,true); this._superText.width=620; this._superText.height=190; this._superText.x=20; this._superText.y=70; this._superText.background=true; this._superText.backgroundColor=1052688; this._superText.alpha=0.92; this._superText.mouseEnabled=false; this._superText.visible=false; addChild(this._superText);\n         this._diagText=new TextField(); this._diagText.defaultTextFormat=new TextFormat("_typewriter",13,16777215,true); this._diagText.width=430; this._diagText.height=125; this._diagText.x=12; this._diagText.y=10; this._diagText.background=true; this._diagText.backgroundColor=0; this._diagText.alpha=0.75; this._diagText.mouseEnabled=false; this._diagText.visible=false; addChild(this._diagText);\n         if(this.main.campaign != null) for(var superType:int=1; superType<=20; superType++) this.main.campaign.applySuperResearch(this.team,superType);\n'''
one(U,'         addChild(this.helpMessage);\n','         addChild(this.helpMessage);\n'+init,'init')
one(U,'         this._hud = null;\n         Util.recursiveRemoval(Sprite(this));\n','         this._possessedUnit=null; this._superText=null; this._diagText=null;\n         this._hud = null;\n         Util.recursiveRemoval(Sprite(this));\n','cleanup')
one(U,'         this.keyBoardState.isDisabled = this.chat.isInput;\n','         this.keyBoardState.isDisabled = this.chat.isInput;\n         this.updateSuperControls();\n','update hook')
one(U,'         if(this.keyBoardState.isPressed(32))\n','         if(!this._possessMode && this.keyBoardState.isPressed(32))\n','space guard')
one(U,'         if(this.keyBoardState.isDown(39))\n','         if(!this._possessMode && this.keyBoardState.isDown(39))\n','right guard')
one(U,'         if(this.keyBoardState.isDown(37))\n','         if(!this._possessMode && this.keyBoardState.isDown(37))\n','left guard')
methods=r'''      private function updateSuperControls() : void
      {
         if(this.chat.isInput || this.gameScreen.isPaused) return;
         if(this.keyBoardState.isPressed(70)) this.togglePossession();
         if(this.keyBoardState.isPressed(85)) { this._masteryOpen=!this._masteryOpen; this._superText.visible=this._masteryOpen; this.refreshMasteryText(); }
         if(this._masteryOpen && this.keyBoardState.isPressed(13)) this.buyMastery();
         if(this.keyBoardState.isPressed(113)) { this._sandboxMode=!this._sandboxMode; this.helpMessage.showMessage(this._sandboxMode?"SUPER SANDBOX ON — 1-9 spawn, Shift enemy, G/M resources, B swarm, Delete clear":"SUPER SANDBOX OFF"); }
         if(this.keyBoardState.isPressed(112)) { this._diagnostics=!this._diagnostics; this._diagText.visible=this._diagnostics; }
         if(this._sandboxMode) this.updateSandbox();
         this.updateHybrid();
         if(this._possessMode) this.updatePossession();
         if(this._diagnostics) this.updateDiagnostics();
      }
      
      private function togglePossession() : void
      {
         if(this._possessMode) { this._possessMode=false; this._possessedUnit=null; this.helpMessage.showMessage("Possession released"); return; }
         if(this.selectedUnits.selected.length != 1) { this.helpMessage.showMessage("Select exactly one combat unit, then press F"); return; }
         var u:Unit=Unit(this.selectedUnits.selected[0]);
         if(u==null || !u.isAlive() || Boolean(u.interactsWith & Unit.I_IS_BUILDING)) { this.helpMessage.showMessage("That unit cannot be possessed"); return; }
         this._possessedUnit=u; this._possessMode=true; u.ai.setCommand(this.gameScreen.game,new HoldCommand(this.gameScreen.game));
         this.helpMessage.showMessage("POSSESSED — WASD/Arrows move, Space attacks, ability hotkeys work, F exits");
      }
      
      private function updatePossession() : void
      {
         if(this._possessedUnit==null || !this._possessedUnit.isAlive()) { this._possessMode=false; this._possessedUnit=null; return; }
         var mx:Number=0; var my:Number=0; var target:Unit=null;
         if(this.keyBoardState.isDown(65)||this.keyBoardState.isDown(37)) mx-=1;
         if(this.keyBoardState.isDown(68)||this.keyBoardState.isDown(39)) mx+=1;
         if(this.keyBoardState.isDown(87)||this.keyBoardState.isDown(38)) my-=1;
         if(this.keyBoardState.isDown(83)||this.keyBoardState.isDown(40)) my+=1;
         if(mx!=0 || my!=0) this._possessedUnit.walk(mx,my,mx==0?this._possessedUnit.getDirection():int(mx));
         if(this.keyBoardState.isDown(32)) { target=this._possessedUnit.ai.getClosestUnitTarget(); this._possessedUnit.ai.currentTarget=target; if(target!=null && this._possessedUnit.mayAttack(target)) this._possessedUnit.attack(); }
         this.gameScreen.game.targetScreenX=this._possessedUnit.px-this.gameScreen.game.map.screenWidth/2; this.isSlowCamera=false;
      }
      
      private function refreshMasteryText() : void
      {
         if(!this._masteryOpen || this.main.campaign==null) return;
         if(this.selectedUnits.selected.length==0) { this._superText.text="SUPER MASTERY — 108 nodes\nSelect a unit. U closes. Enter buys its next node."; return; }
         var type:int=Unit(this.selectedUnits.selected[0]).type; var rank:int=this.main.campaign.getSuperRank(type); var next:int=rank+1;
         this._superText.text="SUPER MASTERY — 108 nodes (18 x 6)\nType "+type+"   Rank "+rank+"/6   Points "+this.main.campaign.campaignPoints+"\n"+(rank>=6?"MAXED":"Next: "+this.main.campaign.getSuperTechName(type,next)+"   Cost: "+this.main.campaign.getSuperCost(type))+"\nEnter purchase | U close | F possess | Y hybrid";
      }
      
      private function buyMastery() : void
      {
         if(this.main.campaign==null || this.selectedUnits.selected.length==0) return;
         var u:Unit=Unit(this.selectedUnits.selected[0]);
         if(this.main.campaign.buySuperRank(u.type)) { this.main.campaign.applySuperResearch(this.team,u.type); u.applySuperMastery(this.main.campaign.getSuperRank(u.type)); this.main.campaign.save(); this.helpMessage.showMessage("Unlocked "+this.main.campaign.getSuperTechName(u.type,this.main.campaign.getSuperRank(u.type))); }
         else this.helpMessage.showMessage("Need more campaign points or mastery is maxed");
         this.refreshMasteryText();
      }
      
      private function sandboxTypeForKey(index:int, target:Team) : int
      {
         var order:Array=[Unit.U_MINER,Unit.U_SWORDWRATH,Unit.U_ARCHER,Unit.U_SPEARTON,Unit.U_NINJA,Unit.U_FLYING_CROSSBOWMAN,Unit.U_MONK,Unit.U_MAGIKILL,Unit.U_ENSLAVED_GIANT];
         var chaos:Array=[Unit.U_CHAOS_MINER,Unit.U_CAT,Unit.U_BOMBER,Unit.U_KNIGHT,Unit.U_DEAD,Unit.U_WINGIDON,Unit.U_SKELATOR,Unit.U_MEDUSA,Unit.U_GIANT];
         return target.type==Team.T_CHAOS?int(chaos[index]):int(order[index]);
      }
      
      private function spawnSuperUnit(type:int, target:Team) : Unit
      {
         if(target==null) return null;
         var u:Unit=this.gameScreen.game.unitFactory.getUnit(type);
         if(!this._sandboxNoPop && target.population+u.population>300) { this.gameScreen.game.unitFactory.returnUnit(type,u); this.helpMessage.showMessage("Population safety cap: 300 (O toggles)"); return null; }
         target.spawn(u,this.gameScreen.game); u.x=u.px=target.homeX+target.direction*(700+this.gameScreen.game.random.nextNumber()*300); u.y=u.py=this.gameScreen.game.map.height/2+this.gameScreen.game.random.nextNumber()*180-90; target.population+=u.population; return u;
      }
      
      private function updateSandbox() : void
      {
         var i:int=0; var victim:Unit=null; var victims:Array=null; var target:Team=this.keyBoardState.isShift?this.team.enemyTeam:this.team;
         for(i=0;i<9;i++) if(this.keyBoardState.isPressed(49+i)) this.spawnSuperUnit(this.sandboxTypeForKey(i,target),target);
         if(this.keyBoardState.isPressed(71)) this.team.gold+=1000;
         if(this.keyBoardState.isPressed(77)) this.team.mana+=1000;
         if(this.keyBoardState.isPressed(79)) { this._sandboxNoPop=!this._sandboxNoPop; this.helpMessage.showMessage(this._sandboxNoPop?"Population safety disabled":"Population safety enabled"); }
         if(this.keyBoardState.isPressed(46)) { victims=this.team.enemyTeam.units.slice(); for each(victim in victims) if(victim.isAlive()) victim.damage(0,100000000,null); }
         if(this.keyBoardState.isPressed(73)) this.team.enemyTeam.statue.damage(0,100000000,null);
         if(this.keyBoardState.isPressed(66)) for(i=0;i<12;i++) this.spawnSuperUnit(this.sandboxTypeForKey(i%9,this.team.enemyTeam),this.team.enemyTeam);
      }
      
      private function updateHybrid() : void
      {
         if(this.main.campaign==null || this.main.campaign.getHybridSlots()<=0 || !this.keyBoardState.isPressed(89)) return;
         var victim:Unit=null; var foreign:int=0; var cross:int=this.team.type==Team.T_CHAOS?Unit.U_SPEARTON:Unit.U_KNIGHT;
         for each(victim in this.team.units)
         {
            if(this.team.type==Team.T_CHAOS) { if(victim.type>=Unit.U_MINER && victim.type<=Unit.U_ENSLAVED_GIANT) ++foreign; }
            else if(victim.type==Unit.U_CHAOS_MINER||victim.type==Unit.U_CAT||victim.type==Unit.U_BOMBER||victim.type==Unit.U_KNIGHT||victim.type==Unit.U_DEAD||victim.type==Unit.U_WINGIDON||victim.type==Unit.U_SKELATOR||victim.type==Unit.U_MEDUSA||victim.type==Unit.U_GIANT) ++foreign;
         }
         if(foreign>=this.main.campaign.getHybridSlots()) { this.helpMessage.showMessage("Hybrid slots full: "+foreign+"/"+this.main.campaign.getHybridSlots()); return; }
         if(this.team.gold<1000 || this.team.mana<250) { this.helpMessage.showMessage("Hybrid deployment costs 1000 gold + 250 mana"); return; }
         this.team.gold-=1000; this.team.mana-=250; this.spawnSuperUnit(cross,this.team); this.helpMessage.showMessage("Hybrid deployed: "+(foreign+1)+"/"+this.main.campaign.getHybridSlots());
      }
      
      private function updateDiagnostics() : void
      {
         if(this.gameScreen.game.frame-this._lastDiagFrame<5) return; this._lastDiagFrame=this.gameScreen.game.frame;
         var units:int=this.gameScreen.game.teamA.units.length+this.gameScreen.game.teamB.units.length; var shots:int=this.gameScreen.game.projectileManager.projectiles.length; var fx:int=this.gameScreen.game.projectileManager.airEffects.length;
         this._diagText.text="SUPER STICK WAR DIAGNOSTICS\nFPS "+int(this.gameScreen.simulation.fps)+"   Units "+units+"   Projectiles "+shots+"   FX "+fx+"\nPlayer pop "+this.team.population+"   Enemy pop "+this.team.enemyTeam.population+"\nQuality "+this.gameScreen.quality+"   Possess "+this._possessMode+"   Sandbox "+this._sandboxMode+"\nF1 diagnostics | F2 sandbox | F possess | U mastery | Y hybrid";
      }
      
      public function get possessMode() : Boolean { return this._possessMode; }
      public function enableDiagnostics() : void { this._diagnostics=true; this._diagText.visible=true; }
      
'''
one(U,'      public function mouseUpEvent(evt:Event) : void\n',methods+'      public function mouseUpEvent(evt:Event) : void\n','methods')

G='com/brockw/stickwar/GameScreen.as'
one(G,'      public var strictPause:Boolean;\n','      public var strictPause:Boolean;\n      \n      private var _superPerfLastFrame:int;\n','perf field')
one(G,'         this.isFastForward = false;\n         this._isFastForwardFrame = false;\n','         this.isFastForward = false;\n         this._isFastForwardFrame = false;\n         this._superPerfLastFrame = 0;\n','perf init')
hook='''         if(this.game != null && this.game.frame-this._superPerfLastFrame>=30)\n         {\n            this._superPerfLastFrame=this.game.frame;\n            var actorLoad:int=this.game.teamA.units.length+this.game.teamB.units.length+this.game.projectileManager.projectiles.length;\n            if(actorLoad>=220 || this.simulation.fps<24) this.quality=S_LOW_QUALITY;\n            else if(actorLoad>=120 || this.simulation.fps<38) this.quality=S_MEDIUM_QUALITY;\n            else if(actorLoad<90 && this.simulation.fps>52) this.quality=S_HIGH_QUALITY;\n         }\n'''
one(G,'      public function update(evt:Event, timeDiff:Number) : void\n      {\n         var m:ScreenPositionUpdateMove = null;\n','      public function update(evt:Event, timeDiff:Number) : void\n      {\n         var m:ScreenPositionUpdateMove = null;\n'+hook,'perf hook')
print('Super UI/possession/sandbox/diagnostics V1 applied')
