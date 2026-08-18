package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.utils.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12926")]
   public class SoldierHeroCronan extends §dynamic const class§
   {
      
      public var regeneration:int;
      
      public var §try const class§:int;
      
      public var §_-vw§:int;
      
      public var §_-K2§:int;
      
      public var deepLashesLevel:int;
      
      public var deepLashesActive:Boolean;
      
      public var isCastingDeepLashes:Boolean;
      
      public var deepLashesDamage:int;
      
      public var deepLashesBleedDamage:int;
      
      public var deepLashesBleedDuration:int;
      
      public var deepLashesReloadTime:int;
      
      public var deepLashesReloadTimeCounter:int;
      
      public var §_-ce§:int;
      
      public var §_-sI§:Boolean;
      
      public var §true const break§:int;
      
      public var §_-52§:int;
      
      public var §catch for if§:int;
      
      public var falconerLevel:int;
      
      public var §_-jT§:*;
      
      public var falconerFalcons:int;
      
      public var falconerReloadTime:int;
      
      public var falconerReloadTimeCounter:int;
      
      public var §use for dynamic§:int;
      
      public var isCastingStampede:Boolean;
      
      public var stampedeRhinos:int;
      
      public var stampedeCastRange:int;
      
      public var §continue for package§:int;
      
      public var §_-hH§:int;
      
      public var §_-45§:int;
      
      public var §with const throw§:int;
      
      public var nodes:Array;
      
      public var boars:Array;
      
      public var falcons:Array;
      
      public var beastsAttackXpMultiplier:Number;
      
      public var deepLashesDamageXpMultiplier:Number;
      
      public var deepLashesXpMultiplier:Number;
      
      public var stampedeXpMultiplier:Number;
      
      private var referencePath:int;
      
      private var referenceNode:int;
      
      private var §default true§:Point;
      
      private var originalSpeed:Number;
      
      private var configuration:Object;
      
      public function SoldierHeroCronan(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(0,this.frame1,6,this.frame7,29,this.frame30,57,this.frame58,103,this.frame104,149,this.frame150,164,this.frame165,227,this.frame228);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroCronan.portrait;
         this.§implements const else§ = 23;
         this.§override set§ = 12;
         this.configuration = this.cRoot.gameSettings.heroes.heroCronan;
         this.§dynamic const§ = this.configuration.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.configuration.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.configuration.respawn;
         this.attackReloadTime = this.configuration.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.faceHuggerAdjust.x = 0;
         this.faceHuggerAdjust.y = -4;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 13;
         this.levelUpSoundShoot = 5;
         this.level = this.cRoot.game.gameHeroData.heroCronan.level;
         this.xp = this.cRoot.game.gameHeroData.heroCronan.xp;
         this.lifes = 1;
         this.xAdjust = 5;
         this.idleTime = 30;
         this.lifeBar = new LifeBarMedium(new Point(0,-35),this.health,this.initHealth);
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
         this.speed = 2.5 / 1.28;
         this.lifes = 1;
         this.xAdjust = 13;
         this.idleTime = 30;
         this.visible = false;
         this.falcons = [];
         this.boars = [];
         this.nodes = [];
         var _loc2_:Object = this.cRoot.§else native§(0,new Point(this.x,this.y));
         this.referenceNode = _loc2_.referenceNode;
         this.referencePath = _loc2_.referencePath;
         this.nodes = this.§_-Sf§(new Point(this.x,this.y));
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
         this.cRoot.§break default§(this);
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§_-kk§();
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "cronan";
         param1.sName = Locale.loadStringEx("HERO_CRONAN_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroCronan.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override protected function §_-wj§() : void
      {
         this.§finally var§();
         this.invokeFalcons();
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
         this.beastsAttackXpMultiplier = this.configuration.beastsAttackXpMultiplier;
         this.deepLashesXpMultiplier = this.configuration.deepLashesXpMultiplier;
         this.deepLashesDamageXpMultiplier = this.configuration.deepLashesDamageXpMultiplier;
         this.stampedeXpMultiplier = this.configuration.stampedeXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      override protected function §_-xK§() : Boolean
      {
         this.processRegenerationSkill();
         ++this.deepLashesReloadTimeCounter;
         if(this.§true const break§ > this.boars.length)
         {
            ++this.§catch for if§;
         }
         if(this.falconerFalcons > this.falcons.length)
         {
            ++this.falconerReloadTimeCounter;
         }
         ++this.§_-hH§;
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.deepLashesActive && this.evalDeepLashes())
         {
            return true;
         }
         if(this.§_-ce§ > 0 && this.§_-xz§())
         {
            return true;
         }
         if(this.§use for dynamic§ > 0 && this.evalCastStampede())
         {
            return true;
         }
         return false;
      }
      
      public function evalCastStampede() : Boolean
      {
         var _loc1_:int = 0;
         if(Boolean(this.isWalking || this.isCastingDeepLashes || this.§_-jT§) || Boolean(this.§_-sI§) || this.isCharging)
         {
            return false;
         }
         if(this.isCastingStampede)
         {
            return true;
         }
         if(this.§_-hH§ < this.§continue for package§)
         {
            return false;
         }
         if(!this.canCastStampede())
         {
            _loc1_ = 5;
            this.§_-hH§ -= _loc1_;
            return false;
         }
         this.isCastingStampede = true;
         this.startCastingStampede();
         return true;
      }
      
      public function startCastingStampede() : void
      {
         var _loc5_:Number = NaN;
         var _loc1_:Object = this.cRoot.§else native§(0,new Point(this.x,this.y));
         var _loc2_:int = int(_loc1_.pathIndex);
         var _loc3_:int = _loc1_.referenceNode - 4;
         if(!this.cRoot.§_-ly§(_loc2_,_loc3_ - 2,0))
         {
            _loc3_ -= 2;
         }
         var _loc4_:Point = this.cRoot.§_-V8§[_loc2_][0][_loc3_];
         if(this.x > _loc4_.x)
         {
            _loc5_ = -1;
         }
         else
         {
            _loc5_ = 1;
         }
         this.scaleX = _loc5_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         var _loc6_:Number = 15 / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("tarzan");
         this.cRoot.game.gameSounds.§false for import§();
      }
      
      public function castStampede() : void
      {
         var _loc5_:Boolean = false;
         var _loc6_:§do const use§ = null;
         this.§_-Ug§(this.§use for dynamic§,this.stampedeXpMultiplier);
         this.§_-hH§ = 0;
         var _loc1_:int = this.§_-45§;
         var _loc2_:int = §_-Mm§.getRandomFrom(0,3);
         var _loc3_:int = this.§with const throw§;
         var _loc4_:int = 0;
         while(_loc4_ < this.stampedeRhinos)
         {
            if(!this.cRoot.§_-ly§(_loc1_,_loc3_,0))
            {
               if(_loc4_ == 0)
               {
                  _loc5_ = true;
               }
               else
               {
                  _loc5_ = false;
               }
               _loc6_ = new §do const use§(this.cRoot,_loc1_,_loc2_,_loc3_,this.configuration.rhino,this.§use for dynamic§,_loc4_,_loc5_);
               this.cRoot.entities.addChild(_loc6_);
               _loc2_ = (_loc2_ + 1) % 3;
               _loc3_ -= 2;
            }
            _loc4_++;
         }
      }
      
      public function endCastingStampede() : void
      {
         this.isCastingStampede = false;
         this.§_-hH§ = 0;
         this.§_-Os§();
      }
      
      public function canCastStampede() : Boolean
      {
         var _loc1_:int = 5;
         var _loc2_:Object = this.§extends const super§(this.nodes,_loc1_,this.stampedeCastRange);
         this.§_-45§ = _loc2_.enemyPathIndex;
         this.§with const throw§ = _loc2_.rhinoNode;
         if(_loc2_.rhinoNode != -1 && _loc2_.enemyPathIndex != -1)
         {
            return true;
         }
         return false;
      }
      
      public function invokeFalcons() : void
      {
         var _loc2_:Number = NaN;
         var _loc3_:Number = NaN;
         var _loc4_:Point = null;
         var _loc5_:SoldierFalcon = null;
         var _loc1_:Object = this.configuration.falconerSkill;
         while(this.falcons.length < this.falconerFalcons)
         {
            _loc2_ = §_-Mm§.getRandomFrom(10,30) * §_-Mm§.getRandomSign();
            _loc3_ = -§_-Mm§.getRandomFrom(0,5) * §_-Mm§.getRandomSign();
            _loc4_ = §_-Mm§.ccpAdd(new Point(this.x,this.y - 100),new Point(_loc2_,_loc3_));
            _loc5_ = new SoldierFalcon(this,_loc4_,40,false,_loc1_,this.falconerLevel);
            this.falcons.push(_loc5_);
            this.cRoot.entities.addChild(_loc5_);
            _loc5_.scaleX = this.scaleX;
         }
      }
      
      public function §_-xz§() : Boolean
      {
         if(Boolean(this.isWalking || this.isCastingDeepLashes || this.§_-jT§) || Boolean(this.isCastingStampede) || this.isCharging)
         {
            return false;
         }
         if(this.§_-sI§)
         {
            return true;
         }
         if(this.boars.length == this.§true const break§)
         {
            return false;
         }
         if(this.§catch for if§ < this.§_-52§)
         {
            return false;
         }
         this.§_-sI§ = true;
         this.§_-Ht§();
         return true;
      }
      
      public function §_-Ht§() : void
      {
         var _loc6_:Number = NaN;
         var _loc1_:Object = this.cRoot.§else native§(0,new Point(this.x,this.y));
         var _loc2_:int = int(_loc1_.pathIndex);
         var _loc3_:int = _loc1_.referenceNode - 4;
         var _loc4_:Array = this.cRoot.§_-V8§[_loc2_][0];
         _loc3_ = this.§continue return§(_loc3_,_loc4_);
         var _loc5_:Point = this.cRoot.§_-V8§[_loc2_][0][_loc3_];
         if(this.x > _loc5_.x)
         {
            _loc6_ = -1;
         }
         else
         {
            _loc6_ = 1;
         }
         this.scaleX = _loc6_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         var _loc7_:Number = 35 / this.cRoot.gameSettings.framesRate;
         this.gotoAndPlay("call");
         this.cRoot.game.gameSounds.§return const break§();
      }
      
      public function endInvokeSummonWildBoars() : void
      {
         this.§_-sI§ = false;
         this.§catch for if§ = 0;
         this.§_-Os§();
      }
      
      public function invokeWildBoars() : void
      {
         var _loc10_:Array = null;
         var _loc11_:Point = null;
         var _loc12_:§_-Fu§ = null;
         this.§catch for if§ = 0;
         var _loc1_:Object = this.cRoot.§else native§(0,new Point(this.x,this.y));
         var _loc2_:int = int(_loc1_.pathIndex);
         var _loc3_:int = int(_loc1_.referenceNode);
         var _loc4_:Object = this.configuration.wildBoar;
         var _loc5_:int = 1;
         var _loc6_:int = _loc3_ - 4;
         var _loc7_:int = 20;
         var _loc8_:int = -2;
         var _loc9_:int = -1;
         while(this.boars.length < this.§true const break§)
         {
            _loc10_ = this.cRoot.§_-V8§[_loc2_][_loc5_];
            _loc6_ = this.§continue return§(_loc6_,_loc10_);
            _loc11_ = _loc10_[_loc6_];
            if(!this.§package const switch§(_loc11_,30 * §_-Mm§.GAME_SCALE) || _loc9_ == _loc6_)
            {
               _loc12_ = new §_-Fu§(this.cRoot,this,_loc11_,40,false,_loc4_,this.§_-ce§);
               this.boars.push(_loc12_);
               this.cRoot.entities.addChild(_loc12_);
               _loc12_.scaleX = this.scaleX;
            }
            _loc9_ = _loc6_;
            _loc6_ += _loc8_;
            _loc5_ = (_loc5_ + 1) % 3;
            if(_loc3_ - _loc6_ > _loc7_)
            {
               _loc8_ = 2;
               _loc6_ = _loc3_ + _loc8_;
            }
            if(_loc6_ - _loc3_ > _loc7_)
            {
               break;
            }
         }
      }
      
      public function §package const switch§(param1:Point, param2:Number) : Boolean
      {
         var _loc3_:§_-Fu§ = null;
         for each(_loc3_ in this.boars)
         {
            if(§_-Mm§.ccpDistance(param1,_loc3_.position) < param2)
            {
               return true;
            }
         }
         return false;
      }
      
      public function evalDeepLashes() : Boolean
      {
         if(Boolean(this.isWalking || this.§_-sI§ || this.§_-jT§) || Boolean(this.isCastingStampede) || this.isCharging)
         {
            return false;
         }
         if(this.isCastingDeepLashes)
         {
            return true;
         }
         if(this.deepLashesReloadTimeCounter < this.deepLashesReloadTime)
         {
            return false;
         }
         if(!this.isFighting)
         {
            return false;
         }
         this.isCastingDeepLashes = true;
         this.deepLashesReloadTimeCounter = 0;
         this.processDeepLashSkill();
         return true;
      }
      
      public function processDeepLashSkill() : void
      {
         this.gotoAndPlay("deepLash");
      }
      
      public function endDeepLashAnimation() : void
      {
         this.isCastingDeepLashes = false;
         this.deepLashesReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function §_-cm§() : void
      {
         this.cRoot.game.gameSounds.§_-dj§();
      }
      
      public function processDelayedDeepLash() : void
      {
         this.§_-cm§();
         var _loc1_:int = this.cRoot.gameSettings.framesRate;
         var _loc2_:int = this.deepLashesBleedDuration / this.cRoot.gameSettings.framesRate;
         var _loc3_:int = this.deepLashesBleedDamage / _loc2_;
         var _loc4_:§include function§ = null;
         if(this.enemy.§super static§)
         {
            _loc4_ = new §include function§(this.cRoot,this.deepLashesLevel,this.enemy);
         }
         this.enemy.setDamage(this.deepLashesDamage,1,_loc4_);
         this.gainXpByDamage(this.deepLashesDamage * this.deepLashesDamageXpMultiplier);
         this.§_-Ug§(this.deepLashesLevel,this.deepLashesXpMultiplier);
      }
      
      public function processRegenerationSkill() : void
      {
         var _loc1_:§_-Fu§ = null;
         if(this.regeneration <= 0)
         {
            return;
         }
         ++this.§_-K2§;
         if(this.§_-K2§ < this.§_-vw§)
         {
            return;
         }
         this.§_-K2§ = 0;
         this.heal(this.regeneration);
         for each(_loc1_ in this.boars)
         {
            _loc1_.heal(this.§try const class§);
         }
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.isCastingDeepLashes = false;
         this.§_-sI§ = false;
         this.§_-jT§ = false;
         this.isCastingStampede = false;
      }
      
      override public function §_-my§() : void
      {
         var _loc1_:SoldierFalcon = null;
         super.§_-my§();
         this.isCastingDeepLashes = false;
         this.§_-sI§ = false;
         this.§_-jT§ = false;
         this.isCastingStampede = false;
         for each(_loc1_ in this.falcons)
         {
            _loc1_.§null const final§();
         }
         this.falcons = [];
      }
      
      public function onWildBoarDied(param1:§_-Fu§) : void
      {
         this.boars.splice(this.boars.indexOf(param1),1);
      }
      
      public function onFalconDied(param1:SoldierFalcon) : void
      {
         this.falcons.splice(this.falcons.indexOf(param1),1);
      }
      
      public function onBeastPerformedDamage(param1:int) : void
      {
         this.gainXpByDamage(param1 * this.beastsAttackXpMultiplier);
      }
      
      override protected function §_-Ew§() : void
      {
         this.§catch for if§ = 0;
         this.§true const break§ = 0;
         this.§_-ce§ = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCronan.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.boarmasterSkill;
         this.§_-ce§ = _loc1_;
         this.§_-sI§ = false;
         this.§true const break§ = _loc2_.boars[_loc1_ - 1];
         this.§_-52§ = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.§catch for if§ = this.§_-52§;
      }
      
      override protected function §_-kZ§() : void
      {
         this.§_-hH§ = 0;
         this.stampedeRhinos = 0;
         this.§use for dynamic§ = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCronan.skill2.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.stampedeSkill;
         this.§use for dynamic§ = _loc1_;
         this.isCastingStampede = false;
         this.stampedeRhinos = _loc2_.rhinos[_loc1_ - 1];
         this.§continue for package§ = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.stampedeCastRange = _loc2_.range[_loc1_ - 1];
      }
      
      override protected function §get const default§() : void
      {
         this.falconerReloadTimeCounter = 0;
         this.falconerLevel = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCronan.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.falconerSkill;
         this.falconerLevel = _loc1_;
         this.§_-jT§ = false;
         this.falconerFalcons = _loc2_.falcons[_loc1_ - 1];
         this.falconerReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
      }
      
      override protected function §_-kp§() : void
      {
         this.deepLashesReloadTimeCounter = 0;
         this.deepLashesActive = false;
         this.deepLashesLevel = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCronan.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.deepLashesLevel = _loc1_;
         var _loc2_:Object = this.configuration.deeplashesSkill;
         this.deepLashesActive = true;
         this.deepLashesDamage = _loc2_.damages[_loc1_ - 1];
         this.deepLashesBleedDamage = _loc2_.bleedDamage[_loc1_ - 1];
         this.deepLashesBleedDuration = _loc2_.bleedDuration[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.deepLashesReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
      }
      
      override protected function §_-gF§() : void
      {
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroCronan.skill5.level);
         if(_loc1_ == 0)
         {
            return;
         }
         var _loc2_:Object = this.configuration.regenerationSkill;
         this.§_-K2§ = 0;
         this.regeneration = _loc2_.factor[_loc1_ - 1];
         this.§try const class§ = _loc2_.boarsFactor[_loc1_ - 1];
         this.§_-vw§ = _loc2_.cooldown[_loc1_ - 1];
      }
      
      public function §switch for catch§(param1:Point) : void
      {
         var _loc7_:§_-Fu§ = null;
         var _loc8_:Array = null;
         var _loc9_:Point = null;
         var _loc10_:Array = null;
         var _loc11_:§_-Sk§ = null;
         var _loc12_:§_-Sk§ = null;
         if(this.boars.length == 0)
         {
            return;
         }
         var _loc2_:int = 1;
         var _loc3_:int = -4;
         var _loc4_:Object = this.cRoot.§else native§(0,param1);
         var _loc5_:int = int(_loc4_.pathIndex);
         var _loc6_:int = _loc4_.referenceNode - 4;
         for each(_loc7_ in this.boars)
         {
            _loc8_ = this.cRoot.§_-V8§[_loc5_][_loc2_];
            _loc6_ = this.§continue return§(_loc6_,_loc8_);
            _loc9_ = _loc8_[_loc6_ + _loc3_];
            _loc10_ = null;
            if(_loc10_ == null)
            {
               _loc10_ = new Array();
               for each(_loc11_ in this.path)
               {
                  _loc12_ = new §_-Sk§(_loc11_.position,_loc11_.§try return§);
                  _loc10_.push(_loc12_);
               }
               _loc9_ = _loc8_[_loc6_];
            }
            _loc7_.§_-C8§(_loc9_,_loc10_);
            _loc2_ = (_loc2_ + 1) % 3;
            _loc3_ -= 2;
         }
      }
      
      internal function clone(param1:Object) : *
      {
         var _loc2_:ByteArray = new ByteArray();
         _loc2_.writeObject(param1);
         _loc2_.position = 0;
         return _loc2_.readObject();
      }
      
      public function §continue return§(param1:int, param2:Array) : int
      {
         if(param1 < 0)
         {
            return 0;
         }
         if(param1 >= param2.length)
         {
            return param2.length - 1;
         }
         return param1;
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
            case "deepLashEnd":
            case "respawningEnd":
            case "deepLashEnd":
            case "callEnd":
            case "tarzanEnd":
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
         if(this.currentFrame == 103)
         {
            this.invokeWildBoars();
            this.endInvokeSummonWildBoars();
         }
         if(this.currentFrame == 120)
         {
            this.castStampede();
         }
         if(this.currentFrameLabel == "tarzanEnd")
         {
            this.endCastingStampede();
         }
         if(this.currentFrame == 36)
         {
            this.§_-cm§();
         }
         if(this.currentFrame == 47)
         {
            this.processDelayedDeepLash();
         }
         if(this.currentFrame == 56)
         {
            this.endDeepLashAnimation();
         }
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.isFacehugger)
         {
            return;
         }
         super.§_-jv§(param1);
         this.nodes = this.§_-Sf§(param1);
         var _loc2_:Object = this.cRoot.§else native§(0,param1);
         this.referenceNode = _loc2_.referenceNode;
         this.referencePath = _loc2_.referencePath;
         this.§switch for catch§(param1);
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§_-kk§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§_-me§();
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame7() : *
      {
         gotoAndPlay("running");
      }
      
      internal function frame30() : *
      {
         stop();
      }
      
      internal function frame58() : *
      {
         stop();
      }
      
      internal function frame104() : *
      {
         stop();
      }
      
      internal function frame150() : *
      {
         stop();
      }
      
      internal function frame165() : *
      {
         stop();
      }
      
      internal function frame228() : *
      {
         stop();
      }
   }
}

