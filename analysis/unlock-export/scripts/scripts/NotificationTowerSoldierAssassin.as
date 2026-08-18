package
{
   import flash.display.MovieClip;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11203")]
   public class NotificationTowerSoldierAssassin extends Notification
   {
      
      public var butClose:MovieClip;
      
      public function NotificationTowerSoldierAssassin(param1:Level, param2:Boolean = true)
      {
         addFrameScript(13,this.frame14,24,this.frame25);
         super(param1,param2);
      }
      
      override protected function onInit() : void
      {
         this.level.§final if§ = 6;
         this.level.unlockMaxBarracks = 6;
         this.level.game.§_-Pg§.notificationTowerSoldiersAssassin = true;
         this.level.game.§_-Pg§.notificationTowerArchersCrossbow = true;
         this.level.game.§_-Pg§.§case super§();
      }
      
      override protected function onExit() : void
      {
      }
      
      internal function frame14() : *
      {
         stop();
      }
      
      internal function frame25() : *
      {
         stop();
      }
   }
}

