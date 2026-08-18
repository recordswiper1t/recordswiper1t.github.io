package
{
   import flash.display.MovieClip;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11237")]
   public class NotificationTowerLevel3 extends Notification
   {
      
      public var butClose:MovieClip;
      
      public function NotificationTowerLevel3(param1:Level, param2:Boolean = true)
      {
         addFrameScript(16,this.frame17,28,this.frame29);
         super(param1,param2);
         this.inTime = 27;
         this.outTime = 21;
      }
      
      override protected function onInit() : void
      {
         this.level.unlockMaxMages = 3;
         this.level.§final if§ = 3;
         this.level.unlockMaxBarracks = 3;
         this.level.§var while§ = 3;
         this.level.game.§_-Pg§.notificationTowerArchersLevel3 = true;
         this.level.game.§_-Pg§.notificationTowerSoldiersLevel3 = true;
         this.level.game.§_-Pg§.notificationTowerEngineersLevel3 = true;
         this.level.game.§_-Pg§.notificationTowerMagesLevel3 = true;
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

