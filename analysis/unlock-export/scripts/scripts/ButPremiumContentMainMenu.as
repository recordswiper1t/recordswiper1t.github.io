package
{
   import §_-aQ§.*;
   import flash.events.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol9745")]
   public class ButPremiumContentMainMenu extends §extends const true§
   {
      
      protected var §_-sP§:§each const each§;
      
      protected var cRoot:MainMenu;
      
      public function ButPremiumContentMainMenu(param1:MainMenu, param2:§each const each§)
      {
         super();
         addFrameScript(0,this.frame1);
         this.cRoot = param1;
         this.§_-sP§ = param2;
         this.x = -158;
         this.y = 118;
         if(this.§_-sP§.mpc)
         {
            this.gotoAndStop("idleActive");
         }
         else
         {
            this.gotoAndStop("idle");
         }
         this.addEventListener(MouseEvent.CLICK,this.click,false,0,true);
         this.addEventListener(MouseEvent.ROLL_OVER,this.rollOver,false,0,true);
         this.addEventListener(MouseEvent.ROLL_OUT,this.rollOut,false,0,true);
         this.addEventListener(MouseEvent.MOUSE_DOWN,this.mouseDown,false,0,true);
         this.addEventListener(MouseEvent.MOUSE_UP,this.mouseUp,false,0,true);
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      public function init(param1:Event) : void
      {
         this.§_-P0§();
      }
      
      protected function click(param1:MouseEvent) : void
      {
         if(!§each const each§.onlineHandler.isLoggedIn())
         {
            this.cRoot.§implements const do§.tryToLogin(true);
         }
         else
         {
            this.§each throw§();
         }
      }
      
      protected function rollOver(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.buttonMode = true;
         this.mouseChildren = false;
         this.useHandCursor = true;
         if(this.§_-sP§.mpc)
         {
            this.gotoAndStop("overActive");
         }
         else
         {
            this.gotoAndStop("over");
         }
      }
      
      protected function rollOut(param1:MouseEvent) : void
      {
         this.useHandCursor = false;
         if(this.§_-sP§.mpc)
         {
            this.gotoAndStop("idleActive");
         }
         else
         {
            this.gotoAndStop("idle");
         }
      }
      
      protected function mouseDown(param1:MouseEvent) : void
      {
         if(this.§_-sP§.mpc)
         {
            this.gotoAndStop("pressActive");
         }
         else
         {
            this.gotoAndStop("press");
         }
      }
      
      protected function mouseUp(param1:MouseEvent) : void
      {
         if(this.§_-sP§.mpc)
         {
            this.gotoAndStop("overActive");
         }
         else
         {
            this.gotoAndStop("over");
         }
      }
      
      public function §each throw§(param1:Boolean = false) : void
      {
         this.cRoot.§_-kf§();
         this.cRoot.§_-6P§ = new §_-Wl§(null,this.cRoot,param1);
         this.cRoot.addChild(this.cRoot.§_-6P§);
      }
      
      public function §_-bB§(param1:int) : void
      {
         if(param1 == 2)
         {
            this.gotoAndStop("idleActive");
         }
         else
         {
            this.gotoAndStop("idle");
         }
      }
      
      public function §_-P0§(param1:Boolean = false) : void
      {
         if(§each const each§.onlineHandler == null)
         {
            return;
         }
         if(!param1)
         {
            if(!§each const each§.onlineHandler.isLoggedIn())
            {
               this.gotoAndStop("idle");
            }
         }
      }
      
      protected function §_-q9§(param1:Object) : void
      {
         var _loc2_:int = 0;
         if(param1.success)
         {
            _loc2_ = int(param1.data);
            this.§_-bB§(_loc2_);
         }
         else
         {
            this.gotoAndStop("idle");
         }
      }
      
      public function destroyThis() : void
      {
         this.cRoot = null;
         this.§_-sP§ = null;
         this.removeEventListener(Event.ADDED_TO_STAGE,this.init);
         if(this.parent != null)
         {
            this.parent.removeChild(this);
         }
      }
      
      internal function frame1() : *
      {
         stop();
      }
   }
}

