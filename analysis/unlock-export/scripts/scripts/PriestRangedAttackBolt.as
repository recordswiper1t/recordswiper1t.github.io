package
{
   import flash.events.*;
   import flash.geom.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol14553")]
   public class PriestRangedAttackBolt extends §_-cy§
   {
      
      public function PriestRangedAttackBolt(param1:Point, param2:Enemy, param3:int, param4:* = 0, param5:Point = null)
      {
         addFrameScript(1,this.frame2,10,this.frame11);
         super(param1,param2,param3,param4,param5);
      }
      
      override protected function §_-OU§() : void
      {
         if(this.target != null && this.target.isDead)
         {
            this.cRoot.bullets.addChild(new §_-pZ§(new Point(this.target.x + this.target.xAdjust,this.target.y + this.target.yAdjust),"zap"));
         }
      }
      
      override protected function init(param1:Event) : void
      {
         this.cRoot = Level(this.parent.parent);
         this.cRoot.game.gameSounds.§while do§();
         this.maxAceleration = 10;
         this.§case for finally§();
         this.moveMe(false);
      }
      
      override protected function §case for finally§() : void
      {
         this.minDamage = this.cRoot.gameSettings.heroes.heroDierdre.minRangeDamage[this.cRoot.game.gameHeroData.heroDierdre.level - 1];
         this.maxDamage = this.cRoot.gameSettings.heroes.heroDierdre.maxRangeDamage[this.cRoot.game.gameHeroData.heroDierdre.level - 1];
      }
      
      internal function frame2() : *
      {
         gotoAndPlay("travel");
      }
      
      internal function frame11() : *
      {
         stop();
      }
   }
}

