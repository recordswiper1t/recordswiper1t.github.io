package
{
   import §_-aW§.*;
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13153")]
   public class SoldierHeroAlien extends §dynamic const class§
   {
      
      internal var configuration:Object;
      
      internal var energyGlaiveLevel:int;
      
      internal var energyGlaiveCastMinRange:int;
      
      internal var energyGlaiveCastMaxRange:int;
      
      internal var energyGlaiveReloadTime:int;
      
      internal var energyGlaiveReloadTimeCounter:int;
      
      internal var §_-fv§:Boolean;
      
      internal var energyGlaiveTarget:EnemyCommon;
      
      internal var energyGlaiveTargetPosition:Point;
      
      internal var §_-8g§:int;
      
      internal var purificationProtocolDrones:int;
      
      internal var purificationProtocolMinRange:int;
      
      internal var purificationProtocolMaxRange:int;
      
      internal var §while try§:int;
      
      internal var §_-eQ§:int;
      
      internal var §_-fK§:Boolean;
      
      internal var §finally try§:EnemyCommon;
      
      internal var purificationProtocolTargetPosition:Point;
      
      internal var §_-K9§:int;
      
      internal var abductionTotalHealth:int;
      
      internal var §dynamic extends§:int;
      
      internal var §_-Yw§:int;
      
      internal var abductionMaxRange:int;
      
      internal var §else const with§:int;
      
      internal var §_-By§:int;
      
      internal var isCastingAbduction:Boolean;
      
      internal var §with const set§:EnemyCommon;
      
      internal var finalCountdownDamage:int;
      
      internal var finalCountdownRange:int;
      
      internal var referencePath:int;
      
      internal var referenceNode:int;
      
      internal var energyGlaiveXpMultiplier:Number;
      
      internal var purificationProtocolDroneXpMultiplier:Number;
      
      internal var abductionXpMultiplier:Number;
      
      internal var §break for do§:§var const do§;
      
      public function SoldierHeroAlien(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,5,this.frame6,30,this.frame31,67,this.frame68,97,this.frame98,131,this.frame132,198,this.frame199,256,this.frame257,273,this.frame274);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroShatra.portrait;
         this.§_-sT§ = true;
         this.§implements const else§ = 26;
         this.§override set§ = 8;
         this.configuration = this.cRoot.gameSettings.heroes.heroShatra;
         this.§dynamic const§ = this.configuration.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.configuration.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.configuration.respawn;
         this.attackReloadTime = this.configuration.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 16;
         this.levelUpSoundShoot = 5;
         this.level = this.cRoot.game.gameHeroData.heroShatra.level;
         this.xp = this.cRoot.game.gameHeroData.heroShatra.xp;
         this.speed = 2.5 * §_-Mm§.GAME_SCALE;
         this.lifes = 1;
         this.xAdjust = 13;
         this.idleTime = 30;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -4;
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.lifeBar = new LifeBarMedium(new Point(0,-30),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.§false switch§();
         this.levelUpWithAnimation(false);
         this.visible = false;
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
         this.cRoot.§break default§(this);
      }
      
      override public function pause() : void
      {
         super.pause();
         if(this.§break for do§ != null)
         {
            this.§break for do§.pause();
         }
      }
      
      override public function unPause() : void
      {
         if(this.§break for do§ != null)
         {
            this.§break for do§.unPause();
         }
         switch(this.currentFrameLabel)
         {
            case "runningEnd":
               this.gotoAndPlay("running");
               break;
            case "fightingEnd":
            case "shootEnd":
            case "shootDownEnd":
            case "shootUpEnd":
            case "specialEnd":
            case "respawningEnd":
            case "explodeEnd":
            case "deadEnd":
            case "idle":
               break;
            default:
               this.play();
         }
         this.§do const throw§();
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "shatra";
         param1.sName = Locale.loadStringEx("HERO_SHATRA_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroShatra.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      public function §var const false§() : void
      {
         this.gotoAndPlay("idle");
      }
      
      override protected function levelUpWithAnimation(param1:Boolean) : void
      {
         if(param1)
         {
            super.levelUpWithAnimation(param1);
         }
         this.health = this.initHealth = this.configuration.health[this.level - 1];
         this.regenerateHealth = this.configuration.regen[this.level - 1];
         this.armor = this.configuration.armor[this.level - 1];
         this.minDamage = this.configuration.minDamage[this.level - 1];
         this.maxDamage = this.configuration.maxDamage[this.level - 1];
         this.xpMultiplier = this.configuration.meleeAttackXpMultiplier;
         this.energyGlaiveXpMultiplier = this.configuration.energyGlaiveXpMultiplier;
         this.purificationProtocolDroneXpMultiplier = this.configuration.purificationProtocolDroneXpMultiplier;
         this.abductionXpMultiplier = this.configuration.abductionXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.energyGlaiveReloadTimeCounter;
         ++this.§_-eQ§;
         ++this.§_-By§;
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.§native throw§())
         {
            return true;
         }
         if(this.§set include§())
         {
            return true;
         }
         if(this.evalCastAbduction())
         {
            return true;
         }
         return false;
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.§_-fv§ = false;
         this.§_-fK§ = false;
         this.isCastingAbduction = false;
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.§_-fv§ = false;
         this.§_-fK§ = false;
         this.isCastingAbduction = false;
      }
      
      override public function onFrameUpdate() : void
      {
         this.§for const super§();
         super.onFrameUpdate();
      }
      
      public function §for const super§() : void
      {
         if(this.currentFrame == 45)
         {
            this.§throw const case§();
         }
         if(this.currentFrame == 67)
         {
            this.endCastingEnergyGlaive();
         }
         if(this.currentFrame == 97)
         {
            this.§null const catch§();
            this.endCastingPurificationProtocol();
         }
         if(this.currentFrame == 108)
         {
            this.castAbduction();
         }
         if(this.currentFrame == 131)
         {
            this.endCastingAbduction();
         }
         if(this.currentFrame == 186)
         {
            this.performExplosion();
         }
      }
      
      private function performExplosion() : void
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:§dynamic const in§ = null;
         var _loc3_:§dynamic const in§ = null;
         if(this.isFacehugger)
         {
            return;
         }
         this.cRoot.game.gameSounds.playAliendDeathExplosion();
         this.cRoot.game.gameSounds.§_-7o§();
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = new §dynamic const in§(this.x - 0 / 2,this.y - 0 / 2,0,0);
            _loc3_ = new §dynamic const in§(this.x - this.finalCountdownRange / 2,this.y - this.finalCountdownRange / 2,this.finalCountdownRange,this.finalCountdownRange);
            if(!_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && !_loc2_.containsPoint(new Point(_loc1_.x,_loc1_.y)) && _loc3_.containsPoint(new Point(_loc1_.x,_loc1_.y)))
            {
               this.§case for break§(_loc1_);
            }
         }
      }
      
      public function §native throw§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:§dynamic const in§ = null;
         var _loc3_:§dynamic const in§ = null;
         if(this.energyGlaiveLevel <= 0)
         {
            return false;
         }
         if(this.isWalking || this.§_-fK§ || this.isCastingAbduction || this.isCharging)
         {
            return false;
         }
         if(this.§_-fv§)
         {
            return true;
         }
         if(this.energyGlaiveReloadTimeCounter < this.energyGlaiveReloadTime)
         {
            return false;
         }
         this.energyGlaiveTarget = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = new §dynamic const in§(this.x - this.energyGlaiveCastMinRange / 2,this.y - this.energyGlaiveCastMinRange / 2,this.energyGlaiveCastMinRange,this.energyGlaiveCastMinRange);
            _loc3_ = new §dynamic const in§(this.x - this.energyGlaiveCastMaxRange / 2,this.y - this.energyGlaiveCastMaxRange / 2,this.energyGlaiveCastMaxRange,this.energyGlaiveCastMaxRange);
            if(!_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && !_loc2_.containsPoint(new Point(_loc1_.x,_loc1_.y)) && _loc3_.containsPoint(new Point(_loc1_.x,_loc1_.y)))
            {
               this.energyGlaiveTarget = _loc1_;
               this.energyGlaiveTargetPosition = new Point(this.energyGlaiveTarget.x,this.energyGlaiveTarget.y);
               break;
            }
         }
         if(this.energyGlaiveTarget == null)
         {
            return false;
         }
         this.§finally for set§();
         return true;
      }
      
      public function §_-GN§(param1:Number, param2:Number, param3:EnemyCommon) : void
      {
         var _loc4_:EnemyCommon = null;
         var _loc5_:§dynamic const in§ = null;
         var _loc6_:§dynamic const in§ = null;
         for each(_loc4_ in this.cRoot.enemies)
         {
            _loc5_ = new §dynamic const in§(this.x - param1 / 2,this.y - param1 / 2,param1,param1);
            _loc6_ = new §dynamic const in§(this.x - param2 / 2,this.y - param2 / 2,param2,param2);
            if(!_loc4_.isDead && _loc4_.isActive && _loc4_.§dynamic const for§ && !_loc4_.§import for dynamic§ && !_loc5_.containsPoint(new Point(_loc4_.x,_loc4_.y)) && _loc6_.containsPoint(new Point(_loc4_.x,_loc4_.y)))
            {
               param3 = _loc4_;
               break;
            }
         }
      }
      
      public function §finally for set§() : void
      {
         var _loc1_:Number = NaN;
         this.§_-fv§ = true;
         this.energyGlaiveReloadTimeCounter = 0;
         if(this.x > this.energyGlaiveTargetPosition.x)
         {
            _loc1_ = -1;
         }
         else
         {
            _loc1_ = 1;
         }
         this.scaleX = _loc1_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.gotoAndPlay("disk");
      }
      
      public function §throw const case§() : void
      {
         var _loc1_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2f(this.scaleX ? -22 : 22,16));
         var _loc2_:§default const true§ = new §default const true§(this,this.cRoot,_loc1_,this.energyGlaiveTarget,this.energyGlaiveTargetPosition,this.configuration.energyGlaiveConfiguration,this.energyGlaiveLevel);
         this.cRoot.bullets.addChild(_loc2_);
         this.energyGlaiveTarget = null;
      }
      
      public function endCastingEnergyGlaive() : void
      {
         this.§_-fv§ = false;
         this.energyGlaiveReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function §set include§() : Boolean
      {
         if(this.§_-8g§ <= 0)
         {
            return false;
         }
         if(this.isWalking || this.§_-fv§ || this.isCastingAbduction || this.isCharging)
         {
            return false;
         }
         if(this.§_-fK§)
         {
            return true;
         }
         if(this.§_-eQ§ < this.§while try§)
         {
            return false;
         }
         if(!this.§override for const§())
         {
            return false;
         }
         this.§true const return§();
         return true;
      }
      
      public function §override for const§() : Boolean
      {
         this.§_-Bt§();
         if(this.§finally try§ == null)
         {
            return false;
         }
         return true;
      }
      
      private function §_-Bt§() : void
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:§dynamic const in§ = null;
         var _loc3_:§dynamic const in§ = null;
         this.§finally try§ = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = new §dynamic const in§(this.x - this.purificationProtocolMinRange / 2,this.y - this.purificationProtocolMinRange / 2,this.purificationProtocolMinRange,this.purificationProtocolMinRange);
            _loc3_ = new §dynamic const in§(this.x - this.purificationProtocolMaxRange / 2,this.y - this.purificationProtocolMaxRange / 2,this.purificationProtocolMaxRange,this.purificationProtocolMaxRange);
            if(!_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && !_loc1_.isBoss && !_loc2_.containsPoint(new Point(_loc1_.x,_loc1_.y)) && _loc3_.containsPoint(new Point(_loc1_.x,_loc1_.y)))
            {
               this.§finally try§ = _loc1_;
               this.purificationProtocolTargetPosition = new Point(_loc1_.x,_loc1_.y);
               break;
            }
         }
      }
      
      public function §true const return§() : void
      {
         var _loc1_:Number = NaN;
         this.§_-fK§ = true;
         if(this.x > this.purificationProtocolTargetPosition.x)
         {
            _loc1_ = -1;
         }
         else
         {
            _loc1_ = 1;
         }
         this.scaleX = _loc1_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         var _loc2_:Number = 34 / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("ship");
      }
      
      public function §null const catch§() : void
      {
         this.§_-Ug§(this.§_-8g§,this.purificationProtocolDroneXpMultiplier);
         if(this.§finally try§ == null || this.§finally try§.isDead)
         {
            this.§_-Bt§();
            if(this.§finally try§ == null)
            {
               return;
            }
         }
         this.§_-eQ§ = 0;
         var _loc1_:int = 0;
         while(_loc1_ < this.purificationProtocolDrones)
         {
            this.§break for do§ = new §var const do§(this.cRoot,this.purificationProtocolTargetPosition,this.§finally try§,this.configuration.purificationProtocolConfiguration,this.§_-8g§);
            this.cRoot.entities.addChild(this.§break for do§);
            _loc1_++;
         }
      }
      
      public function endCastingPurificationProtocol() : void
      {
         this.§_-fK§ = false;
         this.§_-Os§();
      }
      
      public function evalCastAbduction() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:§dynamic const in§ = null;
         var _loc3_:§dynamic const in§ = null;
         if(this.§_-K9§ <= 0)
         {
            return false;
         }
         if(this.isWalking || this.§_-fK§ || this.§_-fv§ || this.isCharging)
         {
            return false;
         }
         if(this.isCastingAbduction)
         {
            return true;
         }
         if(this.§_-By§ < this.§else const with§)
         {
            return false;
         }
         this.§with const set§ = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = new §dynamic const in§(this.x - 0 / 2,this.y - 0 / 2,0,0);
            _loc3_ = new §dynamic const in§(this.x - this.abductionMaxRange / 2,this.y - this.abductionMaxRange / 2,this.abductionMaxRange,this.abductionMaxRange);
            if(!_loc1_.isFlying && !_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && !_loc1_.§import for dynamic§ && !(this.§_-K9§ < 3 && _loc1_.health > this.abductionTotalHealth) && !_loc1_.onTunnel && !(_loc1_ is EnemyJungleSpiderTiny) && !(_loc1_ is EnemyFinalBossPiece) && !_loc1_.isBoss && !_loc2_.containsPoint(new Point(_loc1_.x,_loc1_.y)) && _loc3_.containsPoint(new Point(_loc1_.x,_loc1_.y)))
            {
               this.§with const set§ = _loc1_;
               break;
            }
         }
         if(this.§with const set§ == null)
         {
            return false;
         }
         this.startCastingAbduction();
         return true;
      }
      
      public function startCastingAbduction() : void
      {
         var _loc1_:Number = NaN;
         this.isCastingAbduction = true;
         if(this.x > this.§with const set§.x)
         {
            _loc1_ = -1;
         }
         else
         {
            _loc1_ = 1;
         }
         this.scaleX = _loc1_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.gotoAndPlay("motherShip");
      }
      
      public function castAbduction() : void
      {
         var _loc5_:EnemyCommon = null;
         var _loc6_:AbductionShip = null;
         var _loc7_:EnemyCommon = null;
         var _loc8_:§dynamic const in§ = null;
         var _loc9_:§dynamic const in§ = null;
         var _loc1_:Array = [];
         if(this.§with const set§ == null || this.§with const set§.isDead || !this.§with const set§.isActive)
         {
            for each(_loc7_ in this.cRoot.enemies)
            {
               _loc8_ = new §dynamic const in§(this.x - 0 / 2,this.y - 0 / 2,0,0);
               _loc9_ = new §dynamic const in§(this.x - this.abductionMaxRange / 2,this.y - this.abductionMaxRange / 2,this.abductionMaxRange,this.abductionMaxRange);
               if(!_loc7_.isFlying && !_loc7_.isDead && _loc7_.isActive && _loc7_.§dynamic const for§ && !_loc7_.§import for dynamic§ && !(this.§_-K9§ < 3 && _loc7_.health > this.abductionTotalHealth) && !_loc7_.onTunnel && !(_loc7_ is EnemyJungleSpiderTiny) && !(_loc7_ is EnemyFinalBossPiece) && !_loc7_.isBoss && !_loc8_.containsPoint(new Point(_loc7_.x,_loc7_.y)) && _loc9_.containsPoint(new Point(_loc7_.x,_loc7_.y)))
               {
                  this.§with const set§ = _loc7_;
                  break;
               }
            }
            if(this.§with const set§ == null || this.§with const set§.isDead || !this.§with const set§.isActive)
            {
               this.endCastingAbduction();
               return;
            }
         }
         this.§_-Ug§(this.§_-K9§,this.abductionXpMultiplier);
         this.§_-By§ = 0;
         _loc1_.push(this.§with const set§);
         var _loc2_:int = this.§dynamic extends§;
         var _loc3_:int = this.abductionTotalHealth - this.§with const set§.health;
         var _loc4_:* = this.§_-Yw§;
         for each(_loc5_ in this.cRoot.enemies)
         {
            if(!(!_loc5_.isActive || _loc5_.isBoss || _loc5_.isDead))
            {
               if(_loc5_ != this.§with const set§)
               {
                  if(_loc3_ < 0)
                  {
                     break;
                  }
                  if(_loc4_ < 0)
                  {
                     break;
                  }
                  if(§_-Mm§.ccpDistance(new Point(this.§with const set§.x,this.§with const set§.y),new Point(_loc5_.x,_loc5_.y)) < _loc2_ && _loc5_.health <= _loc3_)
                  {
                     _loc1_.push(_loc5_);
                     _loc3_ -= _loc5_.health;
                     _loc4_--;
                  }
               }
            }
         }
         _loc6_ = new AbductionShip(§_-Mm§.ccpAdd(new Point(this.§with const set§.x,this.§with const set§.y),§_-Mm§.wc2f(0,0)),_loc1_,this.configuration,this.§_-K9§);
         this.cRoot.entities.addChild(_loc6_);
         this.cRoot.game.gameSounds.playAlienAbduction();
      }
      
      public function endCastingAbduction() : void
      {
         this.isCastingAbduction = false;
         this.§_-Os§();
      }
      
      override public function §finally const final§() : void
      {
         if(this.isFacehugger)
         {
            return;
         }
         this.cRoot.game.gameSounds.§_-7o§();
      }
      
      public function castFinalCountdown() : void
      {
         this.gotoAndPlay("explode");
         this.health = 0;
         this.lifeBar.updateProgress(this.health);
      }
      
      public function §case for break§(param1:EnemyCommon) : void
      {
         param1.setDamage(this.finalCountdownDamage,§_-Mm§.I_ARMOR);
      }
      
      override protected function §_-Ew§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroShatra.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.energyGlaiveLevel = _loc1_;
         var _loc2_:Object = this.configuration.energyGlaiveSkill;
         this.energyGlaiveCastMinRange = _loc2_.castMinRange[_loc1_ - 1];
         this.energyGlaiveCastMaxRange = _loc2_.castMaxRange[_loc1_ - 1];
         this.energyGlaiveReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.energyGlaiveReloadTimeCounter = this.energyGlaiveReloadTime;
      }
      
      override protected function §_-kZ§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroShatra.skill2.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§_-8g§ = _loc1_;
         var _loc2_:Object = this.configuration.purificationProtocolSkill;
         this.purificationProtocolMinRange = _loc2_.minRange[_loc1_ - 1];
         this.purificationProtocolMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.§while try§ = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.§_-eQ§ = this.§while try§;
         this.purificationProtocolDrones = _loc2_.drones[_loc1_ - 1];
      }
      
      override protected function §get const default§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroShatra.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§_-K9§ = _loc1_;
         var _loc2_:Object = this.configuration.abductionSkill;
         this.§_-Yw§ = _loc2_.targets[_loc1_ - 1];
         this.§else const with§ = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.abductionMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.abductionTotalHealth = _loc2_.totalHealth[_loc1_ - 1];
         this.§dynamic extends§ = _loc2_.multipleTargetsDistance[_loc1_ - 1];
         this.§_-By§ = this.§else const with§;
      }
      
      override protected function §_-kp§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroShatra.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.vibroBladesSkill;
         var _loc3_:int = int(_loc2_.damage[_loc1_ - 1]);
         this.§_-vd§ = §_-Mm§.I_ARMOR;
         this.minDamage += _loc3_;
         this.maxDamage += _loc3_;
      }
      
      override public function setDamage(param1:int, param2:Boolean = false) : *
      {
         if(!this.isActive || this.isDead)
         {
            return;
         }
         this.targetedTimeCounter = 0;
         if(!param2)
         {
            this.health -= param1 - this.armor * param1 / 100;
         }
         else
         {
            this.health -= param1;
         }
         if(this.health <= 0)
         {
            if(this.finalCountdownDamage > 0 && !this.isFacehugger)
            {
               this.castFinalCountdown();
               this.§finally const final§();
            }
            else
            {
               this.gotoAndPlay("dead");
               this.§finally const final§();
            }
            this.health = 0;
            this.isActive = false;
            this.isDead = true;
            this.§_-GH§(true);
            this.isCharging = false;
            this.§break finally§ = 0;
            this.lifeBar.hide();
            if(this.isBlocking)
            {
               this.unBlock();
            }
            this.cRoot.game.§const for set§.§_-8c§(this.cRoot);
            this.§_-my§();
            return;
         }
         if(this.cRoot.game.gameUpgrades.barracksUpBarbedArmor == true && (this.cRoot.§_-wi§ == 0 || this.cRoot.§_-wi§ == 5))
         {
            if(this.enemy != null && this.enemy.isActive)
            {
               this.enemy.setDamage(Math.ceil(param1 * 0.1),§_-Mm§.P_ARMOR);
               if(!this.enemy.isActive)
               {
                  this.unBlock();
               }
            }
         }
         this.§include for if§(param1);
         this.afterDamage();
         this.updateLifebarProgress();
      }
      
      override protected function §_-gF§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroShatra.skill5.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.finalCountdownSkill;
         this.finalCountdownDamage = _loc2_.damage[_loc1_ - 1];
         this.finalCountdownRange = _loc2_.range[_loc1_ - 1];
         var _loc3_:Number = 1 / this.cRoot.gameSettings.framesRate;
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§_-Oi§();
      }
      
      override protected function §_-wj§() : void
      {
         this.cRoot.game.gameSounds.§_-Oi§();
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame6() : *
      {
         gotoAndPlay("running");
      }
      
      internal function frame31() : *
      {
         stop();
      }
      
      internal function frame68() : *
      {
         stop();
      }
      
      internal function frame98() : *
      {
         stop();
      }
      
      internal function frame132() : *
      {
         stop();
      }
      
      internal function frame199() : *
      {
         stop();
      }
      
      internal function frame257() : *
      {
         stop();
      }
      
      internal function frame274() : *
      {
         stop();
      }
   }
}

