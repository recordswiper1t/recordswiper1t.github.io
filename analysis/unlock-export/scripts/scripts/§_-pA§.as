package
{
   import fl.transitions.*;
   import fl.transitions.easing.*;
   import flash.display.MovieClip;
   import flash.events.*;
   import §super for super§.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol11319")]
   public class §_-pA§ extends §extends const true§
   {
      
      protected static const NORMAL:int = 0;
      
      protected static const MOVING_UP:int = 1;
      
      protected static const CLOSING:int = 2;
      
      public var §_-K4§:MovieClip;
      
      public var position:int;
      
      protected var status:int;
      
      protected var level:Level;
      
      public var pauseNotification:String;
      
      protected var ytween:Tween;
      
      protected var outTimer:int = 8;
      
      protected var outTimerCounter:int = 0;
      
      public function §_-pA§(param1:Level, param2:String)
      {
         super();
         this.status = NORMAL;
         this.level = param1;
         this.level.game.gameSounds.playGUINotificationPopup();
         this.pauseNotification = param2;
         this.§_-6H§(param2);
         this.§_-Jf§();
         this.§_-K4§.addEventListener(MouseEvent.CLICK,this.click,false,0,true);
         this.§_-K4§.addEventListener(MouseEvent.ROLL_OVER,this.rollOver,false,0,true);
         this.§_-K4§.addEventListener(MouseEvent.ROLL_OUT,this.rollOut,false,0,true);
         this.§_-K4§.addEventListener(MouseEvent.MOUSE_DOWN,this.mouseDown,false,0,true);
         this.§_-K4§.addEventListener(MouseEvent.MOUSE_UP,this.mouseUp,false,0,true);
      }
      
      public function update() : void
      {
         if(this.status == NORMAL)
         {
            return;
         }
         if(this.status == CLOSING)
         {
            if(this.outTimerCounter < this.outTimer)
            {
               ++this.outTimerCounter;
               return;
            }
            this.destroyThis();
         }
      }
      
      public function §_-6H§(param1:String) : void
      {
         param1 = §else false§.remove(param1,"Notification").toLowerCase();
         if(§else false§.beginsWith(param1,"enemy"))
         {
            this.§_-K4§.type.gotoAndStop("creep");
         }
         else if(Boolean(§else false§.beginsWith(param1,"tower")) || Boolean(§else false§.beginsWith(param1,"power")))
         {
            this.§_-K4§.type.gotoAndStop("unlock");
         }
         else if(§else false§.beginsWith(param1,"tip"))
         {
            this.§_-K4§.type.gotoAndStop("tip");
         }
         else if(§else false§.beginsWith(param1,"alert"))
         {
            this.§_-K4§.type.gotoAndStop("alert");
         }
      }
      
      public function moveTo(param1:int) : void
      {
         this.status = MOVING_UP;
         this.ytween = new Tween(this,"y",Strong.easeOut,this.y,param1,0.7,true);
         this.ytween.addEventListener(TweenEvent.MOTION_FINISH,this.moveFinish,false,0,true);
      }
      
      public function moveFinish(param1:TweenEvent) : *
      {
         this.status = NORMAL;
         --this.position;
      }
      
      public function click(param1:MouseEvent) : void
      {
         if(this.status != NORMAL)
         {
            return;
         }
         if(this.level.data.levelIndex == 0 && Level1(this.level).notificationSign != null)
         {
            Level1(this.level).notificationSign.closeMe();
         }
         this.level.§include return§.§finally const default§ = this;
         this.level.sendPauseNotification(this.pauseNotification);
      }
      
      public function close(param1:MouseEvent) : void
      {
         if(this.status != NORMAL)
         {
            return;
         }
         this.closeMe();
      }
      
      public function closeMe() : void
      {
         if(this.status != NORMAL)
         {
            return;
         }
         this.level.§include return§.removeNotification(this.position);
         this.status = CLOSING;
         this.§_-K4§.gotoAndPlay("close");
      }
      
      protected function rollOver(param1:MouseEvent) : void
      {
         this.level.game.gameSounds.playGUIMouseOverCommon();
         this.§_-K4§.buttonMode = true;
         this.§_-K4§.mouseChildren = false;
         this.§_-K4§.useHandCursor = true;
         this.§_-K4§.gotoAndStop("over");
      }
      
      protected function rollOut(param1:MouseEvent) : void
      {
         this.level.game.gameSounds.stopGUIMouseOverCommon();
         this.§_-K4§.useHandCursor = false;
         this.§_-K4§.gotoAndStop("idle");
      }
      
      protected function mouseDown(param1:MouseEvent) : void
      {
         this.§_-K4§.gotoAndStop("press");
      }
      
      protected function mouseUp(param1:MouseEvent) : void
      {
         this.§_-K4§.gotoAndStop("over");
      }
      
      protected function §_-Jf§() : void
      {
         var _loc2_:String = null;
         var _loc1_:String = §else false§.remove(this.pauseNotification.toLowerCase(),"notification").toLowerCase();
         if(§else false§.beginsWith(_loc1_,"enemy"))
         {
            _loc2_ = §_-Mm§.getEnemyString(§else false§.remove(this.pauseNotification,"Notification"));
            trace(_loc2_);
            this.§_-K4§.type.portrait.gotoAndStop(_loc2_.toLowerCase());
         }
         else if(§else false§.beginsWith(_loc1_,"tip"))
         {
            this.§_-K4§.type.portrait.gotoAndStop(§else false§.remove(this.pauseNotification.toLowerCase(),"notificationtip"));
         }
         else if(§else false§.beginsWith(_loc1_,"alert"))
         {
            this.§_-K4§.type.portrait.gotoAndStop(§else false§.remove(this.pauseNotification.toLowerCase(),"notificationalert"));
         }
      }
      
      protected function initAction(param1:String) : void
      {
         param1 = §else false§.remove(param1,"Notification").toLowerCase();
         if(§else false§.beginsWith(param1,"enemy"))
         {
            return;
         }
         switch(param1)
         {
            case "powerreinforcement":
               this.level.§finally const function§();
               break;
            case "powerfireball":
               this.level.§do for import§();
               break;
            case "towerlevel2":
               this.level.unlockMaxMages = 2;
               this.level.§final if§ = 2;
               this.level.unlockMaxBarracks = 2;
               this.level.§var while§ = 2;
               break;
            case "towerlevel3":
               this.level.unlockMaxMages = 3;
               this.level.§final if§ = 3;
               this.level.unlockMaxBarracks = 3;
               this.level.§var while§ = 3;
               break;
            case "towerarcherranger":
               this.level.§final if§ = 4;
               break;
            case "towerarchermusketeer":
               this.level.§final if§ = 5;
               break;
            case "towersoldierpaladin":
               this.level.unlockMaxBarracks = 4;
               break;
            case "towersoldierbarbarian":
               this.level.unlockMaxBarracks = 5;
               break;
            case "towermage":
               this.level.unlockMaxMages = 1;
               this.level.updateCash(100);
               break;
            case "towermagearcane":
               this.level.unlockMaxMages = 4;
               break;
            case "towermagesorcerer":
               this.level.unlockMaxMages = 5;
               break;
            case "towerengineer":
               this.level.§var while§ = 1;
               break;
            case "towerengineerbfg":
               this.level.§var while§ = 4;
               break;
            case "towerengineertesla":
               this.level.§var while§ = 5;
         }
      }
      
      protected function destroyThis() : void
      {
         this.level = null;
         this.ytween = null;
         this.§_-K4§.removeEventListener(MouseEvent.CLICK,this.click);
         this.§_-K4§.removeEventListener(MouseEvent.ROLL_OVER,this.rollOver);
         this.§_-K4§.removeEventListener(MouseEvent.ROLL_OUT,this.rollOut);
         this.§_-K4§.removeEventListener(MouseEvent.MOUSE_DOWN,this.mouseDown);
         this.§_-K4§.removeEventListener(MouseEvent.MOUSE_UP,this.mouseUp);
         this.parent.removeChild(this);
      }
   }
}

