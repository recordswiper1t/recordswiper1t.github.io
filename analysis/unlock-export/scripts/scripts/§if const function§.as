package
{
   import §_-uz§.*;
   import com.greensock.*;
   import fl.transitions.*;
   import fl.transitions.easing.*;
   import flash.display.MovieClip;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.text.TextField;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol8018")]
   public class §if const function§ extends §extends const true§
   {
      
      public static const UNLOCK_STAGE_MIRAGE:Number = 3;
      
      public static const UNLOCK_STAGE_CRONAN:Number = 6;
      
      public static var SKU_NIVUS:String = "krf-hero_nivus";
      
      public static var SKU_ASHBITE:String = "krf-hero_ashbite";
      
      public static var SKU_SHATRA:String = "krf-hero_shatra";
      
      public static var SKU_GRAWL:String = "krf-hero_grawl";
      
      public static var SKU_DIERDRE:String = "krf-hero_dierdre";
      
      public static var SKU_CAPTAIN:String = "krf-hero_captain";
      
      public var skillPoints:TextField;
      
      public var §continue for false§:TextField;
      
      public var armor:TextField;
      
      public var attackIcon:MovieClip;
      
      public var §_-Bk§:TextField;
      
      public var §extends const use§:MovieClip;
      
      public var health:TextField;
      
      public var §try do§:MovieClip;
      
      public var bigPortraitGlowFast:MovieClip;
      
      public var heroClass:TextField;
      
      public var bigPortraitGlowSlow:MovieClip;
      
      public var heroLevel:MovieClip;
      
      public var damage:TextField;
      
      public var speed:TextField;
      
      public var butTrain:MovieClip;
      
      public var butSubmit:MovieClip;
      
      public var bigPortraits:MovieClip;
      
      public var helpBubble0:§import in§;
      
      public var helpBubble1:§_-bO§;
      
      public var game:§_-BQ§;
      
      public var §_-hr§:Sprite;
      
      public var selectedHero:Object;
      
      public var selectedPortrait:Object;
      
      public var §_-y5§:Object;
      
      public var §_-l5§:§var const continue§;
      
      public var §_-xT§:§_-Mm§;
      
      public var §use const else§:§var const continue§;
      
      public var skill1:§var const continue§;
      
      public var skill2:§var const continue§;
      
      public var skill3:§var const continue§;
      
      public var skill4:§var const continue§;
      
      public var skill5:§var const continue§;
      
      public var skillBoxArray:Array;
      
      public var portraitAlric:§_-re§;
      
      public var portraitMirage:§_-re§;
      
      public var portraitCronan:§_-re§;
      
      public var portraitCaptain:§_-re§;
      
      public var portraitNivus:§_-re§;
      
      public var portraitDierdre:§_-re§;
      
      public var portraitGrawl:§_-re§;
      
      public var §case const function§:§_-re§;
      
      public var portraitAshbite:§_-re§;
      
      public var PortraitArray:Array;
      
      public var skillBarArray1:Array;
      
      public var skillBarArray2:Array;
      
      public var skillBarArray3:Array;
      
      public var skillBarArray4:Array;
      
      public var skillBarArray5:Array;
      
      private var frame:§_-ov§;
      
      protected var ytween:Tween;
      
      protected var §_-T8§:Tween;
      
      private var overButtonTrain:Boolean;
      
      private var §_-R9§:Boolean;
      
      private var dark:§static function§;
      
      public var §with for dynamic§:MovieClip;
      
      private var §_-g2§:Boolean;
      
      public var onlinePurchaseWarning:§_-lS§;
      
      public var isActive:Boolean = true;
      
      public function §if const function§(param1:§_-BQ§)
      {
         super();
         this.game = param1;
         this.x = 400;
         this.y = 10;
         this.§_-xT§ = new §_-Mm§(this.game,false);
         this.ytween = new Tween(this,"y",Strong.easeOut,-550,5,0.5,true);
         this.selectedHero = this.game.gameHeroData.selectedHero;
         this.bigPortraits.gotoAndStop(this.selectedHero.name);
         this.heroLevel.gotoAndStop(this.selectedHero.level);
         this.heroClass.text = this.selectedHero.heroClass;
         this.§_-Pe§(this.selectedHero);
         this.§_-1Z§(this.selectedHero);
         this.§_-aP§(this.selectedHero);
         this.speed.text = this.selectedHero.speed;
         this.skillPoints.text = this.selectedHero.skillPoints;
         this.§use const else§ = new §var const continue§(this.selectedHero.skillKey1,this.selectedHero.skill1,58,277,true,0,this);
         this.skill1 = new §var const continue§(this.selectedHero.skillKey1,this.selectedHero.skill1,52,448,false,this.selectedHero.skill1.cost[this.selectedHero.skill1.level],this);
         this.skill2 = new §var const continue§(this.selectedHero.skillKey2,this.selectedHero.skill2,113,448,false,this.selectedHero.skill2.cost[this.selectedHero.skill2.level],this);
         this.skill3 = new §var const continue§(this.selectedHero.skillKey3,this.selectedHero.skill3,175,448,false,this.selectedHero.skill3.cost[this.selectedHero.skill3.level],this);
         this.skill4 = new §var const continue§(this.selectedHero.skillKey4,this.selectedHero.skill4,236,448,false,this.selectedHero.skill4.cost[this.selectedHero.skill4.level],this);
         this.skill5 = new §var const continue§(this.selectedHero.skillKey5,this.selectedHero.skill5,297,448,false,this.selectedHero.skill5.cost[this.selectedHero.skill5.level],this);
         this.skillBoxArray = [this.skill1,this.skill2,this.skill3,this.skill4,this.skill5];
         this.addChild(this.§use const else§);
         this.addChild(this.skill1);
         this.addChild(this.skill2);
         this.addChild(this.skill3);
         this.addChild(this.skill4);
         this.addChild(this.skill5);
         this.portraitAlric = new §_-re§(this.game.gameHeroData.heroAlric,-272,135,this);
         this.portraitMirage = new §_-re§(this.game.gameHeroData.heroMirage,-204,135,this);
         this.portraitCronan = new §_-re§(this.game.gameHeroData.heroCronan,-136,135,this);
         this.portraitCaptain = new §_-re§(this.game.gameHeroData.heroCaptain,-68,135,this);
         this.portraitNivus = new §_-re§(this.game.gameHeroData.heroNivus,0,135,this);
         this.portraitDierdre = new §_-re§(this.game.gameHeroData.heroDierdre,68,135,this);
         this.portraitGrawl = new §_-re§(this.game.gameHeroData.heroGrawl,136,135,this);
         this.§case const function§ = new §_-re§(this.game.gameHeroData.heroShatra,204,135,this);
         this.portraitAshbite = new §_-re§(this.game.gameHeroData.heroAshbite,272,135,this);
         this.PortraitArray = [this.portraitAlric,this.portraitMirage,this.portraitCronan,this.portraitCaptain,this.portraitNivus,this.portraitDierdre,this.portraitGrawl,this.§case const function§,this.portraitAshbite];
         this.addChild(this.portraitAlric);
         this.addChild(this.portraitMirage);
         this.addChild(this.portraitCronan);
         this.addChild(this.portraitCaptain);
         this.addChild(this.portraitNivus);
         this.addChild(this.portraitDierdre);
         this.addChild(this.portraitGrawl);
         this.addChild(this.§case const function§);
         this.addChild(this.portraitAshbite);
         this.frame = new §_-ov§(-1,136);
         this.addChild(this.frame);
         this.§package use§();
         this.§_-c8§();
         this.deselectAllSkillBoxes();
         this.skill1.select();
         switch(this.selectedHero.name)
         {
            case "alric":
               this.portraitAlric.§_-2B§();
               this.portraitAlric.select();
               break;
            case "mirage":
               this.portraitMirage.§_-2B§();
               this.portraitMirage.select();
               break;
            case "cronan":
               this.portraitCronan.§_-2B§();
               this.portraitCronan.select();
               break;
            case "captain":
               this.portraitCaptain.§_-2B§();
               this.portraitCaptain.select();
               break;
            case "nivus":
               this.portraitNivus.§_-2B§();
               this.portraitNivus.select();
               break;
            case "dierdre":
               this.portraitDierdre.§_-2B§();
               this.portraitDierdre.select();
               break;
            case "grawl":
               this.portraitGrawl.§_-2B§();
               this.portraitGrawl.select();
               break;
            case "shatra":
               this.§case const function§.§_-2B§();
               this.§case const function§.select();
               break;
            case "ashbite":
               this.portraitAshbite.§_-2B§();
               this.portraitAshbite.select();
         }
         this.butSubmit.addEventListener(MouseEvent.CLICK,this.§dynamic in§,false,0,true);
         this.butSubmit.addEventListener(MouseEvent.ROLL_OVER,this.§const extends§,false,0,true);
         this.butSubmit.addEventListener(MouseEvent.ROLL_OUT,this.§finally for false§,false,0,true);
         this.butSubmit.addEventListener(MouseEvent.MOUSE_DOWN,this.§_-cb§,false,0,true);
         this.butSubmit.addEventListener(MouseEvent.MOUSE_UP,this.§_-R5§,false,0,true);
         this.§try do§.addEventListener(MouseEvent.CLICK,this.§const const return§,false,0,true);
         this.§try do§.addEventListener(MouseEvent.ROLL_OUT,this.§native false§,false,0,true);
         this.§try do§.addEventListener(MouseEvent.ROLL_OVER,this.§_-9C§,false,0,true);
         this.§try do§.addEventListener(MouseEvent.MOUSE_DOWN,this.ButtonSelectMouseDown,false,0,true);
         this.§with for dynamic§.gotoAndStop("idle");
         this.§try do§.gotoAndStop("selected");
         this.§try do§.price.visible = false;
         this.butSubmit.gotoAndStop("idle");
         this.butTrain.gotoAndStop("idle");
         this.§with for dynamic§.addEventListener(MouseEvent.CLICK,this.resetButton,false,0,true);
         this.§with for dynamic§.addEventListener(MouseEvent.ROLL_OVER,this.§false const default§,false,0,true);
         this.§with for dynamic§.addEventListener(MouseEvent.ROLL_OUT,this.§_-2J§,false,0,true);
         this.§with for dynamic§.addEventListener(MouseEvent.MOUSE_DOWN,this.§in const switch§,false,0,true);
         this.§with for dynamic§.addEventListener(MouseEvent.MOUSE_UP,this.§_-F7§,false,0,true);
         this.butTrain.addEventListener(MouseEvent.CLICK,this.§break const case§,false,0,true);
         this.butTrain.addEventListener(MouseEvent.ROLL_OVER,this.§continue const return§,false,0,true);
         this.butTrain.addEventListener(MouseEvent.ROLL_OUT,this.§_-a0§,false,0,true);
         this.butTrain.addEventListener(MouseEvent.MOUSE_DOWN,this.ButtonTrainMouseDown,false,0,true);
         this.butTrain.addEventListener(MouseEvent.MOUSE_UP,this.ButtonTrainMouseUp,false,0,true);
         if(this.game.lastLevelWon < 1 && !this.game.bubblesShowed)
         {
            this.dark = new §static function§(0,-5);
            this.addChild(this.dark);
            this.dark.addEventListener(MouseEvent.CLICK,this.§static for for§,false,0,true);
            this.helpBubble0 = new §import in§(-264,534);
            this.helpBubble1 = new §_-bO§(174,392);
            this.addChild(this.helpBubble0);
            this.addChild(this.helpBubble1);
            this.helpBubble0.addEventListener(MouseEvent.CLICK,this.§static for for§,false,0,true);
            this.helpBubble1.addEventListener(MouseEvent.CLICK,this.§static for for§,false,0,true);
            this.game.bubblesShowed = true;
         }
         this.§false const function§(this.selectedHero);
      }
      
      public function §_-HD§() : void
      {
         this.onlinePurchaseWarning = new §_-lS§(this);
         this.addChild(this.onlinePurchaseWarning);
      }
      
      protected function disableResetButton() : void
      {
         this.§_-g2§ = false;
         this.§with for dynamic§.alpha = 0.3;
      }
      
      protected function enableResetButton() : void
      {
         this.§_-g2§ = true;
         this.§with for dynamic§.alpha = 1;
      }
      
      public function §static for for§(param1:Event) : void
      {
         this.dark.visible = false;
         this.dark.removeEventListener(MouseEvent.CLICK,this.§static for for§);
         this.removeChild(this.dark);
         this.helpBubble1.removeEventListener(MouseEvent.CLICK,this.§static for for§);
         this.helpBubble0.removeEventListener(MouseEvent.CLICK,this.§static for for§);
         this.closeBubbles();
      }
      
      public function closeBubbles() : void
      {
         this.helpBubble0.destroyThis();
         this.helpBubble1.destroyThis();
      }
      
      public function levelUp() : void
      {
         trace("?");
         if(this.selectedPortrait.hero.level < 10)
         {
            this.selectedPortrait.hero.level += 1;
         }
         else
         {
            this.selectedPortrait.hero.level = 1;
         }
         this.§false const function§(this.selectedHero);
      }
      
      public function §use const class§(param1:Object) : void
      {
         var _loc2_:Object = null;
         if(this.game.lastLevelWon < UNLOCK_STAGE_MIRAGE && param1.name == "mirage")
         {
            this.§try do§.gotoAndStop("unlock4");
            this.§_-R9§ = false;
         }
         if(this.game.lastLevelWon < UNLOCK_STAGE_CRONAN && param1.name == "cronan")
         {
            this.§try do§.gotoAndStop("unlock7");
            this.§_-R9§ = false;
         }
         if(this.checkPremiumContent(param1.name))
         {
            if(§each const each§.heroPrices != null && this.game.§_-yX§ || §each const each§.heroPrices != null && §each const each§.onlineHandler.getService() == §each const each§.SERVICE_FACEBOOK)
            {
               _loc2_ = §each const each§.heroPrices[this.§_-UU§(param1.name)];
               this.§try do§.gotoAndStop("getNow");
               if(_loc2_ == null)
               {
                  this.§try do§.price.text = "";
               }
               else
               {
                  this.§try do§.price.text = "$" + Number(_loc2_);
               }
               this.§try do§.price.visible = true;
            }
            else if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE)
            {
               this.§try do§.gotoAndStop("getNowKong");
            }
            else if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_CHROME)
            {
               this.§try do§.gotoAndStop("getMobile");
            }
            else
            {
               this.§try do§.gotoAndStop("onlyPremium");
            }
            this.§_-R9§ = false;
         }
      }
      
      public function checkPremiumContent(param1:String) : Boolean
      {
         switch(param1)
         {
            case "captain":
               return §each const each§.purchasedHeroes.indexOf(SKU_CAPTAIN) < 0;
            case "nivus":
               return §each const each§.purchasedHeroes.indexOf(SKU_NIVUS) < 0;
            case "dierdre":
               return §each const each§.purchasedHeroes.indexOf(SKU_DIERDRE) < 0;
            case "grawl":
               return §each const each§.purchasedHeroes.indexOf(SKU_GRAWL) < 0;
            case "shatra":
               return §each const each§.purchasedHeroes.indexOf(SKU_SHATRA) < 0;
            case "ashbite":
               return §each const each§.purchasedHeroes.indexOf(SKU_ASHBITE) < 0;
            case "cronan":
               return false;
            case "mirage":
               return false;
            case "alric":
               return false;
            default:
               return true;
         }
      }
      
      private function §native false§(param1:MouseEvent) : void
      {
         this.§try do§.useHandCursor = true;
         if(this.§_-R9§)
         {
            this.§try do§.gotoAndStop("select");
         }
         if(this.§try do§.currentFrameLabel == "getNowOver")
         {
            this.§try do§.gotoAndStop("getNow");
            this.§try do§.price.textColor = 4401152;
         }
         if(this.§try do§.currentFrameLabel == "getNowKongOver")
         {
            this.§try do§.gotoAndStop("getNowKong");
            this.§try do§.price.textColor = 4401152;
         }
         if(this.§try do§.currentFrameLabel == "getMobileOver")
         {
            this.§try do§.gotoAndStop("getMobile");
         }
      }
      
      protected function ButtonSelectMouseDown(param1:MouseEvent) : void
      {
         if(this.§_-R9§)
         {
            this.§try do§.useHandCursor = false;
         }
      }
      
      private function §_-9C§(param1:MouseEvent) : void
      {
         if(this.§_-R9§)
         {
            this.§try do§.buttonMode = true;
            this.§try do§.mouseChildren = false;
            this.§try do§.useHandCursor = true;
            this.§try do§.gotoAndStop("selectOver");
         }
         else if(this.§try do§.currentFrameLabel == "getNow")
         {
            this.§try do§.buttonMode = true;
            this.§try do§.mouseChildren = false;
            this.§try do§.useHandCursor = true;
            this.§try do§.gotoAndStop("getNowOver");
            this.§try do§.price.textColor = 16777215;
         }
         else if(this.§try do§.currentFrameLabel == "getNowKong")
         {
            this.§try do§.buttonMode = true;
            this.§try do§.mouseChildren = false;
            this.§try do§.useHandCursor = true;
            this.§try do§.gotoAndStop("getNowKongOver");
            this.§try do§.price.textColor = 16777215;
         }
         else if(this.§try do§.currentFrameLabel == "getMobile")
         {
            this.§try do§.buttonMode = true;
            this.§try do§.mouseChildren = false;
            this.§try do§.useHandCursor = true;
            this.§try do§.gotoAndStop("getMobileOver");
         }
         else
         {
            this.§try do§.buttonMode = false;
         }
      }
      
      protected function §in const switch§(param1:MouseEvent) : void
      {
         if(this.§with for dynamic§.alpha == 1)
         {
            this.§with for dynamic§.useHandCursor = false;
            this.§with for dynamic§.gotoAndStop("press");
         }
      }
      
      protected function §_-F7§(param1:MouseEvent) : void
      {
         this.§with for dynamic§.gotoAndStop("idle");
      }
      
      protected function §false const default§(param1:MouseEvent) : void
      {
         if(this.§with for dynamic§.alpha == 1)
         {
            this.game.gameSounds.§break const null§();
            this.§with for dynamic§.buttonMode = true;
            this.§with for dynamic§.mouseChildren = false;
            this.§with for dynamic§.useHandCursor = true;
            this.§with for dynamic§.gotoAndStop("over");
         }
      }
      
      protected function §_-2J§(param1:MouseEvent) : void
      {
         this.§with for dynamic§.useHandCursor = false;
         this.§with for dynamic§.gotoAndStop("idle");
      }
      
      protected function §_-cb§(param1:MouseEvent) : void
      {
         this.butSubmit.gotoAndStop("press");
      }
      
      protected function §_-R5§(param1:MouseEvent) : void
      {
         this.butSubmit.gotoAndStop("idle");
      }
      
      public function §continue const return§(param1:Event) : void
      {
         if(this.butTrain.currentFrameLabel != "off")
         {
            this.butTrain.buttonMode = true;
            this.butTrain.mouseChildren = false;
            this.butTrain.useHandCursor = true;
            this.butTrain.gotoAndStop("on");
         }
         else
         {
            this.butTrain.enabled = false;
            this.butTrain.useHandCursor = false;
         }
      }
      
      public function §_-a0§(param1:Event) : void
      {
         this.butTrain.useHandCursor = false;
         if(this.butTrain.currentFrameLabel != "off")
         {
            this.butTrain.gotoAndStop("idle");
         }
      }
      
      protected function ButtonTrainMouseDown(param1:MouseEvent) : void
      {
         if(this.butTrain.currentFrameLabel == "on")
         {
            this.butTrain.gotoAndStop("press");
         }
      }
      
      protected function ButtonTrainMouseUp(param1:MouseEvent) : void
      {
      }
      
      public function §break const case§(param1:Event) : void
      {
         if(this.§_-y5§.cost[this.§_-y5§.level] != 0 && this.selectedPortrait.hero.skillPoints >= this.§_-y5§.cost[this.§_-y5§.level] && this.§_-y5§.level < 3 && this.butTrain.currentFrameLabel != "off")
         {
            this.game.gameSounds.§_-ql§();
            this.selectedPortrait.hero.skillPoints -= this.§_-y5§.cost[this.§_-y5§.level];
            ++this.§_-y5§.level;
            this.updateSkill(this.§_-y5§);
            this.skillPoints.text = this.selectedPortrait.hero.skillPoints;
            this.updateBars();
            this.updateTrainButton();
            this.§_-l5§.§in const§.play();
            this.game.§_-6X§.§_-8I§();
            this.§_-aP§(this.selectedPortrait.hero);
            this.§_-Pe§(this.selectedPortrait.hero);
            this.§_-1Z§(this.selectedPortrait.hero);
            this.enableResetButton();
         }
      }
      
      public function updateTrainButton() : void
      {
         if(this.selectedPortrait == null)
         {
            this.selectedPortrait = new Object();
            this.selectedPortrait.hero = this.selectedHero;
         }
         if(this.selectedPortrait.hero.skillPoints == 0 || this.§_-y5§.level >= 3 || this.selectedPortrait.hero.skillPoints < this.§_-y5§.cost[this.§_-y5§.level])
         {
            this.butTrain.enabled = false;
            this.butTrain.useHandCursor = false;
            this.butTrain.gotoAndStop("off");
         }
         else
         {
            this.butTrain.gotoAndStop("on");
         }
         this.updateResetButton();
      }
      
      public function updateTrainButtonReset() : void
      {
         if(this.selectedPortrait == null)
         {
            this.selectedPortrait = new Object();
            this.selectedPortrait.hero = this.selectedHero;
         }
         var _loc1_:* = this.selectedPortrait.hero;
         if(_loc1_.skillPoints == 0 || this.§_-y5§.level >= 3 || _loc1_.skillPoints < this.§_-y5§.cost[this.§_-y5§.level] || _loc1_.name == "mirage" && this.game.lastLevelWon < UNLOCK_STAGE_MIRAGE || _loc1_.name == "cronan" && this.game.lastLevelWon < UNLOCK_STAGE_CRONAN || this.§try do§.currentFrameLabel == "onlyPremium" || this.§try do§.currentFrameLabel == "getNow" || this.§try do§.currentFrameLabel == "getNowKong" || this.§try do§.currentFrameLabel == "getMobile")
         {
            this.butTrain.useHandCursor = false;
            this.butTrain.gotoAndStop("off");
         }
         else
         {
            this.butTrain.enabled = true;
            this.butTrain.gotoAndStop("idle");
         }
      }
      
      public function updateBars() : void
      {
         var _loc1_:§var const continue§ = null;
         for each(_loc1_ in this.skillBoxArray)
         {
            _loc1_.updateBars();
            _loc1_.updateCosts();
         }
      }
      
      public function §const const return§(param1:Event) : void
      {
         if(this.§try do§.currentFrameLabel == "selectOver")
         {
            this.game.gameSounds.§true for use§();
            this.§_-R9§ = false;
            this.updateSelectButton(this.selectedHero);
            this.§package use§();
            this.selectedHero = this.selectedPortrait.hero;
            switch(this.selectedHero.name)
            {
               case "alric":
                  this.portraitAlric.§_-2B§();
                  this.portraitAlric.select();
                  break;
               case "mirage":
                  this.portraitMirage.§_-2B§();
                  this.portraitMirage.select();
                  break;
               case "cronan":
                  this.portraitCronan.§_-2B§();
                  this.portraitCronan.select();
                  break;
               case "captain":
                  this.portraitCaptain.§_-2B§();
                  this.portraitCaptain.select();
                  break;
               case "nivus":
                  this.portraitNivus.§_-2B§();
                  this.portraitNivus.select();
                  break;
               case "dierdre":
                  this.portraitDierdre.§_-2B§();
                  this.portraitDierdre.select();
                  break;
               case "grawl":
                  this.portraitGrawl.§_-2B§();
                  this.portraitGrawl.select();
                  break;
               case "shatra":
                  this.§case const function§.§_-2B§();
                  this.§case const function§.select();
                  break;
               case "ashbite":
                  this.portraitAshbite.§_-2B§();
                  this.portraitAshbite.select();
            }
            this.game.gameHeroData.selectedHero = this.selectedHero;
            this.game.§_-6X§.§_-Ck§.hero_icon.gotoAndStop(this.game.gameHeroData.selectedHero.name);
            this.bigPortraitGlowSlow.gotoAndPlay(2);
            this.game.§_-6X§.§_-8I§();
            this.§throw const if§();
         }
         else if(this.checkPremiumContent(this.selectedPortrait.hero.name))
         {
            if(§each const each§.onlineHandler.isLoggedIn() && this.game.§_-yX§ || (§each const each§.onlineHandler.isLoggedIn() && §each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE || §each const each§.onlineHandler.getService() == §each const each§.SERVICE_FACEBOOK))
            {
               §each const each§.onlineHandler.showSingleHeroStoreForSku(this.§_-UU§(this.selectedPortrait.hero.name),this);
            }
            else if(!§each const each§.onlineHandler.isLoggedIn() && (§each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE || §each const each§.onlineHandler.getService() == §each const each§.SERVICE_CHROME))
            {
               §each const each§.onlineHandler.openLogin();
            }
         }
      }
      
      public function §_-UU§(param1:String) : String
      {
         switch(param1)
         {
            case "captain":
               return SKU_CAPTAIN;
            case "nivus":
               return SKU_NIVUS;
            case "dierdre":
               return SKU_DIERDRE;
            case "grawl":
               return SKU_GRAWL;
            case "shatra":
               return SKU_SHATRA;
            case "ashbite":
               return SKU_ASHBITE;
            default:
               return;
         }
      }
      
      public function updateSelectButton(param1:Object) : void
      {
         this.§try do§.price.visible = false;
         if(this.selectedHero.name != param1.name)
         {
            this.§_-R9§ = true;
            this.§try do§.gotoAndStop("select");
            this.§try do§.useHandCursor = true;
            this.§use const class§(param1);
         }
         else
         {
            this.§_-R9§ = false;
            this.§try do§.gotoAndStop("selected");
            this.§try do§.useHandCursor = false;
         }
      }
      
      public function updateResetButton() : void
      {
         var _loc1_:int = this.§_-Mn§();
         if(_loc1_ > 0)
         {
            this.enableResetButton();
         }
         else
         {
            this.disableResetButton();
         }
      }
      
      public function §false const function§(param1:Object) : void
      {
         this.updateSelectButton(param1);
         var _loc2_:int = int(this.§_-xT§.heroes.heroesSavageMasterTable.common_tables.master_xp[param1.level - 1]);
         var _loc3_:int = this.§_-xT§.heroes.heroesSavageMasterTable.common_tables.master_xp[param1.level] - _loc2_;
         if(param1.level == 10)
         {
            this.§extends const use§.scaleX = 1;
         }
         else
         {
            this.§extends const use§.scaleX = 1 - (_loc3_ - (param1.xp - _loc2_)) / _loc3_;
         }
         this.bigPortraitGlowFast.gotoAndPlay(2);
         this.bigPortraits.gotoAndStop(param1.name);
         this.heroLevel.gotoAndStop(param1.level);
         this.heroClass.text = param1.heroClass;
         this.§_-Pe§(param1);
         this.§_-1Z§(param1);
         this.§_-aP§(param1);
         this.speed.text = param1.speed;
         this.skillPoints.text = param1.skillPoints;
         this.attackIcon.gotoAndStop(param1.type);
         this.§_-Bk§.text = param1.skill1.name[param1.skill1.level];
         this.§continue for false§.text = param1.skill1.description[param1.skill1.level];
         this.§use const else§.updateInfo(param1.skillKey1,param1.skill1,true,param1.skill1.cost[param1.skill1.level]);
         this.skill1.updateInfo(param1.skillKey1,param1.skill1,false,param1.skill1.cost[param1.skill1.level]);
         this.skill2.updateInfo(param1.skillKey2,param1.skill2,false,param1.skill2.cost[param1.skill2.level]);
         this.skill3.updateInfo(param1.skillKey3,param1.skill3,false,param1.skill3.cost[param1.skill3.level]);
         this.skill4.updateInfo(param1.skillKey4,param1.skill4,false,param1.skill4.cost[param1.skill4.level]);
         this.skill5.updateInfo(param1.skillKey5,param1.skill5,false,param1.skill5.cost[param1.skill5.level]);
         this.deselectAllSkillBoxes();
         this.skill1.select();
         this.updateBars();
         this.updateResetButton();
      }
      
      public function §_-c8§() : void
      {
         var _loc1_:§_-re§ = null;
         for each(_loc1_ in this.PortraitArray)
         {
            _loc1_.deSelect();
         }
      }
      
      public function §throw const if§() : void
      {
         switch(this.selectedPortrait.hero.name)
         {
            case "alric":
               this.game.gameSounds.§catch if§();
               break;
            case "mirage":
               this.game.gameSounds.§_-uY§();
               break;
            case "captain":
               this.game.gameSounds.§case catch§();
               break;
            case "dierdre":
               this.game.gameSounds.§case for§();
               break;
            case "pirate":
               this.game.gameSounds.§case catch§();
               break;
            case "grawl":
               this.game.gameSounds.§_-1O§();
               break;
            case "shatra":
               this.game.gameSounds.§function native§();
               break;
            case "nivus":
               this.game.gameSounds.§dynamic for use§();
               break;
            case "ashbite":
               this.game.gameSounds.§_-YN§();
               break;
            case "cronan":
               this.game.gameSounds.§var const var§();
         }
      }
      
      public function §_-aP§(param1:Object) : void
      {
         var _loc5_:* = undefined;
         var _loc2_:* = this.§_-xT§.heroes.heroArray[param1.number];
         var _loc3_:Number = Number(_loc2_.minDamage[param1.level - 1]);
         var _loc4_:Number = Number(_loc2_.maxDamage[param1.level - 1]);
         if((param1.name == "alric" || param1.name == "captain") && param1.skill1.level != 0)
         {
            _loc3_ += _loc2_.swordsmanshipExtraDamage[param1.skill1.level - 1];
            _loc4_ += _loc2_.swordsmanshipExtraDamage[param1.skill1.level - 1];
         }
         else if(param1.name == "nivus")
         {
            if(param1.skill5.level != 0)
            {
               _loc3_ = _loc2_.minRangeDamage[param1.level - 1] + _loc2_.arcaneFocusSkill.damageIncrease[param1.skill5.level - 1];
               _loc4_ = _loc2_.maxRangeDamage[param1.level - 1] + _loc2_.arcaneFocusSkill.damageIncrease[param1.skill5.level - 1];
            }
            else
            {
               _loc3_ = Number(_loc2_.minRangeDamage[param1.level - 1]);
               _loc4_ = Number(_loc2_.maxRangeDamage[param1.level - 1]);
            }
         }
         else if(param1.name == "shatra" && param1.skill4.level != 0)
         {
            _loc5_ = _loc2_.vibroBladesSkill;
            _loc3_ += _loc5_.damage[param1.skill4.level - 1];
            _loc4_ += _loc5_.damage[param1.skill4.level - 1];
         }
         this.damage.text = _loc3_.toString() + "-" + _loc4_.toString();
      }
      
      public function §_-Pe§(param1:Object) : void
      {
         var _loc3_:Number = NaN;
         var _loc2_:Number = Number(this.§_-xT§.heroes.heroArray[param1.number].health[param1.level - 1]);
         if(param1.name == "alric" && param1.skill3.level != 0 || param1.name == "captain" && param1.skill3.level != 0)
         {
            _loc3_ = _loc2_ + this.§_-xT§.heroes.heroArray[param1.number].toughnessHealthPoints[param1.skill3.level - 1];
         }
         else if(param1.name == "grawl" && param1.skill5.level != 0)
         {
            _loc3_ = _loc2_ + this.§_-xT§.heroes.heroArray[param1.number].hardRockSkill.extraHealth[param1.skill5.level - 1];
         }
         else if(param1.name == "dierdre" && param1.skill5.level != 0)
         {
            _loc3_ = _loc2_ + this.§_-xT§.heroes.heroArray[param1.number].divineHealthSkill.extraHealth[param1.skill5.level - 1];
         }
         else
         {
            _loc3_ = _loc2_;
         }
         this.health.text = _loc3_;
      }
      
      public function §_-1Z§(param1:Object) : void
      {
         var _loc2_:String = param1.armor;
         if(param1.name == "dierdre" && param1.skill4.level != 0)
         {
            switch(param1.skill4.level)
            {
               case 1:
                  _loc2_ = "Low";
                  break;
               case 2:
                  _loc2_ = "Medium";
                  break;
               case 3:
                  _loc2_ = "High";
            }
         }
         if(param1.name == "alric")
         {
            if(param1.level < 4)
            {
               this.armor.text = "Low";
            }
            if(param1.level < 10 && param1.level >= 4)
            {
               this.armor.text = "Medium";
            }
            if(param1.level == 10)
            {
               this.armor.text = "High";
            }
            return;
         }
         if(param1.name == "grawl")
         {
            if(param1.level < 4)
            {
               this.armor.text = "Low";
            }
            if(param1.level >= 4)
            {
               this.armor.text = "Medium";
            }
            return;
         }
         if(param1.name == "grawl")
         {
            if(param1.level < 4)
            {
               this.armor.text = "Low";
            }
            if(param1.level >= 4)
            {
               this.armor.text = "Medium";
            }
            return;
         }
         if(param1.name == "shatra")
         {
            if(param1.level < 6)
            {
               this.armor.text = "Low";
            }
            if(param1.level >= 6)
            {
               this.armor.text = "Medium";
            }
            return;
         }
         this.armor.text = _loc2_;
      }
      
      public function §package use§() : void
      {
         var _loc1_:§_-re§ = null;
         for each(_loc1_ in this.PortraitArray)
         {
            _loc1_.§true for const§();
         }
      }
      
      public function deselectAllSkillBoxes() : void
      {
         var _loc1_:§var const continue§ = null;
         for each(_loc1_ in this.skillBoxArray)
         {
            _loc1_.deSelect();
         }
      }
      
      protected function init(param1:Event) : void
      {
      }
      
      public function updateSkill(param1:Object) : void
      {
         this.§_-y5§ = param1;
         this.§_-Bk§.text = param1.name[param1.level];
         this.§continue for false§.text = param1.description[param1.level];
      }
      
      public function §const extends§(param1:Event) : void
      {
         this.game.gameSounds.§break const null§();
         this.butSubmit.buttonMode = true;
         this.butSubmit.mouseChildren = false;
         this.butSubmit.useHandCursor = true;
         this.butSubmit.gotoAndStop("over");
      }
      
      public function §finally for false§(param1:Event) : void
      {
         this.butSubmit.useHandCursor = false;
         this.butSubmit.gotoAndStop("idle");
      }
      
      public function §dynamic in§(param1:Event) : void
      {
         this.isActive = false;
         this.butSubmit.removeEventListener(MouseEvent.CLICK,this.§dynamic in§);
         this.game.gameSounds.playGUIButtonCommon();
         this.game.§_-6X§.removeMapBlock();
         TweenMax.to(this,0.3,{
            "y":-550,
            "onComplete":this.destroyThis
         });
      }
      
      public function resetButton(param1:Event) : void
      {
         if(!this.§_-g2§)
         {
            return;
         }
         var _loc2_:Number = this.§_-Mn§();
         if(_loc2_ > 0)
         {
            this.game.gameSounds.playGUIButtonCommon();
            this.§throw return§(_loc2_);
            this.game.§_-6X§.§_-8I§();
         }
         this.updateTrainButtonReset();
         this.disableResetButton();
      }
      
      public function §_-Mn§() : Number
      {
         var _loc4_:* = undefined;
         var _loc5_:int = 0;
         var _loc1_:Number = 0;
         var _loc2_:* = this.selectedPortrait.hero;
         var _loc3_:int = 0;
         while(_loc3_ < 5)
         {
            _loc4_ = _loc2_.skillArray[_loc3_];
            if(_loc4_.level > 0)
            {
               _loc5_ = 0;
               while(_loc5_ < _loc4_.level)
               {
                  _loc1_ += _loc4_.cost[_loc5_];
                  _loc5_++;
               }
            }
            _loc3_++;
         }
         return _loc1_;
      }
      
      public function §throw return§(param1:Number) : void
      {
         this.selectedPortrait.hero.skillPoints += param1;
         var _loc2_:int = 0;
         while(_loc2_ < 5)
         {
            this.selectedPortrait.hero.skillArray[_loc2_].level = 0;
            this.§false const function§(this.selectedPortrait.hero);
            _loc2_++;
         }
      }
      
      protected function destroyThis() : void
      {
         this.game.§_-6X§.§null const null§ = false;
         if(!this.game.§_-yX§)
         {
            this.game.§_-OE§();
         }
         else
         {
            this.game.§_-6X§.§static else§();
         }
         this.removeEventListener(Event.ADDED_TO_STAGE,this.init);
         this.butSubmit.removeEventListener(MouseEvent.CLICK,this.§dynamic in§);
         this.butSubmit.removeEventListener(MouseEvent.CLICK,this.§dynamic in§);
         this.butSubmit.removeEventListener(MouseEvent.ROLL_OVER,this.§const extends§);
         this.butSubmit.removeEventListener(MouseEvent.ROLL_OUT,this.§finally for false§);
         this.butSubmit.removeEventListener(MouseEvent.MOUSE_DOWN,this.§_-cb§);
         this.butSubmit.removeEventListener(MouseEvent.MOUSE_UP,this.§_-R5§);
         this.§try do§.removeEventListener(MouseEvent.CLICK,this.§const const return§);
         this.§try do§.removeEventListener(MouseEvent.ROLL_OUT,this.§native false§);
         this.§try do§.removeEventListener(MouseEvent.ROLL_OVER,this.§_-9C§);
         this.§try do§.removeEventListener(MouseEvent.MOUSE_DOWN,this.ButtonSelectMouseDown);
         this.§with for dynamic§.removeEventListener(MouseEvent.CLICK,this.resetButton);
         this.§with for dynamic§.removeEventListener(MouseEvent.ROLL_OVER,this.§false const default§);
         this.§with for dynamic§.removeEventListener(MouseEvent.ROLL_OUT,this.§_-2J§);
         this.§with for dynamic§.removeEventListener(MouseEvent.MOUSE_DOWN,this.§in const switch§);
         this.§with for dynamic§.removeEventListener(MouseEvent.MOUSE_UP,this.§_-F7§);
         this.butTrain.removeEventListener(MouseEvent.CLICK,this.§break const case§);
         this.butTrain.removeEventListener(MouseEvent.ROLL_OVER,this.§continue const return§);
         this.butTrain.removeEventListener(MouseEvent.ROLL_OUT,this.§_-a0§);
         this.butTrain.removeEventListener(MouseEvent.MOUSE_DOWN,this.ButtonTrainMouseDown);
         this.butTrain.removeEventListener(MouseEvent.MOUSE_UP,this.ButtonTrainMouseUp);
         this.parent.removeChild(this);
      }
   }
}

