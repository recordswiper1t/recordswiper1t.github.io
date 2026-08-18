package
{
   import §_-aW§.*;
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12272")]
   public class SoldierHeroMirage extends §dynamic const class§
   {
      
      private var referencePath:int;
      
      private var §_-c0§:int;
      
      private var §default true§:Point;
      
      private var rangeShootLevel:int;
      
      private var rangeShootTarget:EnemyCommon;
      
      private var rangeShootPoint:Point;
      
      private var §_-Rn§:Boolean;
      
      private var rangeShootReloadTime:Number;
      
      private var rangeShootReloadTimeCounter:int;
      
      private var rangeShootChargeTime:int;
      
      private var rangeShootChargeTimeCounter:int;
      
      private var rangeShootWidth:int;
      
      private var rangeShootHeight:int;
      
      private var rangeShootMinDamage:int;
      
      private var rangeShootMaxDamage:int;
      
      private var rangeShootMinDistance:int;
      
      private var dodge:int;
      
      private var §catch null§:Boolean;
      
      private var §var null§:int;
      
      private var §_-Ai§:int;
      
      private var §_-f0§:int;
      
      private var §_-8R§:int;
      
      private var isLethal:Boolean;
      
      private var §_-nO§:EnemyCommon;
      
      private var §_-fN§:Point;
      
      private var lethalOldPosition:Point;
      
      private var §var const get§:int;
      
      private var §_-Ny§:int;
      
      private var §_-Yh§:int;
      
      private var §_-qY§:int;
      
      private var §_-ns§:int;
      
      private var §return super§:int;
      
      private var lethalMinDamage:int;
      
      private var lethalMaxDamage:int;
      
      private var lethalInstakillPercent:int;
      
      private var §_-fw§:int;
      
      private var §_-VI§:Boolean;
      
      private var §for for super§:int;
      
      private var §use for const§:int;
      
      private var §with var§:int;
      
      private var §continue finally§:int;
      
      private var §_-N5§:int;
      
      private var §_-Od§:int;
      
      private var shadowMinRange:int;
      
      private var shadowCopies:int;
      
      private var rangeAttackXpMultiplier:Number;
      
      private var shadowDanceXpMultiplier:Number;
      
      private var lethalStrikeXpMultiplier:Number;
      
      private var originalSpeed:Number;
      
      public function SoldierHeroMirage(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,5,this.frame6,27,this.frame28,41,this.frame42,55,this.frame56,60,this.frame61,67,this.frame68,92,this.frame93,102,this.frame103,125,this.frame126,141,this.frame142,195,this.frame196);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroMirage.portrait;
         this.§implements const else§ = 23;
         this.§override set§ = 9;
         this.rangeShootChargeTime = 16;
         this.§_-Yh§ = 40;
         this.§with var§ = 24;
         this.§dynamic const§ = this.cRoot.gameSettings.heroes.heroMirage.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.cRoot.gameSettings.heroes.heroMirage.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.cRoot.gameSettings.heroes.heroMirage.respawn;
         this.attackReloadTime = this.cRoot.gameSettings.heroes.heroMirage.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.§var null§ = 12;
         this.dodge = 0;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 16;
         this.levelUpSoundShoot = 5;
         this.speed = 2.4 / 1.28;
         this.originalSpeed = this.speed;
         this.level = this.cRoot.game.gameHeroData.heroMirage.level;
         this.xp = this.cRoot.game.gameHeroData.heroMirage.xp;
         this.lifes = 1;
         this.xAdjust = 5;
         this.idleTime = 30;
         this.lifeBar = new LifeBarMedium(new Point(0,-27),this.health,this.initHealth);
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
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§final for finally§();
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
         this.health = this.initHealth = this.cRoot.gameSettings.heroes.heroMirage.health[this.level - 1];
         this.regenerateHealth = this.cRoot.gameSettings.heroes.heroMirage.regen[this.level - 1];
         this.armor = this.cRoot.gameSettings.heroes.heroMirage.armor[this.level - 1];
         this.minDamage = this.cRoot.gameSettings.heroes.heroMirage.minDamage[this.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroMirage.maxDamage[this.level - 1];
         this.rangeShootReloadTime = this.cRoot.gameSettings.heroes.heroMirage.rangeShootReloadTime * this.cRoot.gameSettings.framesRate - this.rangeShootChargeTime;
         this.rangeShootWidth = this.cRoot.gameSettings.heroes.heroMirage.rangeShootRangeWidth;
         this.rangeShootHeight = this.rangeShootWidth * this.cRoot.gameSettings.rangeRatio;
         this.rangeShootMinDistance = this.cRoot.gameSettings.heroes.heroMirage.rangeShootMinDistance;
         this.rangeShootMinDamage = this.cRoot.gameSettings.heroes.heroMirage.minRangeDamage[this.cRoot.game.gameHeroData.heroMirage.level - 1];
         this.rangeShootMaxDamage = this.cRoot.gameSettings.heroes.heroMirage.maxRangeDamage[this.cRoot.game.gameHeroData.heroMirage.level - 1];
         this.xpMultiplier = this.cRoot.gameSettings.heroes.heroMirage.meleeAttackXpMultiplier;
         this.rangeAttackXpMultiplier = this.cRoot.gameSettings.heroes.heroMirage.rangeAttackXpMultiplier;
         this.shadowDanceXpMultiplier = this.cRoot.gameSettings.heroes.heroMirage.shadowDanceXpMultiplier;
         this.lethalStrikeXpMultiplier = this.cRoot.gameSettings.heroes.heroMirage.lethalStrikeXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "mirage";
         param1.sName = Locale.loadStringEx("HERO_MIRAGE_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroMirage.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override protected function §_-Ew§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroMirage.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:int = int(this.cRoot.gameSettings.heroes.heroMirage.precisionExtraDamage[_loc1_ - 1]);
         this.rangeShootMinDamage += _loc2_;
         this.rangeShootMaxDamage += _loc2_;
         this.rangeShootWidth += this.cRoot.gameSettings.heroes.heroMirage.precisionExtraRange[_loc1_ - 1];
      }
      
      override protected function §_-kZ§() : void
      {
         this.§_-f0§ = this.cRoot.game.gameHeroData.heroMirage.skill2.level;
         if(this.§_-f0§ == 0)
         {
            return;
         }
         this.dodge = this.cRoot.gameSettings.heroes.heroMirage.shadowDodgeIncrement[this.§_-f0§ - 1];
      }
      
      override protected function §get const default§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroMirage.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Number = this.cRoot.gameSettings.heroes.heroMirage.swiftnessSpeedIncrement[_loc1_ - 1] * §_-Mm§.GAME_SCALE;
         this.speed = this.originalSpeed + this.originalSpeed * _loc2_ / 100;
      }
      
      override protected function §_-kp§() : void
      {
         this.§_-fw§ = this.cRoot.game.gameHeroData.heroMirage.skill4.level;
         if(this.§_-fw§ == 0)
         {
            return;
         }
         this.§for for super§ = this.cRoot.gameSettings.heroes.heroMirage.ShadowDanceCooldown * this.cRoot.gameSettings.framesRate;
         this.§_-N5§ = this.cRoot.gameSettings.heroes.heroMirage.shadowDanceRange;
         this.§_-Od§ = this.§_-N5§ * this.cRoot.gameSettings.rangeRatio;
         this.shadowMinRange = this.cRoot.gameSettings.heroes.heroMirage.shadowDanceMinRange;
         this.shadowCopies = this.cRoot.gameSettings.heroes.heroMirage.shadowDanceCopies[this.§_-fw§ - 1];
      }
      
      override protected function §_-gF§() : void
      {
         this.§_-8R§ = this.cRoot.game.gameHeroData.heroMirage.skill5.level;
         if(this.§_-8R§ == 0)
         {
            return;
         }
         this.§var const get§ = this.cRoot.gameSettings.heroes.heroMirage.lethalCooldown * this.cRoot.gameSettings.framesRate;
         this.lethalMinDamage = this.cRoot.gameSettings.heroes.heroMirage.lethalDamage * this.§_-8R§;
         this.lethalMaxDamage = this.cRoot.gameSettings.heroes.heroMirage.lethalDamage * this.§_-8R§;
         this.§_-ns§ = this.cRoot.gameSettings.heroes.heroMirage.lethalRange;
         this.§return super§ = this.§_-ns§ * this.cRoot.gameSettings.rangeRatio;
         this.lethalInstakillPercent = this.cRoot.gameSettings.heroes.heroMirage.lethalInstakillPercent[this.§_-8R§ - 1];
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
               break;
            default:
               this.play();
         }
         this.§do const throw§();
      }
      
      public function §break§(param1:Point, param2:*) : void
      {
         var _loc3_:Number = param2.y + param1.y;
         var _loc4_:Number = param2.x - param1.x;
         var _loc5_:Number = Math.round(Math.atan2(_loc3_,_loc4_) * 180);
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
            this.playAnimationShoot();
         }
         else
         {
            this.playAnimationShoot();
         }
      }
      
      override public function onFrameUpdate() : void
      {
         this.§for const super§();
         super.onFrameUpdate();
      }
      
      public function §for const super§() : void
      {
         if(this.currentFrameLabel == "fadeBackEnd")
         {
            if(this.isLethal)
            {
               this.§try use§();
            }
         }
         if(this.currentFrameLabel == "lethalStrikeEnd")
         {
            this.§_-xl§();
         }
         if(this.currentFrameLabel == "fadeBackEnd")
         {
            this.§set each§();
         }
      }
      
      public function playAnimationShoot() : void
      {
         this.gotoAndPlay("shoot");
      }
      
      public function playAnimationShootUp() : void
      {
         this.gotoAndPlay("shootUp");
      }
      
      public function §true switch§() : void
      {
         this.cRoot.game.gameSounds.§include include§();
         this.§true const use§();
      }
      
      public function §true const use§() : void
      {
         this.gotoAndPlay("fadeBack");
      }
      
      public function §set each§() : void
      {
         var _loc1_:SoldierMirageIllusion = null;
         this.gotoAndPlay("fadeInFront");
         if(this.enemy != null && this.enemy.isActive)
         {
            _loc1_ = new SoldierMirageIllusion(new Point(this.x,this.y),new Point(this.x,this.y),null,40,true,new Point(this.x,this.y),null,0);
            _loc1_.isActive = true;
            _loc1_.isDead = false;
            _loc1_.isBlocking = true;
            _loc1_.isFighting = true;
            _loc1_.enemy = this.enemy;
            _loc1_.scaleX = this.scaleX;
            this.enemy.soldier = _loc1_;
            this.§in const while§ = this.getNewDodgePosition();
            this.rallyPoint = this.§in const while§;
            this.x = this.§in const while§.x;
            this.y = this.§in const while§.y;
            this.cRoot.entities.addChild(_loc1_);
         }
         this.isBlocking = false;
         this.isFighting = false;
         this.isCharging = false;
         this.enemy = null;
      }
      
      public function §while const null§() : void
      {
         this.gotoAndPlay("fadeBack");
         this.cRoot.game.gameSounds.§break const import§();
      }
      
      public function §try use§() : void
      {
         var _loc1_:Point = null;
         this.gotoAndPlay("lethalStrike");
         this.cRoot.game.gameSounds.§_-HF§();
         this.lethalOldPosition = new Point(this.x,this.y);
         this.x = this.§_-fN§.x;
         this.y = this.§_-fN§.y;
         if(this.§_-nO§ != null)
         {
            if(!this.§_-nO§.isBlocked && Boolean(this.§_-nO§.isActive) && !this.§_-nO§.isBoss && Boolean(this.§_-nO§.§get for catch§))
            {
               this.§_-nO§.doStun();
            }
            _loc1_ = this.getLethalPosition(this.§_-nO§);
            this.x = _loc1_.x;
            this.y = _loc1_.y;
            this.scaleX = this.§_-nO§.x > this.x ? -1 : 1;
            this.lifeBar.§dynamic for const§(this.scaleX);
         }
      }
      
      public function §_-xl§() : void
      {
         this.gotoAndPlay("fadeIn");
         this.x = this.lethalOldPosition.x;
         this.y = this.lethalOldPosition.y;
      }
      
      public function §_-f8§() : void
      {
         this.gotoAndPlay("special");
         this.cRoot.game.gameSounds.§dynamic for finally§();
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.rangeShootReloadTimeCounter;
         ++this.§_-Ny§;
         ++this.§use for const§;
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.§_-fw§ != 0 && this.§extends throw§())
         {
            return true;
         }
         if(this.§_-8R§ != 0 && this.§extends get§())
         {
            return true;
         }
         if(Boolean(this.§catch null§) && this.§var const return§())
         {
            return true;
         }
         if(this.evalRangeShoot())
         {
            return true;
         }
         return false;
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.§_-Rn§ = false;
         this.isCharging = false;
         this.isLevelUp = false;
         this.§catch null§ = false;
         this.isLethal = false;
         this.§_-VI§ = false;
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.§_-Rn§ = false;
         this.isCharging = false;
         this.isLevelUp = false;
         this.§catch null§ = false;
         this.§_-b3§();
         this.§_-VI§ = false;
      }
      
      public function §extends get§() : Boolean
      {
         if(this.isWalking || Boolean(this.§_-Rn§) || Boolean(this.§catch null§) || Boolean(this.§_-VI§))
         {
            return false;
         }
         if(!this.isLethal)
         {
            if(this.§_-Ny§ < this.§var const get§)
            {
               return false;
            }
            if(!this.§_-RZ§())
            {
               return false;
            }
            this.isLethal = true;
            this.§_-qY§ = 0;
            this.§_-Ny§ = 0;
            this.§true extends§();
            return true;
         }
         if(this.§_-qY§ < this.§_-Yh§)
         {
            ++this.§_-qY§;
            if(this.§_-qY§ == 10)
            {
               if(this.§_-nO§ != null && Boolean(this.§_-nO§.isActive))
               {
                  if(!this.§_-nO§.isBoss && Math.random() < this.lethalInstakillPercent / 100)
                  {
                     this.§_-nO§.explode();
                  }
                  else
                  {
                     switch(this.§_-nO§.bloodClass)
                     {
                        case "BloodViolet":
                           this.cRoot.bullets.addChild(new MirageBloodViolet(new Point(this.§_-nO§.x,this.§_-nO§.y),this.cRoot));
                           break;
                        case "BloodGreen":
                           this.cRoot.bullets.addChild(new MirageBloodGreen(new Point(this.§_-nO§.x,this.§_-nO§.y),this.cRoot));
                           break;
                        default:
                           this.cRoot.bullets.addChild(new MirageBlood(new Point(this.§_-nO§.x,this.§_-nO§.y),this.cRoot));
                     }
                     this.§_-nO§.setDamage(this.lethalMinDamage,§_-Mm§.I_ARMOR);
                  }
               }
            }
            if(this.§_-qY§ == 17)
            {
               if(this.§_-nO§ != null && Boolean(this.§_-nO§.isActive))
               {
                  if(!this.§_-nO§.isBlocked && !this.§_-nO§.isBoss && Boolean(this.§_-nO§.§get for catch§))
                  {
                     this.§_-nO§.endStun();
                  }
               }
            }
            return true;
         }
         this.isLethal = false;
         this.§_-Ny§ = 0;
         this.§_-nO§ = null;
         this.§_-Os§();
         return false;
      }
      
      public function §_-b3§() : void
      {
         this.isLethal = false;
         if(this.§_-nO§ != null && Boolean(this.§_-nO§.isActive))
         {
            if(!this.§_-nO§.isBlocked && !this.§_-nO§.isBoss)
            {
               this.§_-nO§.endStun();
            }
         }
      }
      
      public function §_-RZ§() : Boolean
      {
         var _loc2_:EnemyCommon = null;
         var _loc3_:§dynamic const in§ = null;
         if(this.isBlocking && this.isFighting && this.enemy != null)
         {
            this.§_-nO§ = this.enemy;
            this.§_-fN§ = this.getLethalPosition(this.§_-nO§);
            return true;
         }
         var _loc1_:EnemyCommon = null;
         this.§_-nO§ = null;
         for each(_loc2_ in this.cRoot.enemies)
         {
            _loc3_ = new §dynamic const in§(this.x - this.§_-ns§ / 2,this.y - this.§return super§ / 2,this.§_-ns§,this.§return super§);
            if(_loc2_.§_-On§ && _loc2_.isActive && !_loc2_.isFlying && _loc2_.§dynamic const for§ && !_loc2_.§import for dynamic§ && _loc3_.containsPoint(new Point(_loc2_.x,_loc2_.y)))
            {
               _loc1_ = _loc2_;
               break;
            }
         }
         if(_loc1_ != null)
         {
            this.§_-nO§ = _loc1_;
            this.§_-fN§ = this.getLethalPosition(this.§_-nO§);
            return true;
         }
         return false;
      }
      
      public function §true extends§() : void
      {
         this.scaleX = this.§_-nO§.scaleX ? 1 : -1;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.§while const null§();
         this.§_-Ug§(this.§_-8R§,this.lethalStrikeXpMultiplier);
      }
      
      public function getLethalPosition(param1:EnemyCommon) : Point
      {
         if(param1.scaleX == -1)
         {
            return new Point(param1.x + param1.xSoldierAdjust,param1.y);
         }
         return new Point(param1.x - param1.xSoldierAdjust,param1.y);
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.isLethal)
         {
            return;
         }
         super.§_-jv§(param1);
      }
      
      override public function setDamage(param1:int, param2:Boolean = false) : *
      {
         if(Boolean(this.§catch null§) || Boolean(this.isLethal))
         {
            return;
         }
         super.setDamage(param1,param2);
      }
      
      public function §extends throw§() : Boolean
      {
         if(this.isWalking || Boolean(this.§_-Rn§) || Boolean(this.§catch null§) || Boolean(this.isLethal) || this.isBlocking || this.isFighting)
         {
            return false;
         }
         if(!this.§_-VI§)
         {
            if(this.§use for const§ < this.§for for super§)
            {
               return false;
            }
            if(!this.§in class§())
            {
               return false;
            }
            this.§_-VI§ = true;
            this.§continue finally§ = 0;
            this.§use for const§ = 0;
            this.§_-f8§();
            return true;
         }
         if(this.§continue finally§ < this.§with var§)
         {
            ++this.§continue finally§;
            if(this.§continue finally§ == 7)
            {
               this.§_-hQ§();
            }
            return true;
         }
         this.§_-VI§ = false;
         this.§use for const§ = 0;
         this.§_-Os§();
         return false;
      }
      
      public function §in class§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            if(_loc1_.isActive && !_loc1_.isFlying && _loc1_.§dynamic const for§ && !_loc1_.§import for dynamic§ && this.§_-9t§(_loc1_) && §_-Mm§.ellipseContainsWH(this.x,this.y,_loc1_,this.§_-N5§,this.§_-Od§))
            {
               return true;
            }
         }
         return false;
      }
      
      public function §_-hQ§() : void
      {
         var _loc3_:EnemyCommon = null;
         var _loc4_:§dynamic const in§ = null;
         var _loc5_:SoldierMirageIllusion = null;
         var _loc6_:int = 0;
         this.§_-Ug§(this.§_-fw§,this.shadowDanceXpMultiplier);
         var _loc1_:int = 0;
         var _loc2_:EnemyCommon = null;
         for each(_loc3_ in this.cRoot.enemies)
         {
            _loc4_ = new §dynamic const in§(this.x - this.§_-N5§ * 1.5 / 2,this.y - this.§_-Od§ * 1.5 / 2,this.§_-N5§ * 1.5,this.§_-Od§ * 1.5);
            if(_loc3_.isActive && !_loc3_.isFlying && _loc3_.§dynamic const for§ && _loc4_.containsPoint(new Point(_loc3_.x,_loc3_.y)))
            {
               _loc5_ = new SoldierMirageIllusion(new Point(this.x,this.y),new Point(this.x,this.y),null,40,true,new Point(this.x,this.y),_loc3_,this.§_-fw§);
               this.cRoot.entities.addChild(_loc5_);
               _loc2_ = _loc3_;
               _loc1_++;
               if(this.shadowCopies == _loc1_)
               {
                  break;
               }
            }
         }
         if(_loc1_ < this.shadowCopies && _loc2_ != null)
         {
            _loc6_ = 0;
            while(_loc6_ < this.shadowCopies - _loc1_)
            {
               _loc5_ = new SoldierMirageIllusion(new Point(this.x,this.y),new Point(this.x,this.y),null,40,true,new Point(this.x,this.y),_loc2_,this.§_-fw§);
               this.cRoot.entities.addChild(_loc5_);
               _loc6_++;
            }
         }
      }
      
      public function §_-9t§(param1:EnemyCommon) : Boolean
      {
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:Number = NaN;
         _loc3_ = param1.x - this.x;
         _loc4_ = param1.y - this.y;
         _loc2_ = Math.sqrt(_loc3_ * _loc3_ + _loc4_ * _loc4_);
         if(_loc2_ > this.shadowMinRange)
         {
            return true;
         }
         return false;
      }
      
      override public function §_-7X§() : Boolean
      {
         if(this.isFacehugger || Boolean(this.isLethal) || Boolean(this.§_-Rn§) || Boolean(this.§_-VI§))
         {
            return false;
         }
         if(Math.random() <= this.dodge / 100)
         {
            if(this.§catch null§)
            {
               return false;
            }
            if(this.isCharging)
            {
               this.isCharging = false;
               this.§break finally§ = 0;
            }
            this.§catch null§ = true;
            this.§_-Ai§ = 0;
            this.§true switch§();
            return true;
         }
         return false;
      }
      
      public function §var const return§() : Boolean
      {
         if(!this.§catch null§)
         {
            return false;
         }
         if(this.§_-Ai§ < this.§var null§)
         {
            ++this.§_-Ai§;
            if(this.§_-Ai§ == 3)
            {
               this.cRoot.entities.addChild(new MirageSmoke(new Point(this.x,this.y),this.cRoot));
            }
            return true;
         }
         this.§catch null§ = false;
         this.§_-Os§();
         return false;
      }
      
      public function getNewDodgePosition() : Point
      {
         var _loc4_:int = 0;
         var _loc5_:Point = null;
         var _loc1_:int = 12;
         var _loc2_:int = 20;
         var _loc3_:int = this.enemy.§package for var§;
         if(_loc3_ + _loc1_ < this.enemy.§with const static§.length - _loc2_)
         {
            _loc4_ = _loc3_ + _loc1_;
            if(_loc4_ > _loc3_)
            {
               return new Point(this.enemy.§with const static§[_loc4_].x,this.enemy.§with const static§[_loc4_].y);
            }
         }
         else if(_loc3_ - _loc1_ >= _loc2_)
         {
            _loc4_ = _loc3_ - _loc1_;
            if(_loc4_ < _loc3_)
            {
               return new Point(this.enemy.§with const static§[_loc4_].x,this.enemy.§with const static§[_loc4_].y);
            }
         }
         return new Point(this.x,this.y);
      }
      
      public function evalRangeShoot() : Boolean
      {
         var _loc1_:int = 0;
         var _loc2_:MirageArrow = null;
         if(Boolean(this.isLethal) || Boolean(this.§catch null§) || this.isFighting || this.isWalking || Boolean(this.§_-VI§))
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
               this.lifeBar.§dynamic for const§(1);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(-1);
            }
            this.§_-Rn§ = true;
            this.rangeShootChargeTimeCounter = 0;
            this.§break§(new Point(this.x,this.y),this.rangeShootPoint);
            return true;
         }
         if(this.rangeShootChargeTimeCounter < this.rangeShootChargeTime)
         {
            ++this.rangeShootChargeTimeCounter;
            if(this.rangeShootChargeTimeCounter == 5)
            {
               _loc1_ = this.getDamageRangeShoot();
               _loc2_ = new MirageArrow(1,this.rangeShootTarget,this.rangeShootPoint,null,0,false,0,0);
               _loc2_.x = this.x;
               _loc2_.y = this.y - 7;
               this.cRoot.bullets.addChild(_loc2_);
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
      
      public function §_-ax§(param1:*) : Boolean
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
      
      public function onRangeShoot(param1:*) : Boolean
      {
         var _loc2_:§dynamic const in§ = new §dynamic const in§(this.x - this.rangeShootWidth / 2,this.y - this.rangeShootHeight / 2,this.rangeShootWidth,this.rangeShootHeight);
         return _loc2_.containsPoint(new Point(param1.x,param1.y));
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§final for finally§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§default null§();
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame6() : *
      {
         gotoAndPlay("running");
      }
      
      internal function frame28() : *
      {
         stop();
      }
      
      internal function frame42() : *
      {
         stop();
      }
      
      internal function frame56() : *
      {
         stop();
      }
      
      internal function frame61() : *
      {
         stop();
      }
      
      internal function frame68() : *
      {
         stop();
      }
      
      internal function frame93() : *
      {
         stop();
      }
      
      internal function frame103() : *
      {
         stop();
      }
      
      internal function frame126() : *
      {
         stop();
      }
      
      internal function frame142() : *
      {
         stop();
      }
      
      internal function frame196() : *
      {
         stop();
      }
   }
}

