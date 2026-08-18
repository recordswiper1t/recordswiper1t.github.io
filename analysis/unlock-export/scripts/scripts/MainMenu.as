package
{
   import §_-aQ§.*;
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.net.*;
   import flash.text.TextField;
   import ironhide.utils.tooltip.*;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol7640")]
   public class MainMenu extends §extends const true§
   {
      
      public var §use const continue§:MovieClip;
      
      public var §continue const break§:MovieClip;
      
      public var §case class§:MovieClip;
      
      public var §finally finally§:MovieClip;
      
      public var link_armorgames:MovieClip;
      
      public var §for const final§:TextField;
      
      public var §_-XL§:MovieClip;
      
      public var §break do§:MovieClip;
      
      public var §if else§:MovieClip;
      
      public var §else while§:MovieClip;
      
      public var §break const default§:MovieClip;
      
      private var location:int;
      
      private var §do native§:Boolean = false;
      
      private var §each const case§:Boolean = false;
      
      private var inTime:int = 46;
      
      private var inCreditsTime:int = 20;
      
      private var inTimeCounter:int = 0;
      
      private var outSlotTime:int = 6;
      
      private var outSlotTimeCounter:int = 0;
      
      private var outTime:int = 12;
      
      private var outTimeCounter:int = 0;
      
      public var §true for package§:§include in§ = new §include in§();
      
      public var §implements const do§:§_-im§;
      
      public var §_-6P§:§_-Wl§;
      
      public var §do const catch§:ButPremiumContentMainMenu;
      
      private var §_-l6§:§_-sK§;
      
      private var §_-ky§:§_-dB§;
      
      private var slotOnline1:§set for package§;
      
      private var slotOnline2:§set for package§;
      
      private var slotOnline3:§set for package§;
      
      private var readyToGetOnlineData:Boolean = false;
      
      private var §class each§:Boolean = false;
      
      protected var tooltip:§_-RP§;
      
      private var slot1:§try throw§;
      
      private var slot2:§try throw§;
      
      private var slot3:§try throw§;
      
      private var §use const get§:String;
      
      private var §include package§:§break const override§;
      
      private var §var for switch§:§_-LO§;
      
      private const ON_START:int = 0;
      
      private const ON_SLOT_OUT:int = 1;
      
      private const IDLE:int = 2;
      
      private const §if const try§:int = 3;
      
      public var §function for break§:MovieClip;
      
      public function MainMenu()
      {
         super();
         addFrameScript(46,this.frame47,58,this.frame59,74,this.frame75,81,this.frame82);
         this.§implements const do§ = new §_-im§(new Point(-160,36),this);
         this.tooltip = new §_-RP§(this,new Point(this.mouseX + 5,this.mouseY - 5),new Point(this.mouseX - 5,this.mouseY - 5));
         if(§each const each§.localOnly)
         {
            this.slot1 = new §try throw§(new Point(53,32),"krslot1",this);
            this.slot2 = new §try throw§(new Point(53,99),"krslot2",this);
            this.slot3 = new §try throw§(new Point(53,166),"krslot3",this);
         }
         else
         {
            this.slot1 = new §try throw§(new Point(238,32),"krslot1",this);
            this.slot2 = new §try throw§(new Point(238,99),"krslot2",this);
            this.slot3 = new §try throw§(new Point(238,166),"krslot3",this);
         }
         this.slotOnline1 = new §set for package§(new Point(17,32),1,this);
         this.slotOnline2 = new §set for package§(new Point(17,99),2,this);
         this.slotOnline3 = new §set for package§(new Point(17,166),3,this);
         MovieClip(this.§use const continue§).mouseEnabled = false;
         MovieClip(this.§use const continue§).mouseChildren = false;
         this.addEventListener(Event.ADDED_TO_STAGE,this.init,false,0,true);
      }
      
      public function init(param1:Event) : void
      {
         this.§_-l6§ = new §_-sK§(this,§each const each§(this.parent));
         this.§do const catch§ = new ButPremiumContentMainMenu(this,§each const each§(this.parent));
         this.§_-ky§ = new §_-dB§(this);
         this.§var for switch§ = new §_-LO§(§each const each§(this.parent),new Point(12,12));
         this.addChild(this.§var for switch§);
         this.§include package§ = new §break const override§(§each const each§(this.parent),new Point(48,12),true);
         this.addChild(this.§include package§);
         §for for dynamic§.getInstance().stopSound("music_Map_Theme");
         §for for dynamic§.getInstance().playSound("music_savage_music_theme",1,0,9999);
         this.gotoAndPlay("in");
         this.§break do§.gotoAndStop("idle");
         MovieClip(this.§_-XL§).buttonMode = true;
         MovieClip(this.§_-XL§).mouseChildren = false;
         MovieClip(this.§_-XL§).useHandCursor = true;
         MovieClip(this.§_-XL§).addEventListener(MouseEvent.CLICK,this.§_-As§,false,0,true);
         MovieClip(this.link_armorgames).buttonMode = true;
         MovieClip(this.link_armorgames).mouseChildren = false;
         MovieClip(this.link_armorgames).useHandCursor = true;
         MovieClip(this.link_armorgames).addEventListener(MouseEvent.CLICK,this.linkArmorGames,false,0,true);
         MovieClip(this.link_armorgames).gotoAndStop(§each const each§.menuLinkLabel);
         if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_CHROME)
         {
            this.link_armorgames.visible = false;
            this.§_-XL§.visible = false;
         }
         this.§for const final§.text = "1.1.6a";
         this.§break const default§.addEventListener(MouseEvent.CLICK,this.twitter,false,0,true);
         this.§break const default§.addEventListener(MouseEvent.ROLL_OVER,this.§_-oX§,false,0,true);
         this.§break const default§.addEventListener(MouseEvent.ROLL_OUT,this.§_-Sg§,false,0,true);
         this.§break const default§.addEventListener(MouseEvent.MOUSE_DOWN,this.§null const include§,false,0,true);
         this.§break const default§.addEventListener(MouseEvent.MOUSE_UP,this.§if const while§,false,0,true);
         this.§else while§.addEventListener(MouseEvent.CLICK,this.facebook,false,0,true);
         this.§else while§.addEventListener(MouseEvent.ROLL_OVER,this.rollOverFacebook,false,0,true);
         this.§else while§.addEventListener(MouseEvent.ROLL_OUT,this.rollOutFacebook,false,0,true);
         this.§else while§.addEventListener(MouseEvent.MOUSE_DOWN,this.mouseDownFacebook,false,0,true);
         this.§else while§.addEventListener(MouseEvent.MOUSE_UP,this.mouseUpFacebook,false,0,true);
         this.§continue const break§.addEventListener(MouseEvent.CLICK,this.§false for package§,false,0,true);
         this.§continue const break§.addEventListener(MouseEvent.ROLL_OVER,this.§finally else§,false,0,true);
         this.§continue const break§.addEventListener(MouseEvent.ROLL_OUT,this.§_-dY§,false,0,true);
         this.§continue const break§.addEventListener(MouseEvent.MOUSE_DOWN,this.§implements const case§,false,0,true);
         this.§continue const break§.addEventListener(MouseEvent.MOUSE_UP,this.§dynamic for var§,false,0,true);
         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);
      }
      
      public function §_-kf§() : void
      {
         if(!this.contains(this.§true for package§))
         {
            this.addChild(this.§true for package§);
         }
         this.§true for package§.show();
      }
      
      public function §_-Uu§() : Boolean
      {
         return this.contains(this.§true for package§);
      }
      
      public function §else import§() : void
      {
         if(this.contains(this.§true for package§))
         {
            this.§true for package§.hide();
         }
      }
      
      public function showTooltip(param1:String, param2:String) : void
      {
         this.tooltip.loadTooltip(new Point(this.mouseX + 5,this.mouseY - 5),new Point(this.mouseX - 5,this.mouseY - 5),230,{
            "title":param1,
            "text":param2,
            "width":240
         });
         this.addChild(this.tooltip);
      }
      
      public function hideTooltip() : void
      {
         if(this.tooltip != null && this.contains(this.tooltip))
         {
            this.tooltip.hideTooltip();
         }
      }
      
      public function moveTooltip(param1:int) : void
      {
         if(this.tooltip != null)
         {
            this.tooltip.x = this.mouseX + 12 * param1;
            this.tooltip.y = this.mouseY - 8;
         }
      }
      
      public function §override each§(param1:Object, param2:Object) : void
      {
         var _loc3_:§default false§ = null;
         if(this.stage == null)
         {
            return;
         }
         if(param2.Success)
         {
            _loc3_ = new §default false§(this.stage.loaderInfo.url,param1.blUrls);
            if(_loc3_.§do for throw§())
            {
               this.addChild(new §_-De§());
            }
         }
      }
      
      public function eFrameEvents(param1:Event) : void
      {
         if(this.readyToGetOnlineData)
         {
            this.readyToGetOnlineData = false;
            this.§class each§ = true;
            this.slotOnline1.§false const break§();
            this.slotOnline2.§false const break§();
            this.slotOnline3.§false const break§();
            §each const each§.onlineHandler.retrieveOnlineData(this.§_-q9§);
         }
         if(this.location == this.ON_START)
         {
            if(!this.§do native§)
            {
               ++this.inTimeCounter;
               if(this.inTimeCounter == this.inTime)
               {
                  this.§break do§.addEventListener(MouseEvent.CLICK,this.clickEvent,false,0,true);
                  this.§break do§.addEventListener(MouseEvent.ROLL_OVER,this.§function const const§,false,0,true);
                  this.§break do§.addEventListener(MouseEvent.ROLL_OUT,this.§case for set§,false,0,true);
                  this.§break do§.addEventListener(MouseEvent.MOUSE_DOWN,this.§if override§,false,0,true);
                  this.§break do§.addEventListener(MouseEvent.MOUSE_UP,this.§_-Js§,false,0,true);
                  this.§do native§ = true;
                  this.inTime = 21;
                  this.inCreditsTime = 1;
                  this.location = this.IDLE;
               }
               if(this.inTimeCounter == this.inCreditsTime)
               {
                  this.§if else§.gotoAndStop("idle");
                  this.§if else§.visible = true;
                  this.§if else§.addEventListener(MouseEvent.CLICK,this.§for const§,false,0,true);
                  this.§if else§.addEventListener(MouseEvent.ROLL_OVER,this.§static set§,false,0,true);
                  this.§if else§.addEventListener(MouseEvent.ROLL_OUT,this.§_-Dy§,false,0,true);
                  this.§if else§.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-78§,false,0,true);
                  this.§if else§.addEventListener(MouseEvent.MOUSE_UP,this.§finally const do§,false,0,true);
               }
               return;
            }
         }
         if(this.location == this.§if const try§)
         {
            if(this.outTimeCounter < this.outTime)
            {
               ++this.outTimeCounter;
               return;
            }
            this.§function const with§();
            this.location = this.IDLE;
            this.§if else§.visible = false;
         }
         if(this.location == this.ON_SLOT_OUT)
         {
            if(this.outSlotTimeCounter < this.outSlotTime)
            {
               ++this.outSlotTimeCounter;
               return;
            }
            this.§_-ne§();
            this.gotoAndPlay("inMenu");
            this.§break do§.gotoAndStop("idle");
            this.location = this.ON_START;
            this.§do native§ = false;
            this.inTimeCounter = 0;
         }
      }
      
      public function §_-15§() : void
      {
         this.slot1.§_-vc§();
         this.slot2.§_-vc§();
         this.slot3.§_-vc§();
      }
      
      public function §use for package§() : void
      {
         this.slot1.§_-pB§();
         this.slot2.§_-pB§();
         this.slot3.§_-pB§();
      }
      
      public function §default in§() : void
      {
         this.readyToGetOnlineData = true;
      }
      
      public function §_-ml§() : void
      {
         §each const each§(this.parent).mpc = false;
         this.slotOnline1.§_-1F§();
         this.slotOnline2.§_-1F§();
         this.slotOnline3.§_-1F§();
      }
      
      public function §import for§() : void
      {
         §each const each§(this.parent).loadGame(this.§use const get§);
         this.destroyThis();
      }
      
      private function §_-g7§() : void
      {
         this.§break do§.removeEventListener(MouseEvent.CLICK,this.clickEvent);
         this.§break do§.removeEventListener(MouseEvent.ROLL_OVER,this.§function const const§);
         this.§break do§.removeEventListener(MouseEvent.ROLL_OUT,this.§case for set§);
         this.§break do§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§if override§);
         this.§break do§.removeEventListener(MouseEvent.MOUSE_UP,this.§_-Js§);
         this.§if else§.removeEventListener(MouseEvent.CLICK,this.§for const§);
         this.§if else§.removeEventListener(MouseEvent.ROLL_OVER,this.§static set§);
         this.§if else§.removeEventListener(MouseEvent.ROLL_OUT,this.§_-Dy§);
         this.§if else§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-78§);
         this.§if else§.removeEventListener(MouseEvent.MOUSE_UP,this.§finally const do§);
      }
      
      private function §function const with§() : void
      {
         this.gotoAndPlay("inSave");
         if(§each const each§.localOnly == false)
         {
            this.§case class§.visible = false;
            this.§finally finally§.addChild(this.§implements const do§);
            this.§finally finally§.addChild(this.slotOnline1);
            this.§finally finally§.addChild(this.slotOnline2);
            this.§finally finally§.addChild(this.slotOnline3);
            this.§finally finally§.addChild(this.slot1);
            this.§finally finally§.addChild(this.slot2);
            this.§finally finally§.addChild(this.slot3);
            this.§finally finally§.butBack.addEventListener(MouseEvent.CLICK,this.§_-fA§,false,0,true);
            this.§finally finally§.butBack.addEventListener(MouseEvent.ROLL_OVER,this.§_-IO§,false,0,true);
            this.§finally finally§.butBack.addEventListener(MouseEvent.ROLL_OUT,this.§var use§,false,0,true);
            this.§finally finally§.butBack.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-EE§,false,0,true);
            this.§finally finally§.butBack.addEventListener(MouseEvent.MOUSE_UP,this.§_-a8§,false,0,true);
            this.§finally finally§.butBack.gotoAndStop("idle");
         }
         else
         {
            if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE)
            {
               §each const each§.onlineHandler.retrieveHeroesPurchased();
            }
            this.§finally finally§.visible = false;
            this.§case class§.addChild(this.slot1);
            this.§case class§.addChild(this.slot2);
            this.§case class§.addChild(this.slot3);
            this.§case class§.butBack.addEventListener(MouseEvent.CLICK,this.§_-fA§,false,0,true);
            this.§case class§.butBack.addEventListener(MouseEvent.ROLL_OVER,this.§_-IO§,false,0,true);
            this.§case class§.butBack.addEventListener(MouseEvent.ROLL_OUT,this.§var use§,false,0,true);
            this.§case class§.butBack.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-EE§,false,0,true);
            this.§case class§.butBack.addEventListener(MouseEvent.MOUSE_UP,this.§_-a8§,false,0,true);
            this.§case class§.butBack.gotoAndStop("idle");
         }
      }
      
      private function §_-ne§() : void
      {
         if(this.§case class§ != null && §each const each§.localOnly)
         {
            this.§case class§.removeChild(this.slot1);
            this.§case class§.removeChild(this.slot2);
            this.§case class§.removeChild(this.slot3);
         }
         if(this.§finally finally§ != null && !§each const each§.localOnly)
         {
            this.§finally finally§.removeChild(this.§implements const do§);
            if(this.§do const catch§ != null && this.§finally finally§.contains(this.§do const catch§))
            {
               this.§finally finally§.removeChild(this.§do const catch§);
            }
            this.§finally finally§.removeChild(this.slotOnline1);
            this.§finally finally§.removeChild(this.slotOnline2);
            this.§finally finally§.removeChild(this.slotOnline3);
            this.§finally finally§.removeChild(this.slot1);
            this.§finally finally§.removeChild(this.slot2);
            this.§finally finally§.removeChild(this.slot3);
         }
      }
      
      public function initGame(param1:String) : void
      {
         this.§use const get§ = param1;
         §each const each§(this.parent).showTransition(null,null,this);
      }
      
      public function initOnlineGame(param1:String, param2:Object, param3:int) : void
      {
         this.§use const get§ = param1;
         §each const each§(this.parent).onlineData = param2;
         §each const each§(this.parent).onlineSlotNumber = param3;
         §each const each§(this.parent).showTransition(null,null,this);
      }
      
      private function §static default§(param1:Number, param2:Number) : Boolean
      {
         if(param1 > 700 || param1 < 0 || (param2 < 0 || param2 > 600))
         {
            return true;
         }
         return false;
      }
      
      private function §_-q9§(param1:Object) : void
      {
         var _loc2_:Object = null;
         if(this.§_-ky§ == null)
         {
            return;
         }
         this.§class each§ = false;
         if(param1.success)
         {
            if(this.§finally finally§ != null)
            {
               if(this.contains(this.§_-ky§))
               {
                  this.removeChild(this.§_-ky§);
               }
               _loc2_ = param1.keys;
               if(_loc2_.kingdomRushPremiumContentEnabled == null || _loc2_.kingdomRushPremiumContentEnabled != 2)
               {
                  §each const each§(this.parent).mpc = false;
               }
               else if(_loc2_.kingdomRushPremiumContentEnabled == 2)
               {
                  §each const each§(this.parent).mpc = true;
               }
               this.§do const catch§.§_-bB§(_loc2_.kingdomRushPremiumContentEnabled);
               this.slotOnline1.§const const if§(_loc2_.slot1);
               this.slotOnline2.§const const if§(_loc2_.slot2);
               this.slotOnline3.§const const if§(_loc2_.slot3);
               if(this.§_-6P§ != null && this.contains(this.§_-6P§))
               {
                  this.§_-6P§.updatePC(§each const each§(this.parent).mpc);
               }
               this.§_-5y§();
            }
         }
         else
         {
            this.§_-ml§();
            this.§_-ky§.action = "get_data";
            if(this.§_-6P§ != null && this.contains(this.§_-6P§))
            {
               this.§else import§();
               this.§_-6P§.destroyThis();
            }
            if(!this.contains(this.§_-ky§))
            {
               this.addChild(this.§_-ky§);
            }
            else
            {
               this.§_-ky§.§class function§();
            }
         }
      }
      
      public function §_-5y§() : void
      {
      }
      
      public function §break try§() : void
      {
         if(this.§finally finally§.contains(this.§_-l6§))
         {
            this.§case class§.removeChild(this.§_-l6§);
         }
      }
      
      public function §continue default§() : void
      {
         if(!this.§finally finally§.contains(this.§_-l6§))
         {
            this.§case class§.addChild(this.§_-l6§);
         }
      }
      
      public function §_-T3§() : Boolean
      {
         var _loc1_:SharedObject = null;
         var _loc2_:SharedObject = null;
         var _loc3_:SharedObject = null;
         try
         {
            _loc1_ = SharedObject.getLocal("krslot1");
            if(_loc1_.data.levels != undefined)
            {
               _loc1_.close();
               return true;
            }
            _loc1_.close();
         }
         catch(err:Error)
         {
         }
         try
         {
            _loc2_ = SharedObject.getLocal("krslot2");
            if(_loc2_.data.levels != undefined)
            {
               _loc2_.close();
               return true;
            }
            _loc1_.close();
         }
         catch(err:Error)
         {
         }
         try
         {
            _loc3_ = SharedObject.getLocal("krslot3");
            if(_loc3_.data.levels != undefined)
            {
               _loc3_.close();
               return true;
            }
            _loc1_.close();
         }
         catch(err:Error)
         {
         }
         return false;
      }
      
      public function clickEvent(param1:MouseEvent) : void
      {
         this.§_-g7§();
         this.gotoAndPlay("out");
         this.location = this.§if const try§;
         this.outTimeCounter = 0;
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
      }
      
      public function §function const const§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.§break do§.buttonMode = true;
         this.§break do§.mouseChildren = false;
         this.§break do§.useHandCursor = true;
         this.§break do§.gotoAndStop("over");
      }
      
      public function §case for set§(param1:MouseEvent) : void
      {
         this.§break do§.useHandCursor = false;
         this.§break do§.gotoAndStop("idle");
      }
      
      public function §if override§(param1:MouseEvent) : void
      {
         this.§break do§.gotoAndStop("press");
      }
      
      public function §_-Js§(param1:MouseEvent) : void
      {
         this.§break do§.gotoAndStop("idle");
      }
      
      public function §_-qN§() : void
      {
         §each const each§(this.parent).goToCredits();
         this.destroyThis();
      }
      
      public function §for const§(param1:MouseEvent) : void
      {
         this.§_-g7§();
         §each const each§(this.parent).showTransition(null,null,null,null,this);
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
      }
      
      public function §static set§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.§if else§.buttonMode = true;
         this.§if else§.mouseChildren = false;
         this.§if else§.useHandCursor = true;
         this.§if else§.gotoAndStop("over");
      }
      
      public function §_-Dy§(param1:MouseEvent) : void
      {
         this.§if else§.useHandCursor = false;
         this.§if else§.gotoAndStop("idle");
      }
      
      public function §_-78§(param1:MouseEvent) : void
      {
         this.§if else§.gotoAndStop("press");
      }
      
      public function §finally const do§(param1:MouseEvent) : void
      {
         this.§if else§.gotoAndStop("idle");
      }
      
      public function §_-HI§() : void
      {
         if(this.§case class§ != null && §each const each§.localOnly)
         {
            this.§case class§.butBack.removeEventListener(MouseEvent.CLICK,this.§_-fA§);
            this.§case class§.butBack.removeEventListener(MouseEvent.ROLL_OVER,this.§_-IO§);
            this.§case class§.butBack.removeEventListener(MouseEvent.ROLL_OUT,this.§var use§);
            this.§case class§.butBack.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-EE§);
            this.§case class§.butBack.removeEventListener(MouseEvent.MOUSE_UP,this.§_-a8§);
         }
         if(this.§case class§ != null && !§each const each§.localOnly)
         {
            this.§finally finally§.butBack.removeEventListener(MouseEvent.CLICK,this.§_-fA§);
            this.§finally finally§.butBack.removeEventListener(MouseEvent.ROLL_OVER,this.§_-IO§);
            this.§finally finally§.butBack.removeEventListener(MouseEvent.ROLL_OUT,this.§var use§);
            this.§finally finally§.butBack.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-EE§);
            this.§finally finally§.butBack.removeEventListener(MouseEvent.MOUSE_UP,this.§_-a8§);
         }
      }
      
      public function §_-fA§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         this.§_-HI§();
         this.gotoAndPlay("outSave");
         this.location = this.ON_SLOT_OUT;
         this.outSlotTimeCounter = 0;
      }
      
      public function §_-IO§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         if(§each const each§.localOnly)
         {
            this.§case class§.butBack.buttonMode = true;
            this.§case class§.butBack.mouseChildren = false;
            this.§case class§.butBack.useHandCursor = true;
            this.§case class§.butBack.gotoAndStop("over");
         }
         else
         {
            this.§finally finally§.butBack.buttonMode = true;
            this.§finally finally§.butBack.mouseChildren = false;
            this.§finally finally§.butBack.useHandCursor = true;
            this.§finally finally§.butBack.gotoAndStop("over");
         }
      }
      
      public function §var use§(param1:MouseEvent) : void
      {
         if(§each const each§.localOnly)
         {
            this.§case class§.butBack.useHandCursor = false;
            this.§case class§.butBack.gotoAndStop("idle");
         }
         else
         {
            this.§finally finally§.butBack.useHandCursor = false;
            this.§finally finally§.butBack.gotoAndStop("idle");
         }
      }
      
      public function §_-EE§(param1:MouseEvent) : void
      {
         if(§each const each§.localOnly)
         {
            this.§case class§.butBack.gotoAndStop("press");
         }
         else
         {
            this.§finally finally§.butBack.gotoAndStop("press");
         }
      }
      
      public function §_-a8§(param1:MouseEvent) : void
      {
         if(§each const each§.localOnly)
         {
            this.§case class§.butBack.gotoAndStop("idle");
         }
         else
         {
            this.§finally finally§.butBack.gotoAndStop("idle");
         }
      }
      
      private function §_-As§(param1:MouseEvent) : void
      {
         var _loc2_:String = "http://www.ironhidegames.com/?ref=KRFRONTIERS";
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         navigateToURL(_loc3_,"_blank");
      }
      
      private function linkArmorGames(param1:MouseEvent) : void
      {
         var _loc2_:String = §each const each§.LINK_SITE;
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         navigateToURL(_loc3_,"_blank");
      }
      
      protected function §false for package§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         var _loc2_:String = "http://getmobile.kingdomrushfrontiers.com";
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         navigateToURL(_loc3_,"_blank");
      }
      
      protected function §finally else§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.§continue const break§.mc.buttonMode = true;
         this.§continue const break§.mc.mouseChildren = false;
         this.§continue const break§.mc.useHandCursor = true;
         this.§continue const break§.mc.gotoAndStop("over");
      }
      
      protected function §_-dY§(param1:MouseEvent) : void
      {
         this.§continue const break§.useHandCursor = false;
         this.§continue const break§.mc.gotoAndStop("idle");
      }
      
      protected function §implements const case§(param1:MouseEvent) : void
      {
         this.§continue const break§.mc.gotoAndStop("press");
      }
      
      protected function §dynamic for var§(param1:MouseEvent) : void
      {
         this.§continue const break§.mc.gotoAndStop("idle");
      }
      
      protected function facebook(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         var _loc2_:String = "http://www.facebook.com/pages/Ironhide-Game-Studio/146919875341692";
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         navigateToURL(_loc3_,"_blank");
      }
      
      protected function rollOverFacebook(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.§else while§.buttonMode = true;
         this.§else while§.mouseChildren = false;
         this.§else while§.useHandCursor = true;
         this.§else while§.gotoAndStop("over");
      }
      
      protected function rollOutFacebook(param1:MouseEvent) : void
      {
         this.§else while§.useHandCursor = false;
         this.§else while§.gotoAndStop("idle");
      }
      
      protected function mouseDownFacebook(param1:MouseEvent) : void
      {
         this.§else while§.gotoAndStop("press");
      }
      
      protected function mouseUpFacebook(param1:MouseEvent) : void
      {
         this.§else while§.gotoAndStop("idle");
      }
      
      protected function twitter(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_button_common");
         §for for dynamic§.getInstance().playSound("gui_button_common",1,0,0);
         var _loc2_:String = "http://twitter.com/#!/ironhidegames";
         var _loc3_:URLRequest = new URLRequest(_loc2_);
         navigateToURL(_loc3_,"_blank");
      }
      
      protected function §_-oX§(param1:MouseEvent) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().playSound("gui_mouse_over_tower_common",1,0,0);
         this.§break const default§.buttonMode = true;
         this.§break const default§.mouseChildren = false;
         this.§break const default§.useHandCursor = true;
         this.§break const default§.gotoAndStop("over");
      }
      
      protected function §_-Sg§(param1:MouseEvent) : void
      {
         this.§break const default§.useHandCursor = false;
         this.§break const default§.gotoAndStop("idle");
      }
      
      protected function §null const include§(param1:MouseEvent) : void
      {
         this.§break const default§.gotoAndStop("press");
      }
      
      protected function §if const while§(param1:MouseEvent) : void
      {
         this.§break const default§.gotoAndStop("idle");
      }
      
      public function destroyThis() : void
      {
         this.§_-l6§.destroyThis();
         this.§_-l6§ = null;
         this.§do const catch§.destroyThis();
         this.§do const catch§ = null;
         this.§_-ky§.destroyThis();
         this.§_-ky§ = null;
         if(this.tooltip != null)
         {
            this.tooltip.destroyThis();
         }
         this.tooltip = null;
         this.§include package§.destroyThis();
         this.§include package§ = null;
         this.§var for switch§.destroyThis();
         this.§var for switch§ = null;
         if(this.§_-XL§ != null)
         {
            this.§break const default§.removeEventListener(MouseEvent.CLICK,this.twitter);
            this.§break const default§.removeEventListener(MouseEvent.ROLL_OVER,this.§_-oX§);
            this.§break const default§.removeEventListener(MouseEvent.ROLL_OUT,this.§_-Sg§);
            this.§break const default§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§null const include§);
            this.§break const default§.removeEventListener(MouseEvent.MOUSE_UP,this.§if const while§);
            this.§else while§.removeEventListener(MouseEvent.CLICK,this.facebook);
            this.§else while§.removeEventListener(MouseEvent.ROLL_OVER,this.rollOverFacebook);
            this.§else while§.removeEventListener(MouseEvent.ROLL_OUT,this.rollOutFacebook);
            this.§else while§.removeEventListener(MouseEvent.MOUSE_DOWN,this.mouseDownFacebook);
            this.§else while§.removeEventListener(MouseEvent.MOUSE_UP,this.mouseUpFacebook);
         }
         this.removeEventListener(Event.ENTER_FRAME,this.eFrameEvents);
         this.removeEventListener(Event.ADDED_TO_STAGE,this.init);
         this.§_-HI§();
         this.§_-ne§();
         this.§else import§();
         this.§true for package§ = null;
         this.parent.removeChild(this);
      }
      
      internal function frame47() : *
      {
         stop();
      }
      
      internal function frame59() : *
      {
         stop();
      }
      
      internal function frame75() : *
      {
         stop();
      }
      
      internal function frame82() : *
      {
         stop();
      }
   }
}

