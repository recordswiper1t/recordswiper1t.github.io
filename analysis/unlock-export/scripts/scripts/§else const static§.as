package
{
   import com.greensock.*;
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12558")]
   public class §else const static§ extends §dynamic const class§
   {
      
      internal var §_-dN§:Object;
      
      internal var §_-vf§:Boolean;
      
      internal var boulderThrowTime:int;
      
      internal var boulderThrowTimeCounter:int;
      
      internal var boulderThrowTarget:EnemyCommon;
      
      internal var boulderThrowTargetPosition:Point;
      
      internal var boulderThrowExplosionYAdsjust:int;
      
      internal var boulderThrowMinDistance:int;
      
      internal var boulderThrowRange:int;
      
      internal var boulderThrowMinDamage:int;
      
      internal var boulderThrowMaxDamage:int;
      
      internal var boulderThrowAreaDamage:int;
      
      internal var boulderThrowLevel:int;
      
      internal var isCastingStomp:Boolean;
      
      internal var stompStunChance:Number;
      
      internal var stompStunDuration:int;
      
      internal var stompSlowDuration:int;
      
      internal var §_-fk§:Number;
      
      internal var stompDamage:int;
      
      internal var stompRange:int;
      
      internal var stompTriggerRange:int;
      
      internal var §_-CE§:int;
      
      internal var §use§:int;
      
      internal var §native for package§:int;
      
      internal var §_-1W§:int;
      
      internal var §do for while§:int;
      
      internal var §super throw§:int;
      
      internal var §_-48§:int;
      
      internal var §_-S7§:int;
      
      internal var §implements do§:int;
      
      internal var §throw continue§:int;
      
      internal var §_-JN§:int;
      
      internal var bastionBonusMaxDamage:int;
      
      internal var isCastingMassiveDamage:Boolean;
      
      internal var §_-Mk§:int;
      
      internal var §super const get§:Number;
      
      internal var massiveDamageChance:int;
      
      internal var §implements native§:int;
      
      internal var §var do§:int;
      
      internal var massiveDamageExtraDamage:int;
      
      internal var §_-PK§:int;
      
      internal var areaAttackRangeWidth:int;
      
      internal var boulderXpMultiplier:Number;
      
      internal var stompXpMultiplier:Number;
      
      internal var massiveDamageXpMultiplier:Number;
      
      internal var §_-BJ§:§extends const true§;
      
      internal var §_-vX§:Number;
      
      public function §else const static§(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,24,this.frame25,42,this.frame43,68,this.frame69,100,this.frame101,118,this.frame119,134,this.frame135,212,this.frame213);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.canBePoison = false;
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroGrawl.portrait;
         this.§_-dN§ = this.cRoot.gameSettings.heroes.heroGrawl;
         this.§implements const else§ = 16;
         this.§override set§ = 10;
         this.§dynamic const§ = this.§_-dN§.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.§_-dN§.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.§_-dN§.respawn;
         this.attackReloadTime = this.§_-dN§.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -18;
         this.§_-L6§ = 14;
         this.§_-ZX§ = 14;
         this.levelUpSoundShoot = 5;
         this.§_-62§ = 18;
         this.speed = 1.25;
         this.lifes = 1;
         this.xAdjust = 15;
         this.idleTime = 30;
         this.visible = false;
         this.§_-BJ§ = new BastionDecal(0,0);
         this.§_-BJ§.alpha = 0;
         this.addChild(this.§_-BJ§);
         this.level = this.cRoot.game.gameHeroData.heroGrawl.level;
         this.xp = this.cRoot.game.gameHeroData.heroGrawl.xp;
         this.lifeBar = new LifeBarMedium(new Point(0,-45),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.§false switch§();
         this.levelUpWithAnimation(false);
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.cRoot.§break default§(this);
         this.visible = false;
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "grawl";
         param1.sName = Locale.loadStringEx("HERO_GRAWL_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroGrawl.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override public function pause() : void
      {
         super.pause();
         this.§_-BJ§.stop();
         TweenMax.pauseAll();
      }
      
      override public function unPause() : void
      {
         TweenMax.resumeAll();
         this.§_-BJ§.play();
         switch(this.currentFrameLabel)
         {
            case "runningEnd":
               this.gotoAndPlay("running");
               break;
            case "fightingEnd":
            case "instaKillEnd":
            case "respawningEnd":
            case "stoneThrowEnd":
            case "groundPunchEnd":
            case "deadEnd":
            case "idle":
               break;
            default:
               this.play();
         }
         this.§do const throw§();
      }
      
      override public function onFrameUpdate() : void
      {
         this.§for const super§();
         super.onFrameUpdate();
      }
      
      public function §for const super§() : void
      {
         if(this.currentFrame == 93)
         {
            this.§_-E8§();
         }
         if(this.currentFrame == 100)
         {
            this.endBoulderThrow();
         }
         if(this.currentFrame == 61)
         {
            this.doMassiveDamage();
         }
         if(this.currentFrame == 68)
         {
            this.endMassiveDamage();
         }
         if(this.currentFrame == 108)
         {
            this.cRoot.game.gameSounds.playGrawlStomp();
            this.doStomp();
            this.cRoot.bullets.addChild(new §in const get§(new Point(this.x - 10,this.y),this.cRoot));
         }
         if(this.currentFrame == 116)
         {
            this.doStomp();
            this.cRoot.bullets.addChild(new §in const get§(new Point(this.x + 10,this.y),this.cRoot));
         }
         if(this.currentFrame == 118)
         {
            if(this.§_-vX§ > 0)
            {
               this.gotoAndPlay("groundPunch");
            }
            else
            {
               this.endStomp();
            }
         }
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§_-MO§();
      }
      
      override protected function §_-wj§() : void
      {
         this.§finally var§();
      }
      
      override protected function levelUpWithAnimation(param1:Boolean) : void
      {
         if(param1)
         {
            super.levelUpWithAnimation(param1);
         }
         this.health = this.initHealth = this.§_-dN§.health[this.level - 1];
         this.regenerateHealth = this.§_-dN§.regen[this.level - 1];
         this.armor = this.§_-dN§.armor[this.level - 1];
         this.minDamage = this.§_-dN§.minDamage[this.level - 1];
         this.maxDamage = this.§_-dN§.maxDamage[this.level - 1];
         this.areaAttackRangeWidth = this.§_-dN§.areaAttackConfig.range;
         this.xpMultiplier = this.§_-dN§.meleeAttackXpMultiplier;
         this.boulderXpMultiplier = this.§_-dN§.boulderXpMultiplier;
         this.stompXpMultiplier = this.§_-dN§.stompXpMultiplier;
         this.massiveDamageXpMultiplier = this.§_-dN§.massiveDamageXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      public function §native use§() : void
      {
      }
      
      override protected function §_-Ew§() : void
      {
         this.boulderThrowTime = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroGrawl.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.boulderThrowLevel = _loc1_;
         var _loc2_:Object = this.§_-dN§.boulderThrowSkill;
         this.boulderThrowMinDistance = _loc2_.minDistance;
         this.boulderThrowRange = _loc2_.range;
         this.boulderThrowMinDamage = _loc2_.minDamage[_loc1_ - 1];
         this.boulderThrowMaxDamage = _loc2_.maxDamage[_loc1_ - 1];
         this.boulderThrowAreaDamage = _loc2_.areaDamage;
         this.boulderThrowTime = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.boulderThrowTimeCounter = 0;
      }
      
      override protected function §_-kZ§() : void
      {
         this.isCastingStomp = false;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroGrawl.skill2.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§super throw§ = _loc1_;
         var _loc2_:Object = this.§_-dN§.stompSkill;
         this.stompStunChance = _loc2_.stunChance / 100;
         this.stompStunDuration = _loc2_.duration[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.§_-CE§ = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.stompRange = _loc2_.range;
         this.stompTriggerRange = _loc2_.rangeTrigger;
         this.stompSlowDuration = _loc2_.slowDuration * this.cRoot.gameSettings.framesRate;
         this.§_-fk§ = _loc2_.slowFactor / 100;
         this.stompDamage = _loc2_.damage[_loc1_ - 1];
         this.§native for package§ = _loc2_.loops[_loc1_ - 1];
         this.§_-1W§ = _loc2_.minEnemiesToTrigger;
         this.§do for while§ = _loc2_.minEnemyHealthToTrigger;
         this.§use§ = 0;
      }
      
      override protected function §get const default§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroGrawl.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.bastionSkill;
         this.§_-48§ = 0;
         this.§_-S7§ = _loc2_.maxWalkDistance;
         this.§implements do§ = _loc2_.damagePerTick[_loc1_ - 1];
         this.bastionBonusMaxDamage = _loc2_.maxBonusDamage[_loc1_ - 1];
         this.§throw continue§ = _loc2_.tickTime * this.cRoot.gameSettings.framesRate;
         this.§_-JN§ = 0;
      }
      
      override protected function §_-kp§() : void
      {
         this.massiveDamageChance = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroGrawl.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.massiveDamageSkill;
         this.§_-Mk§ = _loc1_;
         this.§super const get§ = _loc2_.healthFactor;
         this.massiveDamageChance = _loc2_.chance[_loc1_ - 1];
         this.§implements native§ = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.§var do§ = 0;
         this.massiveDamageExtraDamage = _loc2_.extraDamage[_loc1_ - 1];
         this.§_-PK§ = _loc2_.damageType;
      }
      
      override protected function §_-gF§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroGrawl.skill5.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.hardRockSkill;
         var _loc3_:int = int(_loc2_.extraHealth[_loc1_ - 1]);
         this.health += _loc3_;
         this.initHealth += _loc3_;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.§use§;
         ++this.boulderThrowTimeCounter;
         ++this.§var do§;
         this.evalBastion();
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.isCastingMassiveDamage)
         {
            return true;
         }
         if(!this.§_-vf§ && this.evalStomp())
         {
            return true;
         }
         if(this.§_-QT§())
         {
            return true;
         }
         return false;
      }
      
      public function evalStomp() : Boolean
      {
         if(this.stompStunDuration == 0 || this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.isCastingStomp)
         {
            return true;
         }
         if(this.§use§ < this.§_-CE§)
         {
            return false;
         }
         if(!this.canStomp())
         {
            return false;
         }
         this.isCastingStomp = true;
         this.playAnimationStomp();
         return true;
      }
      
      public function canStomp() : Boolean
      {
         var _loc3_:EnemyCommon = null;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc2_:int = 0;
         for each(_loc3_ in this.cRoot.enemies)
         {
            if(_loc3_.isActive && !_loc3_.isBoss && !_loc3_.isFlying && _loc3_.§dynamic const for§ && §_-Mm§.ellipseContains(this.x,this.y,_loc3_,this.stompTriggerRange,_loc1_))
            {
               if(++_loc2_ >= this.§_-1W§ || _loc3_.health > this.§do for while§)
               {
                  return true;
               }
            }
         }
         return false;
      }
      
      public function playAnimationStomp() : void
      {
         this.§_-Ug§(this.§super throw§,this.stompXpMultiplier);
         var _loc1_:Number = 5 / this.cRoot.gameSettings.framesRate;
         var _loc2_:Number = 1 / this.cRoot.gameSettings.framesRate;
         this.§_-vX§ = this.§native for package§ * 2;
         this.gotoAndPlay("groundPunch");
         this.resetCooldownStomp();
      }
      
      public function resetCooldownStomp() : void
      {
         this.§use§ = 0;
      }
      
      public function §import for const§() : void
      {
         var _loc1_:Number = this.cRoot.gameSettings.framesRate;
      }
      
      public function playStompLeftRockAnimation() : *
      {
      }
      
      public function playStompRightRockAnimation() : void
      {
      }
      
      public function doStomp() : void
      {
         var _loc4_:EnemyCommon = null;
         var _loc5_:int = 0;
         --this.§_-vX§;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc2_:Boolean = false;
         var _loc3_:Object = this.cRoot.enemies;
         for each(_loc4_ in _loc3_)
         {
            if(!_loc4_.§import for dynamic§)
            {
               if(_loc4_.isActive && !_loc4_.isFlying && §_-Mm§.ellipseContains(this.x,this.y,_loc4_,this.stompRange,_loc1_))
               {
                  _loc5_ = this.stompDamage;
                  _loc4_.setDamage(_loc5_,§_-Mm§.P_ARMOR);
                  if(_loc4_.isActive && !_loc4_.isFlying)
                  {
                     _loc4_.§_-qI§(new GiantStompSlow(this.cRoot,1,_loc4_));
                     if(!_loc2_ && !_loc4_.isBoss && !_loc4_.§_-6o§ && _loc4_.§get for catch§)
                     {
                        _loc2_ = true;
                        if(Math.random() < this.stompStunChance)
                        {
                           _loc4_.§_-qI§(new §import switch§(this.cRoot,1,_loc4_,this.stompStunDuration));
                        }
                     }
                  }
               }
            }
         }
      }
      
      public function endStomp() : void
      {
         this.isCastingStomp = false;
         this.§_-Os§();
      }
      
      override protected function readyToAttack() : Boolean
      {
         ++this.§_-NL§;
         if(this.§_-NL§ == this.attackReloadTime)
         {
            if(!this.evalMassiveDamage())
            {
               this.§_-Vs§();
            }
            this.§_-NL§ = 0;
            return true;
         }
         return false;
      }
      
      public function evalMassiveDamage() : Boolean
      {
         if(this.massiveDamageChance == 0)
         {
            return false;
         }
         if(this.§var do§ < this.§implements native§)
         {
            return false;
         }
         this.isCastingMassiveDamage = true;
         this.playAnimationMassiveDamage();
         return true;
      }
      
      public function playAnimationMassiveDamage() : void
      {
         var _loc1_:Number = 17 / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("instaKill");
         this.cRoot.game.gameSounds.§true const throw§();
      }
      
      public function doMassiveDamage() : void
      {
         if(this.enemy == null || !this.enemy.isActive)
         {
            return;
         }
         var _loc1_:int = this.getDamage() + this.massiveDamageExtraDamage;
         this.§_-xX§(_loc1_,this.§_-PK§,this.massiveDamageChance / 100,Math.ceil(this.initHealth / this.§super const get§));
         this.§_-Ug§(this.§_-Mk§,this.massiveDamageXpMultiplier);
      }
      
      public function §_-xX§(param1:int, param2:int, param3:Number, param4:int) : *
      {
         var _loc5_:§extends const true§ = null;
         switch(enemy.size)
         {
            case §_-Mm§.SMALL:
               _loc5_ = new §_-vk§(enemy.x,enemy.y);
               break;
            case §_-Mm§.MEDIUM:
            case §_-Mm§.LARGE:
               _loc5_ = new §_-xZ§(enemy.x,enemy.y);
         }
         this.cRoot.bullets.addChild(_loc5_);
         var _loc6_:int = this.predictDamage(param1,param2,0);
         var _loc7_:int = enemy.health - _loc6_;
         if(_loc7_ <= 0 && !enemy.isBoss)
         {
            enemy.explode();
         }
         else if(enemy.isBoss || _loc7_ > param4 || Math.random() >= param3)
         {
            enemy.setDamage(param1,param2);
         }
         else
         {
            enemy.explode();
         }
      }
      
      public function predictDamage(param1:int, param2:int, param3:int) : int
      {
         var _loc4_:int = 0;
         var _loc5_:Number = NaN;
         var _loc6_:Number = NaN;
         if(enemy.hasDebuff("DebuffWeakness"))
         {
            _loc4_ = int(this.cRoot.gameSettings.archers.totem.weaknessExtraDamagePercent);
            _loc5_ = _loc4_ / 100;
            _loc6_ = Math.round(param1 * _loc5_);
            param1 += _loc6_;
         }
         return enemy.getArmorDamage(param2,param1,param3);
      }
      
      public function endMassiveDamage() : void
      {
         this.isCastingMassiveDamage = false;
         this.§_-NL§ = 0;
         this.§var do§ = 0;
         this.§_-Os§();
      }
      
      public function evalBastion() : void
      {
         if(this.§throw continue§ == 0 || this.isWalking || !this.isActive)
         {
            return;
         }
         ++this.§_-JN§;
         if(this.§_-JN§ < this.§throw continue§)
         {
            return;
         }
         this.§_-JN§ = 0;
         if(this.§_-48§ >= this.bastionBonusMaxDamage)
         {
            this.§_-tK§(true);
            return;
         }
         this.bastionApplyDamage(this.§implements do§);
         this.§_-tK§(false);
      }
      
      public function §_-QT§() : Boolean
      {
         if(this.boulderThrowTime == 0 || this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.§_-vf§)
         {
            return true;
         }
         if(this.boulderThrowTimeCounter < this.boulderThrowTime)
         {
            return false;
         }
         if(!this.§_-7h§())
         {
            return false;
         }
         if(this.boulderThrowTarget.x >= this.x)
         {
            this.scaleX = 1;
            this.lifeBar.§dynamic for const§(this.scaleX);
         }
         else
         {
            this.scaleX = -1;
            this.lifeBar.§dynamic for const§(this.scaleX);
         }
         this.§_-vf§ = true;
         this.§continue for for§();
         return true;
      }
      
      public function §continue for for§() : void
      {
         var _loc1_:Number = 23 / this.cRoot.gameSettings.framesRate;
         this.cRoot.game.gameSounds.§class for break§();
         this.gotoAndPlay("stoneThrow");
      }
      
      public function endBoulderThrow() : void
      {
         this.§_-vf§ = false;
         this.§_-Os§();
      }
      
      public function §_-E8§() : void
      {
         this.§_-Ug§(this.boulderThrowLevel,this.boulderXpMultiplier);
         this.boulderThrowTimeCounter = 0;
         var _loc1_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2f((this.scaleX ? -1 : 1) * 0,77));
         var _loc2_:§false const do§ = new §_-CA§(_loc1_,this.boulderThrowTargetPosition,1,this.boulderThrowAreaDamage,this.boulderThrowMinDamage,this.boulderThrowMaxDamage,this.boulderThrowExplosionYAdsjust);
         this.cRoot.bullets.addChild(_loc2_);
      }
      
      public function boulderAddDecal() : void
      {
         var _loc1_:§_-sG§ = new §_-sG§(new Point(this.x,this.y),18 / this.cRoot.gameSettings.framesRate);
         this.cRoot.decals.addChild(_loc1_);
         _loc1_.scaleX = this.scaleX;
      }
      
      public function §_-7h§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc1_:EnemyCommon = null;
         this.boulderThrowTarget = null;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && !_loc2_.isFlying && _loc2_.§dynamic const for§ && this.§_-ax§(_loc2_) && this.onRangeShoot(_loc2_))
            {
               _loc1_ = _loc2_;
               break;
            }
         }
         if(_loc1_ != null)
         {
            this.boulderThrowTarget = _loc1_;
            this.boulderThrowTargetPosition = _loc1_.§with const static§[_loc1_.§package for var§ + _loc1_.getNodesSpeed(6)];
            this.boulderThrowTargetPosition = §_-Mm§.ccpAdd(this.boulderThrowTargetPosition,§_-Mm§.ccp(0,_loc1_.yAdjust));
            this.boulderThrowExplosionYAdsjust = _loc1_.yAdjust;
            return true;
         }
         return false;
      }
      
      public function §_-ax§(param1:EnemyCommon) : Boolean
      {
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:Number = NaN;
         _loc3_ = param1.x - this.x;
         _loc4_ = param1.y - this.y;
         _loc2_ = Math.sqrt(_loc3_ * _loc3_ + _loc4_ * _loc4_);
         if(_loc2_ > this.boulderThrowMinDistance)
         {
            return true;
         }
         return false;
      }
      
      public function onRangeShoot(param1:EnemyCommon) : Boolean
      {
         var _loc2_:Number = this.cRoot.gameSettings.rangeRatio;
         return §_-Mm§.ellipseContains(this.x,this.y,param1,this.boulderThrowRange,_loc2_);
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.isCastingStomp = false;
         this.isCastingMassiveDamage = false;
         this.bastionApplyDamage(-this.§_-48§);
         this.§_-JN§ = 0;
         this.§_-vf§ = false;
         this.§case for use§();
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.isCastingStomp = false;
         this.isCastingMassiveDamage = false;
         this.§_-vf§ = false;
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         super.§_-jv§(param1);
         if(§_-Mm§.ccpDistance(new Point(this.x,this.y),this.§in const while§) > this.§_-S7§)
         {
            this.bastionApplyDamage(-this.§_-48§);
            this.§_-JN§ = 0;
            this.§case for use§();
         }
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§_-MO§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§function throw§();
      }
      
      public function bastionApplyDamage(param1:int) : void
      {
         this.§_-48§ += param1;
         this.minDamage += param1;
         this.maxDamage += param1;
      }
      
      public function §_-tK§(param1:Boolean) : *
      {
         if(param1)
         {
            this.§_-BJ§.scaleX = 1;
            this.§_-BJ§.scaleY = 1;
         }
         else
         {
            this.§_-BJ§.scaleX = 0.5;
            this.§_-BJ§.scaleY = 0.5;
         }
         if(this.§_-BJ§.alpha != 0)
         {
            return;
         }
         TweenMax.to(this.§_-BJ§,0.2,{"alpha":1});
         this.§_-BJ§.play();
      }
      
      public function §case for use§() : void
      {
         this.§_-BJ§.stop();
         TweenMax.to(this.§_-BJ§,0.2,{"alpha":0});
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame25() : *
      {
         gotoAndPlay("running");
      }
      
      internal function frame43() : *
      {
         stop();
      }
      
      internal function frame69() : *
      {
         stop();
      }
      
      internal function frame101() : *
      {
         stop();
      }
      
      internal function frame119() : *
      {
         stop();
      }
      
      internal function frame135() : *
      {
         stop();
      }
      
      internal function frame213() : *
      {
         stop();
      }
   }
}

