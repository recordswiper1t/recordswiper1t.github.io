package
{
   import flash.events.*;
   import flash.geom.*;
   import flash.utils.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13542")]
   public class MirageArrow extends §extends const true§
   {
      
      public var level:int;
      
      public var isActive:Boolean = true;
      
      public var doubleDamage:Boolean;
      
      public var §_-FF§:int;
      
      public var target:Enemy;
      
      public var minDamage:int;
      
      public var maxDamage:int;
      
      public var §continue for finally§:§_-td§;
      
      public var §_-g4§:int = 11;
      
      public var §_-Ju§:int = 0;
      
      public var xSpeed:Number;
      
      public var ySpeed:Number;
      
      public var maxSpeed:Number = 20;
      
      public var destX:Number;
      
      public var destY:Number;
      
      public var §if case§:Number;
      
      public var §if const finally§:Number;
      
      public var §use const static§:Number;
      
      public var §get const return§:Number;
      
      public var §native function§:Number;
      
      public var §return const try§:Number;
      
      public var §_-qx§:Number;
      
      public var t0:Number;
      
      public var t1:Number;
      
      public var g:Number = 1;
      
      public var buffPercent:int;
      
      public var cRoot:Level;
      
      public function MirageArrow(param1:int, param2:Enemy, param3:Point = null, param4:§_-td§ = null, param5:int = 0, param6:Boolean = false, param7:int = 0, param8:int = 0)
      {
         super();
         addFrameScript(1,this.frame2,8,this.frame9);
         this.target = param2;
         this.level = param1;
         this.§continue for finally§ = param4;
         this.doubleDamage = param6;
         this.§_-FF§ = param7;
         this.buffPercent = param8;
         this.t0 = 0;
         this.t1 = 14;
         if(param5 != 0)
         {
            this.t1 = param5;
         }
         if(this.target == null)
         {
            this.destX = param3.x;
            this.destY = param3.y;
         }
         else if(this.target.§const const each§)
         {
            this.destX = this.target.x + this.target.xAdjust;
            this.destY = this.target.y + this.target.yAdjust;
         }
         else
         {
            this.destX = this.target.x + this.target.xAdjust + this.target.xSpeed * this.t1 + Math.random() * 10;
            this.destY = this.target.y + this.target.yAdjust + this.target.ySpeed * this.t1 + Math.random() * 10 - 10;
         }
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      public function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.cRoot.game.gameSounds.§finally for import§();
         this.§if case§ = this.x;
         this.§if const finally§ = this.y;
         this.xSpeed = (this.destX - this.§if case§) / this.t1;
         this.ySpeed = (this.destY - this.§if const finally§ - this.g * this.t1 * (this.t1 / 2)) / this.t1;
         this.§case for finally§();
      }
      
      public function getRandom(param1:*, param2:*) : Number
      {
         var _loc3_:Number = NaN;
         return Math.round(Math.random() * (param2 - param1)) + param1;
      }
      
      public function onFrameUpdate() : void
      {
         var _loc1_:Class = null;
         if(!this.isActive)
         {
            this.§_-PZ§();
            return;
         }
         this.moveArrow();
         if(this.target != null && this.target.isActive)
         {
            if(this.t0 + 2 >= this.t1 && this.hitTestObject(this.target))
            {
               this.x = this.target.x + this.target.xAdjust;
               this.y = this.target.y + this.target.yAdjust;
               if(this.target.§extends for use§)
               {
                  _loc1_ = getDefinitionByName(this.target.bloodClass) as Class;
                  this.cRoot.bullets.addChild(new _loc1_(new Point(this.x,this.y),this.rotation,this.cRoot));
               }
               this.target.setDamage(this.getDamage(),§_-Mm§.P_ARMOR,this.§continue for finally§,this.§_-FF§);
               if(this.doubleDamage)
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.target.x + this.target.xAdjust,this.target.y + this.target.yAdjust),"crit"));
               }
               else if(this.target != null && this.target.isDead)
               {
                  this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.target.x + this.target.xAdjust,this.target.y + this.target.yAdjust),"shunt_violet"));
               }
               this.gotoAndPlay("hit");
               this.isActive = false;
               return;
            }
         }
         if(this.t0 == this.t1)
         {
            this.sendToDecall();
            this.isActive = false;
            return;
         }
         ++this.t0;
      }
      
      public function pause() : void
      {
      }
      
      public function unPause() : void
      {
      }
      
      private function getDamage() : int
      {
         var _loc1_:int = this.minDamage + Math.ceil(Math.random() * (this.maxDamage - this.minDamage));
         if(this.doubleDamage)
         {
            return _loc1_ * 2;
         }
         return _loc1_;
      }
      
      private function §case for finally§() : void
      {
         this.minDamage = this.cRoot.gameSettings.heroes.heroMirage.minRangeDamage[this.cRoot.game.gameHeroData.heroMirage.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroMirage.maxRangeDamage[this.cRoot.game.gameHeroData.heroMirage.level - 1];
      }
      
      private function sendToDecall() : void
      {
         this.destroyThis();
      }
      
      private function moveArrow() : void
      {
         this.x = this.§if case§ + this.t0 * this.xSpeed;
         this.y = this.§if const finally§ + this.t0 * this.ySpeed + this.g * this.t0 * this.t0 / 2;
         ++this.t0;
         this.§use const static§ = this.§if const finally§ + this.t0 * this.ySpeed + this.g * this.t0 * this.t0 / 2;
         this.§get const return§ = this.§if case§ + this.t0 * this.xSpeed;
         --this.t0;
         this.§native function§ = this.§use const static§ - this.y;
         this.§return const try§ = this.§get const return§ - this.x;
         this.§_-qx§ = Math.atan2(this.§native function§,this.§return const try§);
         this.rotation = 180 - Math.atan2(-Math.sin(this.§_-qx§) * this.maxSpeed,Math.cos(this.§_-qx§) * this.maxSpeed) * 180 / Math.PI;
      }
      
      private function §_-PZ§() : void
      {
         if(this.§_-Ju§ == this.§_-g4§)
         {
            this.destroyThis();
         }
         ++this.§_-Ju§;
      }
      
      private function destroyThis() : void
      {
         this.target = null;
         this.§continue for finally§ = null;
         this.cRoot = null;
         this.removeEventListener(Event.ADDED_TO_STAGE,this.init);
         this.parent.removeChild(this);
      }
      
      internal function frame2() : *
      {
         gotoAndPlay("travel");
      }
      
      internal function frame9() : *
      {
         stop();
      }
   }
}

