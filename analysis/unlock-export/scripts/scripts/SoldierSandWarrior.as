package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13650")]
   public class SoldierSandWarrior extends §_-OB§
   {
      
      protected var level:int;
      
      protected var §_-K7§:Boolean;
      
      protected var §override super§:int;
      
      protected var §_-7N§:int;
      
      protected var §package for var§:int;
      
      public function SoldierSandWarrior(param1:Point, param2:Point, param3:§_-5u§, param4:Point, param5:int, param6:int, param7:int, param8:int)
      {
         addFrameScript(0,this.frame1,22,this.frame23,63,this.frame64,74,this.frame75,93,this.frame94);
         super(param1,param2,param3,param4);
         this.level = param5;
         this.§override super§ = param6;
         this.§package for var§ = param7;
         this.§_-7N§ = param8;
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.lifes = 1;
         this.speed = 2 / 1.28;
         this.xAdjust = 5;
         this.§implements const else§ = 8;
         this.§override set§ = 4;
         this.§_-ZX§ = 22;
         this.deadTime = 50;
         this.idleTime = 30;
         this.canBePoison = false;
         this.§while for throw§ = false;
         this.maxSize = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorSize;
         this.maxLevel = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorMaxLevel;
         this.§dynamic const§ = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorRangeRally;
         this.§null for set§ = this.§dynamic const§ * this.cRoot.gameSettings.rangeRatio;
         this.regenerateHealth = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorRegen;
         this.§static while§ = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorRegenReload;
         this.armor = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorArmor;
         this.attackReloadTime = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorReload - this.§implements const else§;
         this.lifeBar = new LifeBarSmall(new Point(0,-25),this.health,this.initHealth);
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
         this.addChild(lifeBar);
         this.isActive = false;
         this.isDead = true;
         this.§_-K7§ = true;
         this.deadTimeCounter = this.deadTime - 1;
         this.§throw const for§ = true;
         this.lifeTime = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorLife + this.level * this.cRoot.gameSettings.heroes.heroAlric.sandWarriorLifeIncrement;
         this.§break package§ = 0;
         this.cRoot.§break default§(this);
         this.levelUp(this.level);
         this.gotoAndPlay("respawning");
         this.addEventListener(MouseEvent.CLICK,clickEvents,false,0,true);
      }
      
      override public function §_-dz§(param1:Object) : void
      {
         param1.sIconName = "sandwarrior";
         param1.sName = Locale.loadStringEx("HERO_SAND_WARRIOR_NAME",Locale.getDefaultLang());
         param1.sRespawn = "-";
      }
      
      override public function unPause() : void
      {
         switch(this.currentFrameLabel)
         {
            case "runningEnd":
               break;
            case "runningLoopEnd":
               this.gotoAndPlay("runningLoop");
               break;
            case "fightingEnd":
            case "respawningEnd":
            case "deadEnd":
            case "deadRunningEnd":
            case "idle":
               break;
            default:
               this.play();
         }
         this.§do const throw§();
      }
      
      public function levelUp(param1:int) : void
      {
         this.level = param1;
         this.health = this.initHealth = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorHealth[this.cRoot.game.gameHeroData.heroAlric.skill5.level - 1];
         this.minDamage = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorMinDamage + this.cRoot.gameSettings.heroes.heroAlric.sandWarriorDamageIncrement * this.level;
         this.maxDamage = this.cRoot.gameSettings.heroes.heroAlric.sandWarriorMaxDamage + this.cRoot.gameSettings.heroes.heroAlric.sandWarriorDamageIncrement * this.level;
         this.lifeBar.updateMaxHealth(this.initHealth,this.health);
         this.lifeBar.updateProgress(this.health);
      }
      
      override protected function §extends for throw§() : void
      {
         this.isCharging = false;
      }
      
      override protected function readyToRespawn() : Boolean
      {
         ++this.deadTimeCounter;
         if(this.deadTimeCounter >= this.deadTime)
         {
            if(this.lifes != 1)
            {
               this.destroyThis();
               this.cRoot.removeSoldier(this);
               return false;
            }
            this.isDead = false;
            this.doorQueed = false;
            this.isRespawning = true;
            ++this.lifes;
            return true;
         }
         return false;
      }
      
      override public function unBlock() : void
      {
         super.unBlock();
         if(this.isActive && !this.isDead)
         {
            this.gotoAndPlay("running");
         }
      }
      
      override protected function §_-xK§() : Boolean
      {
         this.§_-VA§();
         return false;
      }
      
      protected function §_-VA§() : void
      {
         if(this.enemy != null && this.enemy.isActive)
         {
            this.§_-K7§ = false;
            return;
         }
         var _loc1_:Number = this.cRoot.§_-V8§[this.§override super§][this.§_-7N§][this.§package for var§ - 1].y - this.y;
         var _loc2_:Number = this.cRoot.§_-V8§[this.§override super§][this.§_-7N§][this.§package for var§ - 1].x - this.x;
         var _loc3_:Number = Math.atan2(_loc1_,_loc2_);
         this.ySpeed = Math.sin(_loc3_) * this.speed;
         this.xSpeed = Math.cos(_loc3_) * this.speed;
         Math.atan2(this.destinationPoint.y - this.y,this.destinationPoint.x - this.x);
         this.x += this.xSpeed;
         this.y += this.ySpeed;
         this.rallyPoint = new Point(this.x,this.y);
         this.§in const while§ = new Point(this.x,this.y);
         if(Math.sqrt(Math.pow(this.cRoot.§_-V8§[this.§override super§][this.§_-7N§][this.§package for var§ - 1].y - this.y,2) + Math.pow(this.cRoot.§_-V8§[this.§override super§][this.§_-7N§][this.§package for var§ - 1].x - this.x,2)) < this.speed + 0.1)
         {
            --this.§package for var§;
            if(this.§package for var§ - 1 < 0 || this.cRoot.§_-ly§(this.§override super§,this.§package for var§))
            {
               this.isActive = false;
               this.isDead = true;
               this.isCharging = false;
               this.§break finally§ = 0;
               this.lifeBar.hide();
               this.gotoAndPlay("dead");
            }
         }
         this.evalRunningEnd();
         this.§_-K7§ = true;
      }
      
      override protected function §do else§() : Boolean
      {
         if(this.isActive)
         {
            if(this.isFighting)
            {
               if(this.enemy == null || !this.enemy.isActive || !this.enemy.isBlocked)
               {
                  this.unBlock();
                  if(!this.§_-uv§())
                  {
                     this.§default const const§();
                  }
               }
               else if(!this.isBlocking)
               {
                  this.§_-uv§();
               }
            }
            else
            {
               this.§_-uv§();
            }
         }
         if(this.§_-K7§)
         {
            return false;
         }
         if(this.§_-pf§())
         {
            return true;
         }
         var _loc1_:Number = Math.atan2(this.destinationPoint.y - this.y,this.destinationPoint.x - this.x);
         if(this.destinationPoint.x < this.x)
         {
            this.scaleX = -1;
            this.lifeBar.§dynamic for const§(-1);
         }
         else
         {
            this.scaleX = 1;
            this.lifeBar.§dynamic for const§(1);
         }
         this.x += Math.cos(_loc1_) * this.speed;
         this.y += Math.sin(_loc1_) * this.speed;
         this.evalRunningEnd();
         return false;
      }
      
      override public function §default const const§() : void
      {
         if(!this.isWalking)
         {
            this.isIdle = false;
            this.isWalking = true;
         }
         this.enemy = null;
         this.isFighting = false;
         this.isBlocking = false;
         this.isCharging = false;
      }
      
      override protected function readyToHide() : Boolean
      {
         ++this.§break package§;
         if(this.§break package§ < this.lifeTime)
         {
            return false;
         }
         this.isActive = false;
         this.isDead = true;
         this.lifeBar.hide();
         if(!this.§_-K7§)
         {
            this.gotoAndPlay("dead");
         }
         else
         {
            this.gotoAndPlay("deadRunning");
         }
         if(this.isBlocking)
         {
            this.unBlock();
         }
         return true;
      }
      
      override protected function animationRun() : void
      {
         this.gotoAndPlay("runningLoop");
      }
      
      override protected function evalRunningEnd() : void
      {
         if(this.currentFrameLabel == "runningLoopEnd")
         {
            this.gotoAndPlay("runningLoop");
         }
      }
      
      override protected function §_-n9§() : void
      {
      }
      
      override protected function §each const dynamic§() : void
      {
      }
      
      internal function frame1() : *
      {
         stop();
      }
      
      internal function frame23() : *
      {
         stop();
      }
      
      internal function frame64() : *
      {
         stop();
      }
      
      internal function frame75() : *
      {
         stop();
      }
      
      internal function frame94() : *
      {
         stop();
      }
   }
}

