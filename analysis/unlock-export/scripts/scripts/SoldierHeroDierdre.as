package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11882")]
   public class SoldierHeroDierdre extends §dynamic const class§
   {
      
      internal var §_-dN§:Object;
      
      internal var §false for function§:Boolean;
      
      internal var holyLightTime:int;
      
      internal var holyLightTimeCounter:int;
      
      internal var holyLightRange:int;
      
      internal var holyLightHeal:int;
      
      internal var holyLightHealCount:int;
      
      internal var holyLightResurrectChance:int;
      
      internal var holyLightLevel:int;
      
      internal var consecrateLevel:int;
      
      internal var consecrateRange:int;
      
      internal var consecrateTime:int;
      
      internal var consecrateTimeCounter:int;
      
      internal var isCastingConsecrate:Boolean;
      
      internal var §break const else§:int;
      
      internal var wingsOfLightBuffRange:int;
      
      internal var §false for switch§:int;
      
      internal var §do function§:Boolean;
      
      internal var §_-Y§:Object;
      
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
      
      internal var healingXpMultiplier:Number;
      
      internal var healingXpMultiplierLevel0:Number;
      
      internal var consecrateXpMultiplier:Number;
      
      public var §function const break§:Boolean;
      
      public var teleportPosition:Point;
      
      public var teleportMinRange:Number;
      
      internal const teleportInLabel:String = "tpIn";
      
      public function SoldierHeroDierdre(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(23,this.frame24,50,this.frame51,140,this.frame141);
         super(param1,param2,param3,param4,0);
         this.teleportPosition = new Point(param1.x,param1.y);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroDierdre.portrait;
         this.§implements const else§ = 23;
         this.§override set§ = 9;
         this.§_-dN§ = this.cRoot.gameSettings.heroes.heroDierdre;
         this.§dynamic const§ = this.§_-dN§.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.§_-dN§.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.§_-dN§.respawn;
         this.attackReloadTime = this.§_-dN§.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -4;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 20;
         this.levelUpSoundShoot = 5;
         this.speed = 3 / 1.28;
         this.lifes = 1;
         this.xAdjust = 5 / 1.28;
         this.idleTime = 60;
         this.teleportMinRange = 100 / 1.28;
         this.level = this.cRoot.game.gameHeroData.heroDierdre.level;
         this.xp = this.cRoot.game.gameHeroData.heroDierdre.xp;
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
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "dierdre";
         param1.sName = Locale.loadStringEx("HERO_DIERDRE_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroDierdre.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override public function unPause() : void
      {
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
         if(this.currentFrame == 153)
         {
            this.doConsecrate();
         }
         if(this.currentFrameLabel == "consecrateEnd")
         {
            this.endConsecrate();
         }
         var _loc1_:int = 199;
         if(this.currentFrame == _loc1_)
         {
            this.§native const override§();
         }
         if(this.currentFrame == _loc1_ + 11)
         {
            this.§_-m4§();
         }
         if(this.currentFrameLabel == "tpInEnd")
         {
            this.teleportEnd();
         }
         if(this.currentFrame == 233)
         {
            this.doRangedShoot();
         }
         if(this.currentFrame == 245)
         {
            this.endRangedShoot();
         }
         if(this.currentFrame == 65)
         {
            this.doHolyLigthHeal();
         }
         if(this.currentFrameLabel == "holyLightEnd")
         {
            this.endHolyLigthHeal();
         }
      }
      
      override protected function §_-wj§() : void
      {
         this.cRoot.game.gameSounds.§_-P3§();
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.§function const break§ || this.isFacehugger)
         {
            return;
         }
         super.§_-jv§(param1);
         if(this.§const for throw§(param1))
         {
            this.§true implements§();
         }
      }
      
      public function §const for throw§(param1:Point) : Boolean
      {
         return this.§else const default§() && §_-Mm§.ccpDistance(new Point(this.x,this.y),param1) > this.teleportMinRange;
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§_-P3§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§const case§();
      }
      
      override protected function levelUpWithAnimation(param1:Boolean) : void
      {
         if(param1)
         {
            super.levelUpWithAnimation(param1);
         }
         var _loc2_:Object = this.cRoot.gameSettings.heroes.heroDierdre;
         this.health = this.initHealth = _loc2_.health[this.level - 1];
         this.regenerateHealth = _loc2_.regen[this.level - 1];
         this.armor = _loc2_.armor[this.level - 1];
         this.minDamage = _loc2_.minDamage[this.level - 1];
         this.maxDamage = _loc2_.maxDamage[this.level - 1];
         this.rangeShootChargeTime = 13;
         this.rangeShootReloadTime = _loc2_.rangeShootReloadTime * this.cRoot.gameSettings.framesRate - this.rangeShootChargeTime;
         this.rangeShootWidth = _loc2_.rangeShootRangeWidth;
         this.rangeShootHeight = this.rangeShootWidth * this.cRoot.gameSettings.rangeRatio;
         this.rangeShootMinDistance = _loc2_.rangeShootMinDistance;
         this.rangeShootMinDamage = _loc2_.minRangeDamage[this.level - 1];
         this.rangeShootMaxDamage = _loc2_.maxRangeDamage[this.level - 1];
         this.xpMultiplier = _loc2_.meleeAttackXpMultiplier;
         this.rangeAttackXpMultiplier = _loc2_.rangeAttackXpMultiplier;
         this.healingXpMultiplier = _loc2_.healingXpMultiplier;
         this.healingXpMultiplierLevel0 = _loc2_.healingXpMultiplierLevel0;
         this.consecrateXpMultiplier = _loc2_.consecrateXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override protected function §_-Ew§() : void
      {
         this.§false for function§ = false;
         this.holyLightLevel = this.cRoot.game.gameHeroData.heroDierdre.skill1.level;
         var _loc1_:Object = this.§_-dN§.holyLightSkill;
         this.holyLightTimeCounter = 0;
         this.holyLightTime = _loc1_.time * this.cRoot.gameSettings.framesRate;
         this.holyLightRange = _loc1_.range;
         this.holyLightHeal = _loc1_.heal[this.holyLightLevel];
         this.holyLightHealCount = _loc1_.healCount[this.holyLightLevel];
         this.holyLightResurrectChance = _loc1_.resurrectChance[this.holyLightLevel];
      }
      
      override protected function §_-kZ§() : void
      {
         this.isCastingConsecrate = false;
         this.consecrateLevel = this.cRoot.game.gameHeroData.heroDierdre.skill2.level;
         if(this.consecrateLevel == 0)
         {
            return;
         }
         var _loc1_:Object = this.§_-dN§.consecrateSkill;
         this.consecrateRange = _loc1_.range;
         this.consecrateTime = _loc1_.time * this.cRoot.gameSettings.framesRate;
         this.consecrateTimeCounter = 0;
      }
      
      override protected function §get const default§() : void
      {
         this.§break const else§ = this.cRoot.game.gameHeroData.heroDierdre.skill3.level;
         if(this.§break const else§ == 0)
         {
            return;
         }
         this.§do function§ = true;
         this.§_-Y§ = this.§_-dN§.wingsOfLightSkill;
         this.§false for switch§ = this.§_-Y§.buffCount[this.§break const else§ - 1];
         this.wingsOfLightBuffRange = this.§_-Y§.buffRange;
      }
      
      override protected function §_-kp§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroDierdre.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.armor = this.§_-dN§.blessedArmorSkill.armor[_loc1_ - 1];
      }
      
      override protected function §_-gF§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroDierdre.skill5.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.§_-dN§.divineHealthSkill;
         var _loc3_:int = int(_loc2_.extraHealth[_loc1_ - 1]);
         this.health += _loc3_;
         this.initHealth += _loc3_;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         var _loc4_:int = int(_loc2_.regenerationFactor[_loc1_ - 1]);
         this.regenerateHealth = Math.ceil(this.initHealth * (_loc4_ / 100));
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.rangeShootReloadTimeCounter;
         ++this.holyLightTimeCounter;
         ++this.consecrateTimeCounter;
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.§function const break§)
         {
            return true;
         }
         if(!this.isCastingConsecrate && !this.§_-Rn§ && this.§_-eu§())
         {
            return true;
         }
         if(!this.§_-Rn§ && this.evalConsecrate())
         {
            return true;
         }
         if(this.evalRangeShoot())
         {
            return true;
         }
         return false;
      }
      
      public function §_-eu§() : Boolean
      {
         if(this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.§false for function§)
         {
            return true;
         }
         if(this.holyLightTimeCounter < this.holyLightTime)
         {
            return false;
         }
         if(!this.§_-Ch§(this.holyLightRange))
         {
            return false;
         }
         this.§false for function§ = true;
         this.§_-oA§();
         return true;
      }
      
      public function §_-Ch§(param1:int) : Boolean
      {
         var _loc3_:Soldier = null;
         var _loc2_:Number = this.cRoot.gameSettings.rangeRatio;
         for each(_loc3_ in this.cRoot.§_-jG§)
         {
            if(_loc3_ != this && _loc3_.§for const null§ && _loc3_.canHeal() && §_-Mm§.ellipseContains(this.x,this.y,_loc3_,param1,_loc2_))
            {
               return true;
            }
         }
         return false;
      }
      
      public function §_-oA§() : void
      {
         var _loc1_:Number = 4 / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("holyLight");
      }
      
      public function doHolyLigthHeal() : void
      {
         this.doHeal(this.holyLightHeal,this.holyLightHealCount,this.holyLightRange,this.holyLightResurrectChance);
         this.holyLightTimeCounter = 0;
         this.cRoot.game.gameSounds.§native for throw§();
      }
      
      public function endHolyLigthHeal() : void
      {
         this.§false for function§ = false;
         this.§_-Os§();
      }
      
      public function doHeal(param1:int, param2:int, param3:int, param4:int) : *
      {
         var rangeRatio:Number;
         var toHealArray:Array;
         var tmpSoldier:Soldier = null;
         var cantHealed:int = 0;
         var healValue:int = param1;
         var cantTargets:int = param2;
         var range:int = param3;
         var reviveChance:int = param4;
         if(this.holyLightLevel == 0)
         {
            this.§_-Ug§(1,this.healingXpMultiplierLevel0);
         }
         else
         {
            this.§_-Ug§(this.holyLightLevel,this.healingXpMultiplier);
         }
         rangeRatio = this.cRoot.gameSettings.rangeRatio;
         toHealArray = [];
         for each(tmpSoldier in this.cRoot.§_-jG§)
         {
            if(tmpSoldier != this && tmpSoldier.§for const null§ && (tmpSoldier.isDead || tmpSoldier.getHealth() != tmpSoldier.getInitHealth()) && §_-Mm§.ellipseContains(this.x,this.y,tmpSoldier,range,rangeRatio))
            {
               toHealArray.push(tmpSoldier);
            }
         }
         toHealArray.sort(function orderHeal(param1:Soldier, param2:Soldier):int
         {
            if(param1.isDead)
            {
               return 1;
            }
            if(param2.isDead)
            {
               return -1;
            }
            var _loc3_:int = param1.getInitHealth() - param2.getHealth();
            var _loc4_:int = param1.getInitHealth() - param2.getHealth();
            return _loc3_ < _loc4_ ? 1 : -1;
         });
         cantHealed = 0;
         for each(tmpSoldier in toHealArray)
         {
            if(tmpSoldier.isDead)
            {
               if(Math.random() < reviveChance / 100)
               {
                  if(tmpSoldier.tryToReviveWithDuration(17))
                  {
                     this.cRoot.bullets.addChild(new PriestReviveSoldierEffect(new Point(tmpSoldier.x,tmpSoldier.y),this.cRoot));
                  }
               }
            }
            else
            {
               tmpSoldier.heal(healValue);
               tmpSoldier.§_-qI§(new §_-Me§(this.cRoot,1,tmpSoldier));
               cantHealed++;
               if(cantHealed == cantTargets)
               {
                  return;
               }
            }
         }
      }
      
      public function evalConsecrate() : Boolean
      {
         if(this.consecrateLevel == 0 || this.isWalking || this.isCharging)
         {
            return false;
         }
         if(this.isCastingConsecrate)
         {
            return true;
         }
         if(this.consecrateTimeCounter < this.consecrateTime)
         {
            return false;
         }
         if(!this.canConsecrate())
         {
            return false;
         }
         this.isCastingConsecrate = true;
         this.playAnimationConsecrate();
         return true;
      }
      
      public function playAnimationConsecrate() : void
      {
         this.gotoAndPlay("consecrate");
         this.cRoot.game.gameSounds.playDierdreConsecrate();
      }
      
      public function canConsecrate() : Boolean
      {
         var _loc2_:§_-5u§ = null;
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         for each(_loc2_ in this.cRoot.towers)
         {
            if(!_loc2_.building && !_loc2_.§implements const if§ && _loc2_.§try package§ && §_-Mm§.ellipseContains(this.x,this.y,_loc2_,this.consecrateRange,_loc1_))
            {
               return true;
            }
         }
         return false;
      }
      
      public function doConsecrate() : void
      {
         var _loc5_:§_-5u§ = null;
         var _loc6_:§_-5u§ = null;
         this.§_-Ug§(this.consecrateLevel,this.consecrateXpMultiplier);
         this.consecrateTimeCounter = 0;
         var _loc1_:int = this.consecrateRange;
         var _loc2_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc3_:§_-5u§ = null;
         var _loc4_:§_-5u§ = null;
         for each(_loc5_ in this.cRoot.towers)
         {
            if(!_loc5_.building && !_loc5_.§implements const if§ && _loc5_.§try package§ && §_-Mm§.ellipseContains(this.x,this.y,_loc5_,_loc1_,_loc2_))
            {
               if(_loc5_.hasDebuff("TowerModifierHeroPriestConsecrate"))
               {
                  if(_loc3_ == null || §_-Mm§.ccpDistance(new Point(_loc3_.x,_loc3_.y),new Point(this.x,this.y)) > §_-Mm§.ccpDistance(new Point(_loc5_.x,_loc5_.y),new Point(this.x,this.y)))
                  {
                     _loc3_ = _loc5_;
                  }
               }
               else if(_loc4_ == null || §_-Mm§.ccpDistance(new Point(_loc4_.x,_loc4_.y),new Point(this.x,this.y)) > §_-Mm§.ccpDistance(new Point(_loc5_.x,_loc5_.y),new Point(this.x,this.y)))
               {
                  _loc4_ = _loc5_;
               }
            }
         }
         _loc6_ = _loc4_ != null ? _loc4_ : _loc3_;
         if(_loc6_ == null)
         {
            return;
         }
         _loc6_.§_-qI§(new TowerModifierHeroPriestConsecrate(this.cRoot,this.consecrateLevel,_loc6_));
      }
      
      public function endConsecrate() : void
      {
         this.isCastingConsecrate = false;
         this.§_-Os§();
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.§_-Rn§ = false;
         this.isCharging = false;
         this.isLevelUp = false;
         this.§false for function§ = false;
         this.isCastingConsecrate = false;
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.§_-Rn§ = false;
         this.isCharging = false;
         this.isLevelUp = false;
         this.§false for function§ = false;
         this.isCastingConsecrate = false;
      }
      
      public function §else const default§() : Boolean
      {
         return this.§do function§;
      }
      
      public function §_-tl§() : void
      {
      }
      
      override protected function runAnimationRespawn() : void
      {
         this.gotoAndPlay(this.teleportInLabel);
      }
      
      public function §true implements§() : Boolean
      {
         this.§_-m4§();
         this.lifeBar.visible = false;
         this.§extends for throw§();
         this.§function const break§ = true;
         this.gotoAndPlay("tpOut");
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
      
      override protected function §_-sB§() : void
      {
         this.§_-m4§();
      }
      
      public function §_-m4§() : void
      {
         var _loc3_:Soldier = null;
         var _loc4_:int = 0;
         var _loc6_:int = 0;
         if(this.§break const else§ == 0)
         {
            return;
         }
         var _loc1_:Number = this.cRoot.gameSettings.rangeRatio;
         var _loc2_:Array = [];
         for each(_loc3_ in this.cRoot.§_-jG§)
         {
            if(_loc3_ != this && _loc3_.isActive && §_-Mm§.ellipseContains(this.x,this.y,_loc3_,this.wingsOfLightBuffRange,_loc1_))
            {
               _loc2_.push(_loc3_);
            }
         }
         _loc4_ = 0;
         while(_loc4_ < this.§false for switch§)
         {
            if(_loc2_.length == 0)
            {
               break;
            }
            _loc6_ = §_-Mm§.getRandom(0,_loc2_.length - 1);
            _loc3_ = _loc2_[_loc6_];
            if(_loc2_.length > 0)
            {
               _loc2_.splice(_loc6_,1);
            }
            _loc3_.§_-qI§(new PriestWingsOfLightModifier(this.cRoot,this.§break const else§,_loc3_,this.§_-Y§));
            _loc4_++;
         }
         var _loc5_:PriestHealWave = new PriestHealWave(new Point(this.x,this.y),this.cRoot);
         this.cRoot.decals.addChild(_loc5_);
         if(this.§function const break§)
         {
            _loc5_.gotoAndPlay("out");
         }
         else
         {
            _loc5_.gotoAndPlay("in");
         }
         this.cRoot.game.gameSounds.§default finally§();
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
         this.§_-QQ§();
         return true;
      }
      
      public function §_-QQ§() : Boolean
      {
         this.gotoAndPlay("rangeShoot");
      }
      
      public function endRangedShoot() : void
      {
         this.§_-Rn§ = false;
         this.rangeShootReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function doRangedShoot() : void
      {
         var _loc1_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2f((this.scaleX > 0 ? -1 : 1) * 9,34));
         var _loc2_:int = this.getDamageRangeShoot();
         var _loc3_:PriestRangedAttackBolt = new PriestRangedAttackBolt(_loc1_,this.rangeShootTarget,1,0,this.rangeShootPoint);
         this.cRoot.bullets.addChild(_loc3_);
         if(_loc2_ > 0)
         {
            this.gainXpNew(_loc2_ * this.rangeAttackXpMultiplier);
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
      
      override protected function §each const dynamic§() : void
      {
         super.§each const dynamic§();
      }
      
      public function getDamageRangeShoot() : int
      {
         return this.rangeShootMinDamage + Math.ceil(Math.random() * (this.rangeShootMaxDamage - this.rangeShootMinDamage));
      }
      
      public function onRangeShoot(param1:EnemyCommon) : Boolean
      {
         return §_-Mm§.ellipseContainsWH(this.x,this.y,param1,this.rangeShootHeight,this.rangeShootWidth);
      }
      
      internal function frame24() : *
      {
         gotoAndPlay("idleLoop");
      }
      
      internal function frame51() : *
      {
         stop();
      }
      
      internal function frame141() : *
      {
         stop();
      }
   }
}

