package
{
   import com.greensock.*;
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol12737")]
   public class SoldierHeroDragon extends §dynamic const class§
   {
      
      public static const DRAGON_GAME_SCALE:* = 1 / 1.28;
      
      internal var configuration:Object;
      
      internal var §_-SH§:Boolean;
      
      internal var rangeAttackMinRange:int;
      
      internal var rangeAttackMaxRange:int;
      
      internal var rangeAttackReloadTime:int;
      
      internal var rangeAttackReloadTimeCounter:int;
      
      internal var rangeAttackTarget:EnemyCommon;
      
      internal var rangeAttackTargetPosition:Point;
      
      internal var §package implements§:Boolean;
      
      internal var longRangeAttackSkillLevel:int;
      
      internal var longRangeAttackMinRange:int;
      
      internal var longRangeAttackMaxRange:int;
      
      internal var longRangeAttackReloadTime:int;
      
      internal var longRangeAttackReloadTimeCounter:int;
      
      internal var longRangeAttackTarget:EnemyCommon;
      
      internal var longRangeAttackTargetPosition:Point;
      
      internal var §_-6J§:Boolean;
      
      internal var blazingBreathSkillLevel:int;
      
      internal var blazingBreathDamage:int;
      
      internal var blazingBreathMinRange:int;
      
      internal var blazingBreathMaxRange:int;
      
      internal var blazingBreathReloadTime:int;
      
      internal var blazingBreathReloadTimeCounter:int;
      
      internal var blazingBreathTarget:EnemyCommon;
      
      internal var blazingBreathTargetPosition:Point;
      
      internal var isCastingFeast:Boolean;
      
      internal var feastSkillLevel:int;
      
      internal var feastDamage:int;
      
      internal var feastMinRange:int;
      
      internal var feastMaxRange:int;
      
      internal var feastDevoreChance:int;
      
      internal var feastBreathReloadTime:int;
      
      internal var feastBreathReloadTimeCounter:int;
      
      internal var feastTarget:EnemyCommon;
      
      internal var §extends implements§:Boolean;
      
      internal var §_-eC§:int;
      
      internal var fieryMistMinRange:int;
      
      internal var fieryMistMaxRange:int;
      
      internal var fieryMistDevoreChance:int;
      
      internal var §set import§:int;
      
      internal var §null for break§:int;
      
      internal var §_-Jl§:EnemyCommon;
      
      internal var fieryMistTargetPosition:Point;
      
      internal var §function for throw§:int;
      
      internal var §try const return§:int;
      
      internal var §_-My§:int;
      
      internal var reignofFireDamage:int;
      
      internal var reignofFireDuration:int;
      
      internal var §with throw§:int;
      
      internal var rangeAttackXpMultiplier:Number;
      
      internal var longRangeAttackXpMultiplier:Number;
      
      internal var fieryMistXpMultiplier:Number;
      
      internal var blazingBreathXpMultiplier:Number;
      
      internal var feastXpMultiplier:Number;
      
      internal var §_-dg§:Number = 0;
      
      internal var §use const override§:Number = 0;
      
      private var §_-Xv§:§switch const package§;
      
      public function SoldierHeroDragon(param1:Point, param2:Point, param3:§_-5u§, param4:Point)
      {
         addFrameScript(17,this.frame18,165,this.frame166);
         super(param1,param2,param3,param4,0);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.orderAdjustY = 200;
         this.isFlying = true;
         this.§_-sT§ = true;
         this.§_-D§ = this.cRoot.gameSettings.heroes.heroAshbite.portrait;
         this.level = this.cRoot.game.gameHeroData.heroAshbite.level;
         this.xp = this.cRoot.game.gameHeroData.heroAshbite.xp;
         this.lifeBar = new LifeBarBig(new Point(0,-150),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.§false switch§();
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.cRoot.§break default§(this);
         this.visible = false;
         this.§_-sT§ = true;
         this.§_-eb§ = false;
         this.canBePoison = false;
         this.§_-62§ = 106;
         this.configuration = this.cRoot.gameSettings.heroes.heroAshbite;
         this.§dynamic const§ = this.configuration.range;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.§static while§ = this.configuration.regenReload * this.cRoot.gameSettings.framesRate;
         this.deadTime = this.configuration.respawn;
         this.attackReloadTime = this.configuration.reload * this.cRoot.gameSettings.framesRate - this.§implements const else§;
         this.rangeAttackMinRange = this.configuration.rangedAttackSkill.minRange;
         this.rangeAttackMaxRange = this.configuration.rangedAttackSkill.maxRange;
         this.§_-L6§ = 19;
         this.§_-ZX§ = 15;
         this.levelUpSoundShoot = 5;
         this.levelUpWithAnimation(false);
         this.speed = 3;
         this.lifes = 1;
         this.xAdjust = 0;
         this.idleTime = 30 * 10;
         this.isActive = false;
         this.isDead = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.visible = false;
         this.rangeAttackReloadTime = this.configuration.rangedAttackSkill.cooldown * this.cRoot.gameSettings.framesRate;
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
         this.cRoot.§break default§(this);
         this.§_-Xv§ = new §switch const package§();
         this.cRoot.decals.addChild(this.§_-Xv§);
      }
      
      public function §_-wc§() : void
      {
         this.gotoAndPlay("dead");
      }
      
      public function §_-q2§(param1:int) : *
      {
         this.scaleX = param1;
      }
      
      public function §finally var§() : void
      {
         this.cRoot.game.gameSounds.§switch try§();
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
         this.rangeAttackXpMultiplier = this.configuration.rangeAttackXpMultiplier;
         this.longRangeAttackXpMultiplier = this.configuration.longRangeAttackXpMultiplier;
         this.fieryMistXpMultiplier = this.configuration.fieryMistXpMultiplier;
         this.blazingBreathXpMultiplier = this.configuration.blazingBreathXpMultiplier;
         this.feastXpMultiplier = this.configuration.feastXpMultiplier;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
         this.portrait.updateXp();
         this.applyAbilities();
      }
      
      public function §get const static§() : void
      {
         if(this.isCastingFeast)
         {
            return;
         }
         if(this.§_-4z§())
         {
            return;
         }
         if(this.§class for function§())
         {
            return;
         }
         if(this.§_-Yz§())
         {
            return;
         }
         if(this.§_-rG§())
         {
            return;
         }
      }
      
      override public function onFrameUpdate() : void
      {
         this.checkFrames();
         super.onFrameUpdate();
         this.§_-Xv§.x = this.x;
         this.§_-Xv§.y = this.y;
         this.§_-Xv§.visible = this.currentFrame < 162 || this.currentFrame > 170;
      }
      
      public function checkFrames() : void
      {
         if(this.currentFrame == 18)
         {
            this.§get const static§();
         }
         if(this.currentFrame == 45)
         {
            this.§_-sA§();
         }
         if(this.currentFrameLabel == "longRangeAttackEnd")
         {
            this.endCastingLongRangeAttack();
         }
         if(this.currentFrame == 128)
         {
            this.castFeast();
         }
         if(this.currentFrameLabel == "feastEnd")
         {
            this.endCastingFeast();
         }
         if(this.currentFrame == 31)
         {
            this.§while true§();
         }
         if(this.currentFrameLabel == "rangeAttackEnd")
         {
            this.endCastingRangeAttack();
         }
         if(this.§extends implements§)
         {
            switch(true)
            {
               case this.currentFrame == 68:
                  this.castFieryMist1();
                  break;
               case this.currentFrame > 68 && this.currentFrame < 89:
                  this.castFieryMist2();
            }
         }
         if(this.currentFrameLabel == "blazingBreathEnd" && this.§extends implements§)
         {
            this.endCastingFieryMist();
         }
         if(this.§_-6J§)
         {
            switch(true)
            {
               case this.currentFrame == 68:
                  this.castBlazingBreath1();
                  break;
               case this.currentFrame > 68 && this.currentFrame < 89:
                  this.castBlazingBreath2();
            }
         }
         if(this.currentFrameLabel == "blazingBreathEnd" && this.§_-6J§)
         {
            this.endCastingBlazingBreath();
         }
      }
      
      override protected function §_-xK§() : Boolean
      {
         ++this.rangeAttackReloadTimeCounter;
         ++this.longRangeAttackReloadTimeCounter;
         ++this.blazingBreathReloadTimeCounter;
         ++this.feastBreathReloadTimeCounter;
         ++this.§null for break§;
         if(super.§_-xK§())
         {
            return true;
         }
         if(this.§_-SH§ || this.§package implements§ || this.§_-6J§ || this.§extends implements§)
         {
            return true;
         }
         if(this.evalFeast())
         {
            return true;
         }
         return false;
      }
      
      public function evalFeast() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         if(this.feastSkillLevel == 0)
         {
            return false;
         }
         if(this.isWalking)
         {
            return false;
         }
         if(this.isCastingFeast)
         {
            return true;
         }
         if(this.feastBreathReloadTimeCounter < this.feastBreathReloadTime)
         {
            return false;
         }
         this.feastTarget = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            if(!_loc1_.isFlying && _loc1_.isActive && _loc1_.§dynamic const for§ && !_loc1_.isBoss && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.feastMaxRange,this.cRoot.gameSettings.rangeRatio) && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.feastMinRange,this.cRoot.gameSettings.rangeRatio))
            {
               this.feastTarget = _loc1_;
               break;
            }
         }
         if(this.feastTarget == null)
         {
            return false;
         }
         this.feastTarget.doStun();
         this.scaleX = this.x > this.feastTarget.x ? -1 : 1;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.startCastingFeast();
         TweenMax.to(this,0.5,{"x":this.feastTarget.x});
         return true;
      }
      
      public function startCastingFeast() : void
      {
         this.isCastingFeast = true;
         this.feastBreathReloadTimeCounter = 0;
         this.cRoot.bullets.addChild(new FeastSmoke(new Point(this.feastTarget.x,this.feastTarget.y),this.cRoot));
         this.gotoAndPlay("feast");
         this.cRoot.game.gameSounds.§switch try§(4);
      }
      
      public function castFeast() : void
      {
         var _loc1_:int = 0;
         var _loc2_:int = 0;
         this.§_-Ug§(this.feastSkillLevel,this.feastXpMultiplier);
         if(this.feastTarget == null)
         {
            return;
         }
         this.feastTarget.endStun();
         if(§_-Mm§.getRandomFrom(0,100) < this.feastDevoreChance)
         {
            this.§_-l§();
         }
         else
         {
            _loc1_ = this.feastTarget.predictDamage(this.feastDamage,§_-Mm§.P_ARMOR);
            _loc2_ = this.feastTarget.health - _loc1_;
            if(_loc2_ <= 0)
            {
               this.§_-l§();
            }
            else
            {
               this.feastTarget.setDamage(this.feastDamage,§_-Mm§.P_ARMOR);
            }
         }
      }
      
      public function §_-l§() : void
      {
         this.cRoot.bullets.addChild(new FeastExplo(new Point(this.feastTarget.x,this.feastTarget.y),this.cRoot));
         this.feastTarget.abduct();
      }
      
      public function endCastingFeast() : void
      {
         this.isCastingFeast = false;
         this.feastBreathReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function §_-Yz§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:int = 0;
         var _loc3_:int = 0;
         var _loc4_:Point = null;
         var _loc5_:Number = NaN;
         var _loc6_:Number = NaN;
         if(this.§_-eC§ == 0)
         {
            return false;
         }
         if(this.isWalking)
         {
            return false;
         }
         if(this.§extends implements§)
         {
            return true;
         }
         if(this.§null for break§ < this.§set import§)
         {
            return false;
         }
         this.§_-Jl§ = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            if(!_loc1_.isFlying && _loc1_.isActive && !_loc1_.isFlying && _loc1_.§dynamic const for§ && !(_loc5_ < this.fieryMistMinRange || _loc5_ > this.fieryMistMaxRange) && _loc6_ <= 80 && !_loc1_.isDead && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.fieryMistMaxRange * 2,this.cRoot.gameSettings.rangeRatio) && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.fieryMistMinRange,this.cRoot.gameSettings.rangeRatio))
            {
               _loc2_ = _loc1_.§false include§;
               _loc3_ = _loc1_.§package for var§ + _loc1_.getNodesSpeed(2);
               _loc4_ = this.cRoot.§default each§(_loc2_,0,_loc3_);
               _loc5_ = Math.abs(this.x - _loc4_.x);
               _loc6_ = Math.abs(this.y - _loc4_.y);
               this.§_-Jl§ = _loc1_;
               this.§function for throw§ = _loc2_;
               this.§try const return§ = _loc3_;
               this.fieryMistTargetPosition = _loc4_;
               break;
            }
         }
         if(this.§_-Jl§ == null)
         {
            return false;
         }
         this.scaleX = this.x > this.fieryMistTargetPosition.x ? -1 : 1;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.§case for function§();
         return true;
      }
      
      public function §case for function§() : void
      {
         this.§extends implements§ = true;
         this.§null for break§ = 0;
         this.§_-Ug§(this.§_-eC§,this.fieryMistXpMultiplier);
         this.gotoAndPlay("blazingBreath");
         this.cRoot.game.gameSounds.§_-Ub§();
      }
      
      public function castFieryMist1() : void
      {
         this.§_-ix§(this.callbackMist);
      }
      
      public function callbackMist() : void
      {
         var _loc9_:int = 0;
         var _loc10_:Point = null;
         var _loc11_:§const const catch§ = null;
         var _loc1_:int = this.§function for throw§;
         var _loc2_:int = this.§try const return§;
         var _loc3_:Object = this.configuration.mist;
         var _loc4_:int = this.§_-eC§;
         var _loc5_:int = 1;
         var _loc6_:int = 0;
         var _loc7_:int = 0;
         var _loc8_:int = 1;
         _loc9_ = 0;
         while(_loc9_ < 7)
         {
            if(!this.cRoot.§_-ly§(_loc1_,_loc2_ + _loc7_ * _loc8_))
            {
               _loc10_ = this.cRoot.§_-V8§[_loc1_][_loc6_][_loc2_ + _loc7_ * _loc8_];
               _loc10_ = §_-Mm§.ccpAdd(_loc10_,§_-Mm§.wc2f(§_-Mm§.getRandomFrom(0,8),§_-Mm§.getRandomFrom(0,8)));
               _loc11_ = new §const const catch§(this.cRoot,§_-Mm§.ccpSub(_loc10_,§_-Mm§.wc2f(0,5)),_loc3_,_loc4_,_loc9_ * 2,_loc9_ * 4);
               _loc11_.scaleX = §_-Mm§.getRandomFrom(0.9,1.1);
               _loc11_.scaleY = §_-Mm§.getRandomFrom(0.9,1.1);
               this.cRoot.entities.addChild(_loc11_);
            }
            _loc7_ += _loc5_;
            _loc6_ = (_loc6_ + 2) % 3;
            _loc9_++;
         }
         _loc8_ = -1;
         _loc7_ = 1;
         _loc6_ = 1;
         _loc9_ = 0;
         while(_loc9_ < 5)
         {
            if(!this.cRoot.§_-ly§(_loc1_,_loc2_ + _loc7_ * _loc8_))
            {
               _loc10_ = this.cRoot.§_-V8§[_loc1_][_loc6_][_loc2_ + _loc7_ * _loc8_];
               _loc10_ = §_-Mm§.ccpAdd(_loc10_,§_-Mm§.wc2f(§_-Mm§.getRandomFrom(0,8),§_-Mm§.getRandomFrom(0,8)));
               _loc11_ = new §const const catch§(this.cRoot,§_-Mm§.ccpSub(_loc10_,§_-Mm§.wc2f(0,5)),_loc3_,_loc4_,_loc9_ * 2,_loc9_ * 4);
               _loc11_.scaleX = §_-Mm§.getRandomFrom(0.9,1.1);
               _loc11_.scaleY = §_-Mm§.getRandomFrom(0.9,1.1);
               this.cRoot.entities.addChild(_loc11_);
            }
            _loc7_ += _loc5_;
            _loc6_ = (_loc6_ + 2) % 3;
            _loc9_++;
         }
      }
      
      public function castFieryMist2() : void
      {
         this.§_-ix§(null);
      }
      
      public function §_-ix§(param1:*) : void
      {
         var _loc2_:Point = new Point(this.x + this.scaleX * 35,this.y - 82);
         var _loc3_:Point = this.fieryMistTargetPosition;
         var _loc4_:§_-f1§ = new §_-f1§(_loc2_,_loc3_,param1);
         this.cRoot.bullets.addChild(_loc4_);
      }
      
      public function endCastingFieryMist() : void
      {
         this.§extends implements§ = false;
         this.§null for break§ = 0;
         this.§_-Os§();
      }
      
      public function §class for function§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:Number = NaN;
         var _loc3_:int = 0;
         var _loc4_:int = 0;
         var _loc5_:Point = null;
         var _loc6_:Number = NaN;
         var _loc7_:Number = NaN;
         if(this.blazingBreathSkillLevel == 0)
         {
            return false;
         }
         if(this.isWalking)
         {
            return false;
         }
         if(this.§_-6J§)
         {
            return true;
         }
         if(this.blazingBreathReloadTimeCounter < this.blazingBreathReloadTime)
         {
            return false;
         }
         this.blazingBreathTarget = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            if(!_loc1_.isFlying && !_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && !this.cRoot.§_-ly§(_loc1_.§false include§,_loc1_.§package for var§) && !_loc1_.isBoss && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.blazingBreathMaxRange * 2,this.cRoot.gameSettings.rangeRatio) && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.blazingBreathMinRange,this.cRoot.gameSettings.rangeRatio))
            {
               _loc3_ = _loc1_.§false include§;
               _loc4_ = _loc1_.§package for var§ + _loc1_.getNodesSpeed(2);
               _loc5_ = this.cRoot.§default each§(_loc3_,0,_loc4_);
               _loc6_ = Math.abs(this.x - _loc5_.x);
               _loc7_ = Math.abs(this.y - _loc5_.y);
               if(_loc6_ < this.blazingBreathMinRange || _loc6_ > this.blazingBreathMaxRange)
               {
                  break;
               }
               if(_loc7_ > 80 / 1.28)
               {
                  break;
               }
               this.blazingBreathTarget = _loc1_;
               this.blazingBreathTargetPosition = _loc5_;
               break;
            }
         }
         if(this.blazingBreathTarget == null)
         {
            return false;
         }
         if(this.x > this.blazingBreathTargetPosition.x)
         {
            _loc2_ = -1;
         }
         else
         {
            _loc2_ = 1;
         }
         this.scaleX = _loc2_;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.§_-N2§();
         return true;
      }
      
      public function §_-N2§() : void
      {
         this.§_-6J§ = true;
         this.blazingBreathReloadTimeCounter = 0;
         this.§_-Ug§(this.blazingBreathSkillLevel,this.blazingBreathXpMultiplier);
         this.gotoAndPlay("blazingBreath");
         this.cRoot.game.gameSounds.§_-MT§();
      }
      
      public function callbackBlazing(param1:§_-sb§) : void
      {
         var _loc2_:§_-WZ§ = new §_-WZ§(this.cRoot,§_-Mm§.ccpSub(new Point(param1.x,param1.y),§_-Mm§.wc2f(0,30)),this.blazingBreathDamage,20,null);
         this.cRoot.entities.addChild(_loc2_);
      }
      
      public function castBlazingBreath1() : void
      {
         var _loc1_:int = this.blazingBreathDamage;
         var _loc2_:int = this.§_-My§;
         this.§_-AB§(this.callbackBlazing);
      }
      
      public function castBlazingBreath2() : void
      {
         this.§_-AB§(null);
      }
      
      public function §_-AB§(param1:*) : void
      {
         var _loc2_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2fDragon(40 * this.scaleX,310 - 210));
         var _loc3_:Point = this.blazingBreathTargetPosition;
         var _loc4_:§_-sb§ = new §_-sb§(this.cRoot,_loc2_,_loc3_,this.blazingBreathDamage,param1);
         this.cRoot.bullets.addChild(_loc4_);
      }
      
      public function endCastingBlazingBreath() : void
      {
         this.§_-6J§ = false;
         this.blazingBreathReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function §_-4z§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:Number = NaN;
         if(this.longRangeAttackSkillLevel == 0)
         {
            return false;
         }
         if(this.isWalking)
         {
            return false;
         }
         if(this.§package implements§)
         {
            return true;
         }
         if(this.longRangeAttackReloadTimeCounter < this.longRangeAttackReloadTime)
         {
            return false;
         }
         this.longRangeAttackTarget = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            if(!_loc1_.isFlying && _loc1_.isActive && !_loc1_.isFlying && _loc1_.§dynamic const for§ && !this.cRoot.§_-ly§(_loc1_.§false include§,_loc1_.§package for var§) && !_loc1_.isDead && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.longRangeAttackMaxRange,this.cRoot.gameSettings.rangeRatio) && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.longRangeAttackMinRange,this.cRoot.gameSettings.rangeRatio))
            {
               this.longRangeAttackTarget = _loc1_;
               this.longRangeAttackTargetPosition = new Point(_loc1_.x,_loc1_.y);
               break;
            }
         }
         if(this.longRangeAttackTarget == null)
         {
            return false;
         }
         this.scaleX = this.x > this.longRangeAttackTargetPosition.x ? -1 : 1;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.§final for for§();
         return true;
      }
      
      public function §final for for§() : void
      {
         this.§package implements§ = true;
         this.longRangeAttackReloadTimeCounter = 0;
         this.gotoAndPlay("longRangeAttack");
         this.cRoot.game.gameSounds.§_-1h§();
      }
      
      public function §_-sA§() : void
      {
         this.§_-Ug§(this.longRangeAttackSkillLevel,this.longRangeAttackXpMultiplier);
         if(this.longRangeAttackTarget != null)
         {
            this.longRangeAttackTargetPosition = new Point(this.longRangeAttackTarget.x,this.longRangeAttackTarget.y);
         }
         var _loc1_:Point = §_-Mm§.wc2fDragon(35 * (this.scaleX > 0 ? 1 : -1),310 - 120);
         var _loc2_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),_loc1_);
         var _loc3_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),§_-Mm§.wc2fDragon(35 * (this.scaleX > 0 ? -1 : 1),310 - 130));
         var _loc4_:Point = this.longRangeAttackTargetPosition;
         var _loc5_:§function const use§ = new §function const use§(_loc2_,_loc3_,_loc4_,this.configuration.longRangedAttackProjectile,this.longRangeAttackSkillLevel,null);
         this.cRoot.bullets.addChild(_loc5_);
      }
      
      public function endCastingLongRangeAttack() : void
      {
         this.§package implements§ = false;
         this.longRangeAttackReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      public function §_-rG§() : Boolean
      {
         var _loc1_:EnemyCommon = null;
         var _loc2_:int = 0;
         var _loc3_:Point = null;
         if(this.isWalking)
         {
            return false;
         }
         if(this.§_-SH§)
         {
            return true;
         }
         if(this.rangeAttackReloadTimeCounter < this.rangeAttackReloadTime)
         {
            return false;
         }
         this.rangeAttackTarget = null;
         for each(_loc1_ in this.cRoot.enemies)
         {
            _loc2_ = _loc1_.§package for var§ + _loc1_.getNodesSpeed(1);
            _loc3_ = _loc1_.§with const static§[_loc2_];
            if(!_loc1_.isDead && _loc1_.isActive && _loc1_.§dynamic const for§ && Math.abs(_loc3_.x - this.x) >= 55 * DRAGON_GAME_SCALE && §_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.rangeAttackMaxRange,this.cRoot.gameSettings.rangeRatio) && !§_-Mm§.ellipseContains(this.x,this.y,_loc1_,this.rangeAttackMinRange,this.cRoot.gameSettings.rangeRatio))
            {
               this.rangeAttackTarget = _loc1_;
               this.rangeAttackTargetPosition = _loc3_;
               break;
            }
         }
         if(this.rangeAttackTarget == null)
         {
            return false;
         }
         this.scaleX = this.x > this.rangeAttackTargetPosition.x ? -1 : 1;
         this.lifeBar.§dynamic for const§(this.scaleX);
         this.§extends for var§();
         return true;
      }
      
      public function §extends for var§() : void
      {
         this.§_-SH§ = true;
         this.rangeAttackReloadTimeCounter = 0;
         this.gotoAndPlay("rangeAttack");
         this.cRoot.game.gameSounds.§_-23§();
      }
      
      public function §while true§() : void
      {
         var _loc7_:EnemyCommon = null;
         var _loc8_:int = 0;
         var _loc9_:Point = null;
         var _loc1_:Number = 0;
         if(this.rangeAttackTarget != null && !this.rangeAttackTarget.isDead)
         {
            _loc7_ = this.rangeAttackTarget;
            _loc8_ = _loc7_.§package for var§ + _loc7_.getNodesSpeed(2);
            _loc9_ = _loc7_.§with const static§[_loc8_];
            this.rangeAttackTargetPosition = _loc9_;
            if(_loc7_.isFlying)
            {
               _loc1_ = _loc7_.yAdjust + 7;
            }
         }
         var _loc2_:Point = §_-Mm§.wc2fDragon(45 * (this.scaleX > 0 ? 1 : -1),0);
         var _loc3_:Point = §_-Mm§.ccpAdd(new Point(this.x,this.y),_loc2_);
         var _loc4_:Point = this.rangeAttackTargetPosition;
         var _loc5_:int = §_-Mm§.getRandomFrom(this.minDamage,this.maxDamage);
         this.gainXpNew(this.rangeAttackXpMultiplier * _loc5_);
         var _loc6_:Function = null;
         this.addChild(new §for break§(new Point(42,-82),this.cRoot));
         this.cRoot.bullets.addChild(new §dynamic else§(this.cRoot,_loc3_,(310 - 198) * DRAGON_GAME_SCALE * -1,_loc4_,_loc1_,_loc5_,this.configuration.rangedAttackProjectile));
      }
      
      public function endCastingRangeAttack() : void
      {
         this.§_-SH§ = false;
         this.rangeAttackReloadTimeCounter = 0;
         this.§_-Os§();
      }
      
      override protected function §_-sB§() : void
      {
         this.cRoot.game.gameSounds.playDragonAwaken();
      }
      
      public function §_-w6§() : Boolean
      {
         return false;
      }
      
      override protected function §_-Ew§() : void
      {
         this.blazingBreathSkillLevel = 0;
         this.blazingBreathReloadTimeCounter = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroAshbite.skill1.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.blazingBreathSkillLevel = _loc1_;
         var _loc2_:Object = this.configuration.blazingBreathSkill;
         this.§_-6J§ = false;
         this.blazingBreathMinRange = _loc2_.minRange[_loc1_ - 1];
         this.blazingBreathMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.blazingBreathReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.blazingBreathDamage = _loc2_.damage[_loc1_ - 1];
      }
      
      override protected function §_-kZ§() : void
      {
         this.feastSkillLevel = 0;
         this.feastBreathReloadTimeCounter = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroAshbite.skill2.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.feastSkillLevel = _loc1_;
         var _loc2_:Object = this.configuration.feastSkill;
         this.isCastingFeast = false;
         this.feastMinRange = _loc2_.minRange[_loc1_ - 1];
         this.feastMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.feastBreathReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
         this.feastDamage = _loc2_.damage[_loc1_ - 1];
         this.feastDevoreChance = _loc2_.devoreChance[_loc1_ - 1];
      }
      
      override protected function §get const default§() : void
      {
         this.§_-eC§ = 0;
         this.§null for break§ = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroAshbite.skill3.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§_-eC§ = _loc1_;
         var _loc2_:Object = this.configuration.fieryMistSkill;
         this.§_-6J§ = false;
         this.fieryMistMinRange = _loc2_.minRange[_loc1_ - 1];
         this.fieryMistMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.§set import§ = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
      }
      
      override protected function §_-kp§() : void
      {
         this.longRangeAttackSkillLevel = 0;
         this.longRangeAttackReloadTimeCounter = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroAshbite.skill4.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.longRangeAttackSkillLevel = _loc1_;
         var _loc2_:Object = this.configuration.wildfireBarrage;
         this.§package implements§ = false;
         this.longRangeAttackMinRange = _loc2_.minRange[_loc1_ - 1];
         this.longRangeAttackMaxRange = _loc2_.maxRange[_loc1_ - 1];
         this.longRangeAttackReloadTime = _loc2_.cooldown[_loc1_ - 1] * this.cRoot.gameSettings.framesRate;
      }
      
      override protected function §_-gF§() : void
      {
         this.§_-My§ = 0;
         var _loc1_:int = int(this.cRoot.game.gameHeroData.heroAshbite.skill5.level);
         if(_loc1_ == 0)
         {
            return;
         }
         this.§_-My§ = _loc1_;
         var _loc2_:Object = this.configuration.reignOfFireSkill;
         this.reignofFireDamage = _loc2_.damage[_loc1_ - 1];
         this.reignofFireDuration = _loc2_.duration[_loc1_ - 1];
         this.§with throw§ = _loc2_.damageReloadTime[_loc1_ - 1];
         this.reignofFireDamage = this.reignofFireDamage * this.§with throw§ / this.reignofFireDuration;
      }
      
      override protected function §_-2R§() : void
      {
      }
      
      override protected function §do else§() : Boolean
      {
         super.§do else§();
      }
      
      override protected function §each const dynamic§() : void
      {
         if(this.currentFrame > 0 && this.currentFrame < 19)
         {
            return;
         }
         this.gotoAndStop("idle");
      }
      
      override protected function animationRun() : void
      {
         if(this.currentFrame > 0 && this.currentFrame < 19)
         {
            return;
         }
         this.gotoAndStop("idle");
      }
      
      override public function §_-my§() : void
      {
         super.§_-my§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.§_-SH§ = false;
         this.§package implements§ = false;
         this.§_-6J§ = false;
         this.isCastingFeast = false;
         this.§extends implements§ = false;
         if(this.feastTarget != null)
         {
            this.feastTarget.isDead = false;
            this.feastTarget.isActive = true;
            this.feastTarget = null;
         }
      }
      
      override protected function §extends for throw§() : void
      {
         super.§extends for throw§();
         this.isCharging = false;
         this.isLevelUp = false;
         this.§_-SH§ = false;
         this.§package implements§ = false;
         this.§_-6J§ = false;
         this.isCastingFeast = false;
         this.§extends implements§ = false;
         if(this.feastTarget != null)
         {
            this.feastTarget.isDead = false;
            this.feastTarget.isActive = true;
            this.feastTarget = null;
         }
      }
      
      override protected function §_-uv§() : Boolean
      {
         return false;
      }
      
      override protected function §_-j4§() : void
      {
         this.cRoot.game.gameSounds.§switch try§();
      }
      
      override public function §finally const final§() : void
      {
         this.cRoot.game.gameSounds.§_-Tn§();
      }
      
      override public function pause() : void
      {
         super.pause();
         TweenMax.pauseAll();
      }
      
      override public function unPause() : void
      {
         TweenMax.resumeAll();
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
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "ashbite";
         param1.sName = Locale.loadStringEx("HERO_ASHBITE_NAME",Locale.getDefaultLang());
         param1.sRespawn = this.cRoot.gameSettings.heroes.heroAshbite.respawn / this.cRoot.gameSettings.framesRate + "s";
      }
      
      override public function destroyThis() : void
      {
         this.§_-Xv§.destroyThis();
         super.destroyThis();
      }
      
      internal function frame18() : *
      {
         gotoAndPlay("idleLoop");
      }
      
      internal function frame166() : *
      {
         stop();
      }
   }
}

