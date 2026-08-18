package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12403")]
   public class SoldierHeroAlric extends §dynamic const class§
   {
      
      private var referencePath:int;
      
      private var referenceNode:int;
      
      private var §default true§:Point;
      
      private var flurryLevel:int;
      
      private var isFlurry:Boolean;
      
      private var §_-4U§:Boolean;
      
      private var §include true§:Boolean;
      
      private var flurryReloadTime:int;
      
      private var flurryReloadTimeCounter:int;
      
      private var flurryStartChargeTime:int;
      
      private var flurryStartChargeTimeCounter:int;
      
      private var flurryEndChargeTime:int;
      
      private var flurryEndChargeTimeCounter:int;
      
      private var flurryAttackChargeTime:int;
      
      private var flurryAttackChargeTimeCounter:int;
      
      private var flurryAttackNumbers:int;
      
      private var flurryAttackCurrent:int;
      
      private var flurryModifier:int;
      
      private var §false continue§:int;
      
      private var sandWarriorLevel:int;
      
      private var isSandWarrior:Boolean;
      
      private var §break const while§:int;
      
      private var §_-iv§:int;
      
      private var §do const native§:int;
      
      private var sandWarriorChargeTimeCounter:int;
      
      private var sandWarriorWarriors:int;
      
      private var spikeDamage:int;
      
      private var §break const dynamic§:int;
      
      private var §throw const package§:int;
      
      private var sandWarriorCastRange:int;
      
      public var nodes:Array;
      
      public function SoldierHeroAlric(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,22,this.frame23,38,this.frame39,69,this.frame70,103,this.frame104,161,this.frame162,180,this.frame181);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.lifes = 1;
         this.speed = 2.2 / 1.28;
         this.xAdjust = 5;
         this.§implements const else§ = 16;
         this.§override set§ = 9;
         this.§_-ZX§ = 19;
         this.deadTime = this.cRoot.gameSettings.heroes.heroAlric.respawn;
         this.idleTime = 30;
         this.§_-L6§ = 19;
         this.§extends null§ = 0;
         this.levelUpSoundShoot = 5;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -4;
         this.maxSize = this.cRoot.gameSettings.heroes.heroAlric.maxSize;
         this.maxLevel = this.cRoot.gameSettings.heroes.heroAlric.maxLevel;
         this.§dynamic const§ = this.cRoot.gameSettings.heroes.heroAlric.range;
         this.§null for set§ = this.cRoot.gameSettings.heroes.heroAlric.range * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.cRoot.gameSettings.heroes.heroAlric.regenReload;
         this.sandWarriorCastRange = 40 / 1.28;
         this.attackReloadTime = this.cRoot.gameSettings.heroes.heroAlric.reload - this.§implements const else§;
         this.xpMultiplier = this.cRoot.gameSettings.heroes.heroAlric.xpMultiplier;
         this.flurryModifier = this.cRoot.gameSettings.heroes.heroAlric.flurryXpMultiplier;
         this.§false continue§ = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorXpMultiplier;
         this.lifeBar = new LifeBarMedium(new Point(0,-29),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroAlric.portrait;
         this.xp = this.cRoot.game.gameHeroData.heroAlric.xp;
         this.level = this.cRoot.game.gameHeroData.heroAlric.level;
         this.§false switch§();
         this.levelUpWithAnimation(false);
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.cRoot.§break default§(this);
         this.§_-DX§();
         this.nodes = [];
         this.nodes = this.§_-Sf§(new Point(this.x,this.y));
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "alric";
         param1.sName = Locale.loadStringEx("HERO_ALRIC_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroAlric.respawn / this.cRoot.gameSettings.framesRate + "s";
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
      
      override protected function levelUpWithAnimation(param1:Boolean) : void
      {
         if(param1)
         {
            super.levelUpWithAnimation(param1);
         }
         this.health = this.initHealth = this.cRoot.gameSettings.heroes.heroAlric.health[this.level - 1];
         this.regenerateHealth = this.cRoot.gameSettings.heroes.heroAlric.regen[this.level - 1];
         this.armor = this.cRoot.gameSettings.heroes.heroAlric.armor[this.level - 1];
         this.minDamage = this.cRoot.gameSettings.heroes.heroAlric.minDamage[this.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroAlric.maxDamage[this.level - 1];
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override protected function §_-xK§() : Boolean
      {
         if(this.flurryLevel != 0)
         {
            ++this.flurryReloadTimeCounter;
         }
         if(this.sandWarriorLevel != 0)
         {
            ++this.§_-iv§;
         }
         if(super.§_-xK§())
         {
            return true;
         }
         if(Boolean(this.isFlurry) && Boolean(this.evalFlurry()))
         {
            return true;
         }
         if(this.sandWarriorLevel != 0 && this.§_-is§())
         {
            return true;
         }
         return false;
      }
      
      override protected function §extends for throw§() : void
      {
         this.isSandWarrior = false;
         this.isFlurry = false;
         this.§_-4U§ = false;
         this.§include true§ = false;
      }
      
      override protected function §_-Vs§() : void
      {
         if(!this.isFacehugger)
         {
            if(Math.random() > 0.5)
            {
               this.gotoAndPlay("fighting");
            }
            else
            {
               this.gotoAndPlay("fighting2");
            }
         }
         this.isCharging = true;
      }
      
      override protected function §_-Ew§() : void
      {
         if(this.cRoot.game.gameHeroData.heroAlric.skill1.level == 0)
         {
            return;
         }
         this.minDamage += this.cRoot.gameSettings.heroes.heroAlric.swordsmanshipExtraDamage[this.cRoot.game.gameHeroData.heroAlric.skill1.level - 1];
         this.maxDamage += this.cRoot.gameSettings.heroes.heroAlric.swordsmanshipExtraDamage[this.cRoot.game.gameHeroData.heroAlric.skill1.level - 1];
      }
      
      override protected function §_-kZ§() : void
      {
         if(this.cRoot.game.gameHeroData.heroAlric.skill2.level == 0)
         {
            return;
         }
         this.spikeDamage += this.cRoot.gameSettings.heroes.heroAlric.spikedArmorDamage[this.cRoot.game.gameHeroData.heroAlric.skill2.level - 1];
      }
      
      override protected function §get const default§() : void
      {
         if(this.cRoot.game.gameHeroData.heroAlric.skill3.level == 0)
         {
            return;
         }
         this.health += this.cRoot.gameSettings.heroes.heroAlric.toughnessHealthPoints[this.cRoot.game.gameHeroData.heroAlric.skill3.level - 1];
         this.initHealth = this.health;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.regenerateHealth += this.cRoot.gameSettings.heroes.heroAlric.toughnessRegenPointsIncrement[this.cRoot.game.gameHeroData.heroAlric.skill3.level - 1];
      }
      
      override protected function §_-kp§() : void
      {
         this.flurryLevel = this.cRoot.game.gameHeroData.heroAlric.skill4.level;
         this.flurryReloadTime = this.cRoot.gameSettings.heroes.heroAlric.flurryCooldown;
         this.flurryReloadTimeCounter = 0;
         this.flurryEndChargeTime = 7;
         this.flurryEndChargeTimeCounter = 0;
         this.flurryAttackChargeTime = 11;
         this.flurryAttackChargeTimeCounter = 0;
         this.flurryStartChargeTime = 13;
         this.flurryStartChargeTimeCounter = 0;
         this.flurryAttackNumbers = this.cRoot.gameSettings.heroes.heroAlric.flurryTimeAttack + this.flurryLevel * this.cRoot.gameSettings.heroes.heroAlric.flurryTimeAttackIncrements;
      }
      
      override protected function §_-gF§() : void
      {
         this.sandWarriorLevel = this.cRoot.game.gameHeroData.heroAlric.skill5.level;
         this.§break const while§ = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorCooldown;
         this.§_-iv§ = 0;
         this.§do const native§ = 33;
         this.sandWarriorChargeTimeCounter = 0;
         this.sandWarriorWarriors = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorWarriors + this.sandWarriorLevel * this.cRoot.gameSettings.heroes.heroAlric.sandWarriorWarriorsIncrement;
      }
      
      override protected function readyToAttack() : Boolean
      {
         ++this.§_-NL§;
         if(this.§_-NL§ == this.attackReloadTime)
         {
            if(!(this.flurryLevel != 0 && Boolean(this.evalFlurry())))
            {
               this.§_-Vs§();
            }
            this.§_-NL§ = 0;
            return true;
         }
         return false;
      }
      
      override public function setDamage(param1:int, param2:Boolean = false) : *
      {
         if(this.isFlurry)
         {
            return;
         }
         super.setDamage(param1,param2);
      }
      
      private function evalFlurry() : Boolean
      {
         if(Boolean(this.isSandWarrior) || this.isFacehugger)
         {
            return false;
         }
         if(!this.isFlurry)
         {
            if(this.flurryReloadTimeCounter < this.flurryReloadTime)
            {
               return false;
            }
            this.isFlurry = true;
            this.§include true§ = true;
            this.§_-4U§ = false;
            this.flurryReloadTimeCounter = 0;
            this.flurryStartChargeTimeCounter = 0;
            this.flurryEndChargeTimeCounter = 0;
            this.flurryAttackChargeTimeCounter = 0;
            this.flurryAttackCurrent = 0;
            this.gotoAndPlay("flurry");
            this.§_-Ug§(this.flurryLevel,this.flurryModifier);
            return true;
         }
         if(this.§include true§)
         {
            ++this.flurryStartChargeTimeCounter;
            if(this.flurryStartChargeTimeCounter < this.flurryStartChargeTime)
            {
               return true;
            }
            this.cRoot.game.gameSounds.playAlricFlurry();
            this.§include true§ = false;
         }
         if(this.§_-4U§)
         {
            ++this.flurryEndChargeTimeCounter;
            if(this.flurryEndChargeTimeCounter < this.flurryEndChargeTime)
            {
               return true;
            }
            this.isFlurry = false;
            this.§_-4U§ = false;
            return false;
         }
         ++this.flurryAttackChargeTimeCounter;
         if(this.flurryAttackChargeTimeCounter < this.flurryAttackChargeTime)
         {
            if(this.flurryAttackChargeTimeCounter == 4 || this.flurryAttackChargeTimeCounter == 9)
            {
               if(this.enemy != null && this.enemy.isActive)
               {
                  this.enemy.setDamage(this.getDamage(),§_-Mm§.P_ARMOR,null,0,false);
               }
            }
         }
         else
         {
            this.flurryAttackCurrent += 2;
            if(this.flurryAttackCurrent == this.flurryAttackNumbers)
            {
               this.§_-4U§ = true;
            }
            else
            {
               this.gotoAndPlay("flurryLoop");
               this.flurryAttackChargeTimeCounter = 0;
               this.cRoot.game.gameSounds.playAlricFlurry();
            }
         }
         return true;
      }
      
      override public function §include for if§(param1:int) : void
      {
         var _loc2_:* = undefined;
         if(this.cRoot.game.gameHeroData.heroAlric.skill2.level != 0)
         {
            if(this.isFighting && this.enemy != null && this.enemy.isActive)
            {
               _loc2_ = Math.ceil(param1 * (this.spikeDamage / 100));
               this.enemy.setDamage(_loc2_,§_-Mm§.I_ARMOR);
               gainXpByDamage(_loc2_);
               if(!this.enemy.isActive)
               {
                  unBlock();
               }
            }
         }
      }
      
      public function canSpawnSandWarrior() : Boolean
      {
         var _loc1_:int = 0;
         var _loc2_:int = int(this.sandWarriorCastRange);
         var _loc3_:int = -1;
         var _loc4_:int = -1;
         var _loc5_:Object = this.§extends const super§(this.nodes,_loc1_,_loc2_);
         this.§break const dynamic§ = _loc5_.enemyPathIndex;
         this.§throw const package§ = _loc5_.rhinoNode;
         if(_loc5_.rhinoNode != -1 && _loc5_.enemyPathIndex != -1)
         {
            return true;
         }
         return false;
      }
      
      protected function §_-is§() : Boolean
      {
         if(this.cRoot.§_-g3§ == 0)
         {
            return false;
         }
         if(Boolean(this.isFlurry) || this.isCharging || this.isWalking)
         {
            return false;
         }
         if(!this.isSandWarrior)
         {
            if(this.§_-iv§ < this.§break const while§)
            {
               return false;
            }
            if(!this.canSpawnSandWarrior())
            {
               this.§_-iv§ -= 5;
               return false;
            }
            this.checkFacingSandWarrior();
            this.isSandWarrior = true;
            this.sandWarriorChargeTimeCounter = 0;
            this.gotoAndPlay("sandWarrior");
            return true;
         }
         if(this.sandWarriorChargeTimeCounter < this.§do const native§)
         {
            ++this.sandWarriorChargeTimeCounter;
            if(this.sandWarriorChargeTimeCounter == 10)
            {
               this.spawnSandWarrior();
               this.§_-iv§ = 0;
               this.cRoot.game.gameSounds.playAlricSandWarrior();
            }
            return true;
         }
         this.isSandWarrior = false;
         this.isCharging = false;
         this.§_-NL§ = 0;
         this.§break finally§ = 0;
         this.sandWarriorChargeTimeCounter = 0;
         this.§_-iv§ = 0;
         this.§_-Os§();
         return false;
      }
      
      public function checkFacingSandWarrior() : void
      {
         var _loc2_:int = 0;
         var _loc1_:int = 0;
         var _loc3_:int = int(this.§break const dynamic§);
         var _loc4_:int = 1;
         if(!this.cRoot.§_-ly§(_loc3_,this.§throw const package§ - 6))
         {
            if(this.cRoot.§_-V8§[_loc3_][_loc1_][this.§throw const package§ - 6].x >= this.x)
            {
               this.scaleX = 1;
               this.lifeBar.§dynamic for const§(1);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(-1);
            }
            return;
         }
         if(!this.cRoot.§_-ly§(_loc3_,this.§throw const package§ + 6))
         {
            if(this.cRoot.§_-V8§[_loc3_][_loc1_][this.§throw const package§ + 6].x >= this.x)
            {
               this.scaleX = 1;
               this.lifeBar.§dynamic for const§(1);
            }
            else
            {
               this.scaleX = -1;
               this.lifeBar.§dynamic for const§(-1);
            }
            return;
         }
      }
      
      public function spawnSandWarrior() : void
      {
         var _loc2_:int = 0;
         var _loc1_:int = 0;
         var _loc3_:int = int(this.§break const dynamic§);
         var _loc4_:int = 1;
         if(this.cRoot.§_-ly§(_loc3_,this.§throw const package§ - 6))
         {
            _loc4_ = -1;
         }
         var _loc5_:int = 0;
         while(_loc5_ < this.sandWarriorWarriors)
         {
            _loc2_ = this.§throw const package§ - §_-Mm§.getRandomFrom(3,6) * _loc4_;
            if(!this.cRoot.§_-ly§(_loc3_,_loc2_))
            {
               this.cRoot.entities.addChild(new SoldierSandWarrior(this.cRoot.§_-V8§[_loc3_][_loc1_][_loc2_],this.cRoot.§_-V8§[_loc3_][_loc1_][_loc2_],null,this.cRoot.§_-V8§[_loc3_][_loc1_][_loc2_],this.sandWarriorLevel,_loc3_,_loc2_,_loc1_));
            }
            if(++_loc1_ == 3 || _loc1_ >= this.cRoot.§_-V8§[_loc3_].length)
            {
               _loc1_ = 0;
            }
            _loc5_++;
         }
         this.§_-Ug§(this.sandWarriorLevel,this.§false continue§);
      }
      
      protected function §_-h5§() : int
      {
         var _loc1_:int = this.referenceNode - this.getRandom(3,5);
         if(_loc1_ < 0)
         {
            _loc1_ = 0;
         }
         return _loc1_;
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.isFacehugger)
         {
            return;
         }
         this.rallyPoint = param1;
         this.§in const while§ = param1;
         this.nodes = this.§_-Sf§(param1);
         if(this.isDead || this.isRespawning)
         {
            return;
         }
         this.isActive = false;
         this.unBlock();
         this.§default const const§();
         this.§extends for throw§();
         this.§_-2R§();
         this.§_-DX§();
         this.§_-j4§();
      }
      
      protected function §_-DX§() : void
      {
         var _loc4_:int = 0;
         var _loc1_:int = 0;
         var _loc2_:int = 0;
         var _loc3_:int = 0;
         while(_loc3_ < this.cRoot.§_-V8§.length)
         {
            if(this.cRoot.pathsActives[_loc3_])
            {
               _loc4_ = 0;
               while(_loc4_ < this.cRoot.§_-V8§[_loc3_][0].length)
               {
                  if(!this.cRoot.§var const override§ || !this.onTunnel(_loc3_,_loc4_))
                  {
                     _loc2_ = Math.sqrt(Math.pow(this.cRoot.§_-V8§[_loc3_][0][_loc4_].y - this.§in const while§.y,2) + Math.pow(this.cRoot.§_-V8§[_loc3_][0][_loc4_].x - this.§in const while§.x,2));
                     if(_loc2_ < 30)
                     {
                        if(_loc1_ == 0 || _loc1_ > _loc2_)
                        {
                           this.referencePath = _loc3_;
                           this.referenceNode = _loc4_;
                           _loc1_ = _loc2_;
                        }
                     }
                  }
                  _loc4_++;
               }
            }
            _loc3_++;
         }
         if(this.referenceNode != 0)
         {
            this.§default true§ = this.cRoot.§_-V8§[this.referencePath][0][this.referenceNode];
         }
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§return const implements§();
      }
      
      override public function §finally const final§() : void
      {
         this.lifeBar.updateProgress(this.health);
         this.cRoot.game.gameSounds.§null const while§();
      }
      
      override protected function §_-wj§() : void
      {
         this.cRoot.game.gameSounds.§return const implements§();
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame23() : *
      {
         stop();
      }
      
      internal function frame39() : *
      {
         stop();
      }
      
      internal function frame70() : *
      {
         stop();
      }
      
      internal function frame104() : *
      {
         stop();
      }
      
      internal function frame162() : *
      {
         stop();
      }
      
      internal function frame181() : *
      {
         stop();
      }
   }
}

