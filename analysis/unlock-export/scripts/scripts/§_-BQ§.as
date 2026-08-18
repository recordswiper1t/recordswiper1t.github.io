package
{
   import fl.lang.*;
   import flash.events.*;
   import flash.net.*;
   import flash.utils.*;
   
   public class §_-BQ§ extends §extends const true§
   {
      
      public var main:§each const each§;
      
      public var §_-6X§:§class const for§;
      
      public var §_-Y1§:int = 77;
      
      public var starsWon:int = 0;
      
      public var stars:int = 0;
      
      public var difficulty:int;
      
      public var §native import§:Array = [];
      
      public var gameUpgrades:GameUpgrades;
      
      public var §const for set§:GameAchievements;
      
      public var §_-Pg§:§null throw§;
      
      public var gameHeroData:§_-2i§;
      
      public var gameSounds:§_-Am§;
      
      public var tips:int = 30;
      
      public var currentLevel:int;
      
      public var §_-2m§:int = 0;
      
      public var §use const get§:String;
      
      public var challengeShow:Boolean;
      
      public var §_-5w§:Boolean = true;
      
      public var earnFacebookStar:Boolean;
      
      public var earnTwitterStar:Boolean;
      
      public var onlineSelectedSlot:int;
      
      public var §_-yX§:Boolean;
      
      public var pcAlreadyGot:Boolean;
      
      public var pcSelectedReinforcement:int;
      
      public var pcHasGold:Boolean;
      
      public var pcLightning:Boolean;
      
      public var pcExtraReinforcement:Boolean;
      
      public var §override for if§:Boolean;
      
      public var levelUpBtnAnim:Boolean = false;
      
      public var lastLevelWon:int = 0;
      
      public var showedUnlockedMirage:Boolean = false;
      
      public var showedUnlockedCronan:Boolean = false;
      
      public var showedLevelUp:Boolean = false;
      
      public var bubblesShowed:Boolean = false;
      
      public var showedDifficulty:Boolean = false;
      
      public var showNewSignMirage:Boolean = false;
      
      public var showNewSignCronan:Boolean = false;
      
      public function §_-BQ§(param1:§each const each§, param2:String)
      {
         super();
         this.main = param1;
         this.§use const get§ = param2;
         if(this.§use const get§ == "online_slot")
         {
            this.§_-yX§ = true;
            this.onlineSelectedSlot = this.main.onlineSlotNumber;
            this.§override for if§ = this.main.mpc;
         }
         else
         {
            this.§_-yX§ = false;
         }
         this.difficulty = §_-Mm§.DIFFICULTY_NORMAL;
         this.gameUpgrades = new GameUpgrades(this);
         this.gameHeroData = new §_-2i§(this);
         this.§const for set§ = new GameAchievements(this);
         this.§_-Pg§ = new §null throw§(this);
         this.gameSounds = new §_-Am§();
         this.§_-gp§();
         if(!this.§_-yX§ && §each const each§.onlineHandler.getService() == §each const each§.SERVICE_ARMORGAMES)
         {
            §each const each§.purchasedHeroes = [];
            if(this.gameHeroData.selectedHero.name != "alric" && this.gameHeroData.selectedHero.name != "cronan" && this.gameHeroData.selectedHero.name != "mirage")
            {
               this.gameHeroData.selectedHero = this.gameHeroData.heroAlric;
            }
         }
         else
         {
            this.gameHeroData.selectedHero = this.gameHeroData.selectedHero;
         }
         this.§var const finally§(null);
      }
      
      public function §do const static§() : void
      {
         this.stars += 15;
         this.starsWon += 15;
         this.§_-Y1§ += 15;
         this.pcAlreadyGot = true;
         this.pcExtraReinforcement = true;
         this.pcHasGold = true;
         this.pcLightning = true;
         this.pcSelectedReinforcement = §_-Mm§.REINFORCEMENT_NORMAL;
         this.§const for set§.§import for import§(this.starsWon);
         §each const each§.onlineHandler.callQuest("StarsEarned",this.starsWon);
      }
      
      public function §while const switch§(param1:int, param2:int, param3:Boolean) : void
      {
         var _loc4_:Level1 = null;
         var _loc5_:Level2 = null;
         var _loc6_:Level3 = null;
         var _loc7_:Level4 = null;
         var _loc8_:Level5 = null;
         var _loc9_:Level6 = null;
         var _loc10_:Level7 = null;
         var _loc11_:Level8 = null;
         var _loc12_:Level9 = null;
         var _loc13_:Level10 = null;
         var _loc14_:Level11 = null;
         var _loc15_:Level12 = null;
         var _loc16_:Level13 = null;
         var _loc17_:Level14 = null;
         var _loc18_:Level15 = null;
         var _loc19_:Class = getDefinitionByName("Level" + param1) as Class;
         this.addChildAt(new _loc19_(this,param2,param3),0);
         this.currentLevel = param1;
      }
      
      public function §var const finally§(param1:*) : void
      {
         if(param1 != null)
         {
            this.endLevel(param1);
         }
         this.§_-6X§ = new §class const for§(this);
         this.addChild(this.§_-6X§);
      }
      
      public function §final throw§() : void
      {
         this.removeChild(this.§_-6X§);
         this.§_-6X§ = null;
      }
      
      public function §_-FP§(param1:Level, param2:int) : void
      {
         this.§const for set§.§case super§();
         this.endLevel(param1);
         this.§while const switch§(this.currentLevel,param2,true);
      }
      
      public function endLevel(param1:Level) : void
      {
         param1.destroyThis();
         param1 = null;
      }
      
      public function §implements break§() : String
      {
         var _loc1_:* = Math.ceil(Math.random() * this.tips);
         return Locale.loadStringEx("TIP_" + _loc1_,Locale.getDefaultLang());
      }
      
      private function §_-gp§() : void
      {
         this.§native import§.push(new §true final§(this,0,0));
         this.§native import§.push(new §true final§(this,1,0));
         this.§native import§.push(new §true final§(this,2,0));
         this.§native import§.push(new §true final§(this,3,0));
         this.§native import§.push(new §true final§(this,4,0));
         this.§native import§.push(new §true final§(this,5,0));
         this.§native import§.push(new §true final§(this,6,0));
         this.§native import§.push(new §true final§(this,7,0));
         this.§native import§.push(new §true final§(this,8,0));
         this.§native import§.push(new §true final§(this,9,0));
         this.§native import§.push(new §true final§(this,10,0));
         this.§native import§.push(new §true final§(this,11,0));
         this.§native import§.push(new §true final§(this,12,0));
         this.§native import§.push(new §true final§(this,13,0));
         this.§native import§.push(new §true final§(this,14,0));
         if(!this.§_-yX§)
         {
            this.§_-aY§();
         }
         else if(this.main.onlineData == null || this.main.onlineData.levels == null)
         {
            this.§_-ZG§();
         }
         else
         {
            this.§_-Gb§();
         }
         this.§_-Zt§();
      }
      
      private function §_-Gb§() : void
      {
         this.starsWon = this.main.onlineData.starsWon;
         this.stars = this.main.onlineData.stars;
         this.difficulty = this.main.onlineData.difficulty;
         this.showedUnlockedMirage = this.main.onlineData.showedUnlockedMirage;
         this.showedUnlockedCronan = this.main.onlineData.showedUnlockedCronan;
         this.showedLevelUp = this.main.onlineData.showedLevelUp;
         this.bubblesShowed = this.main.onlineData.bubblesShowed;
         this.showedDifficulty = this.main.onlineData.showedDifficulty;
         this.earnFacebookStar = this.main.onlineData.earnFacebookStar;
         this.earnTwitterStar = this.main.onlineData.earnTwitterStar;
         this.challengeShow = this.main.onlineData.challengeShow;
         var _loc1_:int = 0;
         while(_loc1_ < this.main.onlineData.levels.length)
         {
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).levelStatus = this.main.onlineData.levels[_loc1_].status;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).stars = this.main.onlineData.levels[_loc1_].stars;
            if(§true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).stars == 3)
            {
               §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).heroicMode = true;
               §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).ironMode = true;
            }
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).heroicModeWin = this.main.onlineData.levels[_loc1_].heroic;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).ironModeWin = this.main.onlineData.levels[_loc1_].iron;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).heroicModeView = this.main.onlineData.levels[_loc1_].heroicView;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).ironModeView = this.main.onlineData.levels[_loc1_].ironView;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).campaignDifficulty = this.main.onlineData.levels[_loc1_].campaignDifficulty;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).heroicDifficulty = this.main.onlineData.levels[_loc1_].heroicDifficulty;
            §true final§(this.§native import§[this.main.onlineData.levels[_loc1_].index]).ironDifficulty = this.main.onlineData.levels[_loc1_].ironDifficulty;
            _loc1_++;
         }
         this.§const for set§.§switch for set§(this.main.onlineData.achievements);
         this.gameUpgrades.§switch for set§(this.main.onlineData.upgrades);
         this.§_-Pg§.§switch for set§(this.main.onlineData.encyclopedia);
         this.gameHeroData.§switch for set§(this.main.onlineData.heroData);
         this.pcAlreadyGot = this.main.onlineData.pcAlreadyGot;
         this.pcExtraReinforcement = this.main.onlineData.pcExtraReinforcement;
         this.pcHasGold = this.main.onlineData.pcHasGold;
         this.pcLightning = this.main.onlineData.pcLightning;
         this.pcSelectedReinforcement = this.main.onlineData.pcSelectedReinforcement;
         this.§_-bX§();
         var _loc2_:Boolean = false;
         var _loc3_:int = 0;
         while(_loc3_ < this.§native import§.length)
         {
            if(§true final§(this.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW || §true final§(this.§native import§[_loc3_]).levelStatus == §true final§.LEVEL_ENABLED_UNCOMPLETED)
            {
               _loc2_ = true;
               break;
            }
            _loc3_++;
         }
         if(!_loc2_)
         {
            this.§case const get§();
         }
      }
      
      private function §_-bX§() : void
      {
         if(this.§override for if§)
         {
            if(!this.pcAlreadyGot)
            {
               this.§do const static§();
            }
            else
            {
               this.§_-Y1§ += 15;
            }
         }
      }
      
      private function §_-aY§() : void
      {
         var §each const function§:Boolean;
         var §with for use§:int;
         var §function for var§:SharedObject = null;
         var §static for const§:int = 0;
         var §_-kS§:§true final§ = null;
         var §_-VB§:int = 0;
         var §switch const throw§:int = 0;
         try
         {
            §function for var§ = SharedObject.getLocal(this.§use const get§);
         }
         catch(err:Error)
         {
            §true final§(this.§native import§[0]).levelStatus = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
            return;
         }
         if(§function for var§.data.levels != undefined)
         {
            §static for const§ = 0;
            while(§static for const§ < §function for var§.data.levels.length)
            {
               §_-kS§ = this.§native import§[§function for var§.data.levels[§static for const§].index];
               §_-kS§.levelStatus = §function for var§.data.levels[§static for const§].status;
               §_-kS§.stars = §function for var§.data.levels[§static for const§].stars;
               if(§_-kS§.stars == 3)
               {
                  §_-kS§.heroicMode = true;
                  §_-kS§.ironMode = true;
               }
               §_-kS§.heroicModeWin = §function for var§.data.levels[§static for const§].heroic;
               §_-kS§.ironModeWin = §function for var§.data.levels[§static for const§].iron;
               §_-kS§.heroicModeView = §function for var§.data.levels[§static for const§].heroicView;
               §_-kS§.ironModeView = §function for var§.data.levels[§static for const§].ironView;
               §_-kS§.campaignDifficulty = §function for var§.data.levels[§static for const§].campaignDifficulty;
               §_-kS§.heroicDifficulty = §function for var§.data.levels[§static for const§].heroicDifficulty;
               §_-kS§.ironDifficulty = §function for var§.data.levels[§static for const§].ironDifficulty;
               §static for const§++;
            }
            this.starsWon = §function for var§.data.starsWon;
            this.stars = §function for var§.data.stars;
            this.difficulty = §function for var§.data.difficulty;
            this.showedUnlockedMirage = §function for var§.data.showedUnlockedMirage;
            this.showedUnlockedCronan = §function for var§.data.showedUnlockedCronan;
            this.showedLevelUp = §function for var§.data.showedLevelUp;
            this.bubblesShowed = §function for var§.data.bubblesShowed;
            this.showedDifficulty = §function for var§.data.showedDifficulty;
            this.earnFacebookStar = §function for var§.data.earnFacebookStar;
            this.earnTwitterStar = §function for var§.data.earnTwitterStar;
            this.challengeShow = §function for var§.data.challengeShow;
            §function for var§.close();
            this.§const for set§.loadData();
            this.gameUpgrades.loadData();
            this.§_-Pg§.loadData();
            this.gameHeroData.loadData();
         }
         else
         {
            §true final§(this.§native import§[0]).levelStatus = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
            §function for var§.data.levels = [];
            §function for var§.data.achievements = new Object();
            §function for var§.data.upgrades = new Object();
            §function for var§.data.encyclopedia = new Object();
            §function for var§.data.heroData = new Object();
            §function for var§.data.starsWon = this.starsWon;
            §function for var§.data.stars = this.stars;
            §function for var§.data.difficulty = §_-Mm§.DIFFICULTY_NORMAL;
            §function for var§.data.earnFacebookStar = false;
            §function for var§.data.earnTwitterStar = false;
            §function for var§.data.challengeShow = false;
            §switch const throw§ = 0;
            while(§switch const throw§ < this.§native import§.length)
            {
               if(§switch const throw§ == 0)
               {
                  §_-VB§ = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
               }
               else
               {
                  §_-VB§ = §true final§.LEVEL_DISABLED;
               }
               §function for var§.data.levels.push({
                  "index":§switch const throw§,
                  "status":§_-VB§,
                  "stars":0,
                  "heroic":false,
                  "iron":false,
                  "heroicView":false,
                  "ironView":false,
                  "campaignDifficulty":2,
                  "heroicDifficulty":2,
                  "ironDifficulty":2
               });
               §switch const throw§++;
            }
            §function for var§.data.achievements = this.§const for set§.§var class§();
            §function for var§.data.upgrades = this.gameUpgrades.§false for const§();
            §function for var§.data.heroData = this.gameHeroData.§_-xs§();
            §function for var§.data.encyclopedia = this.§_-Pg§.§do super§();
            §function for var§.flush();
            §function for var§.close();
         }
         §each const function§ = false;
         §with for use§ = 0;
         while(§with for use§ < this.§native import§.length)
         {
            if(§true final§(this.§native import§[§with for use§]).levelStatus == §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW || §true final§(this.§native import§[§with for use§]).levelStatus == §true final§.LEVEL_ENABLED_UNCOMPLETED)
            {
               §each const function§ = true;
               break;
            }
            §with for use§++;
         }
         if(!§each const function§)
         {
            this.§case const get§();
         }
      }
      
      public function §_-Zt§() : void
      {
         var _loc1_:Number = NaN;
         var _loc2_:int = 0;
         if(§each const each§.onlineHandler == null)
         {
            return;
         }
         if(!§each const each§.onlineHandler.isLoggedIn())
         {
            return;
         }
         if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE)
         {
            if(this.§const for set§.greatDefenderIron)
            {
               §each const each§.onlineHandler.callQuest("IronDefender",1);
            }
            _loc1_ = 0;
            while(_loc2_ < this.§native import§.length)
            {
               if(§true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED || §true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW || §true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_BETTER)
               {
                  _loc1_ = _loc2_ + 1;
               }
               _loc2_++;
            }
            §each const each§.onlineHandler.callQuest("LevelsCompleted",_loc1_);
            §each const each§.onlineHandler.callQuest("StarsEarned",this.starsWon);
            §each const each§.onlineHandler.callQuest("AchievementsEarned",this.§const for set§.achievCant);
            if(this.§const for set§.birthOfAHero)
            {
               §each const each§.onlineHandler.callQuest("BirthofaHero");
            }
            if(this.§const for set§.heroOfTheDay)
            {
               §each const each§.onlineHandler.callQuest("HeroOfTheDay");
            }
            if(this.§const for set§.heroMax)
            {
               §each const each§.onlineHandler.callQuest("Legendary");
            }
            return;
         }
         if(this.§const for set§.moneyTalks)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_moneytalks");
         }
         if(this.§const for set§.easyTowerBuilder)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_constructor");
         }
         if(this.§const for set§.sandWarrior)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_sandwarrior");
         }
         if(this.§const for set§.oneFroggyEvening)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_froggy");
         }
         if(this.§const for set§.genieInABottle)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_geniebottle");
         }
         if(this.§const for set§.dodgeThis)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_dodgethis");
         }
         if(this.§const for set§.saveThePrincess)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_saveprincess");
         }
         if(this.§const for set§.popularBBQ)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_popularbbq");
         }
         if(this.§const for set§.youShallNotPass)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_shallnotpass");
         }
         if(this.§const for set§.mechwarrior)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_mechwarrior");
         }
         if(this.§const for set§.indiana)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_walton");
         }
         if(this.§const for set§.oneUglyMotherfucker)
         {
            §each const each§.onlineHandler.callQuest("krf-quest_ugly");
         }
      }
      
      public function §case const get§() : void
      {
         var _loc1_:int = 0;
         var _loc2_:int = 0;
         while(_loc2_ < this.§native import§.length)
         {
            if(§true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED || §true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW || §true final§(this.§native import§[_loc2_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_BETTER)
            {
               _loc1_ = _loc2_;
            }
            _loc2_++;
         }
         if(_loc1_ < 11)
         {
            §true final§(this.§native import§[_loc1_ + 1]).levelStatus = §true final§.LEVEL_ENABLED_UNCOMPLETED;
         }
      }
      
      public function §_-5o§() : void
      {
         var _loc1_:SharedObject = null;
         if(!this.§_-yX§)
         {
            try
            {
               _loc1_ = SharedObject.getLocal(this.§use const get§);
               _loc1_.data.starsWon = this.starsWon;
               _loc1_.data.stars = this.stars;
               _loc1_.flush();
               _loc1_.close();
            }
            catch(err:Error)
            {
            }
         }
      }
      
      public function §extends const§(param1:int) : void
      {
         var _loc2_:SharedObject = null;
         if(this.difficulty == param1)
         {
            return;
         }
         this.difficulty = param1;
         if(!this.§_-yX§)
         {
            try
            {
               _loc2_ = SharedObject.getLocal(this.§use const get§);
               _loc2_.data.difficulty = this.difficulty;
               _loc2_.flush();
               _loc2_.close();
            }
            catch(err:Error)
            {
            }
         }
      }
      
      public function earnFacebookSocial() : Boolean
      {
         var _loc1_:SharedObject = null;
         if(this.earnFacebookStar)
         {
            return false;
         }
         this.earnFacebookStar = true;
         ++this.starsWon;
         ++this.stars;
         if(!this.§_-yX§)
         {
            try
            {
               _loc1_ = SharedObject.getLocal(this.§use const get§);
               _loc1_.data.earnFacebookStar = true;
               _loc1_.data.starsWon = this.starsWon;
               _loc1_.data.stars = this.stars;
               _loc1_.flush();
               _loc1_.close();
            }
            catch(err:Error)
            {
            }
         }
         return true;
      }
      
      public function earnTwitterSocial() : Boolean
      {
         var _loc1_:SharedObject = null;
         if(this.earnTwitterStar)
         {
            return false;
         }
         this.earnTwitterStar = true;
         ++this.starsWon;
         ++this.stars;
         if(!this.§_-yX§)
         {
            try
            {
               _loc1_ = SharedObject.getLocal(this.§use const get§);
               _loc1_.data.earnTwitterStar = true;
               _loc1_.data.starsWon = this.starsWon;
               _loc1_.data.stars = this.stars;
               _loc1_.flush();
               _loc1_.close();
            }
            catch(err:Error)
            {
            }
         }
         return true;
      }
      
      public function §get final§() : void
      {
         var _loc1_:SharedObject = null;
         if(!this.§_-yX§)
         {
            try
            {
               _loc1_ = SharedObject.getLocal(this.§use const get§);
               _loc1_.data.challengeShow = this.challengeShow;
               _loc1_.flush();
               _loc1_.close();
            }
            catch(err:Error)
            {
            }
         }
      }
      
      public function §_-OE§() : void
      {
         var _loc1_:SharedObject = null;
         var _loc2_:int = 0;
         var _loc3_:Boolean = false;
         var _loc4_:int = 0;
         try
         {
            _loc1_ = SharedObject.getLocal(this.§use const get§);
            _loc1_.data.starsWon = this.starsWon;
            _loc1_.data.stars = this.stars;
            _loc1_.data.difficulty = this.difficulty;
            _loc1_.data.earnFacebookStar = this.earnFacebookStar;
            _loc1_.data.earnTwitterStar = this.earnTwitterStar;
            _loc1_.data.challengeShow = this.challengeShow;
            _loc1_.data.levels = [];
            _loc2_ = 0;
            _loc3_ = false;
            _loc4_ = 0;
            while(_loc4_ < this.§native import§.length)
            {
               if(_loc3_)
               {
                  _loc2_ = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
                  _loc3_ = false;
               }
               else if(§true final§(this.§native import§[_loc4_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW)
               {
                  _loc2_ = §true final§.LEVEL_ENABLED_COMPLETED;
                  _loc3_ = true;
               }
               else
               {
                  _loc2_ = §true final§(this.§native import§[_loc4_]).levelStatus;
               }
               _loc1_.data.levels.push({
                  "index":_loc4_,
                  "status":_loc2_,
                  "stars":§true final§(this.§native import§[_loc4_]).stars,
                  "heroicView":§true final§(this.§native import§[_loc4_]).heroicModeView,
                  "ironView":§true final§(this.§native import§[_loc4_]).ironModeView,
                  "heroic":§true final§(this.§native import§[_loc4_]).heroicModeWin,
                  "iron":§true final§(this.§native import§[_loc4_]).ironModeWin,
                  "campaignDifficulty":§true final§(this.§native import§[_loc4_]).campaignDifficulty,
                  "heroicDifficulty":§true final§(this.§native import§[_loc4_]).heroicDifficulty,
                  "ironDifficulty":§true final§(this.§native import§[_loc4_]).ironDifficulty
               });
               _loc4_++;
            }
            _loc1_.data.achievements = this.§const for set§.§var class§();
            _loc1_.data.upgrades = this.gameUpgrades.§false for const§();
            _loc1_.data.heroData = this.gameHeroData.§_-xs§();
            _loc1_.data.encyclopedia = this.§_-Pg§.§do super§();
            _loc1_.data.showedUnlockedMirage = this.showedUnlockedMirage;
            _loc1_.data.showedUnlockedCronan = this.showedUnlockedCronan;
            _loc1_.data.showedLevelUp = this.showedLevelUp;
            _loc1_.data.bubblesShowed = this.bubblesShowed;
            _loc1_.data.showedDifficulty = this.showedDifficulty;
            _loc1_.flush();
            _loc1_.close();
         }
         catch(err:Error)
         {
         }
      }
      
      public function §_-ZG§() : void
      {
         §true final§(this.§native import§[0]).levelStatus = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
         this.§_-bX§();
      }
      
      public function §for super§() : Object
      {
         var _loc1_:Object = new Object();
         _loc1_.starsWon = this.starsWon;
         _loc1_.stars = this.stars;
         _loc1_.difficulty = this.difficulty;
         _loc1_.earnFacebookStar = this.earnFacebookStar;
         _loc1_.earnTwitterStar = this.earnTwitterStar;
         _loc1_.challengeShow = this.challengeShow;
         _loc1_.showedUnlockedMirage = this.showedUnlockedMirage;
         _loc1_.showedUnlockedCronan = this.showedUnlockedCronan;
         _loc1_.showedLevelUp = this.showedLevelUp;
         _loc1_.bubblesShowed = this.bubblesShowed;
         _loc1_.showedDifficulty = this.showedDifficulty;
         _loc1_.levels = [];
         var _loc2_:int = 0;
         var _loc3_:Boolean = false;
         var _loc4_:int = 0;
         while(_loc4_ < this.§native import§.length)
         {
            if(_loc3_)
            {
               _loc2_ = §true final§.LEVEL_ENABLED_UNCOMPLETED_NEW;
               _loc3_ = false;
            }
            else if(§true final§(this.§native import§[_loc4_]).levelStatus == §true final§.LEVEL_ENABLED_COMPLETED_NEW)
            {
               _loc2_ = §true final§.LEVEL_ENABLED_COMPLETED;
               _loc3_ = true;
            }
            else
            {
               _loc2_ = §true final§(this.§native import§[_loc4_]).levelStatus;
            }
            _loc1_.levels.push({
               "index":_loc4_,
               "status":_loc2_,
               "stars":§true final§(this.§native import§[_loc4_]).stars,
               "heroicView":§true final§(this.§native import§[_loc4_]).heroicModeView,
               "ironView":§true final§(this.§native import§[_loc4_]).ironModeView,
               "heroic":§true final§(this.§native import§[_loc4_]).heroicModeWin,
               "iron":§true final§(this.§native import§[_loc4_]).ironModeWin,
               "campaignDifficulty":§true final§(this.§native import§[_loc4_]).campaignDifficulty,
               "heroicDifficulty":§true final§(this.§native import§[_loc4_]).heroicDifficulty,
               "ironDifficulty":§true final§(this.§native import§[_loc4_]).ironDifficulty
            });
            _loc4_++;
         }
         _loc1_.achievements = this.§const for set§.§var class§();
         _loc1_.upgrades = this.gameUpgrades.§false for const§();
         _loc1_.heroData = this.gameHeroData.§_-xs§();
         _loc1_.encyclopedia = this.§_-Pg§.§do super§();
         _loc1_.pcAlreadyGot = this.pcAlreadyGot;
         _loc1_.pcExtraReinforcement = this.pcExtraReinforcement;
         _loc1_.pcHasGold = this.pcHasGold;
         _loc1_.pcLightning = this.pcLightning;
         _loc1_.pcSelectedReinforcement = this.pcSelectedReinforcement;
         return _loc1_;
      }
      
      public function destroyThis() : void
      {
         this.gameUpgrades.destroyThis();
         this.§const for set§.destroyThis();
         this.§_-Pg§.destroyThis();
         this.gameSounds.destroyThis();
         this.§const for set§ = null;
         this.§const for set§ = null;
         this.§_-Pg§ = null;
         this.gameSounds = null;
         this.parent.removeChild(this);
      }
   }
}

