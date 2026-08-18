package
{
   import §_-aW§.*;
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12105")]
   public class SoldierHeroCaptain extends §dynamic const class§
   {
      
      internal var rangeShootLevel:int;
      
      internal var rangeShootTarget:Enemy;
      
      internal var rangeShootPoint:Point;
      
      internal var §_-Rn§:Boolean;
      
      internal var rangeShootReloadTime:Number;
      
      internal var rangeShootReloadTimeCounter:int;
      
      internal var rangeShootChargeTime:int;
      
      internal var rangeShootChargeTimeCounter:int;
      
      internal var rangeShootWidth:int;
      
      internal var rangeShootHeight:int;
      
      internal var rangeShootMinDamage:int;
      
      internal var rangeShootMaxDamage:int;
      
      internal var rangeShootMinDistance:int;
      
      internal var §extends for set§:int;
      
      internal var isKraken:Boolean;
      
      internal var §_-J4§:int;
      
      internal var §_-W3§:int;
      
      internal var §use const in§:int;
      
      internal var §import native§:int;
      
      internal var §_-Wp§:int;
      
      internal var §default else§:int;
      
      internal var §if const false§:int;
      
      internal var native:Point;
      
      internal var §_-r0§:int;
      
      internal var §if super§:int;
      
      internal var §_-rT§:int;
      
      internal var lootingRange:int;
      
      internal var §_-ya§:Boolean;
      
      internal var §set null§:Point;
      
      internal var §_-AU§:int;
      
      internal var §_-aF§:int;
      
      internal var §set const implements§:int;
      
      internal var §switch throw§:int;
      
      internal var §_-o8§:int;
      
      internal var §_-R1§:int;
      
      internal var §final default§:int;
      
      internal var §_-EU§:int;
      
      internal var bombingMinRange:int;
      
      internal var §_-qF§:int;
      
      internal var rangeAttackXpMultiplier:Number;
      
      internal var barrelXpMultiplier:Number;
      
      internal var krakenXpMultiplier:Number;
      
      public function SoldierHeroCaptain(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,24,this.frame25,52,this.frame53,80,this.frame81,108,this.frame109,152,this.frame153,172,this.frame173,216,this.frame217,281,this.frame282);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroCaptain.portrait;
         this.§implements const else§ = 18;
         this.§override set§ = 9;
         this.rangeShootChargeTime = 28;
         this.§use const in§ = 45;
         this.§dynamic const§ = this.cRoot.gameSettings.heroes.heroCaptain.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.cRoot.gameSettings.heroes.heroCaptain.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.cRoot.gameSettings.heroes.heroCaptain.respawn;
         this.attackReloadTime = this.cRoot.gameSettings.heroes.heroCaptain.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -4;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 17;
         this.levelUpSoundShoot = 5;
         this.§_-o8§ = 33;
         this.level = this.cRoot.game.gameHeroData.heroCaptain.level;
         this.xp = this.cRoot.game.gameHeroData.heroCaptain.xp;
         this.speed = 2.5 / 1.28;
         this.lifes = 1;
         this.xAdjust = 5;
         this.idleTime = 30;
         this.lifeBar = new LifeBarMedium(new Point(0,-30),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.§false switch§();
         this.levelUpWithAnimation(false);
         this.visible = false;
         this.addEventListener(MouseEvent.CLICK,this.clickEvents,false,0,true);
         this.cRoot.§break default§(this);
      }
      
      override public function unPause() : void
      {
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
            case "barrelThrowEnd":
            case "idle":
               break;
            default:
               this.play();
         }
         this.§do const throw§();
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "captain";
         param1.sName = Locale.loadStringEx("HERO_CAPTAIN_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroCaptain.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override protected function clickEvents(param1:MouseEvent) : void
      {
         if(this.cRoot.soldierSelection.soldier == this)
         {
            return;
         }
         if(this.isDead)
         {
            return;
         }
         this.§try const case§();
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§else continue§();
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
         this.health = this.initHealth = this.cRoot.gameSettings.heroes.heroCaptain.health[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.regenerateHealth = this.cRoot.gameSettings.heroes.heroCaptain.regen[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.armor = this.cRoot.gameSettings.heroes.heroCaptain.armor[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.minDamage = this.cRoot.gameSettings.heroes.heroCaptain.minDamage[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroCaptain.maxDamage[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.rangeShootLevel = this.level;
         this.rangeShootReloadTime = this.cRoot.gameSettings.heroes.heroCaptain.rangeShootReloadTime * this.cRoot.gameSettings.framesRate - this.rangeShootChargeTime;
         this.rangeShootWidth = this.cRoot.gameSettings.heroes.heroCaptain.rangeShootRangeWidth;
         this.rangeShootHeight = this.rangeShootWidth * this.cRoot.gameSettings.rangeRatio;
         this.rangeShootMinDistance = this.cRoot.gameSettings.heroes.heroCaptain.rangeShootMinDistance;
         this.rangeShootMinDamage = this.cRoot.gameSettings.heroes.heroCaptain.minRangeDamage[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.rangeShootMaxDamage = this.cRoot.gameSettings.heroes.heroCaptain.maxRangeDamage[this.cRoot.game.gameHeroData.heroCaptain.level - 1];
         this.xpMultiplier = this.cRoot.gameSettings.heroes.heroCaptain.meleeAttackXpMultiplier;
         this.rangeAttackXpMultiplier = this.cRoot.gameSettings.heroes.heroCaptain.rangeAttackXpMultiplier;
         this.barrelXpMultiplier = this.cRoot.gameSettings.heroes.heroCaptain.barrelXpMultiplier;
         this.krakenXpMultiplier = this.cRoot.gameSettings.heroes.heroCaptain.krakenXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override protected function §_-Ew§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCaptain.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:int = int(this.cRoot.gameSettings.heroes.heroCaptain.swordsmanshipExtraDamage[_loc1_ - 1]);
         this.minDamage += _loc2_;
         this.maxDamage += _loc2_;
      }
      
      override protected function §_-kZ§() : void
      {
         this.§_-rT§ = this.cRoot.game.gameHeroData.heroCaptain.skill2.level;
         this.lootingRange = this.cRoot.gameSettings.heroes.heroCaptain.lootingRange;
         this.§_-r0§ = 10;
         this.§if super§ = 0;
      }
      
      override protected function §get const default§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCaptain.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.health += this.cRoot.gameSettings.heroes.heroCaptain.toughnessHealthPoints[_loc1_ - 1];
         this.initHealth = this.health;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.regenerateHealth += this.cRoot.gameSettings.heroes.heroCaptain.toughnessRegenPoints[_loc1_ - 1];
      }
      
      override protected function §_-kp§() : void
      {
         this.§_-qF§ = this.cRoot.game.gameHeroData.heroCaptain.skill4.level;
         if(this.§_-qF§ == 0)
         {
            return;
         }
         this.§set const implements§ = this.cRoot.gameSettings.heroes.heroCaptain.barrelCooldown * this.cRoot.gameSettings.framesRate;
         this.§final default§ = this.cRoot.gameSettings.heroes.heroCaptain.barrelRange;
         this.§_-EU§ = this.§final default§ * this.cRoot.gameSettings.rangeRatio;
         this.bombingMinRange = this.cRoot.gameSettings.heroes.heroCaptain.barrelMinRange;
      }
      
      override protected function §_-gF§() : void
      {
         this.§extends for set§ = this.cRoot.game.gameHeroData.heroCaptain.skill5.level;
         this.§_-J4§ = this.cRoot.gameSettings.heroes.heroCaptain.krakenCooldown * this.cRoot.gameSettings.framesRate;
         this.§_-Wp§ = this.cRoot.gameSettings.heroes.heroCaptain.krakenRange;
         this.§default else§ = this.§_-Wp§ * this.cRoot.gameSettings.rangeRatio;
         this.§if const false§ = this.cRoot.gameSettings.heroes.heroCaptain.krakenMinRange;
      }
      
      public function §break§(param1:Point, param2:Point) : void
      {
         var _loc3_:Number = param2.y - param1.y;
         var _loc4_:Number = param2.x - param1.x;
         var _loc5_:Number = Math.round(Math.atan2(_loc3_,_loc4_) * (180 / 3.14));
         if(_loc5_ < 0)
         {
            _loc5_ += 360;
         }
         if(_loc5_ > 45 && _loc5_ < 135)
         {
            this.playAnimationShootUp();
         }
         else if(_loc5_ >= 135 && _loc5_ <= 210)
         {
            this.playAnimationShoot();
         }
         else if(_loc5_ > 210 && _loc5_ < 315)
         {
            this.playAnimationShootDown();
         }
         else
         {
            this.playAnimationShoot();
         }
      }
      
      public function playAnimationShoot() : void
      {
         this.gotoAndPlay("shoot");
      }
      
      public function playAnimationShootUp() : void
      {
         this.gotoAndPlay("shootDown");
      }
      
      public function playAnimationShootDown() : void
      {
         this.gotoAndPlay("shootUp");
      }
      
      public function playAnimationKraken() : void
      {
         this.gotoAndPlay("special");
         this.cRoot.game.gameSounds.playCaptainKraken();
      }
      
      public function §_-TD§() : void
      {
         this.gotoAndPlay("barrelThrow");
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.rangeShootReloadTimeCounter;
         ++this.§_-W3§;
         ++this.§if super§;
         ++this.§switch throw§;
         this.doLooting();
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.§extends for set§ != 0 && this.evalKraken())
         {
            return true;
         }
         if(this.§_-qF§ != 0 && this.§in const dynamic§())
         {
            return true;
         }
         if(this.rangeShootLevel != 0 && this.evalRangeShoot())
         {
            return true;
         }
         return false;
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.isCharging = false;
         this.isKraken = false;
         this.§_-Rn§ = false;
         this.isLevelUp = false;
         this.§_-ya§ = false;
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.isKraken = false;
         this.§_-Rn§ = false;
         this.isCharging = false;
         this.isLevelUp = false;
         this.§_-ya§ = false;
      }
      
      public function doLooting() : void
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:§dynamic const in§ = null;
         if(this.§if super§ < this.§_-r0§)
         {
            return;
         }
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = new §dynamic const in§(this.x - this.lootingRange / 2,this.y - this.lootingRange * this.cRoot.gameSettings.rangeRatio / 2,this.lootingRange,this.lootingRange * this.cRoot.gameSettings.rangeRatio);
            if(_loc1_.isActive && !_loc1_.isDead && _loc2_.containsPoint(new Point(_loc1_.x,_loc1_.y)))
            {
               _loc1_.§_-qI§(new LootingDebuff(this.cRoot,this.§_-rT§,_loc1_));
            }
         }
         this.§if super§ = 0;
      }
      
      public function evalRangeShoot() : Boolean
      {
         var _loc1_:int = 0;
         var _loc2_:§function super§ = null;
         if(this.isKraken || this.isWalking || this.§_-ya§)
         {
            return false;
         }
         if(!this.§_-Rn§)
         {
            if(this.rangeShootReloadTimeCounter < this.rangeShootReloadTime)
            {
               return false;
            }
            if(!this.§return for import§())
            {
               return false;
            }
            if(this.rangeShootTarget.x >= this.x)
            {
               this.scaleX = 1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            this.§_-Rn§ = true;
            this.rangeShootChargeTimeCounter = 0;
            this.§break§(new Point(this.x,this.y),this.rangeShootPoint);
            return true;
         }
         if(this.rangeShootChargeTimeCounter < this.rangeShootChargeTime)
         {
            ++this.rangeShootChargeTimeCounter;
            if(this.rangeShootChargeTimeCounter == 15)
            {
               _loc1_ = this.getDamageRangeShoot();
               _loc2_ = new §function super§(new Point(this.x,this.y),this.rangeShootTarget,this.rangeShootPoint,false);
               this.cRoot.bullets.addChild(_loc2_);
               _loc2_.minDamage = cRoot.gameSettings.heroes.heroCaptain.minRangeDamage[cRoot.game.gameHeroData.heroCaptain.level - 1];
               _loc2_.minDamage = cRoot.gameSettings.heroes.heroCaptain.maxRangeDamage[cRoot.game.gameHeroData.heroCaptain.level - 1];
               if(_loc1_ > 0)
               {
                  this.gainXpNew(_loc1_ * this.rangeAttackXpMultiplier);
               }
               this.rangeShootReloadTimeCounter = 0;
            }
            return true;
         }
         this.§_-Rn§ = false;
         this.rangeShootReloadTimeCounter = 0;
         this.§_-Os§();
         return false;
      }
      
      public function §return for import§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc1_:EnemyCommon = null;
         this.rangeShootTarget = null;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && _loc2_.§dynamic const for§ && this.§_-ax§(_loc2_) && this.onRangeShoot(_loc2_))
            {
               _loc1_ = _loc2_;
               break;
            }
         }
         if(_loc1_ != null)
         {
            this.rangeShootTarget = _loc1_;
            this.rangeShootPoint = new Point(_loc1_.x + _loc1_.xAdjust,_loc1_.y + _loc1_.yAdjust);
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
         if(_loc2_ > this.rangeShootMinDistance)
         {
            return true;
         }
         return false;
      }
      
      public function getDamageRangeShoot() : int
      {
         return this.rangeShootMinDamage + Math.ceil(Math.random() * (this.rangeShootMaxDamage - this.rangeShootMinDamage));
      }
      
      public function onRangeShoot(param1:EnemyCommon) : Boolean
      {
         var _loc2_:§dynamic const in§ = new §dynamic const in§(this.x - this.rangeShootWidth / 2,this.y - this.rangeShootHeight / 2,this.rangeShootWidth,this.rangeShootHeight);
         return _loc2_.containsPoint(new Point(param1.x,param1.y));
      }
      
      public function evalKraken() : Boolean
      {
         if(this.§_-Rn§ || this.isWalking || this.§_-ya§)
         {
            return false;
         }
         if(!this.isKraken)
         {
            if(this.§_-W3§ < this.§_-J4§)
            {
               return false;
            }
            if(!this.canKraken())
            {
               return false;
            }
            if(this.native.x >= this.x)
            {
               this.scaleX = 1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            this.isKraken = true;
            this.§import native§ = 0;
            this.playAnimationKraken();
            return true;
         }
         if(this.§import native§ < this.§use const in§)
         {
            ++this.§import native§;
            if(this.§import native§ == 15)
            {
               this.§_-W3§ = 0;
               this.doKraken();
            }
            return true;
         }
         this.isKraken = false;
         this.§_-W3§ = 0;
         this.§_-Os§();
         return false;
      }
      
      public function canKraken() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc3_:int = 0;
         var _loc1_:EnemyCommon = null;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && !_loc2_.isFlying && _loc2_.§dynamic const for§ && !_loc2_.§import for dynamic§ && this.§continue switch§(_loc2_) && this.onRangeKraken(_loc2_) && this.onRangeNear(_loc2_))
            {
               _loc1_ = _loc2_;
               break;
            }
         }
         if(_loc1_ != null)
         {
            if(_loc1_.§const const each§ || _loc1_.isBlocked)
            {
               _loc3_ = _loc1_.§package for var§;
            }
            else if(_loc1_.§package for var§ + _loc1_.getNodesSpeed() > _loc1_.§with const static§.length)
            {
               _loc3_ = _loc1_.§package for var§;
            }
            else
            {
               _loc3_ = _loc1_.§package for var§ + _loc1_.getNodesSpeed();
            }
            this.native = new Point(this.cRoot.§_-V8§[_loc1_.§false include§][0][_loc3_].x,this.cRoot.§_-V8§[_loc1_.§false include§][0][_loc3_].y);
            return true;
         }
         return false;
      }
      
      public function doKraken() : void
      {
         this.cRoot.decals.addChild(new §override use§(this.native,this.cRoot,this.§extends for set§));
         this.§_-Ug§(this.§extends for set§,this.krakenXpMultiplier);
      }
      
      public function onRangeKraken(param1:EnemyCommon) : Boolean
      {
         var _loc2_:§dynamic const in§ = new §dynamic const in§(this.x - this.§_-Wp§ / 2,this.y - this.§default else§ / 2,this.§_-Wp§,this.§default else§);
         return _loc2_.containsPoint(new Point(param1.x,param1.y));
      }
      
      public function onRangeNear(param1:EnemyCommon) : Boolean
      {
         var _loc7_:EnemyCommon = null;
         var _loc2_:int = int(this.cRoot.gameSettings.heroes.heroCaptain.krakenNearRange);
         var _loc3_:int = _loc2_ * this.cRoot.gameSettings.rangeRatio;
         var _loc4_:int = int(this.cRoot.gameSettings.heroes.heroCaptain.krakenNearNeededEnemies);
         var _loc5_:§dynamic const in§ = new §dynamic const in§(param1.x - _loc2_ / 2,param1.y - _loc3_ / 2,_loc2_,_loc3_);
         var _loc6_:int = 0;
         for each(_loc7_ in this.cRoot.enemies)
         {
            if(_loc7_ != param1 && _loc7_.isActive && !_loc7_.isFlying && _loc5_.containsPoint(new Point(_loc7_.x,_loc7_.y)))
            {
               if(++_loc6_ >= _loc4_)
               {
                  return true;
               }
            }
         }
         return false;
      }
      
      public function §continue switch§(param1:EnemyCommon) : Boolean
      {
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:Number = NaN;
         _loc3_ = param1.x - this.x;
         _loc4_ = param1.y - this.y;
         _loc2_ = Math.sqrt(_loc3_ * _loc3_ + _loc4_ * _loc4_);
         if(_loc2_ > this.§if const false§)
         {
            return true;
         }
         return false;
      }
      
      public function §in const dynamic§() : Boolean
      {
         if(this.isKraken || this.§_-Rn§ || this.isWalking)
         {
            return false;
         }
         if(!this.§_-ya§)
         {
            if(this.§switch throw§ < this.§set const implements§)
            {
               return false;
            }
            if(!this.§catch use§())
            {
               return false;
            }
            if(this.§set null§.x >= this.x)
            {
               this.scaleX = 1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(this.scaleX);
            }
            this.§_-ya§ = true;
            this.§_-R1§ = 0;
            this.§_-TD§();
            return true;
         }
         if(this.§_-R1§ < this.§_-o8§)
         {
            ++this.§_-R1§;
            if(this.§_-R1§ == 10)
            {
               this.§switch throw§ = 0;
               this.§finally const get§();
            }
            return true;
         }
         this.§_-ya§ = false;
         this.§switch throw§ = 0;
         this.§_-Os§();
         return false;
      }
      
      public function §catch use§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc1_:EnemyCommon = null;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && _loc2_.§dynamic const for§ && !_loc2_.isFlying && this.onRangeBombing(_loc2_))
            {
               _loc1_ = _loc2_;
               break;
            }
         }
         if(_loc1_ != null)
         {
            this.§_-AU§ = _loc1_.§false include§;
            this.§_-aF§ = _loc1_.§package for var§ + _loc1_.getNodesSpeed(2);
            this.§set null§ = this.cRoot.§_-V8§[_loc1_.§false include§][0][this.§_-aF§];
            this.§set null§ = §_-Mm§.ccpAdd(this.§set null§,§_-Mm§.ccp(0,-80 / 1.28));
            return true;
         }
         return false;
      }
      
      public function onRangeBombing(param1:EnemyCommon) : Boolean
      {
         var _loc2_:§dynamic const in§ = new §dynamic const in§(this.x - this.§final default§ / 2,this.y - this.§_-EU§ / 2,this.§final default§,this.§_-EU§);
         return _loc2_.containsPoint(new Point(param1.x,param1.y));
      }
      
      public function §_-Ys§(param1:EnemyCommon) : Boolean
      {
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:Number = NaN;
         _loc3_ = param1.x - this.x;
         _loc4_ = param1.y - this.y;
         _loc2_ = Math.sqrt(_loc3_ * _loc3_ + _loc4_ * _loc4_);
         if(_loc2_ > this.bombingMinRange)
         {
            return true;
         }
         return false;
      }
      
      public function §finally const get§() : void
      {
         this.§_-Ug§(this.§_-qF§,this.barrelXpMultiplier);
         var _loc1_:Point = §_-Mm§.ccpAdd(§_-Mm§.ccp(this.x,this.y),§_-Mm§.ccp(this.scaleX ? 5 : -5,-16 / 1.28));
         this.cRoot.bullets.addChild(new BombBoxPirateNew(this.cRoot,this.§_-qF§,_loc1_,this.§set null§,this.§_-AU§,this.§_-aF§));
         this.cRoot.game.gameSounds.§_-AQ§();
      }
      
      override protected function §try const for§() : void
      {
         var _loc1_:int = 0;
         if(this.enemy == null || !this.enemy.isActive)
         {
            this.unBlock();
            this.§default const const§();
            return;
         }
         if(!this.enemy.§_-ZL§())
         {
            if(Math.random() * 100 <= this.cRoot.gameSettings.heroes.heroCaptain.peakChance)
            {
               this.enemy.§_-aH§(this.cRoot.gameSettings.heroes.heroCaptain.peakMin,this.cRoot.gameSettings.heroes.heroCaptain.peakMax);
            }
            if(Math.random() < 0.1)
            {
               if(Math.random() > 0.5)
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.x + this.enemy.xAdjust,this.y + this.enemy.yAdjust),"Pow"));
               }
               else
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.x + this.enemy.xAdjust,this.y + this.enemy.yAdjust),"Sok"));
               }
            }
            _loc1_ = this.getDamage();
            this.gainXpByDamage(this.enemy.getArmorDamage(this.§_-vd§,_loc1_,0));
            this.enemy.setDamage(_loc1_,this.§_-vd§);
            if(!this.enemy.isActive)
            {
               if(this.enemy.isDead)
               {
                  this.§_-gu§(this.enemy.initHealth);
               }
               this.unBlock();
            }
         }
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§true for import§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§_-C6§();
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame25() : *
      {
         stop();
      }
      
      internal function frame53() : *
      {
         stop();
      }
      
      internal function frame81() : *
      {
         stop();
      }
      
      internal function frame109() : *
      {
         stop();
      }
      
      internal function frame153() : *
      {
         stop();
      }
      
      internal function frame173() : *
      {
         stop();
      }
      
      internal function frame217() : *
      {
         stop();
      }
      
      internal function frame282() : *
      {
         stop();
      }
   }
}

