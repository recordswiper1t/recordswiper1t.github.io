package
{
   import fl.lang.*;
   import fl.transitions.*;
   import fl.transitions.easing.*;
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   
   public class §class const for§ extends Sprite
   {
      
      private static const FLAG_NORMAL:int = 0;
      
      private static const FLAG_NEW:int = 1;
      
      private static const LOADING:int = 2;
      
      private static const IRON_HEROIC_NEW:int = 3;
      
      private static const FLAG_BETTER:int = 4;
      
      private static const FLAG_FIRST:int = 5;
      
      public var game:§_-BQ§;
      
      public var mapBlock:§null while§ = new §null while§();
      
      private var §_-dp§:Array = [];
      
      private var §_-ag§:§_-2p§;
      
      private var terrain:Sprite = new Sprite();
      
      private var §package const include§:Sprite = new Sprite();
      
      private var §with const static§:Sprite = new Sprite();
      
      private var §use extends§:Sprite = new Sprite();
      
      private var socialScreen:§_-Xp§;
      
      private var btnUpgrades:ButUpgrades;
      
      private var §_-tQ§:§_-a7§;
      
      private var §_-sc§:§_-wD§;
      
      private var §false final§:§super for finally§;
      
      public var §_-Ck§:§false for while§;
      
      private var upgradeStarsAlert:UpgradeStarsAlert;
      
      public var §while const import§:§try for while§;
      
      private var §_-4c§:§_-4P§;
      
      private var §_-mz§:§var const else§ = new §var const else§();
      
      private var mode:int;
      
      private var §_-WC§:int;
      
      private var §_-dw§:Boolean;
      
      private var loadingTime:int = 30;
      
      private var loadingTimeCounter:int;
      
      private var §_-SC§:int;
      
      private var §else switch§:int;
      
      private var §continue for super§:Array = [];
      
      private var §_-Na§:int;
      
      private var flagNew:int;
      
      public var signAlertUpgrades:SignAlertUpgrades;
      
      public var §finally const finally§:§final const return§;
      
      public var §_-1C§:SignAlertLevelUp;
      
      public var §_-m3§:§_-NS§;
      
      private var §implements const break§:int = 60;
      
      private var §_-rf§:int = 20;
      
      private var §_-Og§:int = 59;
      
      private var §_-fx§:int = 0;
      
      private var §_-2c§:int;
      
      private var progressCurrentStarsUpgrades:int;
      
      private var §true throw§:int = 30;
      
      private var §_-Tz§:int = 0;
      
      private var §_-KW§:int;
      
      private var §_-ZA§:int;
      
      private var §const get§:int = 30;
      
      private var §_-ML§:int = 0;
      
      private var §include package§:§break const override§;
      
      private var §var for switch§:§_-LO§;
      
      public var §null const null§:Boolean;
      
      private var §_-ou§:Tween;
      
      private var §_-Nx§:Tween;
      
      private var alphaTweenMenuBack:Tween;
      
      private var §null for throw§:Tween;
      
      private var alphaTweenEncyclopedia:Tween;
      
      private var yTweenUpgrades:Tween;
      
      private var alphaTweenUpgrades:Tween;
      
      private var §_-wI§:Tween;
      
      private var alphaTweenHeroRoom:Tween;
      
      private var §_-HZ§:Tween;
      
      private var alphaTweenAchievements:Tween;
      
      private var §default const set§:Tween;
      
      private var alphaTweenPremium:Tween;
      
      public var §_-Th§:§_-sS§;
      
      private var §extends final§:§const for while§;
      
      public function §class const for§(param1:§_-BQ§)
      {
         super();
         this.game = param1;
         this.getMaxLevelWon();
         if(!this.game.§_-yX§)
         {
            this.game.§_-Pg§.§case super§();
            this.game.§const for set§.§case super§();
         }
         else
         {
            this.§static else§();
         }
         this.mode = LOADING;
         this.§_-WC§ = FLAG_NORMAL;
         this.§_-SC§ = 70;
         this.§else switch§ = 0;
         this.addChild(this.terrain);
         this.addChild(this.§package const include§);
         this.addChild(this.§with const static§);
         this.addChild(this.§use extends§);
         this.§var for switch§ = new §_-LO§(this.game.main,new Point(60,18));
         this.addChild(this.§var for switch§);
         this.§include package§ = new §break const override§(this.game.main,new Point(96,18));
         this.addChild(this.§include package§);
         this.§_-4c§ = new §_-4P§();
         this.terrain.addChild(this.§_-4c§);
         this.socialScreen = new §_-Xp§(this.game);
         this.upgradeStarsAlert = new UpgradeStarsAlert();
         this.§while const import§ = new §try for while§(0,0);
         this.§if extends§();
         this.§try override§();
         this.§if const catch§();
         this.game.gameSounds.§return each§();
         this.§extends final§ = new §const for while§(this.game);
         if(this.game.lastLevelWon < 1 && !this.game.showedDifficulty)
         {
            this.addMapBlock();
            this.game.showedDifficulty = true;
            this.§_-Th§ = new §_-sS§(0,0,this);
            this.addChild(this.§_-Th§);
         }
         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);
         this.§finally for catch§();
      }
      
      private function getMaxLevelWon() : void
      {
         var _loc1_:int = 0;
         while(_loc1_ < this.game.§native import§.length)
         {
            if(§true final§(this.game.§native import§[_loc1_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED || §true final§(this.game.§native import§[_loc1_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW || §true final§(this.game.§native import§[_loc1_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_BETTER)
            {
               this.game.lastLevelWon = _loc1_ + 1;
            }
            _loc1_++;
         }
         §each const each§.onlineHandler.callQuest("LevelsCompleted",this.game.lastLevelWon);
      }
      
      public function endSession() : void
      {
         this.game.main.showMainMenu();
         this.destroyThis();
      }
      
      public function eFrameEvents(param1:Event) : void
      {
         if(this.mode == LOADING)
         {
            if(this.loadingTimeCounter < this.loadingTime)
            {
               ++this.loadingTimeCounter;
               return;
            }
            this.§null native§();
            this.mode = this.§_-WC§;
         }
         if(this.mode == FLAG_FIRST && this.§_-Th§ == null)
         {
            if(this.§_-fx§ < this.§implements const break§)
            {
               ++this.§_-fx§;
               if(this.§_-fx§ == this.§_-rf§ - 10)
               {
                  this.game.gameSounds.§_-SL§();
               }
               if(this.§_-fx§ == this.§_-rf§)
               {
                  this.§use extends§.addChild(new §_-H3§(this,this.§_-dp§[0],§true final§(this.game.§native import§[0])));
               }
               if(this.§_-fx§ == this.§_-Og§)
               {
                  if(this.game.lastLevelWon < 1)
                  {
                     this.§_-m3§ = new §_-NS§(new Point(249,125));
                     this.§use extends§.addChild(this.§_-m3§);
                     if(this.§_-Th§ != null)
                     {
                        this.§_-m3§.visible = false;
                     }
                  }
               }
               return;
            }
            this.mode = FLAG_NORMAL;
         }
         if(this.mode == FLAG_NEW)
         {
            if(!this.§_-RR§())
            {
               return;
            }
         }
         if(this.mode == IRON_HEROIC_NEW)
         {
            if(this.§_-Tz§ < this.§true throw§)
            {
               ++this.§_-Tz§;
               return;
            }
            this.game.gameSounds.§_-iQ§("");
            this.§_-mz§.progress.text = this.game.starsWon.toString() + "/" + this.game.§_-Y1§;
            this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
            this.§_-mz§.gotoAndPlay("addStar");
            this.mode = FLAG_NORMAL;
         }
         if(this.mode == FLAG_BETTER)
         {
            if(this.§_-ML§ < this.§const get§)
            {
               if(this.§_-ML§ == 8)
               {
                  this.game.gameSounds.§_-iQ§("");
               }
               if(this.§_-ML§ == 18)
               {
                  if(this.§_-ZA§ >= 2)
                  {
                     if(this.§_-KW§ == 2)
                     {
                        this.§_-mz§.gotoAndPlay("addStar");
                        this.§_-mz§.progress.text = this.§_-2c§ + 1 + "/" + this.game.§_-Y1§;
                        this.upgradeStarsAlert.item.txt.text = (this.progressCurrentStarsUpgrades + 1).toString();
                        ++this.§_-2c§;
                        ++this.progressCurrentStarsUpgrades;
                     }
                     this.game.gameSounds.§_-iQ§("2");
                  }
               }
               if(this.§_-ML§ == 28)
               {
                  if(this.§_-ZA§ == 3)
                  {
                     this.§_-mz§.gotoAndPlay("addStar");
                     this.§_-mz§.progress.text = this.§_-2c§ + 1 + "/" + this.game.§_-Y1§;
                     this.upgradeStarsAlert.item.txt.text = (this.progressCurrentStarsUpgrades + 1).toString();
                     ++this.§_-2c§;
                     ++this.progressCurrentStarsUpgrades;
                     this.game.gameSounds.§_-iQ§("3");
                  }
               }
               ++this.§_-ML§;
               return;
            }
            this.mode = FLAG_NORMAL;
         }
      }
      
      public function §_-EN§(param1:MouseEvent) : void
      {
         if(this.§null const null§)
         {
            return;
         }
         this.addMapBlock();
         this.game.gameSounds.playGUIButtonCommon();
         this.addChild(new §set case§(this.game));
         this.§null const null§ = true;
      }
      
      public function §_-Br§(param1:MouseEvent) : void
      {
         if(this.§null const null§)
         {
            return;
         }
         this.addMapBlock();
         this.game.gameSounds.playGUIButtonCommon();
         this.addChild(new §_-XO§(this.game));
         this.§null const null§ = true;
      }
      
      public function clickUpgrades(param1:MouseEvent) : void
      {
         if(this.§null const null§)
         {
            return;
         }
         this.addMapBlock();
         this.game.gameSounds.playGUIButtonCommon();
         this.addChild(new MenuUpgrades(this.game));
         this.§null const null§ = true;
      }
      
      public function §_-WS§(param1:MouseEvent) : void
      {
         if(this.§null const null§)
         {
            return;
         }
         this.addMapBlock();
         this.game.gameSounds.playGUIButtonCommon();
         if(this.game.§override for if§)
         {
            this.addChild(new §_-3h§(this.game));
            this.§null const null§ = true;
         }
         else
         {
            this.addChild(new §_-Wl§(this.game));
         }
      }
      
      public function §throw while§(param1:MouseEvent) : void
      {
         if(this.§null const null§)
         {
            return;
         }
         this.game.main.showTransition(null,null,null,this);
         this.§null const null§ = true;
      }
      
      protected function §null native§() : void
      {
         if(this.game.lastLevelWon == §if const function§.UNLOCK_STAGE_MIRAGE && !this.game.showedUnlockedMirage)
         {
            this.§finally const finally§ = new §final const return§(237,366);
            this.addChild(this.§finally const finally§);
            this.game.showedUnlockedMirage = true;
            this.game.showNewSignMirage = true;
         }
         if(this.game.lastLevelWon == §if const function§.UNLOCK_STAGE_CRONAN && !this.game.showedUnlockedCronan)
         {
            this.§finally const finally§ = new §final const return§(237,366);
            this.addChild(this.§finally const finally§);
            this.game.showedUnlockedCronan = true;
            this.game.showNewSignCronan = true;
         }
         if(this.game.gameHeroData.selectedHero.name == "alric" && this.game.gameHeroData.selectedHero.level == 2 && !this.game.showedLevelUp)
         {
            this.§_-1C§ = new SignAlertLevelUp(245,365);
            this.addChild(this.§_-1C§);
         }
         this.socialScreen.initMe();
         this.addChild(this.socialScreen);
         this.§_-mz§.x = 620;
         this.§_-mz§.y = 32;
         if(this.§_-WC§ == FLAG_NORMAL || this.§_-WC§ == FLAG_FIRST)
         {
            this.§_-mz§.progress.text = this.game.starsWon + "/" + this.game.§_-Y1§;
         }
         this.terrain.addChild(this.§_-mz§);
         this.§_-sc§ = new §_-wD§();
         this.§_-sc§.x = 631;
         this.§_-sc§.y = 499;
         this.btnUpgrades = new ButUpgrades();
         this.btnUpgrades.x = 446;
         this.btnUpgrades.y = 500;
         this.§_-Ck§ = new §false for while§(this);
         this.§_-Ck§.x = 355;
         this.§_-Ck§.y = 492;
         this.§_-Ck§.hero_icon.gotoAndStop(this.game.gameHeroData.selectedHero.name);
         this.§_-tQ§ = new §_-a7§();
         this.§_-tQ§.x = 531;
         this.§_-tQ§.y = 499;
         this.§false final§ = new §super for finally§();
         this.§false final§.x = 52;
         this.§false final§.y = 518;
         this.§while const import§.x = 77;
         this.§while const import§.y = 20;
         this.§_-Ck§.addChild(this.§while const import§);
         this.§package const include§.addChild(this.§false final§);
         this.§package const include§.addChild(this.btnUpgrades);
         this.§package const include§.addChild(this.§_-tQ§);
         this.§package const include§.addChild(this.§_-sc§);
         this.§package const include§.addChild(this.§_-Ck§);
         this.upgradeStarsAlert.x = 71;
         this.upgradeStarsAlert.y = 11;
         if(this.§_-WC§ == FLAG_NORMAL || this.§_-WC§ == FLAG_FIRST)
         {
            this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
         }
         this.btnUpgrades.addChild(this.upgradeStarsAlert);
         if(this.game.stars == 0)
         {
            this.upgradeStarsAlert.visible = false;
         }
         if(this.game.stars > 0)
         {
            this.upgradeStarsAlert.visible = true;
         }
         if(this.game.gameHeroData.selectedHero.skillPoints == 0)
         {
            this.§while const import§.visible = false;
         }
         else
         {
            this.§while const import§.item.txt.text = this.game.gameHeroData.selectedHero.skillPoints;
         }
         this.§_-ou§ = new Tween(this.§_-mz§,"y",Strong.easeOut,-49,this.§_-mz§.y,0.7,true);
         this.§_-Nx§ = new Tween(this.§false final§,"y",Strong.easeOut,469,this.§false final§.y,0.7,true);
         this.yTweenUpgrades = new Tween(this.btnUpgrades,"y",Strong.easeOut,469,this.btnUpgrades.y,0.7,true);
         this.§null for throw§ = new Tween(this.§_-tQ§,"y",Strong.easeOut,469,this.§_-tQ§.y,0.7,true);
         this.§_-HZ§ = new Tween(this.§_-sc§,"y",Strong.easeOut,468,this.§_-sc§.y,0.7,true);
         this.§_-wI§ = new Tween(this.§_-Ck§,"y",Strong.easeOut,468,this.§_-Ck§.y,0.7,true);
         this.alphaTweenMenuBack = new Tween(this.§false final§,"alpha",Strong.easeOut,0,1,0.7,true);
         this.alphaTweenUpgrades = new Tween(this.btnUpgrades,"alpha",Strong.easeOut,0,1,0.7,true);
         this.alphaTweenEncyclopedia = new Tween(this.§_-tQ§,"alpha",Strong.easeOut,0,1,0.7,true);
         this.alphaTweenAchievements = new Tween(this.§_-sc§,"alpha",Strong.easeOut,0,1,0.7,true);
         this.alphaTweenHeroRoom = new Tween(this.§_-Ck§,"alpha",Strong.easeOut,0.1,1,0.7,true);
         this.§false final§.addEventListener(MouseEvent.CLICK,this.§throw while§,false,0,true);
         this.§false final§.addEventListener(MouseEvent.ROLL_OVER,this.§_-xB§,false,0,true);
         this.§false final§.addEventListener(MouseEvent.ROLL_OUT,this.§null with§,false,0,true);
         this.§false final§.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-ec§,false,0,true);
         this.§false final§.addEventListener(MouseEvent.MOUSE_UP,this.§const const while§,false,0,true);
         this.btnUpgrades.addEventListener(MouseEvent.CLICK,this.clickUpgrades,false,0,true);
         this.btnUpgrades.addEventListener(MouseEvent.ROLL_OVER,this.rollOverUpgrades,false,0,true);
         this.btnUpgrades.addEventListener(MouseEvent.ROLL_OUT,this.rollOutUpgrades,false,0,true);
         this.btnUpgrades.addEventListener(MouseEvent.MOUSE_DOWN,this.mouseDownUpgrades,false,0,true);
         this.btnUpgrades.addEventListener(MouseEvent.MOUSE_UP,this.mouseUpUpgrades,false,0,true);
         this.§_-tQ§.addEventListener(MouseEvent.CLICK,this.§_-EN§,false,0,true);
         this.§_-tQ§.addEventListener(MouseEvent.ROLL_OVER,this.§_-oe§,false,0,true);
         this.§_-tQ§.addEventListener(MouseEvent.ROLL_OUT,this.§_-dd§,false,0,true);
         this.§_-tQ§.addEventListener(MouseEvent.MOUSE_DOWN,this.§finally in§,false,0,true);
         this.§_-tQ§.addEventListener(MouseEvent.MOUSE_UP,this.§_-xW§,false,0,true);
         this.§_-sc§.addEventListener(MouseEvent.CLICK,this.§_-Br§,false,0,true);
         this.§_-sc§.addEventListener(MouseEvent.ROLL_OVER,this.§import function§,false,0,true);
         this.§_-sc§.addEventListener(MouseEvent.ROLL_OUT,this.§_-yM§,false,0,true);
         this.§_-sc§.addEventListener(MouseEvent.MOUSE_DOWN,this.§final try§,false,0,true);
         this.§_-sc§.addEventListener(MouseEvent.MOUSE_UP,this.§function package§,false,0,true);
      }
      
      protected function §_-xB§(param1:MouseEvent) : void
      {
         this.game.gameSounds.§break const null§();
         this.§false final§.buttonMode = true;
         this.§false final§.mouseChildren = false;
         this.§false final§.useHandCursor = true;
         this.§false final§.gotoAndStop("over");
      }
      
      protected function §null with§(param1:MouseEvent) : void
      {
         this.§false final§.useHandCursor = false;
         this.§false final§.gotoAndStop("idle");
      }
      
      protected function §_-ec§(param1:MouseEvent) : void
      {
         this.§false final§.gotoAndStop("press");
      }
      
      protected function §const const while§(param1:MouseEvent) : void
      {
         this.§false final§.gotoAndStop("idle");
      }
      
      protected function rollOverUpgrades(param1:MouseEvent) : void
      {
         this.game.gameSounds.§break const null§();
         this.btnUpgrades.buttonMode = true;
         this.btnUpgrades.mouseChildren = false;
         this.btnUpgrades.useHandCursor = true;
         this.btnUpgrades.gotoAndStop("over");
      }
      
      protected function rollOutUpgrades(param1:MouseEvent) : void
      {
         this.btnUpgrades.useHandCursor = false;
         this.btnUpgrades.gotoAndStop("idle");
      }
      
      protected function mouseDownUpgrades(param1:MouseEvent) : void
      {
         this.btnUpgrades.gotoAndStop("press");
      }
      
      protected function mouseUpUpgrades(param1:MouseEvent) : void
      {
         this.btnUpgrades.gotoAndStop("idle");
      }
      
      protected function §_-oe§(param1:MouseEvent) : void
      {
         this.game.gameSounds.§break const null§();
         this.§_-tQ§.buttonMode = true;
         this.§_-tQ§.mouseChildren = false;
         this.§_-tQ§.useHandCursor = true;
         this.§_-tQ§.gotoAndStop("over");
      }
      
      protected function §_-dd§(param1:MouseEvent) : void
      {
         this.§_-tQ§.useHandCursor = false;
         this.§_-tQ§.gotoAndStop("idle");
      }
      
      protected function §finally in§(param1:MouseEvent) : void
      {
         this.§_-tQ§.gotoAndStop("press");
      }
      
      protected function §_-xW§(param1:MouseEvent) : void
      {
         this.§_-tQ§.gotoAndStop("idle");
      }
      
      protected function §import function§(param1:MouseEvent) : void
      {
         this.game.gameSounds.§break const null§();
         this.§_-sc§.buttonMode = true;
         this.§_-sc§.mouseChildren = false;
         this.§_-sc§.useHandCursor = true;
         this.§_-sc§.gotoAndStop("over");
      }
      
      protected function §_-yM§(param1:MouseEvent) : void
      {
         this.§_-sc§.useHandCursor = false;
         this.§_-sc§.gotoAndStop("idle");
      }
      
      protected function §final try§(param1:MouseEvent) : void
      {
         this.§_-sc§.gotoAndStop("press");
      }
      
      protected function §function package§(param1:MouseEvent) : void
      {
         this.§_-sc§.gotoAndStop("idle");
      }
      
      public function §while const switch§(param1:int, param2:int) : void
      {
         this.game.§while const switch§(param1,param2,false);
         this.game.§final throw§();
      }
      
      public function §extends else§(param1:* = null) : void
      {
         this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
         if(this.game.stars == 0)
         {
            this.upgradeStarsAlert.visible = false;
         }
         else
         {
            this.upgradeStarsAlert.visible = true;
         }
         if(param1)
         {
            this.upgradeStarsAlert.visible = false;
         }
      }
      
      public function §_-8I§() : void
      {
         this.§while const import§.item.txt.text = this.game.gameHeroData.selectedHero.skillPoints.toString();
         if(this.game.gameHeroData.selectedHero.skillPoints == 0)
         {
            this.§while const import§.visible = false;
         }
         else
         {
            this.§while const import§.visible = true;
         }
      }
      
      private function §if extends§() : void
      {
         this.§_-dp§ = [new Point(247,176),new Point(318,194),new Point(330,262),new Point(247,282),new Point(153,329),new Point(296,446),new Point(429,373),new Point(519,470),new Point(620,425),new Point(565,330),new Point(505,286),new Point(490,209),new Point(552,174),new Point(620,178),new Point(692,204)];
      }
      
      private function §try override§() : void
      {
         this.§continue for super§ = [10,16,12,24,138,32,26,24,24,13,15,13,13,13];
      }
      
      private function §if const catch§() : void
      {
         var _loc3_:int = 0;
         var _loc1_:int = 0;
         var _loc2_:String = Locale.getDefaultLang();
         while(_loc3_ < this.game.§native import§.length)
         {
            if(§true final§(this.game.§native import§[_loc3_]).levelStatus != §true final§.LEVEL_DISABLED)
            {
               if(§true final§(this.game.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED || §true final§(this.game.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW || §true final§(this.game.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_BETTER)
               {
                  this.§use extends§.addChild(new §break const switch§(this,this.§_-dp§[_loc3_],§true final§(this.game.§native import§[_loc3_])));
                  if(§true final§(this.game.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW)
                  {
                     this.flagNew = _loc3_ + 1;
                     this.§_-mz§.progress.text = this.game.starsWon - §true final§(this.game.§native import§[_loc3_]).stars + "/" + this.game.§_-Y1§;
                     this.upgradeStarsAlert.item.txt.text = (this.game.stars - §true final§(this.game.§native import§[_loc3_]).stars).toString();
                     this.§_-2c§ = this.game.starsWon - §true final§(this.game.§native import§[_loc3_]).stars;
                     this.progressCurrentStarsUpgrades = this.game.stars - §true final§(this.game.§native import§[_loc3_]).stars;
                     this.§_-WC§ = FLAG_NEW;
                  }
                  else
                  {
                     _loc1_ = _loc3_ + 1;
                  }
                  if(§true final§(this.game.§native import§[_loc3_]).heroicModeRecently || §true final§(this.game.§native import§[_loc3_]).ironModeRecently)
                  {
                     this.§_-mz§.progress.text = this.game.starsWon - 1 + "/" + this.game.§_-Y1§;
                     this.upgradeStarsAlert.item.txt.text = (this.game.stars - 1).toString();
                     this.§_-WC§ = IRON_HEROIC_NEW;
                  }
                  if(§true final§(this.game.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_BETTER)
                  {
                     this.§_-mz§.progress.text = this.game.starsWon - §true final§(this.game.§native import§[_loc3_]).starsBetter + "/" + this.game.§_-Y1§;
                     this.upgradeStarsAlert.item.txt.text = (this.game.stars - §true final§(this.game.§native import§[_loc3_]).starsBetter).toString();
                     this.§_-2c§ = this.game.starsWon - §true final§(this.game.§native import§[_loc3_]).starsBetter;
                     this.progressCurrentStarsUpgrades = this.game.stars - §true final§(this.game.§native import§[_loc3_]).starsBetter;
                     this.§_-ZA§ = §true final§(this.game.§native import§[_loc3_]).stars;
                     this.§_-KW§ = §true final§(this.game.§native import§[_loc3_]).starsBetter;
                     this.§_-WC§ = FLAG_BETTER;
                  }
               }
               else if(_loc3_ != 0)
               {
                  this.§use extends§.addChild(new §_-H3§(this,this.§_-dp§[_loc3_],§true final§(this.game.§native import§[_loc3_])));
               }
               else
               {
                  this.§_-WC§ = FLAG_FIRST;
               }
            }
            _loc3_++;
         }
         if(_loc1_ > 0)
         {
            this.§_-ag§ = new §_-2p§();
            this.§with const static§.addChild(this.§_-ag§);
            if(_loc1_ == 15)
            {
               _loc1_ = 14;
            }
            this.§_-ag§.gotoAndStop(_loc1_ + "to" + (_loc1_ + 1) + "End");
         }
      }
      
      private function §_-RR§() : Boolean
      {
         if(this.§else switch§ < this.§_-SC§)
         {
            ++this.§else switch§;
            if(this.§else switch§ == 5)
            {
               if(§_-BQ§.levelUpBtnAnim)
               {
                  this.§_-Ck§.heroLevelUp.gotoAndPlay("on");
                  §_-BQ§.levelUpBtnAnim = false;
               }
            }
            if(this.§else switch§ == 5)
            {
               this.§_-mz§.gotoAndPlay("addStar");
               this.§_-mz§.progress.text = this.§_-2c§ + 1 + "/" + this.game.§_-Y1§;
               this.upgradeStarsAlert.item.txt.text = (this.progressCurrentStarsUpgrades + 1).toString();
               ++this.§_-2c§;
               ++this.progressCurrentStarsUpgrades;
               this.game.gameSounds.§_-iQ§("");
            }
            if(this.§else switch§ == 15)
            {
               if(§true final§(this.game.§native import§[this.flagNew - 1]).stars >= 2)
               {
                  this.§_-mz§.gotoAndPlay("addStar");
                  this.§_-mz§.progress.text = this.§_-2c§ + 1 + "/" + this.game.§_-Y1§;
                  this.upgradeStarsAlert.item.txt.text = (this.progressCurrentStarsUpgrades + 1).toString();
                  ++this.§_-2c§;
                  ++this.progressCurrentStarsUpgrades;
                  this.game.gameSounds.§_-iQ§("2");
               }
            }
            if(this.§else switch§ == 25)
            {
               if(§true final§(this.game.§native import§[this.flagNew - 1]).stars == 3)
               {
                  this.§_-mz§.gotoAndPlay("addStar");
                  this.§_-mz§.progress.text = this.§_-2c§ + 1 + "/" + this.game.§_-Y1§;
                  this.upgradeStarsAlert.item.txt.text = (this.progressCurrentStarsUpgrades + 1).toString();
                  ++this.§_-2c§;
                  ++this.progressCurrentStarsUpgrades;
                  this.game.gameSounds.§_-iQ§("3");
               }
            }
            if(this.§else switch§ == 26)
            {
               if(§true final§(this.game.§native import§[this.flagNew - 1]).levelIndex == 0 || §true final§(this.game.§native import§[this.flagNew - 1]).levelIndex > 0 && this.game.stars == this.game.starsWon)
               {
                  this.signAlertUpgrades = new SignAlertUpgrades(new Point(460,366),§true final§(this.game.§native import§[this.flagNew - 1]).stars);
                  this.addChild(this.signAlertUpgrades);
               }
            }
            return false;
         }
         if(!this.§_-dw§)
         {
            if(this.flagNew == 15)
            {
               this.§_-ag§ = new §_-2p§();
               this.§with const static§.addChild(this.§_-ag§);
               this.§_-ag§.gotoAndStop("14to15End");
            }
            else
            {
               if(this.flagNew == 1)
               {
                  this.§_-ag§ = new §_-2p§();
                  this.§with const static§.addChild(this.§_-ag§);
               }
               this.§_-ag§.gotoAndPlay(this.flagNew + "to" + (this.flagNew + 1));
               this.§_-dw§ = true;
               this.§_-Na§ = 0;
            }
         }
         if(this.§_-Na§ < this.§continue for super§[this.flagNew - 1])
         {
            ++this.§_-Na§;
            if(this.§_-Na§ == 1 || this.§_-Na§ % 4 == 0)
            {
               this.game.gameSounds.§_-uF§();
            }
            if(this.§_-Na§ == this.§continue for super§[this.flagNew - 1] - 10)
            {
               this.game.gameSounds.§_-SL§();
            }
            return false;
         }
         §true final§(this.game.§native import§[this.flagNew - 1]).setStatusOnly(§true final§.LEVEL_ENABLED_COMPLETED);
         this.mode = FLAG_NORMAL;
         if(this.flagNew != 15)
         {
            §true final§(this.game.§native import§[this.flagNew]).setStatusOnly(§true final§.LEVEL_ENABLED_UNCOMPLETED_NEW);
            this.§use extends§.addChild(new §_-H3§(this,this.§_-dp§[this.flagNew],§true final§(this.game.§native import§[this.flagNew])));
            this.§_-dw§ = false;
            if(!this.§finally const switch§())
            {
               if(this.flagNew == 3 && this.game.earnTwitterStar == false)
               {
                  if(this.contains(this.socialScreen))
                  {
                     this.socialScreen.§finally const dynamic§();
                  }
               }
            }
         }
         return true;
      }
      
      public function addMapBlock() : void
      {
         if(!this.contains(this.mapBlock))
         {
            this.addChild(this.mapBlock);
         }
         this.mapBlock.show();
      }
      
      public function §finally const switch§() : Boolean
      {
         return this.contains(this.mapBlock);
      }
      
      public function removeMapBlock() : void
      {
         if(this.contains(this.mapBlock))
         {
            this.mapBlock.hide();
         }
      }
      
      public function earnFacebookSocial() : void
      {
         this.§_-mz§.progress.text = this.game.starsWon.toString() + "/" + this.game.§_-Y1§;
         this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
         this.upgradeStarsAlert.visible = true;
         this.game.§const for set§.§import for import§(this.game.starsWon);
         §each const each§.onlineHandler.callQuest("StarsEarned",this.game.starsWon);
      }
      
      public function earnTwitterSocial() : void
      {
         this.§_-mz§.progress.text = this.game.starsWon.toString() + "/" + this.game.§_-Y1§;
         this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
         this.upgradeStarsAlert.visible = true;
         this.game.§const for set§.§import for import§(this.game.starsWon);
         §each const each§.onlineHandler.callQuest("StarsEarned",this.game.starsWon);
      }
      
      public function §_-GK§() : void
      {
         if(this.§_-m3§ != null)
         {
            this.§_-m3§.destroyThis();
         }
         this.§_-m3§ = null;
      }
      
      public function destroySignUpgrades() : void
      {
         if(this.signAlertUpgrades != null)
         {
            this.signAlertUpgrades.destroyThis();
         }
         this.signAlertUpgrades = null;
      }
      
      public function updateStars() : void
      {
         this.§_-mz§.progress.text = this.game.starsWon.toString() + "/" + this.game.§_-Y1§;
         this.upgradeStarsAlert.item.txt.text = this.game.stars.toString();
         this.upgradeStarsAlert.visible = true;
      }
      
      public function §static else§() : void
      {
         §each const each§.onlineHandler.submitSave("slot" + this.game.onlineSelectedSlot.toString(),this.game.§for super§(),this.§function const var§);
      }
      
      public function §function const var§(param1:Object) : void
      {
         if(this.game == null)
         {
            return;
         }
         if(param1.success)
         {
            if(this.contains(this.§extends final§))
            {
               this.removeMapBlock();
               this.§extends final§.destroyThis();
            }
            this.addChild(new §if const import§());
         }
         else if(this.contains(this.§extends final§))
         {
            this.§extends final§.§class function§();
         }
         else
         {
            this.addMapBlock();
            this.addChild(this.§extends final§);
            this.§null const null§ = true;
         }
      }
      
      public function destroyThis() : void
      {
         if(this.socialScreen != null)
         {
            this.socialScreen.destroyThis();
         }
         this.§extends final§.destroyThis();
         this.§_-GK§();
         this.§include package§.destroyThis();
         this.§include package§ = null;
         this.§var for switch§.destroyThis();
         this.§var for switch§ = null;
         this.§_-ou§ = null;
         this.§_-Nx§ = null;
         this.yTweenUpgrades = null;
         this.§null for throw§ = null;
         this.§_-HZ§ = null;
         this.§default const set§ = null;
         this.alphaTweenMenuBack = null;
         this.alphaTweenUpgrades = null;
         this.alphaTweenEncyclopedia = null;
         this.alphaTweenAchievements = null;
         this.alphaTweenPremium = null;
         this.§false final§.removeEventListener(MouseEvent.CLICK,this.§throw while§);
         this.§false final§.removeEventListener(MouseEvent.ROLL_OVER,this.§_-xB§);
         this.§false final§.removeEventListener(MouseEvent.ROLL_OUT,this.§null with§);
         this.§false final§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-ec§);
         this.§false final§.removeEventListener(MouseEvent.MOUSE_UP,this.§const const while§);
         this.btnUpgrades.removeEventListener(MouseEvent.CLICK,this.clickUpgrades);
         this.btnUpgrades.removeEventListener(MouseEvent.ROLL_OVER,this.rollOverUpgrades);
         this.btnUpgrades.removeEventListener(MouseEvent.ROLL_OUT,this.rollOutUpgrades);
         this.btnUpgrades.removeEventListener(MouseEvent.MOUSE_DOWN,this.mouseDownUpgrades);
         this.btnUpgrades.removeEventListener(MouseEvent.MOUSE_UP,this.mouseUpUpgrades);
         this.§_-tQ§.removeEventListener(MouseEvent.CLICK,this.§_-EN§);
         this.§_-tQ§.removeEventListener(MouseEvent.ROLL_OVER,this.§_-oe§);
         this.§_-tQ§.removeEventListener(MouseEvent.ROLL_OUT,this.§_-dd§);
         this.§_-tQ§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§finally in§);
         this.§_-tQ§.removeEventListener(MouseEvent.MOUSE_UP,this.§_-xW§);
         this.§_-sc§.removeEventListener(MouseEvent.CLICK,this.§_-Br§);
         this.§_-sc§.removeEventListener(MouseEvent.ROLL_OVER,this.§import function§);
         this.§_-sc§.removeEventListener(MouseEvent.ROLL_OUT,this.§_-yM§);
         this.§_-sc§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§final try§);
         this.§_-sc§.removeEventListener(MouseEvent.MOUSE_UP,this.§function package§);
         this.§package const include§.removeChild(this.btnUpgrades);
         this.§package const include§.removeChild(this.§_-tQ§);
         this.§package const include§.removeChild(this.§_-sc§);
         this.§package const include§.removeChild(this.§false final§);
         this.§package const include§.removeChild(this.§_-Ck§);
         this.btnUpgrades = null;
         this.§_-Ck§ = null;
         this.§_-tQ§ = null;
         this.§_-sc§ = null;
         this.§false final§ = null;
         this.upgradeStarsAlert = null;
         this.§continue for super§ = null;
         this.terrain = null;
         this.§package const include§ = null;
         this.§with const static§ = null;
         this.§use extends§ = null;
         this.§_-dp§ = null;
         this.game = null;
         this.removeMapBlock();
         this.mapBlock = null;
         this.§finally const finally§ = null;
         this.§_-1C§ = null;
         this.removeEventListener(Event.ENTER_FRAME,this.eFrameEvents);
         this.parent.removeChild(this);
      }
      
      private function §finally for catch§() : void
      {
         var _loc3_:int = 0;
         var _loc4_:§true final§ = null;
         var _loc5_:Boolean = false;
         var _loc1_:Boolean = true;
         var _loc2_:int = 15;
         if(!this.game.§const for set§.greatDefender)
         {
            _loc1_ = true;
            _loc3_ = 0;
            while(_loc3_ < _loc2_)
            {
               _loc4_ = this.game.§native import§[_loc3_];
               if(!_loc4_.isCampaignWin() || _loc4_.campaignDifficulty == §_-Mm§.DIFFICULTY_EASY)
               {
                  _loc1_ = false;
                  break;
               }
               _loc3_++;
            }
            if(_loc1_)
            {
               this.game.§const for set§.§static var§(null);
            }
         }
         if(!this.game.§const for set§.supremeDefender)
         {
            _loc5_ = true;
            _loc3_ = 0;
            while(_loc3_ < _loc2_)
            {
               _loc4_ = this.game.§native import§[_loc3_];
               if(!_loc4_.isCampaignWin() || _loc4_.campaignDifficulty != §_-Mm§.DIFFICULTY_HARD)
               {
                  _loc5_ = false;
                  break;
               }
               _loc3_++;
            }
            if(_loc5_)
            {
               this.game.§const for set§.§try const else§(null);
            }
         }
         if(!this.game.§const for set§.greatDefenderHeroic)
         {
            _loc1_ = true;
            _loc3_ = 0;
            while(_loc3_ < _loc2_)
            {
               _loc4_ = this.game.§native import§[_loc3_];
               if(!_loc4_.heroicModeWin || _loc4_.heroicDifficulty == §_-Mm§.DIFFICULTY_EASY)
               {
                  _loc1_ = false;
                  break;
               }
               _loc3_++;
            }
            if(_loc1_)
            {
               this.game.§const for set§.chkGreatDefenderHeroic(null);
            }
         }
         if(!this.game.§const for set§.greatDefenderIron)
         {
            _loc1_ = true;
            _loc3_ = 0;
            while(_loc3_ < _loc2_)
            {
               _loc4_ = this.game.§native import§[_loc3_];
               if(!_loc4_.ironModeWin || _loc4_.ironDifficulty == §_-Mm§.DIFFICULTY_EASY)
               {
                  _loc1_ = false;
                  break;
               }
               _loc3_++;
            }
            if(_loc1_)
            {
               this.game.§const for set§.chkGreatDefenderIron(null);
            }
         }
      }
   }
}

