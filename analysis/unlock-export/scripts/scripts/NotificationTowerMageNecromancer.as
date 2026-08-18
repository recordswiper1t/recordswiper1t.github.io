package
{
   import flash.display.MovieClip;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11170")]
   public class NotificationTowerMageNecromancer extends Notification
   {
      
      public var butClose:MovieClip;
      
      public function NotificationTowerMageNecromancer(param1:Level, param2:Boolean = true)
      {
         addFrameScript(12,this.frame13,24,this.frame25);
         super(param1,param2);
      }
      
      override protected function onInit() : void
      {
         this.level.unlockMaxMages = 7;
         this.level.game.§_-Pg§.notificationTowerMagesNecromancer = true;
         this.level.game.§_-Pg§.§case super§();
      }
      
      override protected function onExit() : void
      {
      }
      
      internal function frame13() : *
      {
         stop();
      }
      
      internal function frame25() : *
      {
         stop();
      }
   }
}

