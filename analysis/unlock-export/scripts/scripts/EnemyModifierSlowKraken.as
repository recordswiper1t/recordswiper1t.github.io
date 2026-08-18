package
{
   public class EnemyModifierSlowKraken extends §_-td§
   {
      
      private var removedSpeed:Number;
      
      public function EnemyModifierSlowKraken(param1:Level, param2:int, param3:Enemy)
      {
         super(param1,param2,param3);
         this.§_-Tb§ = true;
      }
      
      override public function init() : void
      {
         this.setProperties();
      }
      
      override public function §_-Yp§(param1:int) : void
      {
         this.level = param1;
         this.§continue else§ = 0;
      }
      
      override public function §throw with§(param1:Boolean) : void
      {
         this.target.speed += this.removedSpeed;
         this.target.nodeMarginError = this.target.speed + 0.1;
         this.destroyThis();
      }
      
      private function setProperties() : void
      {
         this.durationTime = this.cRoot.gameSettings.heroes.heroCaptain.slowDuration;
         this.removedSpeed = this.cRoot.gameSettings.heroes.heroCaptain.krakenSlowPercent[this.cRoot.game.gameHeroData.heroCaptain.skill5.level - 1] * this.target.speed / 100;
         this.target.speed -= this.removedSpeed;
         this.target.nodeMarginError = this.target.speed + 0.1;
         this.§throw for dynamic§();
         this.§continue else§ = 0;
      }
   }
}

