package
{
   import flash.display.MovieClip;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11260")]
   public class NotificationTowerLevel2 extends Notification
   {
      
      public var butClose:MovieClip;
      
      public function NotificationTowerLevel2(param1:Level, param2:Boolean = true)
      {
         addFrameScript(16,this.frame17,28,this.frame29);
         super(param1,param2);
         this.inTime = 27;
         this.outTime = 21;
      }
      
      override protected function onInit() : void
      {
         this.level.unlockMaxMages = 2;
         this.level.§final if§ = 2;
         this.level.unlockMaxBarracks = 2;
         this.level.§var while§ = 2;
         this.level.game.§_-Pg§.notificationTowerArchersLevel2 = true;
         this.level.game.§_-Pg§.notificationTowerSoldiersLevel2 = true;
         this.level.game.§_-Pg§.notificationTowerEngineersLevel2 = true;
         this.level.game.§_-Pg§.notificationTowerMagesLevel2 = true;
         this.level.game.§_-Pg§.§case super§();
      }
      
      override protected function onExit() : void
      {
      }
      
      internal function frame17() : *
      {
         stop();
      }
      
      internal function frame29() : *
      {
         stop();
      }
   }
}

