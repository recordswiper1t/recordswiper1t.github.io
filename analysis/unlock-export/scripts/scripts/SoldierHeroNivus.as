package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.utils.Dictionary;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11597")]
   public class SoldierHeroNivus extends §dynamic const class§
   {
      
      internal var §_-dN§:Object;
      
      internal var §_-NN§:Boolean;
      
      internal var magicMissileRange:int;
      
      internal var magicMissileRetargetRange:int;
      
      internal var magicMissileQuantity:int;
      
      internal var magicMissileDamage:int;
      
      internal var magicMissileTime:int;
      
      internal var magicMissileTimeCounter:int;
      
      internal var magicMissileLevel:int;
      
      internal var magicMissileLaunchTime:int;
      
      internal var magicMissileLaunchTimeCounter:int;
      
      internal var magicMissilesLaunched:int;
      
      internal var magicMissileIsLaunching:Boolean;
      
      internal var §set for var§:Boolean;
      
      internal var §switch const for§:int;
      
      internal var chainSpellBounceRange:int;
      
      internal var §_-an§:int;
      
      internal var §else const do§:int;
      
      internal var §final const with§:int;
      
      internal var §_-lY§:Boolean;
      
      internal var §const for package§:int;
      
      internal var §override if§:int;
      
      internal var disintegrateQuantityEnemies:int;
      
      internal var §_-bw§:int;
      
      internal var §while for false§:int;
      
      internal var §get override§:int;
      
      internal var §_-e§:int;
      
      internal var rangeShootTarget:EnemyCommon;
      
      internal var rangeShootPoint:Point;
      
      internal var §_-Rn§:Boolean;
      
      internal var rangeShootReloadTime:Number;
      
      internal var rangeShootReloadTimeCounter:int;
      
      internal var rangeShootChargeTime:int;
      
      internal var rangeShootWidth:int;
      
      internal var rangeShootHeight:int;
      
      internal var rangeShootMinDamage:int;
      
      internal var rangeShootMaxDamage:int;
      
      internal var rangeShootMinDistance:int;
      
      internal var rangeAttackXpMultiplier:Number;
      
      internal var magicMissileXpMultiplier:Number;
      
      internal var chainXpMultiplier:Number;
      
      internal var disintegrateXpMultiplier:Number;
      
      internal var teleportRespawnWardFrameNumber:int;
      
      public var _storedAction:Function;
      
      public var §try const final§:Number = 0;
      
      public var §class for const§:Array;
      
      public var §function const break§:Boolean;
      
      public var teleportPosition:Point;
      
      public var teleportMinRange:Number;
      
      public function SoldierHeroNivus(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,16,this.frame17,173,this.frame174,250,this.frame251,269,this.frame270);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroNivus.portrait;
         this.xpMultiplier = this.cRoot.gameSettings.heroes.heroNivus.xpMultiplier;
         this.§implements const else§ = 23;
         this.§override set§ = 9;
         this.§_-dN§ = this.cRoot.gameSettings.heroes.heroNivus;
         this.§dynamic const§ = this.§_-dN§.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.§_-dN§.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.§_-dN§.respawn;
         this.attackReloadTime = this.§_-dN§.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 38;
         this.levelUpSoundShoot = 5;
         this.speed = 1.17;
         this.lifes = 1;
         this.xAdjust = 5;
         this.idleTime = 30;
         this.teleportMinRange = 100;
         this.level = this.cRoot.game.gameHeroData.heroNivus.level;
         this.xp = this.cRoot.game.gameHeroData.heroNivus.xp;
         this.applyAbilities();
         this.lifeBar = new LifeBarMedium(new Point(0,-30),this.health,this.initHealth);
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
         this.cRoot.§break default§(this);
         this.teleportRespawnWardFrameNumber = §_-Mm§.getFramenumberForLabel(this,"respawningPreEnd");
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§_-5x§();
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
         this.rangeShootChargeTime = 17;
         this.rangeShootReloadTime = this.§_-dN§.rangeShootReloadTime * this.cRoot.gameSettings.framesRate - this.rangeShootChargeTime;
         this.rangeShootWidth = this.§_-dN§.rangeShootRangeWidth;
         this.rangeShootHeight = this.rangeShootWidth * this.cRoot.gameSettings.rangeRatio;
         this.rangeShootMinDistance = this.§_-dN§.rangeShootMinDistance;
         this.rangeShootMinDamage = this.§_-dN§.minRangeDamage[this.level - 1];
         this.rangeShootMaxDamage = this.§_-dN§.maxRangeDamage[this.level - 1];
         this.xpMultiplier = this.§_-dN§.meleeAttackXpMultiplier;
         this.rangeAttackXpMultiplier = this.§_-dN§.rangeAttackXpMultiplier;
         this.magicMissileXpMultiplier = this.§_-dN§.magicMissileXpMultiplier;
         this.chainXpMultiplier = this.§_-dN§.chainXpMultiplier;
         this.disintegrateXpMultiplier = this.§_-dN§.disintegrateXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "nivus";
         param1.sName = Locale.loadStringEx("HERO_NIVUS_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroNivus.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override protected function §_-Ew§() : void
      {
         this.magicMissileQuantity = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroNivus.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.magicMissileLevel = _loc1_;
         var _loc2_:Object = this.§_-dN§.magicMissileSkill;
         this.magicMissileRange = _loc2_.range;
         this.magicMissileRetargetRange = _loc2_.retargetRange;
         this.magicMissileDamage = _loc2_.damage[_loc1_ - 1];
         this.magicMissileQuantity = _loc2_.quantity[_loc1_ - 1];
         this.magicMissileTime = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.magicMissileTimeCounter = 0;
         this.magicMissileLaunchTimeCounter = 0;
         this.magicMissileLaunchTime = 2;
         this.magicMissilesLaunched = 0;
      }
      
      override protected function §_-kZ§() : void
      {
         this.§set for var§ = false;
         this.§_-an§ = 0;
         this.§switch const for§ = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroNivus.skill2.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§switch const for§ = _loc1_;
         var _loc2_:Object = this.§_-dN§.chainSpellSkill;
         this.§else const do§ = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.§final const with§ = 0;
         this.chainSpellBounceRange = _loc2_.bounceRange;
         this.§_-an§ = _loc2_.maxJumps[_loc1_ - 1];
      }
      
      override protected function §get const default§() : void
      {
         this.disintegrateQuantityEnemies = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroNivus.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§_-e§ = _loc1_;
         var _loc2_:Object = this.§_-dN§.disintegrateSkill;
         this.§const for package§ = _loc2_.rangeTrigger;
         this.§override if§ = _loc2_.rangeEffect;
         this.§_-bw§ = _loc2_.damagePool[_loc1_ - 1];
         this.disintegrateQuantityEnemies = _loc2_.quantity[_loc1_ - 1];
         this.§while for false§ = _loc2_.time * this.cRoot.gameSettings.framesRate;
         this.§get override§ = 0;
      }
      
      override protected function §_-kp§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroNivus.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.arcaneReachSkill;
         var _loc3_:Number = _loc2_.rangePercentIncrease[_loc1_ - 1] / 100;
         this.rangeShootWidth += Math.ceil(this.rangeShootWidth * _loc3_);
         this.rangeShootHeight += Math.ceil(this.rangeShootHeight * _loc3_);
      }
      
      override protected function §_-gF§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroNivus.skill5level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.arcaneFocusSkill;
         var _loc3_:Number = Number(_loc2_.damageIncrease[_loc1_ - 1]);
         this.minDamage += _loc3_;
         this.maxDamage += _loc3_;
         this.rangeShootMinDamage += _loc3_;
         this.rangeShootMaxDamage += _loc3_;
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.rangeShootReloadTimeCounter;
         ++this.magicMissileTimeCounter;
         ++this.§get override§;
         ++this.§final const with§;
         if(this.§function const break§)
         {
            return true;
         }
         if(super.§_-xK§())
         {
            return true;
         }
         if(!this.§_-Rn§ && !this.§_-NN§ && this.§false static§())
         {
            return true;
         }
         if(!this.§_-Rn§ && !this.§_-lY§ && this.§_-Zo§())
         {
            return true;
         }
         if(!this.§function const break§ && this.evalRangeShoot())
         {
            return true;
         }
         return false;
      }
      
      public function §super override§() : void
      {
         trace("NewFRAME");
         this.§_-Qz§("alt",this.cRoot.game.main.magicMissileParticlesAltPool);
         this.§_-Qz§("A",this.cRoot.game.main.magicMissileParticlesAPool);
         this.§_-Qz§("B",this.cRoot.game.main.magicMissileParticlesBPool);
         this.§_-Qz§("C",this.cRoot.game.main.magicMissileParticlesCPool);
      }
      
      public function §_-Qz§(param1:String, param2:Dictionary) : void
      {
         var _loc4_:Object = null;
         var _loc3_:int = 0;
         for each(_loc4_ in param2)
         {
            if(_loc4_.isActive)
            {
               _loc3_++;
            }
         }
         trace(param1 + " - " + _loc3_);
      }
      
      public function §false static§() : Boolean
      {
         if(this.disintegrateQuantityEnemies == 0 || this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.§_-lY§)
         {
            return true;
         }
         if(this.§get override§ < this.§while for false§)
         {
            return false;
         }
         if(!this.§_-Qt§())
         {
            return false;
         }
         this.§_-lY§ = true;
         this.§_-iY§();
         return true;
      }
      
      public function §_-Qt§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && !_loc2_.isBoss && _loc2_.§dynamic const for§ && _loc2_.health < this.§_-bw§ && §_-Mm§.ellipseContains(this.x,this.y,_loc2_,this.§const for package§,_loc1_))
            {
               return true;
            }
         }
         return false;
      }
      
      public function §_-iY§() : void
      {
         this.gotoAndPlay("instaKill");
      }
      
      public function §null const else§() : void
      {
         var _loc5_:EnemyCommon = null;
         var _loc6_:§_-7Y§ = null;
         this.§_-Ug§(this.§_-e§,this.disintegrateXpMultiplier);
         this.cRoot.game.gameSounds.playNivusDesintegrate();
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc2_:int = this.§_-bw§;
         var _loc3_:int = 0;
         var _loc4_:Dictionary = this.cRoot.enemies;
         for each(_loc5_ in _loc4_)
         {
            if(_loc2_ <= 0)
            {
               break;
            }
            if(_loc5_.isActive && !_loc5_.isBoss && _loc5_.§dynamic const for§ && §_-Mm§.ellipseContains(this.x,this.y,_loc5_,this.§override if§,_loc1_))
            {
               if(_loc5_.health <= _loc2_)
               {
                  _loc2_ -= _loc5_.health;
                  _loc6_ = new §_-7Y§(§_-Mm§.ccpAdd(new Point(_loc5_.x,_loc5_.y),§_-Mm§.ccp(0,_loc5_.yAdjust)),0);
                  this.cRoot.entities.addChild(_loc6_);
                  _loc5_.§_-I2§();
                  if(++_loc3_ >= this.disintegrateQuantityEnemies)
                  {
                     break;
                  }
               }
            }
         }
         this.§get override§ = 0;
         _loc4_ = null;
      }
      
      public function endDisintegrate() : void
      {
         this.§_-lY§ = false;
         this.§_-Os§();
      }
      
      public function §var const false§() : void
      {
         this.gotoAndStop("idle");
      }
      
      override public function unPause() : void
      {
         switch(this.currentFrameLabel)
         {
            case "runningEnd":
               this.gotoAndPlay("running");
               break;
            case "fightingEnd":
            case "fighting2End":
            case "respawningEnd":
            case "flurryEnd":
            case "sandWarriorEnd":
            case "deadEnd":
            case "idle":
            case "proyAttackAction":
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
         if(this.currentFrameLabel == "boltAttackAction")
         {
            this.doRangedShoot();
         }
         if(this.currentFrameLabel == "boltAttackEnd")
         {
            this.endRangedShoot();
         }
         if(this.currentFrameLabel == "teleportIn")
         {
            this.§native const override§();
         }
         if(this.currentFrameLabel == "teleportInEnd")
         {
            this.teleportEnd();
         }
         if(this.currentFrameLabel == "instaKilAction")
         {
            this.§null const else§();
         }
         if(this.currentFrameLabel == "instaKillEnd")
         {
            this.endDisintegrate();
         }
         if(this.currentFrameLabel == "proyAttackAction")
         {
            if(!this.magicMissileIsLaunching)
            {
               this.magicMissileIsLaunching = true;
               this.stop();
            }
            else
            {
               if(this.magicMissilesLaunched >= this.magicMissileQuantity)
               {
                  this.gotoAndPlay(this.currentFrame + 1);
                  this.magicMissileIsLaunching = false;
                  return;
               }
               ++this.magicMissileLaunchTimeCounter;
               if(this.magicMissileLaunchTimeCounter > this.magicMissileLaunchTime)
               {
                  this.magicMissileLaunchTimeCounter = 0;
                  this.§set const each§();
                  return;
               }
            }
         }
         if(this.currentFrameLabel == "proyAttackEnd")
         {
            this.endMagicMissile();
         }
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.§function const break§)
         {
            return;
         }
         this.currentLabels;
         if(!this.isDead && !this.isFacehugger && !this.§function const break§ && this.currentFrame < this.teleportRespawnWardFrameNumber)
         {
            super.§_-jv§(param1);
            if(this.§const for throw§(param1))
            {
               this.§true implements§();
               this.cRoot.game.gameSounds.§break const in§();
            }
         }
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§_-5x§();
      }
      
      public function §const for throw§(param1:Point) : Boolean
      {
         return this.§else const default§() && §_-Mm§.ccpDistance(new Point(this.x,this.y),param1) > this.teleportMinRange;
      }
      
      public function §else const default§() : Boolean
      {
         return true;
      }
      
      public function §true implements§() : Boolean
      {
         this.lifeBar.visible = false;
         this.§extends for throw§();
         this.§function const break§ = true;
         this.gotoAndPlay("teleportOut");
         this.teleportPosition = this.§in const while§;
         if(this.path.length > 0)
         {
            this.path = [];
         }
         return true;
      }
      
      public function §native const override§() : void
      {
         this.x = this.teleportPosition.x;
         this.y = this.teleportPosition.y;
      }
      
      public function teleportEnd() : void
      {
         this.lifeBar.visible = true;
         this.§function const break§ = false;
         this.§_-Os§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§_-i6§();
      }
      
      public function §_-Zo§() : Boolean
      {
         if(this.magicMissileQuantity == 0 || this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.§_-NN§)
         {
            return true;
         }
         if(this.magicMissileTimeCounter < this.magicMissileTime)
         {
            return false;
         }
         if(!this.§default const return§())
         {
            return false;
         }
         this.§_-NN§ = true;
         this.§class case§();
         return true;
      }
      
      public function §class case§() : void
      {
         this.magicMissilesLaunched = 0;
         this.magicMissileLaunchTimeCounter = 0;
         this.gotoAndPlay("proyAttack");
         this.cRoot.game.gameSounds.playNivusMissileSummon();
      }
      
      public function §default const return§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         for each(_loc2_ in this.cRoot.enemies)
         {
            if(_loc2_.isActive && _loc2_.§dynamic const for§ && §_-Mm§.ellipseContains(this.x,this.y,_loc2_,this.magicMissileRange,_loc1_))
            {
               return true;
            }
         }
         return false;
      }
      
      public function §set const each§() : void
      {
         var _loc3_:EnemyCommon = null;
         var _loc4_:Point = null;
         var _loc5_:Boolean = false;
         trace("MagicMissile: " + this.magicMissilesLaunched + " of " + this.magicMissileQuantity);
         ++this.magicMissilesLaunched;
         this.§_-Ug§(this.magicMissileLevel,this.magicMissileXpMultiplier);
         this.magicMissileTimeCounter = 0;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc2_:EnemyCommon = null;
         for each(_loc3_ in this.cRoot.enemies)
         {
            if(_loc3_.isActive && _loc3_.§dynamic const for§ && §_-Mm§.ellipseContains(this.x,this.y,_loc3_,this.magicMissileRange,_loc1_))
            {
               _loc2_ = _loc3_;
            }
         }
         if(_loc2_ == null)
         {
            _loc4_ = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.ccpMult(§_-Mm§.ccpForAngle(§_-Mm§.getRandomFrom(0,360)),50));
            _loc5_ = false;
         }
         else
         {
            _loc4_ = new Point(_loc2_.x,_loc2_.y);
            _loc5_ = _loc2_.isFlying;
         }
         var _loc6_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2f(this.scaleX > 0 ? -16 : 16,36));
         this.cRoot.bullets.addChild(new §_-Q9§(this.cRoot,_loc6_,_loc4_,_loc2_,1,_loc5_,this.scaleX > 0 ? -1 : 1,this.magicMissileDamage,this.magicMissileRetargetRange));
      }
      
      public function endMagicMissile() : void
      {
         this.§_-NN§ = false;
         this.magicMissileIsLaunching = false;
         this.§_-Os§();
      }
      
      public function evalRangeShoot() : Boolean
      {
         if(this.isFighting || this.isWalking)
         {
            return false;
         }
         if(this.§_-Rn§)
         {
            return true;
         }
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
            this.lifeBar.§dynamic for const§(scaleX);
         }
         else
         {
            this.scaleX = -1;
            this.lifeBar.§dynamic for const§(scaleX);
         }
         this.§_-Rn§ = true;
         this.rangeShootReloadTimeCounter = 0;
         this.§_-QQ§();
         return true;
      }
      
      public function §_-QQ§() : void
      {
         var _loc1_:Number = this.rangeShootChargeTime / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("boltAttack");
      }
      
      public function endRangedShoot() : void
      {
         this.§_-Rn§ = false;
         this.rangeShootReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function doRangedShoot() : void
      {
         var _loc1_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2f((this.scaleX > 0 ? 1 : -1) * 17,34));
         var _loc2_:int = 1;
         if(this.rangeShootTarget.isActive && this.§final const with§ >= this.§else const do§ && this.§_-an§ > 0)
         {
            _loc2_ = this.§_-an§;
            this.§final const with§ = 0;
         }
         this.cRoot.bullets.addChild(new §_-HX§(this.cRoot,_loc1_,this.rangeShootTarget,1,_loc2_,[],this.rangeShootMinDamage,this.rangeShootMaxDamage,this.chainSpellBounceRange));
         var _loc3_:int = this.rangeShootMinDamage + (this.rangeShootMaxDamage - this.rangeShootMinDamage) / 2;
         if(_loc2_ > 1)
         {
            this.§_-Ug§(this.§switch const for§,this.chainXpMultiplier);
         }
         else
         {
            this.gainXpNew(_loc3_ * this.rangeAttackXpMultiplier);
         }
         this.rangeShootReloadTimeCounter = 0;
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
            this.rangeShootPoint = §_-Mm§.ccp(_loc1_.x + _loc1_.xAdjust,_loc1_.y + _loc1_.yAdjust);
            return true;
         }
         return false;
      }
      
      public function §_-ax§(param1:EnemyCommon) : Boolean
      {
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:Number = NaN;
         if(param1.isFlying)
         {
            return true;
         }
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
         return §_-Mm§.ellipseContainsWH(this.x,this.y,param1,this.rangeShootWidth,this.rangeShootHeight);
      }
      
      public function §_-tl§() : void
      {
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.§_-Rn§ = false;
         this.§_-lY§ = false;
         this.§_-NN§ = false;
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.§_-Rn§ = false;
         this.§_-lY§ = false;
         this.§_-NN§ = false;
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame17() : *
      {
         stop();
      }
      
      internal function frame174() : *
      {
         stop();
      }
      
      internal function frame251() : *
      {
         stop();
      }
      
      internal function frame270() : *
      {
         stop();
      }
   }
}

