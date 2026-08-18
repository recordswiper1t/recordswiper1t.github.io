package
{
   import §_-aW§.*;
   import flash.events.Event;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol13434")]
   public class §switch for for§ extends §_-OY§
   {
      
      public function §switch for for§(param1:Point, param2:Point, param3:int, param4:int, param5:Level)
      {
         super(param3,param1,param2,param4);
         this.cRoot = param5;
         this.destX = param2.x;
         this.destY = param2.y;
         this.t1 = param4;
         this.x = param1.x;
         this.y = param1.y;
         this.level = param3;
         this.§if case§ = this.x;
         this.§if const finally§ = this.y;
      }
      
      override public function onFrameUpdate() : void
      {
         this.§_-fM§();
         super.onFrameUpdate();
      }
      
      override protected function §_-cz§() : void
      {
         var _loc1_:int = this.t0 + 1;
         var _loc2_:Number = this.§if case§ + _loc1_ * this.xSpeed;
         var _loc3_:Number = this.§if const finally§ + _loc1_ * -(this.ySpeed + this.g * _loc1_ * _loc1_ / 2);
         var _loc4_:Number = _loc2_ - this.x;
         var _loc5_:Number = _loc3_ + this.y;
         var _loc6_:Number = Math.atan2(_loc5_,_loc4_);
         this.rotation = 360 - Math.atan2(Math.sin(_loc6_),Math.cos(_loc6_)) * 180 / 3.14;
      }
      
      override protected function §_-SB§() : void
      {
         this.runInit = false;
         this.cRoot.decals.addChild(new §catch static§(new Point(destX,destY)));
         this.cRoot.decals.addChild(new §while const return§(new Point(destX,destY),this.cRoot));
         this.parent.removeChild(this);
      }
      
      override protected function init(param1:Event) : void
      {
         this.minDamage = this.cRoot.gameSettings.heroes.heroCaptain.barrelDamage[this.cRoot.game.gameHeroData.heroCaptain.skill4.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroCaptain.barrelDamage[this.cRoot.game.gameHeroData.heroCaptain.skill4.level - 1];
         this.§_-aB§ = this.cRoot.gameSettings.heroes.heroCaptain.barrelProyectileRange * 1.5 / 1.28;
         this.g = 1;
         this.t0 = 0;
         this.§const final§ = new §dynamic const in§(this.destX - this.§_-aB§ / 2,this.destY - this.§_-aB§ / 2,this.§_-aB§,this.§_-aB§);
         this.xSpeed = (this.destX - this.§if case§) / this.t1;
         this.ySpeed = (this.destY - this.§if const finally§ - this.g * this.t1 * this.t1 / 2) / this.t1;
         this.rotation = Math.random() * 100;
      }
      
      protected function §_-fM§() : void
      {
         this.§import finally§(new Point(this.x,this.y));
      }
      
      private function §import finally§(param1:Point) : void
      {
         var _loc3_:§override const return§ = null;
         var _loc2_:§override const return§ = null;
         for each(_loc3_ in this.cRoot.game.main.§function for function§)
         {
            if(!_loc3_.isActive)
            {
               _loc3_.§_-TW§(param1,this.cRoot.bulletsDecals);
               return;
            }
            if(_loc2_ == null || _loc2_.§switch return§ < _loc3_.§switch return§)
            {
               _loc2_ = _loc3_;
            }
         }
         _loc2_.§_-TW§(param1,this.cRoot.bulletsDecals);
      }
   }
}

