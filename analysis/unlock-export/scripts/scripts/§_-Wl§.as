package
{
   import §_-aQ§.*;
   import fl.transitions.*;
   import fl.transitions.easing.*;
   import flash.events.*;
   import flash.net.*;
   
   public class §_-Wl§ extends §extends const true§
   {
      
      private var yTween:Tween;
      
      private var alphaTween:Tween;
      
      private var mainMenu:MainMenu;
      
      private var game:§_-BQ§;
      
      public function §_-Wl§(param1:§_-BQ§, param2:MainMenu = null, param3:Boolean = false)
      {
         super();
         this.x = 355;
         this.y = 58;
         this.game = param1;
         this.mainMenu = param2;
         if(this.game != null)
         {
            this.game.gameSounds.playGUIButtonCommon();
            if(this.game.§_-yX§)
            {
               this.setInitLoggedOut();
            }
            else
            {
               this.§for for function§("promo");
            }
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_button_common");
            §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
            if(!param3)
            {
               if(!§each const each§(this.mainMenu.parent).mpc)
               {
                  this.setInitLoggedOut();
               }
               else
               {
                  this.§for for function§("success");
               }
            }
            else
            {
               this.gotoAndStop("loading");
            }
         }
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      public function updatePC(param1:Boolean) : void
      {
         if(!param1)
         {
            this.setInitLoggedOut();
         }
         else
         {
            this.§for for function§("success");
         }
      }
      
      public function init(param1:Event) : void
      {
         this.yTween = new Tween(this,"y",Strong.easeOut,this.y - 50,this.y,0.7,true);
         this.alphaTween = new Tween(this,"alpha",Strong.easeOut,0,1,0.7,true);
      }
      
      public function setInitLoggedOut() : void
      {
         this.gotoAndStop("sell");
         this.but_buyPremium.gotoAndStop("idle");
         this.but_buyPremium.addEventListener(MouseEvent.CLICK,this.§false use§,false,0,true);
         this.but_buyPremium.addEventListener(MouseEvent.ROLL_OVER,this.§_-T9§,false,0,true);
         this.but_buyPremium.addEventListener(MouseEvent.ROLL_OUT,this.§_-gk§,false,0,true);
         this.but_buyPremium.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-Kk§,false,0,true);
         this.but_buyPremium.addEventListener(MouseEvent.MOUSE_UP,this.§catch const in§,false,0,true);
         this.butClose.gotoAndStop("idle");
         this.butClose.addEventListener(MouseEvent.CLICK,this.§include null§,false,0,true);
         this.butClose.addEventListener(MouseEvent.ROLL_OVER,this.§null in§,false,0,true);
         this.butClose.addEventListener(MouseEvent.ROLL_OUT,this.§_-Sn§,false,0,true);
         this.butClose.addEventListener(MouseEvent.MOUSE_DOWN,this.closeMouseDown,false,0,true);
         this.butClose.addEventListener(MouseEvent.MOUSE_UP,this.closeMouseUp,false,0,true);
      }
      
      public function §for for function§(param1:String) : void
      {
         this.gotoAndStop(param1);
         this.but_ok.gotoAndStop("idle");
         this.but_ok.addEventListener(MouseEvent.CLICK,this.§case const else§,false,0,true);
         this.but_ok.addEventListener(MouseEvent.ROLL_OVER,this.§_-N8§,false,0,true);
         this.but_ok.addEventListener(MouseEvent.ROLL_OUT,this.§static const extends§,false,0,true);
         this.but_ok.addEventListener(MouseEvent.MOUSE_DOWN,this.§const const get§,false,0,true);
         this.but_ok.addEventListener(MouseEvent.MOUSE_UP,this.§implements const false§,false,0,true);
      }
      
      protected function §false use§(param1:MouseEvent) : void
      {
         this.§super switch§();
         if(this.game != null)
         {
            this.game.gameSounds.playGUIButtonCommon();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_button_common");
            §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         }
         var _loc2_:String = "https://armorgames.com/purchase/";
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         var _loc4_:URLVariables = new URLVariables();
         _loc3_.method = "POST";
         _loc4_.sku = "KingdomRush-Premium";
         if(this.game != null)
         {
            _loc4_.username = this.game.main.agi.getUserName();
         }
         else
         {
            _loc4_.username = §each const each§(this.mainMenu.parent).agi.getUserName();
         }
         _loc3_.data = _loc4_;
         navigateToURL(_loc3_,"_blank");
         this.§for for function§("process");
      }
      
      public function §_-Ob§(param1:TweenEvent) : *
      {
         this.destroyThis();
      }
      
      protected function §_-T9§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.playGUIMouseOverCommon();
         }
         else
         {
            §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         }
         this.but_buyPremium.buttonMode = true;
         this.but_buyPremium.mouseChildren = false;
         this.but_buyPremium.useHandCursor = true;
         this.but_buyPremium.gotoAndStop("over");
      }
      
      protected function §_-gk§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.stopGUIMouseOverCommon();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         }
         this.but_buyPremium.useHandCursor = false;
         this.but_buyPremium.gotoAndStop("idle");
      }
      
      protected function §_-Kk§(param1:MouseEvent) : void
      {
         this.but_buyPremium.gotoAndStop("press");
      }
      
      protected function §catch const in§(param1:MouseEvent) : void
      {
         this.but_buyPremium.gotoAndStop("idle");
      }
      
      protected function §case const else§(param1:MouseEvent) : void
      {
         this.§super switch§();
         if(this.game != null)
         {
            this.game.gameSounds.playGUIButtonCommon();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_button_common");
            §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         }
         if(this.currentFrameLabel == "process")
         {
            this.gotoAndStop("loading");
            if(this.game != null)
            {
               this.game.main.agi.retrieveUserData(this.§_-q9§,"kingdomRushPremiumContentEnabled");
            }
            else
            {
               §each const each§(this.mainMenu.parent).agi.retrieveUserData(this.§_-q9§,"kingdomRushPremiumContentEnabled");
            }
         }
         else
         {
            if(this.game != null)
            {
               this.game.§_-6X§.removeMapBlock();
            }
            else
            {
               this.mainMenu.§else import§();
            }
            this.yTween = new Tween(this,"y",Strong.easeOut,this.y,this.y - 50,0.7,true);
            this.alphaTween = new Tween(this,"alpha",Strong.easeOut,1,0,0.7,true);
            this.yTween.addEventListener(TweenEvent.MOTION_FINISH,this.§_-Ob§,false,0,true);
         }
      }
      
      protected function §_-q9§(param1:Object) : void
      {
         var _loc2_:int = 0;
         if(param1.success)
         {
            _loc2_ = int(param1.data);
            if(_loc2_ == 2)
            {
               this.§for for function§("success");
               this.§_-mZ§();
            }
            else
            {
               this.§for for function§("fail");
            }
         }
         else
         {
            this.§for for function§("fail");
         }
      }
      
      protected function §_-mZ§() : void
      {
         if(this.game != null)
         {
            this.game.§override for if§ = true;
            this.game.§do const static§();
            this.game.§_-6X§.updateStars();
            this.game.§_-6X§.setBtnPremiumActive();
         }
         else
         {
            this.mainMenu.§default in§();
         }
      }
      
      protected function §_-N8§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.playGUIMouseOverCommon();
         }
         else
         {
            §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         }
         this.but_ok.buttonMode = true;
         this.but_ok.mouseChildren = false;
         this.but_ok.useHandCursor = true;
         this.but_ok.gotoAndStop("over");
      }
      
      protected function §static const extends§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.stopGUIMouseOverCommon();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         }
         this.but_ok.useHandCursor = false;
         this.but_ok.gotoAndStop("idle");
      }
      
      protected function §const const get§(param1:MouseEvent) : void
      {
         this.but_ok.gotoAndStop("press");
      }
      
      protected function §implements const false§(param1:MouseEvent) : void
      {
         this.but_ok.gotoAndStop("idle");
      }
      
      public function §null in§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.§break const null§();
         }
         else
         {
            §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         }
         this.butClose.buttonMode = true;
         this.butClose.mouseChildren = false;
         this.butClose.useHandCursor = true;
         this.butClose.gotoAndStop("over");
      }
      
      public function §_-Sn§(param1:MouseEvent) : void
      {
         if(this.game != null)
         {
            this.game.gameSounds.stopGUIMouseOverCommon();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         }
         this.butClose.useHandCursor = false;
         this.butClose.gotoAndStop("idle");
      }
      
      protected function closeMouseDown(param1:MouseEvent) : void
      {
         this.butClose.gotoAndStop("press");
      }
      
      protected function closeMouseUp(param1:MouseEvent) : void
      {
         this.butClose.gotoAndStop("over");
      }
      
      public function §include null§(param1:MouseEvent) : void
      {
         this.§super switch§();
         if(this.game != null)
         {
            this.game.gameSounds.playGUIButtonCommon();
            this.game.§_-6X§.removeMapBlock();
         }
         else
         {
            §for for dynamic§.getInstance().stopSound("gui_button_common");
            §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
            this.mainMenu.§else import§();
         }
         this.yTween = new Tween(this,"y",Strong.easeOut,this.y,this.y - 50,0.7,true);
         this.alphaTween = new Tween(this,"alpha",Strong.easeOut,1,0,0.7,true);
         this.yTween.addEventListener(TweenEvent.MOTION_FINISH,this.§_-Ob§,false,0,true);
      }
      
      public function §super switch§() : void
      {
         if(this.butClose != null && Boolean(this.butClose.hasEventListener(MouseEvent.CLICK)))
         {
            this.butClose.removeEventListener(MouseEvent.CLICK,this.§include null§);
            this.butClose.removeEventListener(MouseEvent.ROLL_OVER,this.§null in§);
            this.butClose.removeEventListener(MouseEvent.ROLL_OUT,this.§_-Sn§);
            this.butClose.removeEventListener(MouseEvent.MOUSE_DOWN,this.closeMouseDown);
            this.butClose.removeEventListener(MouseEvent.MOUSE_UP,this.closeMouseUp);
         }
         if(this.but_ok != null && Boolean(this.but_ok.hasEventListener(MouseEvent.CLICK)))
         {
            this.but_ok.removeEventListener(MouseEvent.CLICK,this.§case const else§);
            this.but_ok.removeEventListener(MouseEvent.ROLL_OVER,this.§_-N8§);
            this.but_ok.removeEventListener(MouseEvent.ROLL_OUT,this.§static const extends§);
            this.but_ok.removeEventListener(MouseEvent.MOUSE_DOWN,this.§const const get§);
            this.but_ok.removeEventListener(MouseEvent.MOUSE_UP,this.§implements const false§);
         }
         if(this.but_buyPremium != null && Boolean(this.but_buyPremium.hasEventListener(MouseEvent.CLICK)))
         {
            this.but_buyPremium.removeEventListener(MouseEvent.CLICK,this.§false use§);
            this.but_buyPremium.removeEventListener(MouseEvent.ROLL_OVER,this.§_-T9§);
            this.but_buyPremium.removeEventListener(MouseEvent.ROLL_OUT,this.§_-gk§);
            this.but_buyPremium.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-Kk§);
            this.but_buyPremium.removeEventListener(MouseEvent.MOUSE_UP,this.§catch const in§);
         }
      }
      
      public function destroyThis() : void
      {
         if(this.game != null && Boolean(this.game.§_-yX§) && this.game.§_-6X§ != null)
         {
            this.game.§_-6X§.§static else§();
         }
         else if(this.mainMenu != null)
         {
            this.mainMenu.§_-6P§ = null;
         }
         this.§super switch§();
         this.removeEventListener(Event.ADDED_TO_STAGE,this.init);
         this.yTween.removeEventListener(TweenEvent.MOTION_FINISH,this.§_-Ob§);
         this.yTween = null;
         this.alphaTween = null;
         this.game = null;
         this.mainMenu = null;
         this.parent.removeChild(this);
      }
   }
}

