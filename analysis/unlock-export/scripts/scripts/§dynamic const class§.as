package
{
   import flash.events.*;
   import flash.geom.*;
   
   public class §dynamic const class§ extends §_-OB§
   {
      
      public var level:int;
      
      public var xp:int;
      
      protected var xpMultiplier:Number;
      
      protected var §true const override§:Number;
      
      protected var §_-p0§:Number;
      
      protected var isLevelUp:Boolean;
      
      protected var §_-L6§:int;
      
      protected var §extends null§:int;
      
      protected var levelUpSoundShoot:int;
      
      public var portrait:§_-BS§;
      
      public var §_-D§:String;
      
      public var path:Array = [];
      
      public var §_-Zq§:int;
      
      public function §dynamic const class§(param1:Point, param2:Point, param3:§_-5u§, param4:Point, param5:int = 0)
      {
         super(param1,param2,param3,param4,param5);
         this.§_-sT§ = true;
      }
      
      protected function §false switch§() : void
      {
         this.portrait = new §_-BS§(this,this.cRoot);
         this.cRoot.§_-NP§(this.portrait);
         this.cRoot.§_-rd§.addChild(this.portrait);
      }
      
      override protected function respawn() : *
      {
         this.isActive = true;
         this.isDead = false;
         this.isRespawning = false;
         this.isWalking = true;
         this.isCharging = false;
         this.isBlocking = false;
         this.isFighting = false;
         this.isIdle = false;
         this.canBeDesintegrate = false;
         this.§_-JB§ = false;
         this.isFacehugger = false;
         if(this.lifes == 2)
         {
            this.destinationPoint.x = this.rallyPoint.x;
            this.destinationPoint.y = this.rallyPoint.y;
         }
         this.health = this.initHealth;
         this.lifeBar.show();
         this.updateLifebarProgress();
         this.deadTimeCounter = 0;
         this.§_-G1§ = 0;
         this.§_-vC§();
         this.§_-wj§();
         this.animationRun();
      }
      
      override protected function readyToRespawn() : Boolean
      {
         ++this.deadTimeCounter;
         if(this.deadTimeCounter >= this.deadTime)
         {
            this.isDead = false;
            this.doorQueed = false;
            this.isRespawning = true;
            this.visible = true;
            this.runAnimationRespawn();
            this.§_-sB§();
            ++this.lifes;
            this.portrait.endLoading();
            return true;
         }
         this.portrait.updateLoading(this.deadTime,this.deadTimeCounter);
         return false;
      }
      
      protected function runAnimationRespawn() : void
      {
         this.gotoAndPlay("respawning");
      }
      
      override public function §_-jv§(param1:Point) : void
      {
         if(this.isFacehugger)
         {
            return;
         }
         this.rallyPoint = param1;
         this.§in const while§ = param1;
         if(this.isDead || this.isRespawning)
         {
            return;
         }
         this.isActive = false;
         this.unBlock();
         this.§default const const§();
         this.§extends for throw§();
         this.§_-2R§();
         this.§_-j4§();
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
      
      public function §try const case§() : void
      {
         this.cRoot.§false const with§();
         this.cRoot.freeMenues();
         this.cRoot.soldierSelection.§package const do§(this);
         this.cRoot.menu.§static const switch§(this);
         this.cRoot.§_-N0§ = new §_-pO§(this.cRoot,this);
         this.cRoot.bullets.addChild(this.cRoot.§_-N0§);
         this.portrait.§try const case§();
      }
      
      protected function §_-sB§() : void
      {
         this.cRoot.game.gameSounds.PlayHeroLevelUp();
      }
      
      protected function §_-j4§() : void
      {
      }
      
      override public function updateLifebarProgress() : void
      {
         this.lifeBar.updateProgress(this.health);
         this.portrait.updateHealth();
      }
      
      public function §_-Ug§(param1:int, param2:int) : void
      {
         this.gainXpNew(param1 * param2);
      }
      
      public function §_-Df§(param1:int, param2:Array) : Number
      {
         param1--;
         if(param2.length == 0)
         {
            return 1;
         }
         if(param1 >= param2.length)
         {
            param1 = int(param2.length - 1);
         }
         return param2[param1];
      }
      
      public function gainXpNew(param1:int, param2:Boolean = true) : *
      {
         var _loc3_:int = 0;
         var _loc4_:Array = null;
         var _loc5_:Array = null;
         var _loc6_:int = 0;
         var _loc7_:Number = NaN;
         var _loc8_:Number = NaN;
         var _loc9_:int = 0;
         if(this.isDead)
         {
            return;
         }
         if(param2)
         {
            if(this.cRoot.§_-g3§ == 0)
            {
               return;
            }
            _loc3_ = int(this.cRoot.gameSettings.heroes.heroesSavageMasterTable.common_tables.hero_stage_level[this.cRoot.game.currentLevel - 1]);
            _loc4_ = this.cRoot.gameSettings.heroes.heroesSavageMasterTable.common_tables.hero_multipliers_bottom;
            _loc5_ = this.cRoot.gameSettings.heroes.heroesSavageMasterTable.common_tables.hero_multipliers_top;
            _loc6_ = this.level - _loc3_;
            _loc7_ = 0;
            if(_loc6_ < 0)
            {
               _loc7_ = this.§_-Df§(-_loc6_,_loc4_);
            }
            else if(_loc6_ > 0)
            {
               _loc7_ = this.§_-Df§(_loc6_,_loc5_);
            }
            else
            {
               _loc7_ = 1;
            }
            _loc8_ = Number(this.cRoot.gameSettings.heroes.heroesSavageMasterTable.common_tables.hero_multiplier_per_mode[this.cRoot.game.difficulty]);
            param1 = param1 * _loc7_ * _loc8_;
         }
         this.xp += param1;
         this.cRoot.game.gameHeroData.selectedHero.xp += param1;
         this.portrait.updateXp();
         if(this.level < 10)
         {
            _loc9_ = int(this.cRoot.gameSettings.heroes.heroesSavageMasterTable.common_tables.master_xp[this.level]);
            if(this.xp >= _loc9_)
            {
               this.level += 1;
               this.cRoot.game.gameHeroData.selectedHero.level += 1;
               this.cRoot.game.gameHeroData.updateSkillPoints();
               this.cRoot.game.gameHeroData.§case super§();
               this.levelUpWithAnimation(true);
               this.portrait.updateLevel();
               this.portrait.updateXp();
               this.cRoot.game.§const for set§.§_-db§(this.cRoot);
               if(this.level == 5)
               {
                  this.cRoot.game.§const for set§.funcHeroOfTheDay(this.cRoot);
               }
               else if(this.level == 10)
               {
                  this.cRoot.game.§const for set§.§catch each§(this.cRoot);
               }
               this.gainXpNew(0);
            }
         }
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
            if(Math.random() < 0.3)
            {
               if(Math.random() > 0.5)
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.enemy.x,this.enemy.y + this.enemy.yAdjust),"pow"));
               }
               else
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.enemy.x,this.enemy.y + this.enemy.yAdjust),"sok"));
               }
            }
            _loc1_ = this.getDamage();
            this.gainXpByDamage(this.enemy.getArmorDamage(this.§_-vd§,_loc1_,0));
            this.enemy.setDamage(_loc1_,this.§_-vd§);
            if(this.enemy == null || !this.enemy.isActive)
            {
               if(this.enemy != null && this.enemy.isDead)
               {
                  this.§_-gu§(this.enemy.initHealth);
               }
               this.unBlock();
            }
         }
      }
      
      protected function gainXpByDamage(param1:int) : void
      {
         if(param1 == 0)
         {
            return;
         }
         this.gainXpNew(param1 * this.xpMultiplier);
      }
      
      protected function §_-gu§(param1:int) : void
      {
      }
      
      override protected function §_-xK§() : Boolean
      {
         if(this.isLevelUp)
         {
            this.evalLevelUp();
            return true;
         }
         return false;
      }
      
      protected function evalLevelUp() : Boolean
      {
         if(this.§extends null§ < this.§_-L6§)
         {
            ++this.§extends null§;
            return true;
         }
         this.isLevelUp = false;
         this.§extends null§ = 0;
         this.§_-Os§();
         return true;
      }
      
      protected function levelUpWithAnimation(param1:Boolean) : void
      {
         this.§extends for throw§();
         this.gotoAndPlay("respawning");
         this.isLevelUp = true;
         this.§extends null§ = 0;
         this.portrait.addChild(new §_-x8§(new Point(0,2)));
         this.cRoot.game.levelUpBtnAnim = true;
         this.cRoot.game.gameSounds.PlayHeroLevelUp();
      }
      
      override public function afterDamage() : void
      {
         this.portrait.updateHealth();
      }
      
      override public function §_-my§() : void
      {
         this.portrait.updateHealth();
         this.portrait.§native const do§();
         this.§extends for throw§();
         this.portrait.deSelect();
         this.cRoot.heroDied = true;
      }
      
      protected function applyAbilities() : void
      {
         this.§_-Ew§();
         this.§_-kZ§();
         this.§get const default§();
         this.§_-kp§();
         this.§_-gF§();
      }
      
      protected function §_-Ew§() : void
      {
      }
      
      protected function §_-kZ§() : void
      {
      }
      
      protected function §get const default§() : void
      {
      }
      
      protected function §_-kp§() : void
      {
      }
      
      protected function §_-gF§() : void
      {
      }
      
      override protected function §do else§() : Boolean
      {
         if(this.path == null || this.path.length == 0)
         {
            return super.§do else§();
         }
         if(this.§super const class§(this.path[this.§_-Zq§ - 1].getNodeRealPosition()))
         {
            --this.§_-Zq§;
            if(this.§_-Zq§ - 1 == 0)
            {
               this.path = [];
               this.path = null;
               this.§_-Zq§ = 0;
               return super.§do else§();
            }
         }
         var _loc1_:§_-Sk§ = this.path[this.§_-Zq§ - 1];
         var _loc2_:Point = _loc1_.getNodeRealPosition();
         var _loc3_:Number = Math.atan2(_loc2_.y - this.y,_loc2_.x - this.x);
         if(_loc2_.x >= this.x)
         {
            this.scaleX = 1;
            this.lifeBar.§dynamic for const§(1);
         }
         else
         {
            this.scaleX = -1;
            this.lifeBar.§dynamic for const§(-1);
         }
         this.x += Math.cos(_loc3_) * this.speed;
         this.y += Math.sin(_loc3_) * this.speed;
         this.evalRunningEnd();
         return false;
      }
      
      protected function §super const class§(param1:Point) : Boolean
      {
         if(Math.sqrt(Math.pow(param1.y - this.y,2) + Math.pow(param1.x - this.x,2)) <= this.speed)
         {
            return true;
         }
         return false;
      }
      
      protected function §_-2R§() : void
      {
         var _loc1_:§_-Sk§ = null;
         var _loc2_:§_-Sk§ = null;
         if(this.cRoot.§false const return§ == null)
         {
            this.path = null;
            this.§_-Zq§ = 0;
            return;
         }
         _loc1_ = this.cRoot.§false const return§.§super for const§.getNodeAtPosition(new Point(Math.round(this.x / 12.5),Math.round(this.y / 12.5)));
         _loc2_ = this.cRoot.§false const return§.§super for const§.getNodeAtPosition(new Point(Math.round(this.§in const while§.x / 12.5),Math.round(this.§in const while§.y / 12.5)));
         if(_loc1_ == null || _loc2_ == null)
         {
            return;
         }
         this.cRoot.§false const return§.§super for const§.§for catch§ = _loc1_;
         this.cRoot.§false const return§.§super for const§.endNode = _loc2_;
         if(this.cRoot.§false const return§.§function get§())
         {
            if(this.cRoot.§false const return§.path.length > 2)
            {
               this.path = this.cRoot.§false const return§.path;
               this.§_-Zq§ = this.path.length - 1;
            }
         }
         else
         {
            this.path = null;
            this.§_-Zq§ = 0;
         }
      }
      
      public function §extends const super§(param1:Array, param2:int, param3:int) : Object
      {
         var _loc5_:EnemyCommon = null;
         var _loc6_:int = 0;
         var _loc7_:int = 0;
         var _loc4_:Object = new Object();
         _loc4_.enemyPathIndex = -1;
         _loc4_.rhinoNode = -1;
         for each(_loc5_ in this.cRoot.enemies)
         {
            if(_loc5_.isActive && !_loc5_.isFlying && _loc5_.§dynamic const for§ && !_loc5_.§import for dynamic§)
            {
               _loc6_ = _loc5_.§false include§;
               _loc7_ = int(param1[_loc6_]);
               if(_loc7_ != -1)
               {
                  if(_loc5_.§package for var§ + param2 <= _loc7_)
                  {
                     if(_loc7_ - _loc5_.§package for var§ <= param3)
                     {
                        _loc4_.enemyPathIndex = _loc6_;
                        _loc4_.rhinoNode = _loc7_;
                        return _loc4_;
                     }
                  }
               }
            }
         }
         return _loc4_;
      }
      
      public function §_-Sf§(param1:Point) : Array
      {
         var _loc6_:Object = null;
         var _loc2_:Array = [];
         var _loc3_:Number = 30 / 1.28;
         var _loc4_:int = int(this.cRoot.§_-V8§.length);
         var _loc5_:int = 0;
         while(_loc5_ < _loc4_)
         {
            _loc2_[_loc5_] = -1;
            _loc6_ = this.cRoot.findNearestNodeToPosition(param1,_loc3_,_loc5_);
            if(!(_loc6_.node == -1 && _loc6_.subPath == -1))
            {
               _loc2_[_loc5_] = [_loc6_.node];
            }
            _loc5_++;
         }
         return _loc2_;
      }
      
      override public function §throw for false§() : void
      {
         super.§throw for false§();
         this.visible = true;
         this.gotoAndStop("deadEnd");
         this.§_-my§();
      }
      
      override public function eat() : void
      {
         super.eat();
         this.visible = true;
         this.gotoAndStop("deadEnd");
         this.§_-my§();
      }
      
      override public function plasmaDesintegrate() : void
      {
         super.plasmaDesintegrate();
         this.visible = true;
         this.gotoAndStop("deadEnd");
         this.§_-my§();
      }
      
      override public function §_-Wd§() : void
      {
      }
      
      override public function §_-jb§(param1:Point) : void
      {
         super.§_-jb§(param1);
         this.§_-my§();
      }
   }
}

