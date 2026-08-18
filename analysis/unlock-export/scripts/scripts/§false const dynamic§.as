package
{
   import flash.display.Sprite;
   import flash.events.*;
   import flash.geom.*;
   
   public class §false const dynamic§ extends Sprite
   {
      
      public var §finally const default§:§_-pA§;
      
      protected var level:Level;
      
      protected var initNotificationPoint:Point;
      
      protected var §do final§:int;
      
      protected var §_-sk§:int;
      
      public function §false const dynamic§(param1:Level)
      {
         super();
         this.level = param1;
         this.§do final§ = 58;
         this.§_-sk§ = 0;
         this.initNotificationPoint = new Point(31,73);
      }
      
      public function update() : void
      {
         var _loc1_:int = 0;
         while(_loc1_ < this.numChildren)
         {
            §_-pA§(this.getChildAt(_loc1_)).update();
            _loc1_++;
         }
      }
      
      public function §for for var§() : void
      {
         if(this.§finally const default§ != null)
         {
            this.§finally const default§.closeMe();
         }
      }
      
      public function addNotification(param1:String) : void
      {
         if(this.§_-6L§(param1))
         {
            return;
         }
         if(param1 == "NotificationEnemyBouncer" && this.level.game.gameHeroData.selectedHero.name == "alric")
         {
            this.y -= 45;
         }
         var _loc2_:§_-pA§ = new §_-pA§(this.level,param1);
         this.§_-Q3§(_loc2_.pauseNotification);
         ++this.§_-sk§;
         _loc2_.position = this.§_-sk§;
         _loc2_.x = this.initNotificationPoint.x;
         _loc2_.y = this.initNotificationPoint.y + this.§do final§ * this.§_-sk§;
         if(this.level.data.levelIndex == 0 && this.level.mode == §_-Mm§.MODE_CAMPAIGN && param1 == "NotificationEnemyBouncer")
         {
            Level1(this.level).notificationSign = new SignNewNotification(new Point(90,this.level.game.gameHeroData.selectedHero.name == "alric" ? 115 : 158),Level1(this.level));
            this.level.bullets.addChild(Level1(this.level).notificationSign);
         }
         this.addChild(_loc2_);
      }
      
      public function §_-6L§(param1:String) : Boolean
      {
         switch(param1)
         {
            case "NotificationEnemyBouncer":
               return this.level.game.§_-Pg§.notificationEnemyBouncer;
            case "NotificationEnemyDesertRaider":
               return this.level.game.§_-Pg§.notificationEnemyDesertRaider;
            case "NotificationEnemyDesertArcher":
               return this.level.game.§_-Pg§.notificationEnemyDesertArcher;
            case "NotificationEnemyDesertWolf":
               return this.level.game.§_-Pg§.notificationEnemyDesertWolf;
            case "NotificationEnemyDesertWolfSmall":
               return this.level.game.§_-Pg§.notificationEnemyDesertWolfSmall;
            case "NotificationEnemyImmortal":
               return this.level.game.§_-Pg§.notificationEnemyImmortal;
            case "NotificationEnemyFallen":
               return this.level.game.§_-Pg§.notificationEnemyFallen;
            case "NotificationEnemyExecutioner":
               return this.level.game.§_-Pg§.notificationEnemyExecutioner;
            case "NotificationEnemyScorpion":
               return this.level.game.§_-Pg§.notificationEnemyScorpion;
            case "NotificationEnemyWasp":
               return this.level.game.§_-Pg§.notificationEnemyWasp;
            case "NotificationEnemyWaspQueen":
               return this.level.game.§_-Pg§.notificationEnemyWaspQueen;
            case "NotificationEnemyTremor":
               return this.level.game.§_-Pg§.notificationEnemyTremor;
            case "NotificationEnemyMunra":
               return this.level.game.§_-Pg§.notificationEnemyMunra;
            case "NotificationEnemyJungleSpiderBig":
               return this.level.game.§_-Pg§.notificationEnemySpiderBig;
            case "NotificationEnemyJungleSpiderSmall":
               return this.level.game.§_-Pg§.notificationEnemySpiderSmall;
            case "NotificationEnemyCanibal":
               return this.level.game.§_-Pg§.notificationEnemyCanibal;
            case "NotificationEnemyCanibalHunter":
               return this.level.game.§_-Pg§.notificationEnemyCanibalHunter;
            case "NotificationEnemyCanibalShamanPriest":
               return this.level.game.§_-Pg§.notificationEnemyCanibalPriest;
            case "NotificationEnemyCanibalShamanShield":
               return this.level.game.§_-Pg§.notificationEnemyCanibalShield;
            case "NotificationEnemyCanibalShamanMagic":
               return this.level.game.§_-Pg§.notificationEnemyCanibalMagic;
            case "NotificationEnemyCanibalNecromancer":
               return this.level.game.§_-Pg§.notificationEnemyCanibalNecromancer;
            case "NotificationEnemyCanibalZombie":
               return this.level.game.§_-Pg§.notificationEnemyCanibalZombie;
            case "NotificationEnemyCanibalWingRider":
               return this.level.game.§_-Pg§.notificationEnemyWingRaider;
            case "NotificationEnemyAlienReaper":
               return this.level.game.§_-Pg§.notificationEnemyAlienBreeder;
            case "NotificationEnemyAlienReaper":
               return this.level.game.§_-Pg§.notificationEnemyAlienReaper;
            case "NotificationEnemyGorilla":
               return this.level.game.§_-Pg§.notificationEnemyGorilla;
            case "NotificationEnemySaurianQuetzal":
               return this.level.game.§_-Pg§.notificationEnemySaurianQuetzal;
            case "NotificationEnemySaurianRazorwing":
               return this.level.game.§_-Pg§.notificationEnemySaurianRazorwing;
            case "NotificationEnemySaurianBroodguard":
               return this.level.game.§_-Pg§.notificationEnemySaurianBroodguard;
            case "NotificationEnemySaurianMyrmidon":
               return this.level.game.§_-Pg§.notificationEnemySaurianMyrmidon;
            case "NotificationEnemySaurianBlazefang":
               return this.level.game.§_-Pg§.notificationEnemySaurianBlazefang;
            case "NotificationEnemySaurianNightscale":
               return this.level.game.§_-Pg§.notificationEnemySaurianNightscale;
            case "NotificationEnemySaurianDarter":
               return this.level.game.§_-Pg§.notificationEnemySaurianDarter;
            case "NotificationEnemySaurianBrute":
               return this.level.game.§_-Pg§.notificationEnemySaurianBrute;
            case "NotificationEnemySaurianSavant":
               return this.level.game.§_-Pg§.notificationEnemySaurianSavant;
            case "NotificationTipArmorMagic":
               if(this.level.mode == §_-Mm§.MODE_CAMPAIGN)
               {
                  return false;
               }
               break;
            case "NotificationTipArmor":
               if(this.level.mode == §_-Mm§.MODE_CAMPAIGN)
               {
                  return false;
               }
               break;
            case "NotificationTipRallyPoint":
               if(this.level.mode == §_-Mm§.MODE_CAMPAIGN)
               {
                  return false;
               }
         }
         return false;
      }
      
      public function §_-Q3§(param1:String) : void
      {
         switch(param1)
         {
            case "NotificationEnemyBouncer":
               this.level.game.§_-Pg§.notificationEnemyBouncer = true;
               break;
            case "NotificationEnemyDesertRaider":
               this.level.game.§_-Pg§.notificationEnemyDesertRaider = true;
               break;
            case "NotificationEnemyDesertArcher":
               this.level.game.§_-Pg§.notificationEnemyDesertArcher = true;
               break;
            case "NotificationEnemyDesertWolf":
               this.level.game.§_-Pg§.notificationEnemyDesertWolf = true;
               break;
            case "NotificationEnemyDesertWolfSmall":
               this.level.game.§_-Pg§.notificationEnemyDesertWolfSmall = true;
               break;
            case "NotificationEnemyImmortal":
               this.level.game.§_-Pg§.notificationEnemyImmortal = true;
               break;
            case "NotificationEnemyFallen":
               this.level.game.§_-Pg§.notificationEnemyFallen = true;
               break;
            case "NotificationEnemyExecutioner":
               this.level.game.§_-Pg§.notificationEnemyExecutioner = true;
               break;
            case "NotificationEnemyScorpion":
               this.level.game.§_-Pg§.notificationEnemyScorpion = true;
               break;
            case "NotificationEnemyWasp":
               this.level.game.§_-Pg§.notificationEnemyWasp = true;
               break;
            case "NotificationEnemyWaspQueen":
               this.level.game.§_-Pg§.notificationEnemyWaspQueen = true;
               break;
            case "NotificationEnemyTremor":
               this.level.game.§_-Pg§.notificationEnemyTremor = true;
               break;
            case "NotificationEnemyMunra":
               this.level.game.§_-Pg§.notificationEnemyMunra = true;
               break;
            case "NotificationEnemyJungleSpiderBig":
               this.level.game.§_-Pg§.notificationEnemySpiderBig = true;
               break;
            case "NotificationEnemyJungleSpiderSmall":
               this.level.game.§_-Pg§.notificationEnemySpiderSmall = true;
               break;
            case "NotificationEnemyCanibal":
               this.level.game.§_-Pg§.notificationEnemyCanibal = true;
               break;
            case "NotificationEnemyCanibalHunter":
               this.level.game.§_-Pg§.notificationEnemyCanibalHunter = true;
               break;
            case "NotificationEnemyCanibalShamanPriest":
               this.level.game.§_-Pg§.notificationEnemyCanibalPriest = true;
               break;
            case "NotificationEnemyCanibalShamanShield":
               this.level.game.§_-Pg§.notificationEnemyCanibalShield = true;
               break;
            case "NotificationEnemyCanibalShamanMagic":
               this.level.game.§_-Pg§.notificationEnemyCanibalMagic = true;
               break;
            case "NotificationEnemyCanibalNecromancer":
               this.level.game.§_-Pg§.notificationEnemyCanibalNecromancer = true;
               break;
            case "NotificationEnemyCanibalZombie":
               this.level.game.§_-Pg§.notificationEnemyCanibalZombie = true;
               break;
            case "NotificationEnemyCanibalWingRider":
               this.level.game.§_-Pg§.notificationEnemyWingRaider = true;
               break;
            case "NotificationEnemyAlienReaper":
               this.level.game.§_-Pg§.notificationEnemyAlienBreeder = true;
               break;
            case "NotificationEnemyAlienReaper":
               this.level.game.§_-Pg§.notificationEnemyAlienReaper = true;
               break;
            case "NotificationEnemyGorilla":
               this.level.game.§_-Pg§.notificationEnemyGorilla = true;
               break;
            case "NotificationEnemySaurianQuetzal":
               this.level.game.§_-Pg§.notificationEnemySaurianQuetzal = true;
               break;
            case "NotificationEnemySaurianRazorwing":
               this.level.game.§_-Pg§.notificationEnemySaurianRazorwing = true;
               break;
            case "NotificationEnemySaurianBroodguard":
               this.level.game.§_-Pg§.notificationEnemySaurianBroodguard = true;
               break;
            case "NotificationEnemySaurianMyrmidon":
               this.level.game.§_-Pg§.notificationEnemySaurianMyrmidon = true;
               break;
            case "NotificationEnemySaurianBlazefang":
               this.level.game.§_-Pg§.notificationEnemySaurianBlazefang = true;
               break;
            case "NotificationEnemySaurianNightscale":
               this.level.game.§_-Pg§.notificationEnemySaurianNightscale = true;
               break;
            case "NotificationEnemySaurianDarter":
               this.level.game.§_-Pg§.notificationEnemySaurianDarter = true;
               break;
            case "NotificationEnemySaurianBrute":
               this.level.game.§_-Pg§.notificationEnemySaurianBrute = true;
               break;
            case "NotificationEnemySaurianSavant":
               this.level.game.§_-Pg§.notificationEnemySaurianSavant = true;
         }
      }
      
      public function removeNotification(param1:int) : void
      {
         if(param1 == this.§_-sk§)
         {
            --this.§_-sk§;
            return;
         }
         var _loc2_:int = param1 + 1;
         while(_loc2_ <= this.§_-sk§)
         {
            §_-pA§(this.getChildAt(_loc2_ - 1)).moveTo(this.initNotificationPoint.y + this.§do final§ * (_loc2_ - 1));
            _loc2_++;
         }
         --this.§_-sk§;
      }
      
      protected function destroyThis() : void
      {
         this.level = null;
         this.parent.removeChild(this);
      }
   }
}

