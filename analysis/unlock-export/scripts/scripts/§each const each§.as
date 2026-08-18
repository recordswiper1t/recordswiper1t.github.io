package
{
   import §_-Kh§.*;
   import §_-aQ§.*;
   import fl.lang.*;
   import flash.display.*;
   import flash.events.*;
   import flash.net.*;
   import flash.system.*;
   import flash.ui.*;
   import flash.utils.*;
   import §set native§.*;
   
   public class §each const each§ extends §extends const true§
   {
      
      public static var heroPrices:Dictionary;
      
      public static var onlineHandler:§for const break§;
      
      public static var LINK_SITE:*;
      
      public static var menuLinkLabel:String;
      
      public static var purchasedHeroes:Array = [];
      
      public static const SERVICE_ARMORGAMES:* = "ArmorGames";
      
      public static const SERVICE_KONGREGATE:* = "Kongregate";
      
      public static const SERVICE_FACEBOOK:* = "Facebook";
      
      public static const SERVICE_CHROME:* = "Chrome";
      
      public static var localOnly:Boolean = false;
      
      public var §override do§:§in extends§;
      
      public var tooltipsStatus:Boolean;
      
      public var §_-jR§:Boolean = true;
      
      public var §static native§:Boolean = true;
      
      private var intros:MovieClip;
      
      private var introTime:int = 365;
      
      private var introTimeCounter:int = 0;
      
      public var onlineData:Object;
      
      public var mpc:Boolean;
      
      public var onlineSlotNumber:int;
      
      private var §_-Vz§:int = 150;
      
      public var §_-FU§:Dictionary;
      
      private var necromancerParticlesMax:int = 50;
      
      public var necromancerParticlesPool:Dictionary;
      
      private var §_-HM§:int = 60;
      
      public var §set for const§:Dictionary;
      
      private var §var with§:int = 100;
      
      public var §function for function§:Dictionary;
      
      private var §const const dynamic§:int = 200;
      
      public var §_-uS§:Dictionary;
      
      private var §_-LA§:int = 120;
      
      public var §_-V4§:Dictionary;
      
      private var fireballParticlesMax:int = 150;
      
      public var fireballParticlesPool:Dictionary;
      
      private var §in for throw§:int = 120;
      
      public var §_-R8§:Dictionary;
      
      private var §use const false§:int = 150;
      
      public var §_-lc§:Dictionary;
      
      public var magicMissileParticlesMaxAlt:int = 100;
      
      public var magicMissileParticlesMaxTail:int = 20;
      
      public var magicMissileParticlesAltPool:Dictionary;
      
      public var magicMissileParticlesAPool:Dictionary;
      
      public var magicMissileParticlesBPool:Dictionary;
      
      public var magicMissileParticlesCPool:Dictionary;
      
      public function §each const each§()
      {
         var _loc3_:String = null;
         var _loc4_:DisplayObject = null;
         super();
         MochiServices.connect("456fc7d8e751e36a",root,this.onMochiConnectError);
         §each const each§.onlineHandler = new AgiV2Handler();
         §each const each§.onlineHandler.loadSystem(this.stage);
         var _loc1_:ContextMenu = new ContextMenu();
         _loc1_.hideBuiltInItems();
         this.contextMenu = _loc1_;
         var _loc2_:Array = ["armorgames.com","kongregate.com"];
         if(!this.§static const super§(_loc2_))
         {
            this.§override do§.§dynamic const import§.removeChild(this.§override do§.§dynamic const import§.mobile_add_intro);
            _loc3_ = "10016QAA25A02F";
            _loc4_ = new §var const class§(_loc3_);
            this.§override do§.§_-EY§(_loc4_);
         }
         else
         {
            this.§override do§.§dynamic const import§.mobile_add_intro.visible = true;
         }
         this.addEventListener(Event.ADDED_TO_STAGE,this.init);
         this.tabEnabled = false;
         this.tabChildren = false;
      }
      
      public function onMochiConnectError(param1:String) : void
      {
         §var const super§.log("MochiAPI - Error: " + param1);
      }
      
      public function §do const in§(param1:Array) : Boolean
      {
         var _loc2_:int = 0;
         while(_loc2_ < param1.length)
         {
            if(this.§_-dm§(param1[_loc2_]))
            {
               return true;
            }
            _loc2_++;
         }
         return false;
      }
      
      public function §_-dm§(param1:*) : Boolean
      {
         var _loc6_:String = null;
         var _loc2_:String = this.loaderInfo.url;
         var _loc3_:int = _loc2_.indexOf("://") + 3;
         if(_loc2_.substr(0,_loc3_) == "file://")
         {
            return true;
         }
         var _loc4_:int = _loc2_.indexOf("/",_loc3_) - _loc3_;
         var _loc5_:String = _loc2_.substr(_loc3_,_loc4_);
         if(param1 is String)
         {
            param1 = [param1];
         }
         for each(_loc6_ in param1)
         {
            if(_loc5_.substr(-_loc6_.length,_loc6_.length) == _loc6_)
            {
               return true;
            }
         }
         return false;
      }
      
      internal function §static const super§(param1:Array) : Boolean
      {
         var _loc2_:int = 0;
         while(_loc2_ < param1.length)
         {
            if(this.checkDomain(param1[_loc2_]))
            {
               return true;
            }
            _loc2_++;
         }
         return false;
      }
      
      public function checkDomain(param1:*) : Boolean
      {
         var _loc6_:String = null;
         var _loc2_:String = this.loaderInfo.url;
         var _loc3_:int = _loc2_.indexOf("://") + 3;
         if(_loc2_.substr(0,_loc3_) == "file://")
         {
            return true;
         }
         var _loc4_:int = _loc2_.indexOf("/",_loc3_) - _loc3_;
         var _loc5_:String = _loc2_.substr(_loc3_,_loc4_);
         if(param1 is String)
         {
            param1 = [param1];
         }
         for each(_loc6_ in param1)
         {
            if(_loc5_.substr(-_loc6_.length,_loc6_.length) == _loc6_)
            {
               return true;
            }
         }
         return false;
      }
      
      public function init(param1:Event) : void
      {
         this.stop();
         if(this.§override do§ != null)
         {
            this.§override do§.addEventListener(Event.COMPLETE,this.§_-Ea§,false,0,true);
            §in extends§(this.§override do§).setDefense(this);
         }
      }
      
      private function §_-Ea§(param1:Event) : void
      {
         this.§override do§.removeEventListener(Event.COMPLETE,this.§_-Ea§);
         §in extends§(this.§override do§).addPlayListeners();
      }
      
      public function §import for§() : void
      {
         §in extends§(this.§override do§).destroyThis();
         this.§override do§ = null;
         this.gotoAndStop(2);
         this.§try for for§();
         this.§_-Zv§();
         this.§_-hn§();
         this.§override class§();
         this.§_-MI§();
         this.§_-fH§();
         this.§_-cF§();
         this.§_-IV§();
         this.§import§();
         if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_KONGREGATE)
         {
            this.intros = new §_-b8§();
            this.introTime -= 140;
         }
         if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_CHROME)
         {
            this.intros = new §_-SG§();
            this.introTime = 131;
         }
         if(§each const each§.onlineHandler.getService() == §each const each§.SERVICE_ARMORGAMES)
         {
            this.intros = new Intros();
         }
         this.intros.addEventListener(Event.ENTER_FRAME,this.introFrame,false,0,true);
         this.addChild(this.intros);
      }
      
      private function introFrame(param1:Event) : void
      {
         if(this.introTimeCounter < this.introTime)
         {
            ++this.introTimeCounter;
            return;
         }
         this.intros.removeEventListener(Event.ENTER_FRAME,this.introFrame);
         this.removeChild(this.intros);
         this.intros = null;
         this.initGame();
      }
      
      public function initGame() : void
      {
         this.tooltipsStatus = true;
         this.§do§();
         this.§_-1z§();
         this.showMainMenu();
      }
      
      public function showMainMenu() : void
      {
         this.addChildAt(new MainMenu(),0);
      }
      
      public function loadGame(param1:String) : void
      {
         this.addChildAt(new §_-BQ§(this,param1),0);
      }
      
      public function goToCredits() : void
      {
         this.addChildAt(new §_-8x§(this),0);
      }
      
      public function showTransition(param1:§_-rJ§ = null, param2:Level = null, param3:MainMenu = null, param4:§class const for§ = null, param5:MainMenu = null, param6:§_-8x§ = null, param7:ComicEnd = null) : void
      {
         §for for dynamic§.getInstance().stopSound("gui_transition_door");
         §for for dynamic§.getInstance().playSound("gui_transition_door",0.6,0,0);
         this.addChild(new TransitionScreen(param1,param2,param3,param4,param5,param6,param7));
      }
      
      public function §function const null§(param1:Level) : void
      {
         this.addChild(new EndGame(param1));
      }
      
      public function §extends const default§() : void
      {
         §for for dynamic§.getInstance().§throw const get§();
      }
      
      public function §_-1z§() : void
      {
         §for for dynamic§.getInstance().§get const do§(§final const throw§,"gui_quest_completed");
         §for for dynamic§.getInstance().§get const do§(§_-BO§,"gui_win_stars");
         §for for dynamic§.getInstance().§get const do§(§_-BO§,"gui_win_stars2");
         §for for dynamic§.getInstance().§get const do§(§_-BO§,"gui_win_stars3");
         §for for dynamic§.getInstance().§get const do§(§_-om§,"gui_victory_cheer");
         §for for dynamic§.getInstance().§get const do§(§return const return§,"gui_map_new_flag");
         §for for dynamic§.getInstance().§get const do§(§return const return§,"gui_map_new_flag");
         §for for dynamic§.getInstance().§get const do§(§_-tI§,"gui_map_road");
         §for for dynamic§.getInstance().§get const do§(§_-eO§,"gui_next_wave_ready");
         §for for dynamic§.getInstance().§get const do§(§_-W4§,"gui_next_wave_reward");
         §for for dynamic§.getInstance().§get const do§(Sound_LooseLife,"gui_loose_life1");
         §for for dynamic§.getInstance().§get const do§(Sound_LooseLife,"gui_loose_life2");
         §for for dynamic§.getInstance().§get const do§(Sound_LooseLife,"gui_loose_life3");
         §for for dynamic§.getInstance().§get const do§(Sound_LooseLife,"gui_loose_life4");
         §for for dynamic§.getInstance().§get const do§(§_-QE§,"gui_quest_failed");
         §for for dynamic§.getInstance().§get const do§(Sound_GUIButtonCommon,"gui_button_common");
         §for for dynamic§.getInstance().§get const do§(Sound_GUIShowHideMenues,"gui_show_hide_menues");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade");
         §for for dynamic§.getInstance().§get const do§(§_-tm§,"gui_transition_door");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade1");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade2");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade3");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade4");
         §for for dynamic§.getInstance().§get const do§(§extends const final§,"gui_buy_upgrade5");
         §for for dynamic§.getInstance().§get const do§(§_-K§,"gui_open_tower_menu");
         §for for dynamic§.getInstance().§get const do§(§static import§,"gui_mouse_over_tower");
         §for for dynamic§.getInstance().§get const do§(Sound_GUIMouseOverTowerIcon,"gui_mouse_over_tower_common");
         §for for dynamic§.getInstance().§get const do§(§switch const switch§,"gui_mouse_over_metallic");
         §for for dynamic§.getInstance().§get const do§(Sound_AchievementWin,"gui_achievement_win");
         §for for dynamic§.getInstance().§get const do§(§native for super§,"gui_notification_close");
         §for for dynamic§.getInstance().§get const do§(§_-mX§,"gui_notification_popup");
         §for for dynamic§.getInstance().§get const do§(Sound_NotificationOpen,"gui_notification_open");
         §for for dynamic§.getInstance().§get const do§(§_-rE§,"gui_notification_over");
         §for for dynamic§.getInstance().§get const do§(Sound_NotificationPaperOver2,"gui_notification_over2");
         §for for dynamic§.getInstance().§get const do§(§var const if§,"wave_incoming");
         §for for dynamic§.getInstance().§get const do§(§_-LV§,"gui_spell_refresh");
         §for for dynamic§.getInstance().§get const do§(§native for catch§,"gui_spell_select");
         §for for dynamic§.getInstance().§get const do§(§_-Nh§,"gui_rally_point_placed");
         §for for dynamic§.getInstance().§get const do§(§_-Bf§,"tower_building");
         §for for dynamic§.getInstance().§get const do§(§_-KA§,"tower_upgrade");
         §for for dynamic§.getInstance().§get const do§(§_-Ux§,"tower_sell");
         §for for dynamic§.getInstance().§get const do§(archmage_attack_heavy,"archmage_attack_heavy");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack1");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack2");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack3");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack4");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack5");
         §for for dynamic§.getInstance().§get const do§(archmage_attack,"archmage_attack6");
         §for for dynamic§.getInstance().§get const do§(archmage_explosion,"archmage_explosion1");
         §for for dynamic§.getInstance().§get const do§(archmage_explosion,"archmage_explosion2");
         §for for dynamic§.getInstance().§get const do§(archmage_explosion,"archmage_explosion3");
         §for for dynamic§.getInstance().§get const do§(archmage_explosion,"archmage_explosion4");
         §for for dynamic§.getInstance().§get const do§(archmage_precharge,"archmage_precharge1");
         §for for dynamic§.getInstance().§get const do§(archmage_precharge,"archmage_precharge2");
         §for for dynamic§.getInstance().§get const do§(archmage_precharge,"archmage_precharge3");
         §for for dynamic§.getInstance().§get const do§(archmage_precharge,"archmage_precharge4");
         §for for dynamic§.getInstance().§get const do§(archmage_precharge,"archmage_precharge5");
         §for for dynamic§.getInstance().§get const do§(archmage_twister,"archmage_twister1");
         §for for dynamic§.getInstance().§get const do§(archmage_twister,"archmage_twister2");
         §for for dynamic§.getInstance().§get const do§(archmage_twister,"archmage_twister3");
         §for for dynamic§.getInstance().§get const do§(archmage_twister,"archmage_twister4");
         §for for dynamic§.getInstance().§get const do§(necromancer_attack,"necromancer_attack1");
         §for for dynamic§.getInstance().§get const do§(necromancer_attack,"necromancer_attack2");
         §for for dynamic§.getInstance().§get const do§(necromancer_attack,"necromancer_attack3");
         §for for dynamic§.getInstance().§get const do§(necromancer_attack,"necromancer_attack4");
         §for for dynamic§.getInstance().§get const do§(necromancer_attack,"necromancer_attack5");
         §for for dynamic§.getInstance().§get const do§(necromancer_pestilence,"necromancer_pestilence1");
         §for for dynamic§.getInstance().§get const do§(necromancer_pestilence,"necromancer_pestilence2");
         §for for dynamic§.getInstance().§get const do§(necromancer_pestilence,"necromancer_pestilence3");
         §for for dynamic§.getInstance().§get const do§(necromancer_pestilence,"necromancer_pestilence4");
         §for for dynamic§.getInstance().§get const do§(necromancer_pestilence,"necromancer_pestilence5");
         §for for dynamic§.getInstance().§get const do§(necromancer_summon,"necromancer_summon1");
         §for for dynamic§.getInstance().§get const do§(necromancer_summon,"necromancer_summon2");
         §for for dynamic§.getInstance().§get const do§(necromancer_summon,"necromancer_summon3");
         §for for dynamic§.getInstance().§get const do§(necromancer_summon,"necromancer_summon4");
         §for for dynamic§.getInstance().§get const do§(necromancer_summon,"necromancer_summon5");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_spirits,"axlethrower_totem_spirits1");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_spirits,"axlethrower_totem_spirits2");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_spirits,"axlethrower_totem_spirits3");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_spirits,"axlethrower_totem_spirits4");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_vanish,"axlethrower_totem_vanish1");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_vanish,"axlethrower_totem_vanish2");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_vanish,"axlethrower_totem_vanish3");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_vanish,"axlethrower_totem_vanish4");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_weakness,"axlethrower_totem_weakness1");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_weakness,"axlethrower_totem_weakness2");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_weakness,"axlethrower_totem_weakness3");
         §for for dynamic§.getInstance().§get const do§(axlethrower_totem_weakness,"axlethrower_totem_weakness4");
         §for for dynamic§.getInstance().§get const do§(crossbow_eagle,"crossbow_eagle1");
         §for for dynamic§.getInstance().§get const do§(crossbow_eagle,"crossbow_eagle2");
         §for for dynamic§.getInstance().§get const do§(crossbow_eagle,"crossbow_eagle3");
         §for for dynamic§.getInstance().§get const do§(crossbow_eagle,"crossbow_eagle4");
         §for for dynamic§.getInstance().§get const do§(crossbow_multishot,"crossbow_multishot1");
         §for for dynamic§.getInstance().§get const do§(crossbow_multishot,"crossbow_multishot2");
         §for for dynamic§.getInstance().§get const do§(crossbow_multishot,"crossbow_multishot3");
         §for for dynamic§.getInstance().§get const do§(crossbow_multishot,"crossbow_multishot4");
         §for for dynamic§.getInstance().§get const do§(dwaarp_attack,"dwaarp_attack1");
         §for for dynamic§.getInstance().§get const do§(dwaarp_attack,"dwaarp_attack2");
         §for for dynamic§.getInstance().§get const do§(dwaarp_attack,"dwaarp_attack3");
         §for for dynamic§.getInstance().§get const do§(dwaarp_attack,"dwaarp_attack4");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillIn,"dwaarp_drillIn1");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillIn,"dwaarp_drillIn2");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillIn,"dwaarp_drillIn3");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillIn,"dwaarp_drillIn4");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillOut,"dwaarp_drillOut1");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillOut,"dwaarp_drillOut2");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillOut,"dwaarp_drillOut3");
         §for for dynamic§.getInstance().§get const do§(dwaarp_drillOut,"dwaarp_drillOut4");
         §for for dynamic§.getInstance().§get const do§(dwaarp_lavaSmash,"dwaarp_lavaSmash1");
         §for for dynamic§.getInstance().§get const do§(dwaarp_lavaSmash,"dwaarp_lavaSmash2");
         §for for dynamic§.getInstance().§get const do§(dwaarp_lavaSmash,"dwaarp_lavaSmash3");
         §for for dynamic§.getInstance().§get const do§(dwaarp_lavaSmash,"dwaarp_lavaSmash4");
         §for for dynamic§.getInstance().§get const do§(mecha_dropoil,"mecha_dropoil1");
         §for for dynamic§.getInstance().§get const do§(mecha_dropoil,"mecha_dropoil2");
         §for for dynamic§.getInstance().§get const do§(mecha_dropoil,"mecha_dropoil3");
         §for for dynamic§.getInstance().§get const do§(mecha_dropoil,"mecha_dropoil4");
         §for for dynamic§.getInstance().§get const do§(mecha_spawn,"mecha_spawn1");
         §for for dynamic§.getInstance().§get const do§(mecha_spawn,"mecha_spawn2");
         §for for dynamic§.getInstance().§get const do§(mecha_spawn,"mecha_spawn3");
         §for for dynamic§.getInstance().§get const do§(mecha_spawn,"mecha_spawn4");
         §for for dynamic§.getInstance().§get const do§(mecha_steamrelease,"mecha_steamrelease1");
         §for for dynamic§.getInstance().§get const do§(mecha_steamrelease,"mecha_steamrelease2");
         §for for dynamic§.getInstance().§get const do§(mecha_steamrelease,"mecha_steamrelease3");
         §for for dynamic§.getInstance().§get const do§(mecha_steamrelease,"mecha_steamrelease4");
         §for for dynamic§.getInstance().§get const do§(mecha_walk,"mecha_walk1");
         §for for dynamic§.getInstance().§get const do§(mecha_walk,"mecha_walk2");
         §for for dynamic§.getInstance().§get const do§(mecha_walk,"mecha_walk3");
         §for for dynamic§.getInstance().§get const do§(mecha_walk,"mecha_walk4");
         §for for dynamic§.getInstance().§get const do§(assassin_gold,"assassin_gold1");
         §for for dynamic§.getInstance().§get const do§(assassin_gold,"assassin_gold2");
         §for for dynamic§.getInstance().§get const do§(assassin_gold,"assassin_gold3");
         §for for dynamic§.getInstance().§get const do§(assassin_gold,"assassin_gold4");
         §for for dynamic§.getInstance().§get const do§(assassin_sneakattack,"assassin_sneakattack1");
         §for for dynamic§.getInstance().§get const do§(assassin_sneakattack,"assassin_sneakattack2");
         §for for dynamic§.getInstance().§get const do§(assassin_sneakattack,"assassin_sneakattack3");
         §for for dynamic§.getInstance().§get const do§(assassin_sneakattack,"assassin_sneakattack4");
         §for for dynamic§.getInstance().§get const do§(assassin_sneakattack,"assassin_sneakattack5");
         §for for dynamic§.getInstance().§get const do§(templar_arterialStrike,"templar_arterialStrike1");
         §for for dynamic§.getInstance().§get const do§(templar_arterialStrike,"templar_arterialStrike2");
         §for for dynamic§.getInstance().§get const do§(templar_arterialStrike,"templar_arterialStrike3");
         §for for dynamic§.getInstance().§get const do§(templar_arterialStrike,"templar_arterialStrike4");
         §for for dynamic§.getInstance().§get const do§(templar_arterialStrike,"templar_arterialStrike5");
         §for for dynamic§.getInstance().§get const do§(templar_holyGrail,"templar_holyGrail1");
         §for for dynamic§.getInstance().§get const do§(templar_holyGrail,"templar_holyGrail2");
         §for for dynamic§.getInstance().§get const do§(templar_holyGrail,"templar_holyGrail3");
         §for for dynamic§.getInstance().§get const do§(templar_holyGrail,"templar_holyGrail4");
         §for for dynamic§.getInstance().§get const do§(templar_holyGrail,"templar_holyGrail5");
         §for for dynamic§.getInstance().§get const do§(§_-xQ§,"tower_archer_ready");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerArcherTaunt1,"tower_archer_taunt1");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerArcherTaunt2,"tower_archer_taunt2");
         §for for dynamic§.getInstance().§get const do§(axlethrower_taunt_totem1,"axlethrower_taunt_totem1");
         §for for dynamic§.getInstance().§get const do§(axlethrower_taunt_totem2,"axlethrower_taunt_totem2");
         §for for dynamic§.getInstance().§get const do§(axlethrower_taunt_ready,"axlethrower_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(crossbow_taunt_ready,"crossbow_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(crossbow_taunt_multishot,"crossbow_taunt_multishot");
         §for for dynamic§.getInstance().§get const do§(crossbow_taunt_eagle,"crossbow_taunt_eagle");
         §for for dynamic§.getInstance().§get const do§(§while throw§,"tower_mage_ready");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerMageTaunt1,"tower_mage_taunt1");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerMageTaunt2,"tower_mage_taunt2");
         §for for dynamic§.getInstance().§get const do§(archmage_taunt_ready,"archmage_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(archmage_taunt_explosion,"archmage_taunt_explosion");
         §for for dynamic§.getInstance().§get const do§(archmage_taunt_twister,"archmage_taunt_twister");
         §for for dynamic§.getInstance().§get const do§(necromancer_taunt_ready,"necromancer_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(necromancer_taunt_pesti,"necromancer_taunt_pesti");
         §for for dynamic§.getInstance().§get const do§(necromancer_taunt_dknight,"necromancer_taunt_dknight");
         §for for dynamic§.getInstance().§get const do§(necromancer_deathknight_taunt_1,"necromancer_deathknight_taunt_1");
         §for for dynamic§.getInstance().§get const do§(necromancer_deathknight_taunt_2,"necromancer_deathknight_taunt_2");
         §for for dynamic§.getInstance().§get const do§(§catch for use§,"tower_engineer_ready");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerEngineerTaunt1,"tower_engineer_taunt1");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerEngineerTaunt2,"tower_engineer_taunt2");
         §for for dynamic§.getInstance().§get const do§(mecha_taunt_ready,"mecha_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(mecha_taunt_missile,"mecha_taunt_missile");
         §for for dynamic§.getInstance().§get const do§(mecha_taunt_slow,"mecha_taunt_slow");
         §for for dynamic§.getInstance().§get const do§(mecha_taunt_misc,"mecha_taunt_misc");
         §for for dynamic§.getInstance().§get const do§(earthquake_taunt_ready,"earthquake_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(earthquake_taunt_scorched,"earthquake_taunt_scorched");
         §for for dynamic§.getInstance().§get const do§(earthquake_taunt_drill,"earthquake_taunt_drill");
         §for for dynamic§.getInstance().§get const do§(§override const if§,"tower_soldier_ready");
         §for for dynamic§.getInstance().§get const do§(§override implements§,"tower_soldier_move");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerSoldierTaunt1,"tower_soldier_taunt1");
         §for for dynamic§.getInstance().§get const do§(Sound_TowerSoldierTaunt2,"tower_soldier_taunt2");
         §for for dynamic§.getInstance().§get const do§(templar_taunt_ready,"templar_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(templar_taunt_1,"templar_taunt_1");
         §for for dynamic§.getInstance().§get const do§(templar_taunt_2,"templar_taunt_2");
         §for for dynamic§.getInstance().§get const do§(templar_taunt_3,"templar_taunt_3");
         §for for dynamic§.getInstance().§get const do§(assassin_taunt_ready,"assassin_taunt_ready");
         §for for dynamic§.getInstance().§get const do§(assassin_taunt_sneak,"assassin_taunt_sneak");
         §for for dynamic§.getInstance().§get const do§(assassin_taunt_gold,"assassin_taunt_gold");
         §for for dynamic§.getInstance().§get const do§(assassin_taunt_counter,"assassin_taunt_counter");
         §for for dynamic§.getInstance().§get const do§(Sound_Reinforcements1,"reinforcement_event1");
         §for for dynamic§.getInstance().§get const do§(Sound_Reinforcements2,"reinforcement_event2");
         §for for dynamic§.getInstance().§get const do§(Sound_Reinforcements3,"reinforcement_event3");
         §for for dynamic§.getInstance().§get const do§(Sound_Reinforcements4,"reinforcement_event4");
         §for for dynamic§.getInstance().§get const do§(amazon_taunt_1,"amazon_taunt_1");
         §for for dynamic§.getInstance().§get const do§(amazon_taunt_2,"amazon_taunt_2");
         §for for dynamic§.getInstance().§get const do§(pirate_taunt_1,"pirate_taunt_1");
         §for for dynamic§.getInstance().§get const do§(pirate_taunt_2,"pirate_taunt_2");
         §for for dynamic§.getInstance().§get const do§(pirate_taunt_3,"pirate_taunt_3");
         §for for dynamic§.getInstance().§get const do§(legionnaire_taunt_1,"legionnaire_taunt_1");
         §for for dynamic§.getInstance().§get const do§(legionnaire_taunt_2,"legionnaire_taunt_2");
         §for for dynamic§.getInstance().§get const do§(genie_taunt_1,"genie_taunt_1");
         §for for dynamic§.getInstance().§get const do§(genie_taunt_2,"genie_taunt_2");
         §for for dynamic§.getInstance().§get const do§(dwarfArcher_taunt_1,"dwarfArcher_taunt_1");
         §for for dynamic§.getInstance().§get const do§(dwarfArcher_taunt_2,"dwarfArcher_taunt_2");
         §for for dynamic§.getInstance().§get const do§(dwarf_taunt_1,"dwarf_taunt_1");
         §for for dynamic§.getInstance().§get const do§(dwarf_taunt_2,"dwarf_taunt_2");
         §for for dynamic§.getInstance().§get const do§(dwarfBarracks_taunt_1,"dwarfBarracks_taunt_1");
         §for for dynamic§.getInstance().§get const do§(§null class§,"tower_open_door");
         §for for dynamic§.getInstance().§get const do§(§var for const§,"pc_gnome_cash");
         §for for dynamic§.getInstance().§get const do§(§_-gV§,"pc_thunder");
         §for for dynamic§.getInstance().§get const do§(§_-Gm§,"sheep");
         §for for dynamic§.getInstance().§get const do§(§_-fF§,"soldier_fight_1");
         §for for dynamic§.getInstance().§get const do§(§_-cY§,"attack_wolf");
         §for for dynamic§.getInstance().§get const do§(Sound_WolfAttack2,"attack_wolf2");
         §for for dynamic§.getInstance().§get const do§(§with import§,"attack_spider");
         §for for dynamic§.getInstance().§get const do§(Sound_SpiderAttack2,"attack_spider2");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowHit2,"arrow_hit_2");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowHit3,"arrow_hit_3");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease2,"arrow_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease3,"arrow_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease2,"arrow_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease3,"arrow_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease2,"arrow_pool_5");
         §for for dynamic§.getInstance().§get const do§(Sound_ArrowRelease3,"arrow_pool_6");
         §for for dynamic§.getInstance().§get const do§(§_-Z3§,"axe_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-Z3§,"axe_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-Z3§,"axe_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-Z3§,"axe_pool_4");
         §for for dynamic§.getInstance().§get const do§(§use const break§,"shootgun_pool_1");
         §for for dynamic§.getInstance().§get const do§(§use const break§,"shootgun_pool_2");
         §for for dynamic§.getInstance().§get const do§(§use const break§,"shootgun_pool_3");
         §for for dynamic§.getInstance().§get const do§(§use const break§,"shootgun_pool_4");
         §for for dynamic§.getInstance().§get const do§(§var get§,"sniper_pool_1");
         §for for dynamic§.getInstance().§get const do§(§var get§,"sniper_pool_2");
         §for for dynamic§.getInstance().§get const do§(§var get§,"sniper_pool_3");
         §for for dynamic§.getInstance().§get const do§(§var get§,"sniper_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_5");
         §for for dynamic§.getInstance().§get const do§(Sound_Bomb1,"bomb_pool_6");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_1");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_2");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_3");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_4");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_5");
         §for for dynamic§.getInstance().§get const do§(§use for switch§,"bomb_shoot_pool_6");
         §for for dynamic§.getInstance().§get const do§(§_-uE§,"rocket_launch_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-uE§,"rocket_launch_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-uE§,"rocket_launch_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-uE§,"rocket_launch_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-70§,"bolt_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-70§,"bolt_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-70§,"bolt_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-70§,"bolt_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-yT§,"bolt_sorcerer_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-yT§,"bolt_sorcerer_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-yT§,"bolt_sorcerer_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-yT§,"bolt_sorcerer_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-Sz§,"ray_arcane_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-Sz§,"ray_arcane_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-Sz§,"ray_arcane_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-Sz§,"ray_arcane_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_ArcaneDesintegrate,"ray_arcane_desintegrate_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_ArcaneDesintegrate,"ray_arcane_desintegrate_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_ArcaneDesintegrate,"ray_arcane_desintegrate_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_ArcaneDesintegrate,"ray_arcane_desintegrate_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-6W§,"ray_polymorph_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-6W§,"ray_polymorph_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-6W§,"ray_polymorph_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-6W§,"ray_polymorph_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyExplode1,"death_explode_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyExplode1,"death_explode_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyExplode1,"death_explode_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyExplode1,"death_explode_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-yY§,"death_puff_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-yY§,"death_puff_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-yY§,"death_puff_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-yY§,"death_puff_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-LK§,"death_big_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-LK§,"death_big_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-LK§,"death_big_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead1,"death_human_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead2,"death_human_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead1,"death_human_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead3,"death_human_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead4,"death_human_pool_5");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead2,"death_human_pool_6");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead1,"death_human_pool_7");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead3,"death_human_pool_8");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead2,"death_human_pool_9");
         §for for dynamic§.getInstance().§get const do§(Sound_HumanDead4,"death_human_pool_10");
         §for for dynamic§.getInstance().§get const do§(§throw for break§,"death_skeleton_pool_1");
         §for for dynamic§.getInstance().§get const do§(§throw for break§,"death_skeleton_pool_2");
         §for for dynamic§.getInstance().§get const do§(§throw for break§,"death_skeleton_pool_3");
         §for for dynamic§.getInstance().§get const do§(§throw for break§,"death_skeleton_pool_4");
         §for for dynamic§.getInstance().§get const do§(§while for function§,"death_goblin_pool_1");
         §for for dynamic§.getInstance().§get const do§(§while for function§,"death_goblin_pool_2");
         §for for dynamic§.getInstance().§get const do§(§while for function§,"death_goblin_pool_3");
         §for for dynamic§.getInstance().§get const do§(§while for function§,"death_goblin_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-wK§,"death_orc_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-wK§,"death_orc_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-wK§,"death_orc_pool_3");
         §for for dynamic§.getInstance().§get const do§(§import for finally§,"death_troll_pool_1");
         §for for dynamic§.getInstance().§get const do§(§import for finally§,"death_troll_pool_2");
         §for for dynamic§.getInstance().§get const do§(§import for finally§,"death_troll_pool_3");
         §for for dynamic§.getInstance().§get const do§(§import for finally§,"death_troll_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-fY§,"death_elemental_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-fY§,"death_elemental_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-fY§,"death_elemental_pool_3");
         §for for dynamic§.getInstance().§get const do§(§finally for function§,"teleporth_pool_1");
         §for for dynamic§.getInstance().§get const do§(§finally for function§,"teleporth_pool_2");
         §for for dynamic§.getInstance().§get const do§(§finally for function§,"teleporth_pool_3");
         §for for dynamic§.getInstance().§get const do§(§finally for function§,"teleporth_pool_4");
         §for for dynamic§.getInstance().§get const do§(§finally const while§,"thorn_pool_1");
         §for for dynamic§.getInstance().§get const do§(§finally const while§,"thorn_pool_2");
         §for for dynamic§.getInstance().§get const do§(§finally const while§,"thorn_pool_3");
         §for for dynamic§.getInstance().§get const do§(§finally const while§,"thorn_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_PaladinHeal,"paladin_heal_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_PaladinHeal,"paladin_heal_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_PaladinHeal,"paladin_heal_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_PaladinHeal,"paladin_heal_pool_4");
         §for for dynamic§.getInstance().§get const do§(§finally false§,"shrapnel_pool_1");
         §for for dynamic§.getInstance().§get const do§(§finally false§,"shrapnel_pool_2");
         §for for dynamic§.getInstance().§get const do§(§finally false§,"shrapnel_pool_3");
         §for for dynamic§.getInstance().§get const do§(§finally false§,"shrapnel_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-sp§,"area_attack_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-sp§,"area_attack_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-sp§,"area_attack_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-sp§,"area_attack_pool_4");
         §for for dynamic§.getInstance().§get const do§(§_-Tq§,"enemy_healing_pool_1");
         §for for dynamic§.getInstance().§get const do§(§_-Tq§,"enemy_healing_pool_2");
         §for for dynamic§.getInstance().§get const do§(§_-Tq§,"enemy_healing_pool_3");
         §for for dynamic§.getInstance().§get const do§(§_-Tq§,"enemy_healing_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyRocketeer,"rocketeer_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyRocketeer,"rocketeer_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyRocketeer,"rocketeer_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_EnemyRocketeer,"rocketeer_pool_4");
         §for for dynamic§.getInstance().§get const do§(Sound_Chieftain,"rage_pool_1");
         §for for dynamic§.getInstance().§get const do§(Sound_Chieftain,"rage_pool_2");
         §for for dynamic§.getInstance().§get const do§(Sound_Chieftain,"rage_pool_3");
         §for for dynamic§.getInstance().§get const do§(Sound_Chieftain,"rage_pool_4");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack1");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack2");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack3");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack4");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack5");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack6");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack7");
         §for for dynamic§.getInstance().§get const do§(saurian_brute_attack,"saurian_brute_attack8");
         §for for dynamic§.getInstance().§get const do§(canibal_necromancer,"canibal_necromancer1");
         §for for dynamic§.getInstance().§get const do§(canibal_necromancer,"canibal_necromancer2");
         §for for dynamic§.getInstance().§get const do§(canibal_necromancer,"canibal_necromancer3");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_one,"canibal_zombie_one1");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_one,"canibal_zombie_one2");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_one,"canibal_zombie_one3");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_two,"canibal_zombie_two1");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_two,"canibal_zombie_two2");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_two,"canibal_zombie_two3");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_three,"canibal_zombie_three1");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_three,"canibal_zombie_three2");
         §for for dynamic§.getInstance().§get const do§(canibal_zombie_three,"canibal_zombie_three3");
         §for for dynamic§.getInstance().§get const do§(wilhelm_scream,"wilhelm_scream1");
         §for for dynamic§.getInstance().§get const do§(wilhelm_scream,"wilhelm_scream2");
         §for for dynamic§.getInstance().§get const do§(wilhelm_scream,"wilhelm_scream3");
         §for for dynamic§.getInstance().§get const do§(savant_portal_loop,"savant_portal_loop");
         §for for dynamic§.getInstance().§get const do§(savant_portal_loop,"savant_portal_loop2");
         §for for dynamic§.getInstance().§get const do§(savant_portal_loop,"savant_portal_loop3");
         §for for dynamic§.getInstance().§get const do§(§_-7B§,"savant_open_portal1");
         §for for dynamic§.getInstance().§get const do§(§_-7B§,"savant_open_portal2");
         §for for dynamic§.getInstance().§get const do§(§_-7B§,"savant_open_portal3");
         §for for dynamic§.getInstance().§get const do§(savant_attack,"savant_attack1");
         §for for dynamic§.getInstance().§get const do§(savant_attack,"savant_attack2");
         §for for dynamic§.getInstance().§get const do§(savant_attack,"savant_attack3");
         §for for dynamic§.getInstance().§get const do§(nightscale_invisibility,"nightscale_invisibility1");
         §for for dynamic§.getInstance().§get const do§(nightscale_invisibility,"nightscale_invisibility2");
         §for for dynamic§.getInstance().§get const do§(nightscale_invisibility,"nightscale_invisibility3");
         §for for dynamic§.getInstance().§get const do§(myrmidon_bite,"myrmidon_bite1");
         §for for dynamic§.getInstance().§get const do§(myrmidon_bite,"myrmidon_bite2");
         §for for dynamic§.getInstance().§get const do§(myrmidon_bite,"myrmidon_bite3");
         §for for dynamic§.getInstance().§get const do§(darter_teleout,"darter_teleout1");
         §for for dynamic§.getInstance().§get const do§(darter_teleout,"darter_teleout2");
         §for for dynamic§.getInstance().§get const do§(darter_teleout,"darter_teleout3");
         §for for dynamic§.getInstance().§get const do§(canibal_eating,"canibal_eating1");
         §for for dynamic§.getInstance().§get const do§(canibal_eating,"canibal_eating2");
         §for for dynamic§.getInstance().§get const do§(canibal_eating,"canibal_eating3");
         §for for dynamic§.getInstance().§get const do§(blazefang_death,"blazefang_death1");
         §for for dynamic§.getInstance().§get const do§(blazefang_death,"blazefang_death2");
         §for for dynamic§.getInstance().§get const do§(blazefang_death,"blazefang_death3");
         §for for dynamic§.getInstance().§get const do§(blazefang_attack,"blazefang_attack1");
         §for for dynamic§.getInstance().§get const do§(blazefang_attack,"blazefang_attack2");
         §for for dynamic§.getInstance().§get const do§(blazefang_attack,"blazefang_attack3");
         §for for dynamic§.getInstance().§get const do§(wasp_3,"wasp_3");
         §for for dynamic§.getInstance().§get const do§(wasp_2,"wasp_2");
         §for for dynamic§.getInstance().§get const do§(wasp_1,"wasp_1");
         §for for dynamic§.getInstance().§get const do§(sandwraith_coffin,"sandwraith_coffin1");
         §for for dynamic§.getInstance().§get const do§(sandwraith_coffin,"sandwraith_coffin2");
         §for for dynamic§.getInstance().§get const do§(sandwraith_coffin,"sandwraith_coffin3");
         §for for dynamic§.getInstance().§get const do§(savant_telein,"savant_telein1");
         §for for dynamic§.getInstance().§get const do§(savant_telein,"savant_telein2");
         §for for dynamic§.getInstance().§get const do§(savant_telein,"savant_telein3");
         §for for dynamic§.getInstance().§get const do§(boss_cinematic,"boss_cinematic");
         §for for dynamic§.getInstance().§get const do§(bantha_fart,"bantha_fart");
         §for for dynamic§.getInstance().§get const do§(frog_dance,"frog_dance");
         §for for dynamic§.getInstance().§get const do§(tusken,"tusken");
         §for for dynamic§.getInstance().§get const do§(stargate,"stargate1");
         §for for dynamic§.getInstance().§get const do§(stargate,"stargate2");
         §for for dynamic§.getInstance().§get const do§(stargate,"stargate3");
         §for for dynamic§.getInstance().§get const do§(worm_bite,"worm_bite");
         §for for dynamic§.getInstance().§get const do§(worm_dirtLoop,"worm_dirtLoop");
         §for for dynamic§.getInstance().§get const do§(bantha_roar,"bantha_roar1");
         §for for dynamic§.getInstance().§get const do§(bantha_roar,"bantha_roar2");
         §for for dynamic§.getInstance().§get const do§(bantha_roar,"bantha_roar3");
         §for for dynamic§.getInstance().§get const do§(bantha_roar,"bantha_roar4");
         §for for dynamic§.getInstance().§get const do§(music_Desert_Battle,"music_Desert_Battle");
         §for for dynamic§.getInstance().§get const do§(music_Desert_Prep,"music_Desert_Prep");
         §for for dynamic§.getInstance().§get const do§(efreeti_towers_released,"efreeti_towers_released");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_evillaugh,"boss_efreeti_evillaugh");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_snapping,"boss_efreeti_snapping");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_clapping,"boss_efreeti_clapping");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_summon,"boss_efreeti_summon");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_death,"boss_efreeti_death");
         §for for dynamic§.getInstance().§get const do§(boss_efreeti_doorbreak,"boss_efreeti_doorbreak");
         §for for dynamic§.getInstance().§get const do§(indianasound,"indianasound");
         §for for dynamic§.getInstance().§get const do§(indiana_select,"indiana_select1");
         §for for dynamic§.getInstance().§get const do§(indiana_select,"indiana_select2");
         §for for dynamic§.getInstance().§get const do§(indiana_select,"indiana_select3");
         §for for dynamic§.getInstance().§get const do§(indiana_runs,"indiana_runs");
         §for for dynamic§.getInstance().§get const do§(alien_egg_open,"alien_egg_open");
         §for for dynamic§.getInstance().§get const do§(cut_trees,"cut_trees");
         §for for dynamic§.getInstance().§get const do§(volcano_throwVirgin,"volcano_throwVirgin");
         §for for dynamic§.getInstance().§get const do§(volcano_virginSplash.sfk,"volcano_virginSplash.sfk");
         §for for dynamic§.getInstance().§get const do§(volcano_lavaShot,"volcano_lavaShot");
         §for for dynamic§.getInstance().§get const do§(volcano_lavaShotHit,"volcano_lavaShotHit");
         §for for dynamic§.getInstance().§get const do§(§if implements§,"mermaid_1");
         §for for dynamic§.getInstance().§get const do§(§if implements§,"mermaid_2");
         §for for dynamic§.getInstance().§get const do§(§if implements§,"mermaid_3");
         §for for dynamic§.getInstance().§get const do§(§if implements§,"mermaid_4");
         §for for dynamic§.getInstance().§get const do§(carnivore_plant,"carnivore_plant");
         §for for dynamic§.getInstance().§get const do§(volcano_splash,"volcano_splash");
         §for for dynamic§.getInstance().§get const do§(volcano_virginScream,"volcano_virginScream");
         §for for dynamic§.getInstance().§get const do§(jungle_1,"jungle_1");
         §for for dynamic§.getInstance().§get const do§(music_Jungle_Prep,"music_Jungle_Battle");
         §for for dynamic§.getInstance().§get const do§(music_Jungle_Battle,"music_Jungle_Prep");
         §for for dynamic§.getInstance().§get const do§(boss_mono_totem,"boss_mono_totem");
         §for for dynamic§.getInstance().§get const do§(boss_mono_enterscene,"boss_mono_enterscene");
         §for for dynamic§.getInstance().§get const do§(boss_mono_chimps_3,"boss_mono_chimps_3");
         §for for dynamic§.getInstance().§get const do§(boss_mono_chimps_2,"boss_mono_chimps_2");
         §for for dynamic§.getInstance().§get const do§(boss_mono_chimps_1,"boss_mono_chimps_1");
         §for for dynamic§.getInstance().§get const do§(boss_mono_chestdrum,"boss_mono_chestdrum");
         §for for dynamic§.getInstance().§get const do§(boss_mono_saltototem,"boss_mono_saltototem");
         §for for dynamic§.getInstance().§get const do§(boss_mono_death,"boss_mono_death");
         §for for dynamic§.getInstance().§get const do§(boss_mono_attack,"boss_mono_attack1");
         §for for dynamic§.getInstance().§get const do§(boss_mono_attack,"boss_mono_attack2");
         §for for dynamic§.getInstance().§get const do§(boss_mono_attack,"boss_mono_attack3");
         §for for dynamic§.getInstance().§get const do§(ambience_underground_2,"ambience_underground_2");
         §for for dynamic§.getInstance().§get const do§(ambience_underground_1,"ambience_underground_1");
         §for for dynamic§.getInstance().§get const do§(mountain_door,"mountain_door");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_flamethrower,"hero_dragon_flamethrower");
         §for for dynamic§.getInstance().§get const do§(music_Underground_Battle,"music_Underground_Battle");
         §for for dynamic§.getInstance().§get const do§(music_Underground_Prep,"music_Underground_Prep");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm4,"dragonHero_taunt_confirm4");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm3,"dragonHero_taunt_confirm3");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm2,"dragonHero_taunt_confirm2");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm1,"dragonHero_taunt_confirm1");
         §for for dynamic§.getInstance().§get const do§(music_Finalboss_prefight,"music_Finalboss_prefight");
         §for for dynamic§.getInstance().§get const do§(music_Finalboss_fight,"music_Finalboss_fight");
         §for for dynamic§.getInstance().§get const do§(music_Victory_Theme,"music_Victory_Theme");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_openportal,"boss_umbra_openportal");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_release_1,"boss_umbra_release_1");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_release_2,"boss_umbra_release_2");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_respawn,"boss_umbra_respawn");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_teleport,"boss_umbra_teleport");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_shootray,"boss_umbra_shootray");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_explode,"boss_umbra_explode");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_tower,"boss_umbra_tower");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_death,"boss_umbra_death");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_join,"boss_umbra_sphere_join1");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_join,"boss_umbra_sphere_join2");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_join,"boss_umbra_sphere_join3");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_rise,"boss_umbra_sphere_rise1");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_rise,"boss_umbra_sphere_rise2");
         §for for dynamic§.getInstance().§get const do§(boss_umbra_sphere_rise,"boss_umbra_sphere_rise3");
         §for for dynamic§.getInstance().§get const do§(Sound_SpellTowerHold_Dissipate,"Sound_SpellTowerHold_Dissipate");
         §for for dynamic§.getInstance().§get const do§(Sound_SpellTowerHold_Cast,"Sound_SpellTowerHold_Cast");
         §for for dynamic§.getInstance().§get const do§(music_Map_Theme,"music_Map_Theme");
         §for for dynamic§.getInstance().§get const do§(music_MusicSuspense,"music_MusicSuspense");
         §for for dynamic§.getInstance().§get const do§(music_savage_music_theme,"music_savage_music_theme");
         §for for dynamic§.getInstance().§get const do§(music_boss_prefight,"music_boss_prefight");
         §for for dynamic§.getInstance().§get const do§(alric_taunt_confirm_1,"alric_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(alric_taunt_confirm_2,"alric_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(alric_taunt_confirm_3,"alric_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(alric_taunt_confirm_4,"alric_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(alric_taunt_death,"alric_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_alric_flurry,"hero_alric_flurry_1");
         §for for dynamic§.getInstance().§get const do§(hero_alric_flurry,"hero_alric_flurry_2");
         §for for dynamic§.getInstance().§get const do§(hero_alric_flurry,"hero_alric_flurry_3");
         §for for dynamic§.getInstance().§get const do§(hero_alric_sandwarrior,"hero_alric_sandwarrior");
         §for for dynamic§.getInstance().§get const do§(hero_nivus_desintegrate,"hero_nivus_desintegrate");
         §for for dynamic§.getInstance().§get const do§(hero_nivus_teleport,"hero_nivus_teleport");
         §for for dynamic§.getInstance().§get const do§(hero_nivus_attack,"hero_nivus_attack");
         §for for dynamic§.getInstance().§get const do§(hero_nivus_magicmissile_hit,"hero_nivus_magicmissile_hit");
         §for for dynamic§.getInstance().§get const do§(hero_nivus_magicmissile_summon,"hero_nivus_magicmissile_summon");
         §for for dynamic§.getInstance().§get const do§(wizzard_taunt_confirm_4,"wizzard_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(wizzard_taunt_death,"wizzard_taunt_death");
         §for for dynamic§.getInstance().§get const do§(wizzard_taunt_confirm_1,"wizzard_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(wizzard_taunt_confirm_2,"wizzard_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(wizzard_taunt_confirm_3,"wizzard_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_confirm_1,"blackthorne_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_confirm_2,"blackthorne_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_confirm_3,"blackthorne_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_confirm_4,"blackthorne_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_death,"blackthorne_taunt_death");
         §for for dynamic§.getInstance().§get const do§(blackthorne_taunt_extra,"blackthorne_taunt_extra");
         §for for dynamic§.getInstance().§get const do§(hero_blackthorne_barrel,"hero_blackthorne_barrel");
         §for for dynamic§.getInstance().§get const do§(hero_blackthorne_kraken,"hero_blackthorne_kraken");
         §for for dynamic§.getInstance().§get const do§(beastmaster_taunt_confirm_1,"beastmaster_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(beastmaster_taunt_confirm_2,"beastmaster_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(beastmaster_taunt_confirm_3,"beastmaster_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(beastmaster_taunt_confirm_4,"beastmaster_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(beastmaster_taunt_death,"beastmaster_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_rhino_stampede,"hero_cronan_rhino_stampede");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_summon_boar,"hero_cronan_summon_boar");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_summon_rhino,"hero_cronan_summon_rhino");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_whiplash,"hero_cronan_whiplash");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_boar_attack,"hero_cronan_boar_attack");
         §for for dynamic§.getInstance().§get const do§(hero_priest_consecrate,"hero_priest_consecrate");
         §for for dynamic§.getInstance().§get const do§(hero_priest_healing,"hero_priest_healing");
         §for for dynamic§.getInstance().§get const do§(hero_priest_teleport,"hero_priest_teleport");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_1,"priest_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_2,"priest_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_2,"priest_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_3,"priest_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_4,"priest_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_confirm_5,"priest_taunt_confirm_5");
         §for for dynamic§.getInstance().§get const do§(priest_taunt_death,"priest_taunt_death");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm1,"dragonHero_taunt_confirmA1");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm2,"dragonHero_taunt_confirmA2");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm3,"dragonHero_taunt_confirmA3");
         §for for dynamic§.getInstance().§get const do§(dragonHero_taunt_confirm4,"dragonHero_taunt_confirmA4");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_birth,"hero_dragon_birth");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_death,"hero_dragon_death");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_fireball_explode,"hero_dragon_fireball_explode");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_flamethrower,"hero_dragon_flamethrower");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_napalm,"hero_dragon_napalm");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_smoke,"hero_dragon_smoke");
         §for for dynamic§.getInstance().§get const do§(hero_dragon_spit,"hero_dragon_spit");
         §for for dynamic§.getInstance().§get const do§(giant_taunt_confirm_1,"giant_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(giant_taunt_confirm_2,"giant_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(giant_taunt_confirm_3,"giant_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(giant_taunt_confirm_4,"giant_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(giant_taunt_death,"giant_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_bigpunch,"hero_grawl_bigpunch");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_boulder_hit,"hero_grawl_boulder_hit");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_boulder_throw,"hero_grawl_boulder_throw");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_stomp,"hero_grawl_stomp1");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_stomp,"hero_grawl_stomp2");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_stomp,"hero_grawl_stomp3");
         §for for dynamic§.getInstance().§get const do§(hero_grawl_stomp,"hero_grawl_stomp4");
         §for for dynamic§.getInstance().§get const do§(assassinHero_taunt_confirm_1,"assassinHero_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(assassinHero_taunt_confirm_2,"assassinHero_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(assassinHero_taunt_confirm_3,"assassinHero_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(assassinHero_taunt_confirm_4,"assassinHero_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(assassinHero_taunt_death,"assassinHero_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_lethalstrike_hit,"hero_mirage_lethalstrike_hit");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_lethalstrike_vanish,"hero_mirage_lethalstrike_vanish");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_shadowdance_cast,"hero_mirage_shadowdance_cast");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_shadowdance_hit,"hero_mirage_shadowdance_hit");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_shadowdodge_puff,"hero_mirage_shadowdodge_puff");
         §for for dynamic§.getInstance().§get const do§(hero_mirage_shadowdodge,"hero_mirage_shadowdodge");
         §for for dynamic§.getInstance().§get const do§(alien_taunt_confirm_1,"alien_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(alien_taunt_confirm_2,"alien_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(alien_taunt_confirm_3,"alien_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(alien_taunt_confirm_4,"alien_taunt_confirm_4");
         §for for dynamic§.getInstance().§get const do§(alien_taunt_death,"alien_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_alien_abduction,"hero_alien_abduction");
         §for for dynamic§.getInstance().§get const do§(hero_alien_death_explosion,"hero_alien_death_explosion");
         §for for dynamic§.getInstance().§get const do§(hero_alien_disc_bounce,"hero_alien_disc_bounce");
         §for for dynamic§.getInstance().§get const do§(hero_alien_disc_throw,"hero_alien_disc_throw");
         §for for dynamic§.getInstance().§get const do§(hero_alien_drone_call,"hero_alien_drone_call");
         §for for dynamic§.getInstance().§get const do§(hero_alien_drone_leave,"hero_alien_drone_leave");
         §for for dynamic§.getInstance().§get const do§(hero_alien_drone_ray_loop,"hero_alien_drone_ray_loop");
         §for for dynamic§.getInstance().§get const do§(Level_up2,"Level_up2");
         §for for dynamic§.getInstance().§get const do§(dwarf_taunt_1,"dwarf_taunt_1");
         §for for dynamic§.getInstance().§get const do§(dwarf_taunt_2,"dwarf_taunt_2");
         §for for dynamic§.getInstance().§get const do§(dwarfArcher_taunt_2,"dwarfArcher_taunt_2");
         §for for dynamic§.getInstance().§get const do§(dwarfArcher_taunt_1,"dwarfArcher_taunt_1");
         §for for dynamic§.getInstance().§get const do§(dwarfBarracks_taunt_1,"dwarfBarracks_taunt_1");
         §for for dynamic§.getInstance().§get const do§(dwarfHero_taunt_confirm_1,"dwarfHero_taunt_confirm_1");
         §for for dynamic§.getInstance().§get const do§(dwarfHero_taunt_confirm_2,"dwarfHero_taunt_confirm_2");
         §for for dynamic§.getInstance().§get const do§(dwarfHero_taunt_confirm_3,"dwarfHero_taunt_confirm_3");
         §for for dynamic§.getInstance().§get const do§(dwarfHero_taunt_death,"dwarfHero_taunt_death");
         §for for dynamic§.getInstance().§get const do§(hero_cronan_bird_attack,"hero_cronan_bird_attack");
         §for for dynamic§.getInstance().§get const do§(sound_tesla_attack_1,"sound_tesla_attack_1");
         §for for dynamic§.getInstance().§get const do§(sound_tesla_attack_2,"sound_tesla_attack_2");
      }
      
      public function §do§() : void
      {
         Locale.setString("C_WAVE","en","Wave");
         Locale.setString("C_SEC","en"," secs");
         Locale.setString("C_DAMAGE_NONE","en","None");
         Locale.setString("C_LIFE","en","Life");
         Locale.setString("C_HEALING","en","Heal");
         Locale.setString("C_RESPAWN","en","Respawn");
         Locale.setString("C_ARMOR","en","Physical Armor");
         Locale.setString("C_RANGE","en","Range");
         Locale.setString("C_DAMAGE","en","Damage");
         Locale.setString("C_RELOAD","en","Reload");
         Locale.setString("C_COOLDOWN","en","Cooldown");
         Locale.setString("C_UNLOCKS","en","Unlocks");
         Locale.setString("C_CURSE","en","Curse");
         Locale.setString("C_DURATION","en","Duration");
         Locale.setString("C_CHANCE","en","Chance");
         Locale.setString("C_SLOW","en","Slow");
         Locale.setString("C_ONSET_LIFE","en","Onset life");
         Locale.setString("C_MAX_ENEMIES","en","Max enemies");
         Locale.setString("C_MAX_MISSILES","en","Missiles");
         Locale.setString("C_OVER_DURATION","en"," / sec");
         Locale.setString("C_ARMOR_0","en","None");
         Locale.setString("C_ARMOR_1","en","Low");
         Locale.setString("C_ARMOR_2","en","Medium");
         Locale.setString("C_ARMOR_3","en","High");
         Locale.setString("C_ARMOR_4","en","Great");
         Locale.setString("C_SPEED_0","en","Slow");
         Locale.setString("C_SPEED_1","en","Medium");
         Locale.setString("C_SPEED_2","en","Fast");
         Locale.setString("C_RELOAD_0","en","Very Slow");
         Locale.setString("C_RELOAD_1","en","Slow");
         Locale.setString("C_RELOAD_2","en","Average");
         Locale.setString("C_RELOAD_3","en","Fast");
         Locale.setString("C_RELOAD_4","en","Very Fast");
         Locale.setString("C_RANGE_0","en","Short");
         Locale.setString("C_RANGE_1","en","Average");
         Locale.setString("C_RANGE_2","en","Long");
         Locale.setString("C_RANGE_3","en","Great");
         Locale.setString("C_RANGE_4","en","Extreme");
         Locale.setString("C_UNKNOWN","en","Unknown");
         Locale.setString("C_IRON_WAVE","en","Iron Wave");
         Locale.setString("C_MODE_0","en","Campaign");
         Locale.setString("C_MODE_1","en","Heroic");
         Locale.setString("C_MODE_2","en","Iron");
         Locale.setString("C_DIFFICULTY_NORMAL","en","Completed Normal");
         Locale.setString("C_DIFFICULTY_EASY","en","Completed Casual");
         Locale.setString("C_DIFFICULTY_HARD","en","Completed Veteran");
         Locale.setString("TOWER_LOCKED_NAME","en","Locked!");
         Locale.setString("TOWER_LOCKED_DESCRIPTION","en","This item is locked.");
         Locale.setString("TOWER_BARRACKS_RALLY_POINT","en","Rally Point");
         Locale.setString("TOWER_BARRACKS_RALLY_POINT_DESCRIPTION","en","Change the rally point where soldiers defend.");
         Locale.setString("TOWER_BARRACKS_NAME","en","Barracks");
         Locale.setString("TOWER_BARRACKS_DESCRIPTION","en","Trains militia, tough soldiers that block and damage your enemies.");
         Locale.setString("TOWER_BARRACKS_UPGRADE_LEVEL2_NAME","en","Footmen Barracks");
         Locale.setString("TOWER_BARRACKS_UPGRADE_LEVEL2_DESCRIPTION","en","Footmen are better trained and equipped than basic militia. They can become the backbone of a good army.");
         Locale.setString("TOWER_BARRACKS_UPGRADE_LEVEL3_NAME","en","Knights Barracks");
         Locale.setString("TOWER_BARRACKS_UPGRADE_LEVEL3_DESCRIPTION","en","Knights are professional soldiers with heavy armor. Dedicated to his majesty, they will stop your enemies’ advance.");
         Locale.setString("TOWER_ARCHERS_NAME","en","Archer Tower");
         Locale.setString("SPECIAL_DWARF_BASTION_NAME","en","Dwarf Bastion");
         Locale.setString("TOWER_ARCHERS_DESCRIPTION","en","Archers ready to strike at your enemies from a distance.");
         Locale.setString("TOWER_ARCHERS_UPGRADE_LEVEL2_NAME","en","Marksmen Tower");
         Locale.setString("TOWER_ARCHERS_UPGRADE_LEVEL2_DESCRIPTION","en","Marksmen shoot broadhead arrows, dealing more damage. Their longbows have a longer attack range.");
         Locale.setString("TOWER_ARCHERS_UPGRADE_LEVEL3_NAME","en","Sharpshooter Tower");
         Locale.setString("TOWER_ARCHERS_UPGRADE_LEVEL3_DESCRIPTION","en","Once archers reach the sharpshooter level, their attack range and damage potential increases above any other archer’s.");
         Locale.setString("TOWER_ENGINEERS_NAME","en","Dwarven Bombard");
         Locale.setString("TOWER_ENGINEERS_DESCRIPTION","en","Bombards ground enemies dealing area damage.");
         Locale.setString("TOWER_ENGINEERS_UPGRADE_LEVEL2_NAME","en","Dwarven Artillery");
         Locale.setString("TOWER_ENGINEERS_UPGRADE_LEVEL2_DESCRIPTION","en","Enhanced dwarven ordnance, this artillery will blast an even larger area.");
         Locale.setString("TOWER_ENGINEERS_UPGRADE_LEVEL3_NAME","en","Dwarven Howitzer");
         Locale.setString("TOWER_ENGINEERS_UPGRADE_LEVEL3_DESCRIPTION","en","They build them bigger and bigger, don’t they? Your enemies stand no chance!");
         Locale.setString("TOWER_MAGES_NAME","en","Mages");
         Locale.setString("TOWER_MAGES_DESCRIPTION","en","Mages cast armor piercing bolts at your enemies, ignoring any physical protection.");
         Locale.setString("TOWER_MAGES_UPGRADE_LEVEL2_NAME","en","Adept Tower");
         Locale.setString("TOWER_MAGES_UPGRADE_LEVEL2_DESCRIPTION","en","Adepts cast enhanced bolts, which can tear through armor, flesh and bone.");
         Locale.setString("TOWER_MAGES_UPGRADE_LEVEL3_NAME","en","Wizard Tower");
         Locale.setString("TOWER_MAGES_UPGRADE_LEVEL3_DESCRIPTION","en","Wizards cast high-energy bolts, which rip apart the very essence of enemy troops.");
         Locale.setString("TOWER_SELL","en","Sell Tower");
         Locale.setString("TOWER_SELL_DESCRIPTION","en","Sell this tower and get a " + "{price}" + " GP refund.");
         Locale.setString("TOWER_ASSASSIN_NAME","en","Assassins\' Guild");
         Locale.setString("TOWER_ASSASSIN_DESCRIPTION","en","Trains agile and deadly Assassins to ambush and rob enemies.");
         Locale.setString("TOWER_ASSASSIN_SPECIAL","en","Sneak Attack, Counterattack, Pickpocket");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NAME","en","Sneak Attack");
         Locale.setString("TOWER_ASSASSINS_SNEAK_DESCRIPTION","en","Attacks have a chance of becoming Sneak Attacks, dealing 20 to 40 damage and ignoring armor.");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NOTE","en","Requiescat in pace!");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NAME_1","en","Sneak Attack");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NAME_2","en","Sneak Attack II");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NAME_3","en","Sneak Attack III");
         Locale.setString("TOWER_ASSASSINS_SNEAK_DESCRIPTION_1","en","Attacks have a chance of becoming Sneak Attacks, dealing 20 to 40 damage and ignoring armor.");
         Locale.setString("TOWER_ASSASSINS_SNEAK_DESCRIPTION_2","en","Improves Sneak Attack chance, and increases damage to 30-50.");
         Locale.setString("TOWER_ASSASSINS_SNEAK_DESCRIPTION_3","en","Improves Sneak Attack chance, and increases damage to 40-60.");
         Locale.setString("TOWER_ASSASSINS_SNEAK_NOTE_1","en","Requiescat in pace!");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NAME","en","Counterattack");
         Locale.setString("TOWER_ASSASSINS_COUNTER_DESCRIPTION","en","Improves dodge chance to 50% and makes them counterattack dealing 20 to 24 damage.");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NOTE","en","No action without reaction!");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NAME_1","en","Counterattack");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NAME_2","en","Counterattack II");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NAME_3","en","Counterattack III");
         Locale.setString("TOWER_ASSASSINS_COUNTER_DESCRIPTION_1","en","Improves dodge chance to 50% and counterattacks, dealing 20 to 24 damage.");
         Locale.setString("TOWER_ASSASSINS_COUNTER_DESCRIPTION_2","en","Dodge chance increases to 60% and counterattack damage to 30 - 34.");
         Locale.setString("TOWER_ASSASSINS_COUNTER_DESCRIPTION_3","en","Dodge chance increases to 70% and counterattack damage to 40 - 44.");
         Locale.setString("TOWER_ASSASSINS_COUNTER_NOTE_1","en","No action without reaction!");
         Locale.setString("TOWER_ASSASSINS_PICK_NAME","en","Pickpocket");
         Locale.setString("TOWER_ASSASSINS_PICK_DESCRIPTION","en","Assassin attacks have a 30% chance of stealing some gold from their victims.");
         Locale.setString("TOWER_ASSASSINS_PICK_NOTE","en","I call it treasure hunting!");
         Locale.setString("TOWER_ASSASSINS_PICK_NAME_1","en","Pickpocket");
         Locale.setString("TOWER_ASSASSINS_PICK_NAME_2","en","Pickpocket II");
         Locale.setString("TOWER_ASSASSINS_PICK_NAME_3","en","Pickpocket III");
         Locale.setString("TOWER_ASSASSINS_PICK_DESCRIPTION_1","en","Assassin attacks have a 30% chance of stealing some gold from its victim.");
         Locale.setString("TOWER_ASSASSINS_PICK_DESCRIPTION_2","en","Increases Pickpocket chance to 40%.");
         Locale.setString("TOWER_ASSASSINS_PICK_DESCRIPTION_3","en","Increases Pickpocket chance to 50%.");
         Locale.setString("TOWER_TEMPLAR_NAME","en","Knights Templar");
         Locale.setString("TOWER_TEMPLAR_DESCRIPTION","en","Seasoned resilient warriors, the templars are a force to be reckoned!");
         Locale.setString("TOWER_TEMPLAR_SPECIAL","en","Arterial Strike, Holy Grail, Toughness");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NAME","en","Arterial Strike");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_DESCRIPTION","en","Attacks have a chance of cutting an artery and bleeding its target for 75 damage over 3 seconds.");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NOTE","en","Let it bleed!");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NAME_1","en","Arterial Strike");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NAME_2","en","Arterial Strike II");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NAME_3","en","Arterial Strike III");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_DESCRIPTION_1","en","Attacks have a chance of causing bleeding, dealing 75 damage over 3 seconds.");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_DESCRIPTION_2","en","Increases bleeding damage to 120 over 3 seconds.");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_DESCRIPTION_3","en","Increases bleeding damage to 165 over 3 seconds.");
         Locale.setString("TOWER_TEMPLARS_ARTERIAL_NOTE_1","en","Let it bleed!");
         Locale.setString("TOWER_TEMPLARS_HOLY_NAME","en","Holy Grail");
         Locale.setString("TOWER_TEMPLARS_HOLY_DESCRIPTION","en","Templars have a 20% chance of cheating death every time they are dealt lethal damage.");
         Locale.setString("TOWER_TEMPLARS_HOLY_NOTE","en","That\'s the cup of a carpenter.");
         Locale.setString("TOWER_TEMPLARS_HOLY_NAME_1","en","Holy Grail");
         Locale.setString("TOWER_TEMPLARS_HOLY_NAME_2","en","Holy Grail II");
         Locale.setString("TOWER_TEMPLARS_HOLY_NAME_3","en","Holy Grail III");
         Locale.setString("TOWER_TEMPLARS_HOLY_DESCRIPTION_1","en","Templars have a 20% chance of cheating death every time they are dealt lethal damage.");
         Locale.setString("TOWER_TEMPLARS_HOLY_DESCRIPTION_2","en","Holy Grail chance is increased to 30%.");
         Locale.setString("TOWER_TEMPLARS_HOLY_DESCRIPTION_3","en","Holy Grail chance is increased to 40%.");
         Locale.setString("TOWER_TEMPLARS_HOLY_NOTE_1","en","That\'s the cup of a carpenter.");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_NAME","en","Toughness");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_DESCRIPTION","en","Increases knights\' life by an extra 50.");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_NOTE","en","When the going gets tough...");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_NAME_1","en","Toughness");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_NAME_2","en","Toughness II");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_NAME_3","en","Toughness III");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_DESCRIPTION_1","en","Increases templar’s life by an extra 50.");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_DESCRIPTION_2","en","Increases templar’s life by an extra 50.");
         Locale.setString("TOWER_TEMPLARS_TOUGHNESS_DESCRIPTION_3","en","Increases templar’s life by an extra 50.");
         Locale.setString("TOWER_TOTEM_NAME","en","Tribal Axethrowers");
         Locale.setString("TOWER_TOTEM_DESCRIPTION","en","The wildlings are covered in mystery and occult forces, but their axes show deadly precision.");
         Locale.setString("TOWER_TOTEM_SPECIAL","en","Totem of Weakness, Totem of Spirits");
         Locale.setString("TOWER_TOTEM_WEAKNESS_NAME","en","Totem of Weakness");
         Locale.setString("TOWER_TOTEM_WEAKNESS_DESCRIPTION","en","Weakens enemies and makes them sustain 40% extra damage from all sources for 3 seconds.");
         Locale.setString("TOWER_TOTEM_WEAKNESS_NOTE","en","Begone weaklings!");
         Locale.setString("TOWER_TOTEM_WEAKNESS_NAME_1","en","Totem of Weakness");
         Locale.setString("TOWER_TOTEM_WEAKNESS_NAME_2","en","Totem of Weakness II");
         Locale.setString("TOWER_TOTEM_WEAKNESS_NAME_3","en","Totem of Weakness III");
         Locale.setString("TOWER_TOTEM_WEAKNESS_DESCRIPTION_1","en","Weakens enemies and makes them sustain 40% extra damage from all sources for 3 seconds.");
         Locale.setString("TOWER_TOTEM_WEAKNESS_DESCRIPTION_2","en","Increases Totem duration to 6 seconds. ");
         Locale.setString("TOWER_TOTEM_WEAKNESS_DESCRIPTION_3","en","Increases Totem duration to 9 seconds. ");
         Locale.setString("TOWER_TOTEM_SPIRITS_NAME","en","Totem of Spirits");
         Locale.setString("TOWER_TOTEM_SPIRITS_DESCRIPTION","en","Dispels all magic and silences spellcasters in range for 4 seconds.");
         Locale.setString("TOWER_TOTEM_SPIRITS_NOTE","en","Fight magic with magic...");
         Locale.setString("TOWER_TOTEM_SPIRITS_NAME_1","en","Totem of Spirits");
         Locale.setString("TOWER_TOTEM_SPIRITS_NAME_2","en","Totem of Spirits II");
         Locale.setString("TOWER_TOTEM_SPIRITS_NAME_3","en","Totem of Spirits III");
         Locale.setString("TOWER_TOTEM_SPIRITS_DESCRIPTION_1","en","Dispells all magic and silences spellcasters in range for 4 seconds.");
         Locale.setString("TOWER_TOTEM_SPIRITS_DESCRIPTION_2","en","Increases Totem duration to 6 seconds.");
         Locale.setString("TOWER_TOTEM_SPIRITS_DESCRIPTION_3","en","Increases Totem duration to 8 seconds.");
         Locale.setString("TOWER_CROSSBOW_NAME","en","Crossbow Fort");
         Locale.setString("TOWER_CROSSBOW_DESCRIPTION","en","Trained under monastic discipline, these crossbow furies are masters of their craft.");
         Locale.setString("TOWER_CROSSBOW_SPECIAL","en","Falconer, Barrage");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_NAME","en","Barrage");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_DESCRIPTION","en","Shoots up to 6 bolts in quick succession that deal 30 to 40 damage each.");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_NOTE","en","Be quick or be dead!");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_NAME_1","en","Barrage");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_NAME_2","en","Barrage II");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_NAME_3","en","Barrage III");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_DESCRIPTION_1","en","Shoots up to 6 bolts in quick succession that deal 30 to 40 damage each.");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_DESCRIPTION_2","en","Barrage shoots 2 extra bolts for a total of 8.");
         Locale.setString("TOWER_CROSSBOW_BARRAGE_DESCRIPTION_3","en","Barrage shoots 2 extra bolts for a total of 10.");
         Locale.setString("TOWER_CROSSBOW_FALCONER_NAME","en","Falconer");
         Locale.setString("TOWER_CROSSBOW_FALCONER_DESCRIPTION","en","Improves attack range of nearby towers by 10% and grants 5% critical chance to this tower.");
         Locale.setString("TOWER_CROSSBOW_FALCONER_NOTE","en","Aim through falcon eyes!");
         Locale.setString("TOWER_CROSSBOW_FALCONER_NAME_1","en","Falconer");
         Locale.setString("TOWER_CROSSBOW_FALCONER_NAME_2","en","Falconer II");
         Locale.setString("TOWER_CROSSBOW_FALCONER_NAME_3","en","Falconer III");
         Locale.setString("TOWER_CROSSBOW_FALCONER_DESCRIPTION_1","en","Improves attack range of nearby towers by 10% and grants 5% critical chance to this tower.");
         Locale.setString("TOWER_CROSSBOW_FALCONER_DESCRIPTION_2","en","Falconer bonus reaches more towers, improving its bonus to range to 15% and critical to 10%.");
         Locale.setString("TOWER_CROSSBOW_FALCONER_DESCRIPTION_3","en","Falconer bonus reaches more towers, improving its bonus to range to 20% and critical to 15%.");
         Locale.setString("TOWER_NECROMANCER_NAME","en","Necromancer Tower");
         Locale.setString("TOWER_NECROMANCER_DESCRIPTION","en","Dark magic adepts that can raise undead minions from the corpses of fallen enemies.");
         Locale.setString("TOWER_NECROMANCER_SMALL_DESCRIPTION","en","Dark magic adepts that can raise undead minions from the corpses of fallen enemies.");
         Locale.setString("TOWER_NECROMANCER_SPECIAL","en","Pestilence, Summon Death Rider");
         Locale.setString("TOWER_NECROMANCER_EXTRA","en","Fast shooting, it can raise undead minions from the corpses of fallen foes.");
         Locale.setString("TOWER_NECROMANCER_RIDER_NAME","en","Summon Death Rider");
         Locale.setString("TOWER_NECROMANCER_RIDER_DESCRIPTION","en","Summons a Death Rider, a fearsome creature with an aura that bolsters nearby skeletons.");
         Locale.setString("TOWER_NECROMANCER_RIDER_NOTE","en","Honor in death as in life!");
         Locale.setString("TOWER_NECROMANCER_RIDER_NAME_1","en","Summon Death Rider");
         Locale.setString("TOWER_NECROMANCER_RIDER_NAME_2","en","Summon Death Rider II");
         Locale.setString("TOWER_NECROMANCER_RIDER_NAME_3","en","Summon Death Rider III");
         Locale.setString("TOWER_NECROMANCER_RIDER_DESCRIPTION_1","en","Summons a Death Rider, a fearsome creature with an aura that bolsters nearby skeletons.");
         Locale.setString("TOWER_NECROMANCER_RIDER_DESCRIPTION_2","en","The death rider gains increased life, armor and attack damage.");
         Locale.setString("TOWER_NECROMANCER_RIDER_DESCRIPTION_3","en","The death rider gains increased life, armor and attack damage.");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_NAME","en","Pestilence");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_DESCRIPTION","en","Summons a cloud of pestilence for 4 seconds, poisoning enemies for 20 damage each second.");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_NOTE","en","It’s not decay, It’s ripening.");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_NAME_1","en","Pestilence");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_NAME_2","en","Pestilence II");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_NAME_3","en","Pestilence III");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_DESCRIPTION_1","en","Summons a cloud of pestilence for 4 seconds poisoning enemies for 20 damage each second.");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_DESCRIPTION_2","en","Increases Pestilence area of effect and duration to 5 seconds.");
         Locale.setString("TOWER_NECROMANCER_PESTILENCE_DESCRIPTION_3","en","Increases Pestilence area of effect and duration to 6 seconds.");
         Locale.setString("TOWER_ARCHMAGE_NAME","en","Archmage Tower");
         Locale.setString("TOWER_ARCHMAGE_DESCRIPTION","en","Wizards specialized in warfare that can charge its homing magical bolts of deadly magic.");
         Locale.setString("TOWER_ARCHMAGE_SPECIAL","en","Critical Mass, Twister");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_NAME","en","Twister");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_DESCRIPTION","en","Summons a tornado that pushes up to 5 enemies back in the path dealing 40 damage to each.");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_NOTE","en","Is there an F5?");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_NAME_1","en","Twister");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_NAME_2","en","Twister II");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_NAME_3","en","Twister III");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_DESCRIPTION_1","en","Summons a tornado that pushes up to 5 enemies back in the path dealing 40 damage to each.");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_DESCRIPTION_2","en","Increases Twister maximum enemies to 6 and damage to 60.");
         Locale.setString("TOWER_ARCHMAGE_TWISTER_DESCRIPTION_3","en","Increases Twister maximum enemies to 7 and damage to 80.");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_NAME","en","Critical Mass");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_DESCRIPTION","en","Archmage bolts have a 35% chance of exploding, dealing an additional 30 area magic damage.");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_NOTE","en","Energy is never lost...");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_NAME_1","en","Critical Mass");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_NAME_2","en","Critical Mass II");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_NAME_3","en","Critical Mass III");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_DESCRIPTION_1","en","Archmage bolts have a 35% chance of exploding dealing an additional 30 area magic damage.");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_DESCRIPTION_2","en","Explosion magic damage is increased to 60.");
         Locale.setString("TOWER_ARCHMAGE_CRITICAL_DESCRIPTION_3","en","Explosion magic damage is increased to 90.");
         Locale.setString("TOWER_MECH_SOLDIER_NAME","en","Battle-Mecha T200");
         Locale.setString("TOWER_MECH_NAME","en","Battle-Mecha T200");
         Locale.setString("TOWER_MECH_DESCRIPTION","en","A controllable towering unstoppable mobile artillery mecha! Also known as the “Big boy”");
         Locale.setString("TOWER_MECH_SPECIAL","en","Waste Disposal, Wasp Missiles");
         Locale.setString("TOWER_MECH_WASTE_NAME_1","en","Waste Disposal");
         Locale.setString("TOWER_MECH_WASTE_NAME_2","en","Waste Disposal II");
         Locale.setString("TOWER_MECH_WASTE_NAME_3","en","Waste Disposal III");
         Locale.setString("TOWER_MECH_WASTE_DESCRIPTION_1","en","Drops oil that greatly slows ground enemies for %d seconds.");
         Locale.setString("TOWER_MECH_WASTE_DESCRIPTION_2","en","Increases Oil duration to %d seconds.");
         Locale.setString("TOWER_MECH_WASTE_DESCRIPTION_3","en","Increases Oil duration to %d seconds.");
         Locale.setString("TOWER_MECH_WASTE_NOTE","en","Down the garbage chute!");
         Locale.setString("TOWER_MECH_MISSILE_NAME","en","Wasp Missiles");
         Locale.setString("TOWER_MECH_MISSILE_DESCRIPTION","en","Fires a volley of 2 seeking missiles that never miss dealing 20 to 80 damage each.");
         Locale.setString("TOWER_MECH_MISSILE_NOTE","en","Tag \'em and frag \'em!");
         Locale.setString("TOWER_MECH_MISSILE_NAME_1","en","Wasp Missiles");
         Locale.setString("TOWER_MECH_MISSILE_NAME_2","en","Wasp Missiles II");
         Locale.setString("TOWER_MECH_MISSILE_DESCRIPTION_1","en","Fires a volley of 2 seeking missiles that never miss dealing 20 to 80 damage each.");
         Locale.setString("TOWER_MECH_MISSILE_DESCRIPTION_2","en","Fires double the missiles on each volley.");
         Locale.setString("TOWER_MECH_MISSILE_NOTE_1","en","Tag \'em and frag \'em!");
         Locale.setString("TOWER_DWAARP_NAME","en","DWAARP");
         Locale.setString("TOWER_DWAARP_DESCRIPTION","en","The pinnacle of dwarven mining, its quakes damage and slow all enemies around it.");
         Locale.setString("TOWER_DWAARP_SPECIAL","en","Furnace Blast, Core Drill");
         Locale.setString("TOWER_DWAARP_BLAST_NAME","en","Furnace Blast");
         Locale.setString("TOWER_DWAARP_BLAST_DESCRIPTION","en","Burns all enemies in close range for 80 damage over 4 seconds.");
         Locale.setString("TOWER_DWAARP_BLAST_NOTE","en","Give me fuel, give me fire...");
         Locale.setString("TOWER_DWAARP_BLAST_NAME_1","en","Furnace Blast");
         Locale.setString("TOWER_DWAARP_BLAST_NAME_2","en","Furnace Blast II");
         Locale.setString("TOWER_DWAARP_BLAST_NAME_3","en","Furnace Blast III");
         Locale.setString("TOWER_DWAARP_BLAST_DESCRIPTION_1","en","Burns all enemies in close range for 80 damage over 4 seconds.");
         Locale.setString("TOWER_DWAARP_BLAST_DESCRIPTION_2","en","Increases burn damage to 140 over 4 seconds.");
         Locale.setString("TOWER_DWAARP_BLAST_DESCRIPTION_3","en","Increases burn damage to 200 over 4 seconds.");
         Locale.setString("TOWER_DWAARP_BLAST_NOTE_1","en","Give me fuel, give me fire...");
         Locale.setString("TOWER_DWAARP_DRILL_NOTE","en","They *can’t* see what hit em!");
         Locale.setString("TOWER_DWAARP_DRILL_NAME_1","en","Core Drill");
         Locale.setString("TOWER_DWAARP_DRILL_NAME_2","en","Core Drill II");
         Locale.setString("TOWER_DWAARP_DRILL_NAME_3","en","Core Drill III");
         Locale.setString("TOWER_DWAARP_DRILL_DESCRIPTION_1","en","Sends an automated mining drill towards an enemy, reducing it to a mound of gibs!");
         Locale.setString("TOWER_DWAARP_DRILL_DESCRIPTION_2","en","Core Drill cooldown is reduced to %d seconds.");
         Locale.setString("TOWER_DWAARP_DRILL_DESCRIPTION_3","en","Core Drill cooldown is reduced to %d seconds.");
         Locale.setString("POWER_FIREBALL_NAME","en","Rain of Fire");
         Locale.setString("POWER_FIREBALL_DESCRIPTION","en","Rains fire and brimstone from the skies.");
         Locale.setString("POWER_REINFORCEMENTS_NAME","en","Call Reinforcements");
         Locale.setString("POWER_REINFORCEMENTS_DESCRIPTION","en","Summon reinforcements to block and fight enemies.");
         Locale.setString("POWER_PRIEST_NAME","en","Priest");
         Locale.setString("POWER_PRIEST_DESCRIPTION","en","Priest description.");
         Locale.setString("POWER_BATTLE_CRY_NAME","en","Battle Cry");
         Locale.setString("POWER_BATTLE_CRY_DESCRIPTION","en","Battle Cry description.");
         Locale.setString("POWER_LIGHTNING_NAME","en","Lightning Bolt");
         Locale.setString("POWER_LIGHTNING_DESCRIPTION","en","Casts a bolt of lightning at one enemy.");
         Locale.setString("SOLDIER_STANDARD_1_NAME","en","Soldier");
         Locale.setString("SOLDIER_STANDARD_2_NAME","en","Soldier");
         Locale.setString("SOLDIER_STANDARD_3_NAME","en","Soldier");
         Locale.setString("SOLDIER_PALADIN_NAME","en","Paladin");
         Locale.setString("SOLDIER_BARBARIAN_NAME","en","Barbarian");
         Locale.setString("SOLDIER_ELEMENTAL_NAME","en","Elemental");
         Locale.setString("SOLDIER_FARMER_PAUL_NAME","en","Farmer");
         Locale.setString("SOLDIER_FARMER_JOHN_NAME","en","Farmer");
         Locale.setString("SOLDIER_FARMER_RINGO_NAME","en","Farmer");
         Locale.setString("SOLDIER_MILITIA_NAME","en","Militia");
         Locale.setString("SOLDIER_WARRIOR_NAME","en","Warrior");
         Locale.setString("SOLDIER_KNIGHT_NAME","en","Knight");
         Locale.setString("SOLDIER_SASQUASH_NAME","en","Sasquatch");
         Locale.setString("SOLDIER_RANDOM_1_NAME","en","Danger Douglas");
         Locale.setString("SOLDIER_RANDOM_2_NAME","en","Dan McKill");
         Locale.setString("SOLDIER_RANDOM_3_NAME","en","James Lee");
         Locale.setString("SOLDIER_RANDOM_4_NAME","en","Jar Johson");
         Locale.setString("SOLDIER_RANDOM_5_NAME","en","Bomb-Squad Phil");
         Locale.setString("SOLDIER_RANDOM_6_NAME","en","Robin");
         Locale.setString("SOLDIER_RANDOM_7_NAME","en","William");
         Locale.setString("SOLDIER_RANDOM_8_NAME","en","Martin");
         Locale.setString("SOLDIER_RANDOM_9_NAME","en","Arthur");
         Locale.setString("SOLDIER_RANDOM_10_NAME","en","Alvus");
         Locale.setString("SOLDIER_RANDOM_11_NAME","en","Borin");
         Locale.setString("SOLDIER_RANDOM_12_NAME","en","Hadrian");
         Locale.setString("SOLDIER_RANDOM_13_NAME","en","Thomas");
         Locale.setString("SOLDIER_RANDOM_14_NAME","en","Henry");
         Locale.setString("SOLDIER_RANDOM_15_NAME","en","Bryce");
         Locale.setString("SOLDIER_RANDOM_16_NAME","en","Rulf");
         Locale.setString("SOLDIER_RANDOM_17_NAME","en","Allister");
         Locale.setString("SOLDIER_RANDOM_18_NAME","en","Altair");
         Locale.setString("SOLDIER_RANDOM_19_NAME","en","Simon");
         Locale.setString("SOLDIER_RANDOM_20_NAME","en","Egbert");
         Locale.setString("SOLDIER_RANDOM_21_NAME","en","Eldon");
         Locale.setString("SOLDIER_RANDOM_22_NAME","en","Garrett");
         Locale.setString("SOLDIER_RANDOM_23_NAME","en","Godwin");
         Locale.setString("SOLDIER_RANDOM_24_NAME","en","Gordon");
         Locale.setString("SOLDIER_RANDOM_25_NAME","en","Jerald");
         Locale.setString("SOLDIER_RANDOM_26_NAME","en","Kelvin");
         Locale.setString("SOLDIER_RANDOM_27_NAME","en","Lando");
         Locale.setString("SOLDIER_RANDOM_28_NAME","en","Maddox");
         Locale.setString("SOLDIER_RANDOM_29_NAME","en","Peyton");
         Locale.setString("SOLDIER_RANDOM_30_NAME","en","Ramsey");
         Locale.setString("SOLDIER_RANDOM_31_NAME","en","Raymond");
         Locale.setString("SOLDIER_RANDOM_32_NAME","en","Robert");
         Locale.setString("SOLDIER_RANDOM_33_NAME","en","Sawyer");
         Locale.setString("SOLDIER_RANDOM_34_NAME","en","Silas");
         Locale.setString("SOLDIER_RANDOM_35_NAME","en","Stuart");
         Locale.setString("SOLDIER_RANDOM_36_NAME","en","Tanner");
         Locale.setString("SOLDIER_RANDOM_37_NAME","en","Usher");
         Locale.setString("SOLDIER_RANDOM_38_NAME","en","Wallace");
         Locale.setString("SOLDIER_RANDOM_39_NAME","en","Wesley");
         Locale.setString("SOLDIER_RANDOM_40_NAME","en","Willard");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_1_NAME","en","Altair");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_2_NAME","en","Ezio");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_3_NAME","en","Lucien");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_4_NAME","en","Brutus");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_5_NAME","en","Desmond");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_6_NAME","en","Havelock");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_7_NAME","en","Sayid");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_8_NAME","en","Artemis");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_9_NAME","en","47");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_10_NAME","en","Gibson");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_11_NAME","en","Leon");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_12_NAME","en","Rath");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_13_NAME","en","Bain");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_14_NAME","en","Vito");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_15_NAME","en","Carcer");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_16_NAME","en","Kimubi");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_17_NAME","en","Athos");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_18_NAME","en","Artemis");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_19_NAME","en","Lucien");
         Locale.setString("SOLDIER_ASSASSIN_RANDOM_20_NAME","en","Zamzar");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_1_NAME","en","Kormac");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_2_NAME","en","Hugues");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_3_NAME","en","Godfrey");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_4_NAME","en","Reynald");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_5_NAME","en","Armand");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_6_NAME","en","Jaques");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_7_NAME","en","Guillaume");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_8_NAME","en","Thibaud");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_9_NAME","en","Geoffrey");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_10_NAME","en","Bertrand");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_11_NAME","en","William");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_12_NAME","en","Bonabes");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_13_NAME","en","De Brus");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_14_NAME","en","Robert");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_15_NAME","en","Gobert");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_16_NAME","en","Kormac");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_17_NAME","en","Guillaume");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_18_NAME","en","Jaques");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_19_NAME","en","Geoffrey");
         Locale.setString("SOLDIER_TEMPLAR_RANDOM_20_NAME","en","William");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_1_NAME","en","Jean Claude");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_2_NAME","en","Lawrence");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_3_NAME","en","Pierre Le Noir");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_4_NAME","en","Alain");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_5_NAME","en","Chevalier");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_6_NAME","en","Jaques");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_7_NAME","en","Rene");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_8_NAME","en","Andreani");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_9_NAME","en","Armand");
         Locale.setString("SOLDIER_LEGIONNAIRE_RANDOM_10_NAME","en","Philippe");
         Locale.setString("SOLDIER_DJINN_RANDOM_1_NAME","en","Jeliel");
         Locale.setString("SOLDIER_DJINN_RANDOM_2_NAME","en","Nith-Haiah");
         Locale.setString("SOLDIER_DJINN_RANDOM_3_NAME","en","Achaiah");
         Locale.setString("SOLDIER_DJINN_RANDOM_4_NAME","en","Haziel");
         Locale.setString("SOLDIER_DJINN_RANDOM_5_NAME","en","Yerathel");
         Locale.setString("SOLDIER_DJINN_RANDOM_6_NAME","en","Iah-Hel");
         Locale.setString("SOLDIER_DJINN_RANDOM_7_NAME","en","Damabiah");
         Locale.setString("SOLDIER_DJINN_RANDOM_8_NAME","en","Sayatin");
         Locale.setString("SOLDIER_DJINN_RANDOM_9_NAME","en","Khuddam");
         Locale.setString("SOLDIER_DJINN_RANDOM_10_NAME","en","Qorrash");
         Locale.setString("SOLDIER_PIRATES_RANDOM_1_NAME","en","Barbarossa");
         Locale.setString("SOLDIER_PIRATES_RANDOM_2_NAME","en","Blackbeard ");
         Locale.setString("SOLDIER_PIRATES_RANDOM_3_NAME","en","Sparrow");
         Locale.setString("SOLDIER_PIRATES_RANDOM_4_NAME","en","Calico Jack");
         Locale.setString("SOLDIER_PIRATES_RANDOM_5_NAME","en","Morgan");
         Locale.setString("SOLDIER_PIRATES_RANDOM_6_NAME","en","LeChuck");
         Locale.setString("SOLDIER_PIRATES_RANDOM_7_NAME","en","Guybrush");
         Locale.setString("SOLDIER_PIRATES_RANDOM_8_NAME","en","Will Turner");
         Locale.setString("SOLDIER_PIRATES_RANDOM_9_NAME","en","Davy Jones");
         Locale.setString("SOLDIER_PIRATES_RANDOM_10_NAME","en","Black Bart");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_1_NAME","en","Jane");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_2_NAME","en","Sulin");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_3_NAME","en","Balsa");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_4_NAME","en","Chiad");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_5_NAME","en","Enaila");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_6_NAME","en","Shaiel");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_7_NAME","en","Dareis");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_8_NAME","en","Sovin");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_9_NAME","en","Seia");
         Locale.setString("SOLDIER_AMAZONAS_RANDOM_10_NAME","en","Hama");
         Locale.setString("SOLDIER_DWARF_RANDOM_1_NAME","en","Oin");
         Locale.setString("SOLDIER_DWARF_RANDOM_2_NAME","en","Gloin");
         Locale.setString("SOLDIER_DWARF_RANDOM_3_NAME","en","Thorin");
         Locale.setString("SOLDIER_DWARF_RANDOM_4_NAME","en","Gimli");
         Locale.setString("SOLDIER_DWARF_RANDOM_5_NAME","en","Durin");
         Locale.setString("SOLDIER_DWARF_RANDOM_6_NAME","en","Dwalin");
         Locale.setString("SOLDIER_DWARF_RANDOM_7_NAME","en","Balin");
         Locale.setString("SOLDIER_DWARF_RANDOM_8_NAME","en","Bifur");
         Locale.setString("SOLDIER_DWARF_RANDOM_9_NAME","en","Bofur");
         Locale.setString("SOLDIER_DWARF_RANDOM_10_NAME","en","Bombur");
         Locale.setString("SOLDIER_DEATH_KNIGHT_NAME","en","Death Knight");
         Locale.setString("SOLDIER_SKELETON_NORMAL_NAME","en","Skeleton");
         Locale.setString("SOLDIER_SKELETON_KNIGHT_NAME","en","Skeleton Knight");
         Locale.setString("ENEMY_BOUNCER_NAME","en","Desert Thug");
         Locale.setString("ENEMY_BOUNCER_DESCRIPTION","en","These thugs are lowly mercenaries that enjoy pillaging.");
         Locale.setString("ENEMY_BOUNCER_SPECIAL","en","");
         Locale.setString("ENEMY_BOUNCER_EXTRA","en","- AVERAGE SPEED\n- LOW DAMAGE");
         Locale.setString("ENEMY_DESERT_RAIDER_NAME","en","Dune Raider");
         Locale.setString("ENEMY_DESERT_RAIDER_DESCRIPTION","en","Seasoned sellswords from the nomad tribes.");
         Locale.setString("ENEMY_DESERT_RAIDER_SPECIAL","en","");
         Locale.setString("ENEMY_DESERT_RAIDER_EXTRA","en","- LOW ARMOR\n- HIGH DAMAGE\n- AVERAGE SPEED");
         Locale.setString("ENEMY_DESERT_ARCHER_NAME","en","Desert Archer");
         Locale.setString("ENEMY_DESERT_ARCHER_DESCRIPTION","en","Deadly accurate archers from the desert, they will attack nearby soldiers.");
         Locale.setString("ENEMY_DESERT_ARCHER_SPECIAL","en","*Ranged attack");
         Locale.setString("ENEMY_DESERT_ARCHER_EXTRA","en","- RANGED ATTACK\n- LOW MAGIC RESISTANCE\n- AVERAGE SPEED");
         Locale.setString("ENEMY_IMMORTAL_NAME","en","Immortal");
         Locale.setString("ENEMY_IMMORTAL_DESCRIPTION","en","Relentless elite warriors with a reputation for invincibility.");
         Locale.setString("ENEMY_IMMORTAL_SPECIAL","en","*Returns as a Fallen");
         Locale.setString("ENEMY_IMMORTAL_EXTRA","en","- ARMORED\n- HIGH DAMAGE\n- RETURN AS FALLEN");
         Locale.setString("ENEMY_FALLEN_NAME","en","Fallen");
         Locale.setString("ENEMY_FALLEN_DESCRIPTION","en","Reanimated corpses of once great warriors.");
         Locale.setString("ENEMY_FALLEN_SPECIAL","en","");
         Locale.setString("ENEMY_FALLEN_EXTRA","en","- HIGH DAMAGE");
         Locale.setString("ENEMY_DESERT_WOLF_SMALL_NAME","en","Sand Hound");
         Locale.setString("ENEMY_DESERT_WOLF_SMALL_DESCRIPTION","en","Very fast and vicious creatures that can dodge melee attacks.");
         Locale.setString("ENEMY_DESERT_WOLF_SMALL_SPECIAL","en","*Can dodge melee attacks");
         Locale.setString("ENEMY_DESERT_WOLF_SMALL_EXTRA","en","- VERY FAST\n- CAN DODGE MELEE ATTACKS");
         Locale.setString("ENEMY_DESERT_WOLF_NAME","en","War Hound");
         Locale.setString("ENEMY_DESERT_WOLF_DESCRIPTION","en","Cunning, fast beasts that can dodge melee attacks and resist magic attacks.");
         Locale.setString("ENEMY_DESERT_WOLF_SPECIAL","en","*Can dodge melee attacks");
         Locale.setString("ENEMY_DESERT_WOLF_EXTRA","en","- VERY FAST\n- CAN DODGE MELEE ATTACKS\n- MAGIC RESISTANCE");
         Locale.setString("ENEMY_WASP_QUEEN_NAME","en","Giant Wasp Queen");
         Locale.setString("ENEMY_WASP_QUEEN_DESCRIPTION","en","Utterly tough flying insects that carry several offspring in their bellies.");
         Locale.setString("ENEMY_WASP_QUEEN_SPECIAL","en","*Spawns Giant Wasps, Flying");
         Locale.setString("ENEMY_WASP_QUEEN_EXTRA","en","- SLOW SPEED\n- FLYING\n- SPAWNS GIANT WASPS");
         Locale.setString("ENEMY_WASP_NAME","en","Giant Wasp");
         Locale.setString("ENEMY_WASP_DESCRIPTION","en","These fearful creatures are often trained to serve as aerial hunters.");
         Locale.setString("ENEMY_WASP_SPECIAL","en","*Flying");
         Locale.setString("ENEMY_WASP_EXTRA","en","- AVERAGE SPEED\n- FLYING");
         Locale.setString("ENEMY_TREMOR_NAME","en","Dune Terror");
         Locale.setString("ENEMY_TREMOR_DESCRIPTION","en","Ravenous carnivores moving through the sands, always on the prowl, like sharks at sea.");
         Locale.setString("ENEMY_TREMOR_SPECIAL","en","*Burrows");
         Locale.setString("ENEMY_TREMOR_EXTRA","en","- FAST SPEED\n- INVULNERABLE WHILE\n BURROWED");
         Locale.setString("ENEMY_SCORPION_NAME","en","Giant Scorpion");
         Locale.setString("ENEMY_SCORPION_DESCRIPTION","en","Vicious, poisonous, predatory beasts, protected by a thick carapace.");
         Locale.setString("ENEMY_SCORPION_SPECIAL","en","*Poisonous Attack");
         Locale.setString("ENEMY_SCORPION_EXTRA","en","- HEAVY ARMOR\n- POISONOUS ATTACK");
         Locale.setString("ENEMY_EXECUTIONER_NAME","en","Executioner");
         Locale.setString("ENEMY_EXECUTIONER_DESCRIPTION","en","An unstoppable killing force, a strike from its axe delivers a swift death.");
         Locale.setString("ENEMY_EXECUTIONER_SPECIAL","en","*Instakills soldiers");
         Locale.setString("ENEMY_EXECUTIONER_EXTRA","en","- SLOW SPEED\n- VERY HIGH HEALTH\n- CAN EXECUTE SOLDIERS");
         Locale.setString("ENEMY_MUNRA_NAME","en","Sand Wraith");
         Locale.setString("ENEMY_MUNRA_DESCRIPTION","en","Often in command of dark armies, they leave a path of death and decay in their wake.");
         Locale.setString("ENEMY_MUNRA_SPECIAL","en","*Ranged attack, Spawns Fallen");
         Locale.setString("ENEMY_MUNRA_EXTRA","en","- RANGED ATTACK\n- CAN HEAL ALLIES\n- SPAWNS FALLEN");
         Locale.setString("ENEMY_EFREETI_SMALL_NAME","en","Lesser Efreeti");
         Locale.setString("ENEMY_EFREETI_SMALL_DESCRIPTION","en","These lesser efreets do not grant any wishes, but you will wish them gone.");
         Locale.setString("ENEMY_EFREETI_SMALL_SPECIAL","en","");
         Locale.setString("ENEMY_EFREETI_BOSS_NAME","en","Nazeru");
         Locale.setString("ENEMY_EFREETI_BOSS_DESCRIPTION","en","Be careful what you wish for, the red efreets are not the genies you dream of...");
         Locale.setString("ENEMY_EFREETI_BOSS_SPECIAL","en","*Boss");
         Locale.setString("ENEMY_JUNGLE_SPIDER_SMALL_NAME","en","Jungle Spider");
         Locale.setString("ENEMY_JUNGLE_SPIDER_SMALL_DESCRIPTION","en","The jungle variant of this vicious predator is a lot meaner than its forest cousin.");
         Locale.setString("ENEMY_JUNGLE_SPIDER_SMALL_SPECIAL","en","");
         Locale.setString("ENEMY_JUNGLE_SPIDER_SMALL_EXTRA","en","- FAST\n- MAGIC RESISTANCE");
         Locale.setString("ENEMY_JUNGLE_SPIDER_BIG_NAME","en","Jungle Matriarch ");
         Locale.setString("ENEMY_JUNGLE_SPIDER_BIG_DESCRIPTION","en","This aggressive predator hunts using its offspring to overwhelm its victims.");
         Locale.setString("ENEMY_JUNGLE_SPIDER_BIG_SPECIAL","en","*Spawns spiderlings");
         Locale.setString("ENEMY_JUNGLE_SPIDER_BIG_EXTRA","en","- HIGH DAMAGE\n- MAGIC RESISTANCE\n- SPAWNS SPIDERLINGS");
         Locale.setString("ENEMY_JUNGLE_SPIDER_TINY_NAME","en","Spiderling");
         Locale.setString("ENEMY_JUNGLE_SPIDER_TINY_DESCRIPTION","en","No so tiny!");
         Locale.setString("ENEMY_JUNGLE_SPIDER_TINY_SPECIAL","en","");
         Locale.setString("ENEMY_CANIBAL_VOLCANO_NAME","en","Savage Brute");
         Locale.setString("ENEMY_CANIBAL_NAME","en","Savage Warrior");
         Locale.setString("ENEMY_CANIBAL_DESCRIPTION","en","A fearless tribal warrior with the scars to prove his rite of passage.");
         Locale.setString("ENEMY_CANIBAL_SPECIAL","en","*Cannibalizes victims");
         Locale.setString("ENEMY_CANIBAL_EXTRA","en","- AVERAGE SPEED\n- CANNIBALIZES VICTIMS");
         Locale.setString("ENEMY_CANIBAL_PRIEST_NAME","en","Witch Doctor");
         Locale.setString("ENEMY_CANIBAL_PRIEST_DESCRIPTION","en","Aboriginal healers that use a secret mojo to heal their tribal brothers.");
         Locale.setString("ENEMY_CANIBAL_PRIEST_SPECIAL","en","*Aura (Healing)");
         Locale.setString("ENEMY_CANIBAL_PRIEST_EXTRA","en","- AVERAGE SPEED\n- HEALING AURA");
         Locale.setString("ENEMY_CANIBAL_MAGIC_NAME","en","Spirit Shaman");
         Locale.setString("ENEMY_CANIBAL_MAGIC_DESCRIPTION","en","Congressing with spirits, they protect their brethren from magic attacks.");
         Locale.setString("ENEMY_CANIBAL_MAGIC_SPECIAL","en","*Aura (High magic resistance)");
         Locale.setString("ENEMY_CANIBAL_MAGIC_EXTRA","en","- AVERAGE SPEED\n- MAGIC RESISTANCE AURA");
         Locale.setString("ENEMY_CANIBAL_SHIELD_NAME","en","Earth Shaman ");
         Locale.setString("ENEMY_CANIBAL_SHIELD_DESCRIPTION","en","These wise men manipulate the powers of the earth to protect their allies against damage. ");
         Locale.setString("ENEMY_CANIBAL_SHIELD_SPECIAL","en","*Aura (Heavy armor)");
         Locale.setString("ENEMY_CANIBAL_SHIELD_EXTRA","en","- AVERAGE SPEED\n- HEAVY ARMOR AURA");
         Locale.setString("ENEMY_GORILLA_NAME","en","Gorillon");
         Locale.setString("ENEMY_GORILLA_DESCRIPTION","en","Large angry apes trained for battle. A force to be reckoned in the battlefield.");
         Locale.setString("ENEMY_GORILLA_SPECIAL","en","*Area attack");
         Locale.setString("ENEMY_GORILLA_EXTRA","en","- SLOW SPEED\n- VERY TOUGH\n- AREA ATTACK");
         Locale.setString("ENEMY_CANIBAL_BIRD_NAME","en","Poukai");
         Locale.setString("ENEMY_CANIBAL_BIRD_DESCRIPTION","en","Giant flying predators, they are sometimes tamed by the savages to be used as mounts.");
         Locale.setString("ENEMY_CANIBAL_BIRD_SPECIAL","en","*Flying");
         Locale.setString("ENEMY_CANIBAL_BIRD_EXTRA","en","- FLYING");
         Locale.setString("ENEMY_CANIBAL_SAVAGE_HUNTER_NAME","en","Savage Hunter");
         Locale.setString("ENEMY_CANIBAL_SAVAGE_HUNTER_DESCRIPTION","en","The Savage hunters are quick agile warriors that shoot deadly poisonous darts.");
         Locale.setString("ENEMY_CANIBAL_SAVAGE_HUNTER_SPECIAL","en","*Ranged poisonous attack");
         Locale.setString("ENEMY_CANIBAL_SAVAGE_HUNTER_EXTRA","en","- FAST SPEED\n- RANGED POISON ATTACK");
         Locale.setString("ENEMY_CANIBAL_WING_RIDER_NAME","en","Poukai Rider");
         Locale.setString("ENEMY_CANIBAL_WING_RIDER_DESCRIPTION","en","Poukai riders soar the jungle skies, hunting any trespassers they may find.");
         Locale.setString("ENEMY_CANIBAL_WING_RIDER_SPECIAL","en","*Flying, Ranged Attack, Releases mount");
         Locale.setString("ENEMY_CANIBAL_WING_RIDER_EXTRA","en","- FLYING\n- RANGED ATTACK\n- RELEASES POUKAI ON DEATH");
         Locale.setString("ENEMY_ALIEN_REAPER_NAME","en","Reaper");
         Locale.setString("ENEMY_ALIEN_REAPER_DESCRIPTION","en","A terror of unknown origin. Hunters from a faraway tribe voyage to try and hunt one.");
         Locale.setString("ENEMY_ALIEN_REAPER_SPECIAL","en","");
         Locale.setString("ENEMY_ALIEN_REAPER_EXTRA","en","- FAST SPEED\n- HIGH MAGIC RESISTANCE\n- VERY HIGH DAMAGE");
         Locale.setString("ENEMY_ALIEN_BREEDER_NAME","en","Parasyte");
         Locale.setString("ENEMY_ALIEN_BREEDER_DESCRIPTION","en","These critters lay eggs inside their victims, which later spawn horrible monsters.");
         Locale.setString("ENEMY_ALIEN_BREEDER_SPECIAL","en","*Spawns Reapers");
         Locale.setString("ENEMY_ALIEN_BREEDER_EXTRA","en","- VERY FAST SPEED\n- HIGH MAGIC RESISTANCE\n- SPAWNS A REAPER");
         Locale.setString("ENEMY_CANIBAL_NECROMANCER_NAME","en","Blood Trickster");
         Locale.setString("ENEMY_CANIBAL_NECROMANCER_DESCRIPTION","en","These deceivers deal in black magic, reanimating fallen tribesmen.");
         Locale.setString("ENEMY_CANIBAL_NECROMANCER_SPECIAL","en","*Ranged attack, Raises fallen savages");
         Locale.setString("ENEMY_CANIBAL_NECROMANCER_EXTRA","en","- AVERAGE SPEED\n- RANGED ATTACK\n- CAN RAISE FALLEN SAVAGES");
         Locale.setString("ENEMY_CANIBAL_ZOMBIE_NAME","en","Savage Zombie");
         Locale.setString("ENEMY_CANIBAL_ZOMBIE_DESCRIPTION","en","Reanimated fallen savages, they crave only brains... and plants.");
         Locale.setString("ENEMY_CANIBAL_ZOMBIE_SPECIAL","en","");
         Locale.setString("ENEMY_CANIBAL_ZOMBIE_EXTRA","en","- SLOW SPEED");
         Locale.setString("ENEMY_CANIBAL_BOSS_NAME","en","Quincon");
         Locale.setString("ENEMY_CANIBAL_BOSS_DESCRIPTION","en","Fury and strength wrapped in hair and muscle, this giant ape is the stuff of legends.");
         Locale.setString("ENEMY_CANIBAL_BOSS_SPECIAL","en","*Boss");
         Locale.setString("ENEMY_CANIBAL_BOSS_EXTRA","en","");
         Locale.setString("ENEMY_CANIBAL_BOSS_MINION_NAME","en","Mandrilos");
         Locale.setString("ENEMY_CANIBAL_BOSS_MINION_DESCRIPTION","en","Evolved to kick your behind, the Mandrilos will beat the bananas out of you.");
         Locale.setString("ENEMY_CANIBAL_BOSS_MINION_SPECIAL","en","");
         Locale.setString("ENEMY_CANIBAL_BOSS_MINION_EXTRA","en","");
         Locale.setString("ENEMY_SAURIAN_BROODGUARD_NAME","en","Saurian Broodguard");
         Locale.setString("ENEMY_SAURIAN_BROODGUARD_DESCRIPTION","en","Fearless lizard-like warriors, their wounds fuel their combat rage, making them faster.");
         Locale.setString("ENEMY_SAURIAN_BROODGUARD_SPECIAL","en","");
         Locale.setString("ENEMY_SAURIAN_BROODGUARD_EXTRA","en","- WALKS FASTER AS IT GETS INJURED");
         Locale.setString("ENEMY_SAURIAN_MYRMIDON_NAME","en","Saurian Myrmidon ");
         Locale.setString("ENEMY_SAURIAN_MYRMIDON_DESCRIPTION","en","Ferocious elite warriors that fight with sword and fang alike!");
         Locale.setString("ENEMY_SAURIAN_MYRMIDON_SPECIAL","en","*Vampiric bite");
         Locale.setString("ENEMY_SAURIAN_MYRMIDON_EXTRA","en","- HEAVY ARMOR\n- AVERAGE SPEED\n- CAN BITE TO REGAIN HEALTH");
         Locale.setString("ENEMY_SAURIAN_NIGHTSCALE_NAME","en","Saurian Nightscale");
         Locale.setString("ENEMY_SAURIAN_NIGHTSCALE_DESCRIPTION","en","Cunning warriors that can become invisible to get past defenses.");
         Locale.setString("ENEMY_SAURIAN_NIGHTSCALE_SPECIAL","en","*Invisibility");
         Locale.setString("ENEMY_SAURIAN_NIGHTSCALE_EXTRA","en","- CAN USE INVISIBILITY\n- HIGH DAMAGE\n- MAGIC RESISTANCE");
         Locale.setString("ENEMY_SAURIAN_SAVANT_NAME","en","Saurian Savant");
         Locale.setString("ENEMY_SAURIAN_SAVANT_DESCRIPTION","en","Powerful spellcasters, they can summon entire Saurian armies to the battlefield!");
         Locale.setString("ENEMY_SAURIAN_SAVANT_SPECIAL","en","*Ranged attack, Summons saurians");
         Locale.setString("ENEMY_SAURIAN_SAVANT_EXTRA","en","- RANGED ATTACK\n- SLOW SPEED\n- SUMMONS SAURIANS");
         Locale.setString("ENEMY_SAURIAN_DARTER_NAME","en","Saurian Darter");
         Locale.setString("ENEMY_SAURIAN_DARTER_DESCRIPTION","en","A rare breed of Saurian that can teleport by unknown methods.");
         Locale.setString("ENEMY_SAURIAN_DARTER_SPECIAL","en","*Teleports");
         Locale.setString("ENEMY_SAURIAN_DARTER_EXTRA","en","- TELEPORTS WHEN INJURED\n- FAST SPEED");
         Locale.setString("ENEMY_SAURIAN_BRUTE_NAME","en","Saurian Brute");
         Locale.setString("ENEMY_SAURIAN_BRUTE_DESCRIPTION","en","Towering, unstoppable angry reptiles armed with energy whips!");
         Locale.setString("ENEMY_SAURIAN_BRUTE_SPECIAL","en","*Cool energy whips");
         Locale.setString("ENEMY_SAURIAN_BRUTE_EXTRA","en","- VERY TOUGH\n- SLOW SPEED");
         Locale.setString("ENEMY_SAURIAN_BLAZEFANG_NAME","en","Saurian Blazefang");
         Locale.setString("ENEMY_SAURIAN_BLAZEFANG_DESCRIPTION","en","These huge reptiles fire devastating shots from their otherworldly weapons.");
         Locale.setString("ENEMY_SAURIAN_BLAZEFANG_SPECIAL","en","*Ranged attack, Can instakill");
         Locale.setString("ENEMY_SAURIAN_BLAZEFANG_EXTRA","en","- RANGED ATTACK\n- CAN INSTAKILL TARGET\n- HIGH MAGIC RESISTANCE");
         Locale.setString("ENEMY_SAURIAN_QUETZAL_NAME","en","Saurian Quetzal");
         Locale.setString("ENEMY_SAURIAN_QUETZAL_DESCRIPTION","en","Gargantuan flying serpent-like creature that hatches the smaller Razorwings.");
         Locale.setString("ENEMY_SAURIAN_QUETZAL_SPECIAL","en","*Flying, Hatches Razorwings");
         Locale.setString("ENEMY_SAURIAN_QUETZAL_EXTRA","en","- FAST SPEED\n- FLYING\n- HATCHES RAZORWINGS");
         Locale.setString("ENEMY_SAURIAN_RAZORWING_NAME","en","Saurian Razorwing");
         Locale.setString("ENEMY_SAURIAN_RAZORWING_DESCRIPTION","en","Tamed and trained by the Saurians to be used as aerial hunters.");
         Locale.setString("ENEMY_SAURIAN_RAZORWING_SPECIAL","en","*Flying");
         Locale.setString("ENEMY_SAURIAN_RAZORWING_EXTRA","en","- FAST SPEED\n- FLYING");
         Locale.setString("ENEMY_FINAL_BOSS_NAME","en","Umbra");
         Locale.setString("ENEMY_FINAL_BOSS_DESCRIPTION","en","Umbra is not made of shadows, shadows are made of Umbra...");
         Locale.setString("ENEMY_FINAL_BOSS_SPECIAL","en","*Boss");
         Locale.setString("ENEMY_FINAL_BOSS_MINION_NAME","en","Shade Elemental");
         Locale.setString("ENEMY_FINAL_BOSS_MINION_DESCRIPTION","en","Natives of the plane of shadows, the shade elementals embody darkness and death...");
         Locale.setString("ENEMY_FINAL_BOSS_MINION_SPECIAL","en","");
         Locale.setString("ENEMY_FINAL_BOSS_PIECE_NAME","en","Shred of Darkness");
         Locale.setString("ENEMY_FINAL_BOSS_PIECE_DESCRIPTION","en","None");
         Locale.setString("ENEMY_FINAL_BOSS_PIECE_SPECIAL","en","");
         Locale.setString("LEVEL_MODE_CAMPAIGN","en","Campaign");
         Locale.setString("LEVEL_MODE_HEROIC","en","Heroic Challenge");
         Locale.setString("LEVEL_MODE_HEROIC_DESCRIPTION","en","Test your tactical skills against an elite enemy force in this challenge meant for the most heroic defenders!");
         Locale.setString("LEVEL_MODE_IRON","en","Iron Challenge");
         Locale.setString("LEVEL_MODE_IRON_DESCRIPTION","en","A test for the ultimate defender, the iron challenge will take your tactical skills to the limit. ");
         Locale.setString("LEVEL_1_TITLE","en","Hammerhold");
         Locale.setString("LEVEL_1_HISTORY","en","Defender of Linirea!\n\nYour services are once more required, as evil forces are attacking the ancient stronghold of Hammerhold! It hasn´t been attacked in a long time... and now it’s once again under siege by nomadic desert tribes!\n\nTake command of the kingdom’s forces, and defend us!");
         Locale.setString("LEVEL_1_HEROIC","en","Heroic Description 1");
         Locale.setString("LEVEL_1_IRON","en","Iron Description 1");
         Locale.setString("LEVEL_1_MODES_UPGRADES","en","lvl 1 max\nNo Heroes");
         Locale.setString("LEVEL_1_IRON_UNLOCK","en","no archer\nno mage");
         Locale.setString("LEVEL_2_TITLE","en","Sandhawk Hamlet");
         Locale.setString("LEVEL_2_HISTORY","en","In the midst of all the confusion, Lord Malagar stole the powerful Hammer of Ages from Hammerhold!\n\nOur outposts east of the fortress report he\'s fled in that direction, and they are facing him as we speak, delaying his escape. We must hurry, General, and go to their aid!");
         Locale.setString("LEVEL_2_HEROIC","en","Heroic Description 2");
         Locale.setString("LEVEL_2_IRON","en","Iron Description 2");
         Locale.setString("LEVEL_2_MODES_UPGRADES","en","lvl 2 max\nNo Heroes");
         Locale.setString("LEVEL_2_IRON_UNLOCK","en","no archer\nno artillery");
         Locale.setString("LEVEL_3_TITLE","en","Sape Oasis");
         Locale.setString("LEVEL_3_HISTORY","en","Our armies have amassed under your command, as we pursue Lord Malagar across the Azsare desert!\n\nWe have followed his trail to the Sape Oasis, one of the few green spots in this wasteland. As such, the nomad tribes do not take kindly to trespassers, so don´t provoke the desert´s fiercest denizens, the Duskar!");
         Locale.setString("LEVEL_3_HEROIC","en","Heroic Description 2");
         Locale.setString("LEVEL_3_IRON","en","Iron Description 2");
         Locale.setString("LEVEL_3_MODES_UPGRADES","en","lvl 2 max\nNo Heroes");
         Locale.setString("LEVEL_3_IRON_UNLOCK","en","no artillery");
         Locale.setString("LEVEL_4_TITLE","en","Dunes of Despair");
         Locale.setString("LEVEL_4_HISTORY","en","It seems the attack at Sape Oasis was merely a distraction, and Lord Malagar has escaped towards Buccaneer´s Den.\n\nWe have no choice but to cross the treacherous Dunes of Despair. There is no time to go around them, so beware of the shifting sands, as the mysterious beasts crawling through them have caused the doom of many an experienced explorer!");
         Locale.setString("LEVEL_4_HEROIC","en","Heroic Description 3");
         Locale.setString("LEVEL_4_IRON","en","Iron Description 3");
         Locale.setString("LEVEL_4_MODES_UPGRADES","en","lvl 2 max\nNo Heroes");
         Locale.setString("LEVEL_4_IRON_UNLOCK","en","no artillery\nno mages");
         Locale.setString("LEVEL_5_TITLE","en","Buccaneer’s Den");
         Locale.setString("LEVEL_5_HISTORY","en","Behold Buccaneer’s Den!\nNowhere else will you find a worse collection of unruly freebooters and dastardly pirates… and nowhere but here will you find a better crew to sail the Crystal Sea.\n\nAfter greasing some dirty palms we\'ve learned that Lord Malagar has boarded a ship towards The Gates of Nazeru. Hiring a crew, however, will have to wait, as an enemy fleet is heading toward us. Ahoy!");
         Locale.setString("LEVEL_5_HEROIC","en","Heroic Description 4");
         Locale.setString("LEVEL_5_IRON","en","Iron Description 4");
         Locale.setString("LEVEL_5_MODES_UPGRADES","en","lvl 2 max");
         Locale.setString("LEVEL_5_IRON_UNLOCK","en","no barracks\nno artillery");
         Locale.setString("LEVEL_6_TITLE","en","Nazeru\'s Gates");
         Locale.setString("LEVEL_6_HISTORY","en","We have arrived at the legendary Gates of Nazeru, which block passage to the lost lands. Something foul is at play here, and the troops are nervous. Not the roving enemy war bands we\'ve seen, our men can handle those...\n\nFortunately, the Archmage Guild is here to aid us in opening the Gates, and we´ll have them on our side if battle breaks out.");
         Locale.setString("LEVEL_6_HEROIC","en","Heroic Description 5");
         Locale.setString("LEVEL_6_IRON","en","Iron Description 5");
         Locale.setString("LEVEL_6_MODES_UPGRADES","en","lvl 3 max");
         Locale.setString("LEVEL_6_IRON_UNLOCK","en","no barracks\nno archer");
         Locale.setString("LEVEL_7_TITLE","en","Crimson Valley");
         Locale.setString("LEVEL_7_HISTORY","en","The mighty Templar Order joins us as we reach the breathtaking Crimson Valley, a name it\'s earned for being the Ma\'qwa tribe\'s hunting grounds. We\'ve established a base camp here and given the men some time off to rest and recover, but we must remain vigilant.\n\nNone of us has ever seen one of the Ma\'qwa, but the rumors about them are... unsettling, to say the least.");
         Locale.setString("LEVEL_7_HEROIC","en","Heroic Description 6");
         Locale.setString("LEVEL_7_IRON","en","Iron Description 6");
         Locale.setString("LEVEL_7_MODES_UPGRADES","en","lvl 3 max");
         Locale.setString("LEVEL_7_IRON_UNLOCK","en","no artillery\nno archer");
         Locale.setString("LEVEL_8_TITLE","en","Snapvine Bridge");
         Locale.setString("LEVEL_8_HISTORY","en","Scouting troops inform us that Lord Malagar heads east, to the city of Ma’qwa Urqu, beyond the Za’golon river. The only way there is through the Snapvine Bridge, built long ago by the Barrington-Keynes Expedition.\n\nOur newest allies, the Tuk\'va tribe, are sworn enemies of the Ma\'qwa, and they warn us about the vegetation… it seems to have something of an appetite around these parts…");
         Locale.setString("LEVEL_8_HEROIC","en","Heroic Description 7");
         Locale.setString("LEVEL_8_IRON","en","Iron Description 7");
         Locale.setString("LEVEL_8_MODES_UPGRADES","en","lvl 3 max");
         Locale.setString("LEVEL_8_IRON_UNLOCK","en","no mages\nno artillery");
         Locale.setString("LEVEL_9_TITLE","en","Lost Jungle");
         Locale.setString("LEVEL_9_HISTORY","en","On our way to Ma’qwa Urqu, the jungle keeps getting deadlier. As if the tangled maze of roots, trees, and snapvines that have never known the sun’s kiss weren’t enough, something darker lurks within the thick rainforest.\n\nThe men feel as if they’re being hunted by something not of this world… Almost as unsettling are the necromancers we\'ve enlisted. However, their being against Lord Malagar´s plans only stresses the urgency of stopping him.");
         Locale.setString("LEVEL_9_HEROIC","en","Heroic Description 8");
         Locale.setString("LEVEL_9_IRON","en","Iron Description 8");
         Locale.setString("LEVEL_9_MODES_UPGRADES","en","lvl 4 max");
         Locale.setString("LEVEL_9_IRON_UNLOCK","en","no barracks\nno mage");
         Locale.setString("LEVEL_10_TITLE","en","Ma’qwa Urqu");
         Locale.setString("LEVEL_10_HISTORY","en","Cast your gaze upon the ancient city of Ma’qwa Urqu, home to the sinister man-eating tribe that has become our enemy! Hear the battle drums and dark shamanic chanting that emanate from its mountaintop perch, feel the heat from that dangerous volcano; this is their place of power!\n\nTo pursue our dreaded foe, we must first get through the Ma’qwa forces surrounding the city. Good thing our Dwarven engineers and their gnomish tinkerer cousins have cooked up a mighty mechanical surprise…");
         Locale.setString("LEVEL_10_HEROIC","en","Heroic Description 9");
         Locale.setString("LEVEL_10_IRON","en","Iron Description 9");
         Locale.setString("LEVEL_10_MODES_UPGRADES","en","lvl 4 max");
         Locale.setString("LEVEL_10_IRON_UNLOCK","en","no artillery\nno mage");
         Locale.setString("LEVEL_11_TITLE","en","Temple of Saqra");
         Locale.setString("LEVEL_11_HISTORY","en","We have him surrounded! The Temple of Saqra will be Lord Malagar´s last stand! The Ma\'qwa are even fiercer here, where they worship their crocodile-visaged deity, and their own Warlord King is leading them now.\n\nThe combined might of the Ma\'qwa and their leader\'s magics is quite possibly the most impressive array of savagery evil might ever assembled! Fight back with all your prowess, my men, lest we end up as sacrifices to Saqra… or worse.");
         Locale.setString("LEVEL_11_HEROIC","en","Heroic Description 10");
         Locale.setString("LEVEL_11_IRON","en","Iron Description 10");
         Locale.setString("LEVEL_11_MODES_UPGRADES","en","lvl 4 max");
         Locale.setString("LEVEL_11_IRON_UNLOCK","en","no barracks\nno archer");
         Locale.setString("LEVEL_12_TITLE","en","The Underpass");
         Locale.setString("LEVEL_12_HISTORY","en","It seems that the Temple of Saqra was merely the entrance to a vast underground labyrinth, carved into the mountain rock itself! There might just be some truth to the legends that warn about an unspeakable evil here…\n\nWe must head into the maze, for our mission cannot be abandoned. If only the overwhelming darkness were all we had to face…");
         Locale.setString("LEVEL_12_HEROIC","en","Heroic Description 11");
         Locale.setString("LEVEL_12_IRON","en","Iron Description 11");
         Locale.setString("LEVEL_12_MODES_UPGRADES","en","lvl 5 max");
         Locale.setString("LEVEL_12_IRON_UNLOCK","en","no artillery\nno mage");
         Locale.setString("LEVEL_13_TITLE","en","Beresad\'s Lair");
         Locale.setString("LEVEL_13_HISTORY","en","We have been off marching through this stone labyrinth for days without sign of the enemy... until now. Our trackers have found the enemy\'s trail... but the deeper we go, the hotter it gets!\n\nAncient glyphs on the walls tell us we\'re heading into the Halls of Beresad, and if the legends are true, we\'ll get an even warmer reception...");
         Locale.setString("LEVEL_13_HEROIC","en","Heroic Description 12");
         Locale.setString("LEVEL_13_IRON","en","Iron Description 12");
         Locale.setString("LEVEL_13_MODES_UPGRADES","en","lvl 5 max");
         Locale.setString("LEVEL_13_IRON_UNLOCK","en","no mage\nno archer");
         Locale.setString("LEVEL_14_TITLE","en","The Dark Descent");
         Locale.setString("LEVEL_14_HISTORY","en","We\'ve almost run out of supplies, morale is at an all-time low, and some of our men have deserted. Luckily, we’ve bumped into a Dwarven mining crew that dug too deep and have barricaded themselves against the Saurians.\n\nThey\'ve promised to join us in finding our way out of this damned place. Our escape must wait, as we and our newfound allies must repel the oncoming Saurian horde!");
         Locale.setString("LEVEL_14_HEROIC","en","Heroic Description 13");
         Locale.setString("LEVEL_14_IRON","en","Iron Description 13");
         Locale.setString("LEVEL_14_MODES_UPGRADES","en","lvl 5 max");
         Locale.setString("LEVEL_14_IRON_UNLOCK","en","no artillery\nno barracks");
         Locale.setString("LEVEL_15_TITLE","en","Emberspike Depths");
         Locale.setString("LEVEL_15_HISTORY","en","This is it! The final battle against Lord Malagar and his forces is at hand! The dark ritual to unleash his evil master is underway! General, the fate of the world rests upon your shoulders.\n\nWe have travelled through forsaken lands, far beyond the frontiers of our kingdom, in the deadliest of journeys, and only your shining example and exceptional tactics have brought us this far. Only you can see this quest through, and vanquish our enemies. FOR LINIREA!");
         Locale.setString("LEVEL_15_HEROIC","en","Heroic Description 14");
         Locale.setString("LEVEL_15_IRON","en","Iron Description 14");
         Locale.setString("LEVEL_15_MODES_UPGRADES","en","lvl 5 max");
         Locale.setString("LEVEL_15_IRON_UNLOCK","en","no mages");
         Locale.setString("TIP_TITLE","en","Tip: ");
         Locale.setString("TIP_1","en","Enemies and Soldiers with armor receive less physical damage.");
         Locale.setString("TIP_2","en","Support barracks with ranged towers to maximize enemy exposure.");
         Locale.setString("TIP_3","en","Reinforcements are a great way to split enemy forces.");
         Locale.setString("TIP_4","en","Artillery works best against high concentrations of enemies.");
         Locale.setString("TIP_5","en","Artillery damage is highest in the center of the explosion.");
         Locale.setString("TIP_6","en","Use reinforcements constantly to slow and damage the enemy.");
         Locale.setString("TIP_7","en","Always aim rain of fire a little ahead of your target.");
         Locale.setString("TIP_8","en","Rearranging your upgrade points is a good way to adapt your strategy.");
         Locale.setString("TIP_9","en","Magic damage is the best way to deal with armored enemies.");
         Locale.setString("TIP_10","en","Flying enemies cannot be blocked by barracks and won\'t be targeted by most artillery.");
         Locale.setString("TIP_11","en","Enemies with magic resistance receive less damage from magic attacks.");
         Locale.setString("TIP_12","en","Adjust the rally point of soldiers to create better strategies.");
         Locale.setString("TIP_13","en","Sometimes it is better to build more towers instead of upgrading a few.");
         Locale.setString("TIP_14","en","Pestilence damage ignores armor.");
         Locale.setString("TIP_15","en","Upgrading a barrack instantly trains new soldiers.");
         Locale.setString("TIP_16","en","Calling an early wave gives bonus cash and reduces spell cooldowns a bit.");
         Locale.setString("TIP_17","en","Artillery explosions can damage flying enemies even though they cannot target them directly.");
         Locale.setString("TIP_18","en","Use barracks or reinforcements to isolate troublesome enemies.");
         Locale.setString("TIP_19","en","Effects that kill instantly are a great way to deal with tough enemies.");
         Locale.setString("TIP_20","en","Keep your eye out for enemies that trouble your defenses. More may come soon.");
         Locale.setString("TIP_21","en","You can check what enemies are in the incoming wave at the wave icon.");
         Locale.setString("TIP_22","en","Don\'t be afraid of selling a tower and replacing it with a more suitable one.");
         Locale.setString("TIP_23","en","Heroes and soldiers heal when they are idle.");
         Locale.setString("TIP_24","en","Calling a wave earlier doesn´t reduce the cooldown of tower abilities.");
         Locale.setString("TIP_25","en","Sometimes it is wise to save some gold to adapt to unexpected enemies.");
         Locale.setString("TIP_26","en","Savages heal themselves and become stronger every time they eat.");
         Locale.setString("TIP_27","en","Sand wraiths can´t raise coffins while blocked.");
         Locale.setString("TIP_28","en","Poison from enemies is not lethal. Retreat your poisoned soldiers to save them.");
         Locale.setString("TIP_29","en","The Executioner cannot execute heroes.");
         Locale.setString("TIP_30","en","Combined Shaman auras can make Savages nearly invincible.");
         Locale.setString("STAR_WIN_1","en","VICTORY");
         Locale.setString("STAR_WIN_2","en","GREAT VICTORY");
         Locale.setString("STAR_WIN_3","en","PERFECT WIN");
         Locale.setString("TUTORIAL_INTRO_BUTTON_CANCEL","en","SKIP THE BASICS\nBRING IT ON!");
         Locale.setString("TUTORIAL_INTRO_BUTTON_NEXT","en","YES PLEASE SHOW\nME THE BASICS");
         Locale.setString("TUTORIAL_BASICS_BUTTON_CANCEL","en","SKIP THE BASICS\nBRING IT ON!");
         Locale.setString("TUTORIAL_BASICS_BUTTON_NEXT","en","YES PLEASE SHOW\nME THE BASICS");
         Locale.setString("TUTORIAL_TOWERS_BUTTON_CANCEL","en","SKIP THE BASICS\nBRING IT ON!");
         Locale.setString("TUTORIAL_TOWERS_BUTTON_NEXT","en","YES PLEASE SHOW\nME THE BASICS");
         Locale.setString("SPECIAL_LEGIONNAIRE_ARCHER_NAME","en","Legion Archer");
         Locale.setString("SPECIAL_MERCENARY_NAME","en","Mercenary tower");
         Locale.setString("SPECIAL_MERCENARY_DESCRIPTION","en","Here the desert\'s most fierce dwellers await a contract.");
         Locale.setString("SPECIAL_LEGIONNAIRE_NAME","en","Legionnaire");
         Locale.setString("SPECIAL_LEGIONNAIRE_DESCRIPTION","en","Highly trained elite soldiers, they live and die for the glory of battle!");
         Locale.setString("SPECIAL_DJINN_NAME","en","Genie");
         Locale.setString("SPECIAL_DJINN_DESCRIPTION","en","Genies are formidable creatures. They fight with magic and fist alike but ask for a lot of gold.");
         Locale.setString("SPECIAL_PIRATE_NAME","en","SCUMM Bar");
         Locale.setString("SPECIAL_PIRATE_DESCRIPTION","en","A safe haven for reckless pirates looking for gold.");
         Locale.setString("SPECIAL_PIRATE_CAP_NAME","en","Corsair");
         Locale.setString("SPECIAL_PIRATE_CAP_DESCRIPTION","en","Formidable fighters, they love to fight and loot for the highest bidder!");
         Locale.setString("SPECIAL_PIRATE_FLAMER_NAME","en","Buccaneer");
         Locale.setString("SPECIAL_PIRATE_FLAMER_DESCRIPTION","en","These scurvy dogs love their grog and only share it by setting it on fire and throwing it.");
         Locale.setString("SPECIAL_PIRATE_CAMP_NAME","en","Pirate Cap");
         Locale.setString("SPECIAL_PIRATE_CAMP_DESCRIPTION","en","Hire pirates cannons.");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_1_NAME","en","Cannonade I");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_1_DESCRIPTION","en","Shoot one cannon dealing 60 to 120 damage.");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_2_NAME","en","Cannonade II");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_2_DESCRIPTION","en","Shoot two cannons dealing 60 to 120 damage each.");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_3_NAME","en","Cannonade III");
         Locale.setString("SPECIAL_PIRATE_CAMP_SHOOT_3_DESCRIPTION","en","Shoot three cannons dealing 60 to 120 damage each. Devastating!");
         Locale.setString("SPECIAL_AMAZONAS_NAME","en","Spear Maiden Hut");
         Locale.setString("SPECIAL_AMAZONAS_DESCRIPTION","en","A tribe of proud warrior women ready for battle");
         Locale.setString("SPECIAL_AMAZONAS_WARRIOR_NAME","en","Spear Maiden");
         Locale.setString("SPECIAL_AMAZONAS_WARRIOR_DESCRIPTION","en","The maidens are known across the jungle for their unorthodox but deadly fighting style.");
         Locale.setString("SPECIAL_DWARF_BASTION_NAME","en","Dwarven Bastion");
         Locale.setString("SPECIAL_DWARF_BASTION_DESCRIPTION","en","Dwarf Hall description.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_1_NAME","en","Explosive Keg.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_1_DESCRIPTION_1","en","Throws an explosive keg that deals 60 to 100 damage.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_1_DESCRIPTION_2","en","Throws an explosive keg that deals 80 to 160 damage.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_1_DESCRIPTION_3","en","Throws an explosive keg that deals 100 to 220 damage.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_1_NOTE","en","TNT!... and I\'ll win the fight!");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_2_NAME","en","Full Mithril Jacket");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_2_DESCRIPTION_1","en","Increases ranged attack damage by 30 points.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_2_DESCRIPTION_2","en","Increases ranged attack damage by another 30 points.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_2_DESCRIPTION_3","en","Increases ranged attack damage by another 30 points.");
         Locale.setString("SPECIAL_DWARF_TOWER1_UPGRADE_2_NOTE","en","Seven-six-two millimeter...");
         Locale.setString("SPECIAL_DWARF_HALL_NAME","en","Dwarf Hall");
         Locale.setString("SPECIAL_DWARF_HALL_DESCRIPTION","en","Dwarf Hall description.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_NAME_1","en","Mithril Hammers");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_NAME_2","en","Mithril Hammers II");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_NAME_3","en","Mithril Hammers III");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_DESCRIPTION_1","en","Increases each dwarf attack damage by 5.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_DESCRIPTION_2","en","Increases each dwarf attack damage by an additional 5.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_DESCRIPTION_3","en","Increases each dwarf attack damage by yet an additional 5.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_1_NOTE","en","As light as a feather...");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_NAME_1","en","Mithril Armor");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_NAME_2","en","Mithril Armor II");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_NAME_3","en","Mithril Armor III");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_DESCRIPTION_1","en","Increases dwarf armor to Medium.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_DESCRIPTION_2","en","Increases dwarf armor to High.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_DESCRIPTION_3","en","Increases armor to 70%");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_2_NOTE","en","...as hard as dragon scales!");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_NAME_1","en","Dwarfweiser");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_NAME_2","en","Dwarfweiser II");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_NAME_3","en","Dwarfweiser III");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_DESCRIPTION_1","en","A magic drink that grants super life regeneration for 3 seconds.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_DESCRIPTION_2","en","Increases Dwarfweiser duration to 5 seconds.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_DESCRIPTION_3","en","Increases Dwarfweiser duration to 7 seconds.");
         Locale.setString("SPECIAL_DWARF_BARRACKS_UPGRADE_3_NOTE","en","Wassuuuup!");
         Locale.setString("SPECIAL_REPAIR_HOLDER_JUNGLE_NAME","en","Overgrowth");
         Locale.setString("SPECIAL_REPAIR_HOLDER_JUNGLE_DESCRIPTION","en","Clean up the overgrowth to enable this strategic point.");
         Locale.setString("SPECIAL_REPAIR_HOLDER_UNDERGROUND_NAME","en","Rubble");
         Locale.setString("SPECIAL_REPAIR_HOLDER_UNDERGROUND_DESCRIPTION","en","Clean up the rubble to enable this strategic point.");
         Locale.setString("UPGRADE_1_NAME","en","Steady Hand");
         Locale.setString("UPGRADE_1_DESCRIPTION","en","Increases marksmen attack range.");
         Locale.setString("UPGRADE_2_NAME","en","Lumbermill");
         Locale.setString("UPGRADE_2_DESCRIPTION","en","Reduces basic archer construction costs.");
         Locale.setString("UPGRADE_3_NAME","en","Focused Aim");
         Locale.setString("UPGRADE_3_DESCRIPTION","en","Increases marksmen attack damage.");
         Locale.setString("UPGRADE_4_NAME","en","Accuracy");
         Locale.setString("UPGRADE_4_DESCRIPTION","en","Increases marksmen attack damage and range.");
         Locale.setString("UPGRADE_5_NAME","en","Twin shot");
         Locale.setString("UPGRADE_5_DESCRIPTION","en","Marksmen have a chance of shooting two projectiles at the same time.");
         Locale.setString("UPGRADE_6_NAME","en","Defensive Stance");
         Locale.setString("UPGRADE_6_DESCRIPTION","en","Barracks train soldiers with better armor.");
         Locale.setString("UPGRADE_7_NAME","en","Boot Camp");
         Locale.setString("UPGRADE_7_DESCRIPTION","en","Barracks train more resilient soldiers.");
         Locale.setString("UPGRADE_8_NAME","en","Esprit de Corps");
         Locale.setString("UPGRADE_8_DESCRIPTION","en","Increases barracks rally point range and healing rate.");
         Locale.setString("UPGRADE_9_NAME","en","Veteran Squad");
         Locale.setString("UPGRADE_9_DESCRIPTION","en","Soldiers are trained faster and with improved armor.");
         Locale.setString("UPGRADE_10_NAME","en","Courage");
         Locale.setString("UPGRADE_10_DESCRIPTION","en","While in combat, soldiers & reinforcements regenerate health.");
         Locale.setString("UPGRADE_11_NAME","en","Rune of Power");
         Locale.setString("UPGRADE_11_DESCRIPTION","en","Increases mages\' attack range.");
         Locale.setString("UPGRADE_12_NAME","en","Spell Penetration");
         Locale.setString("UPGRADE_12_DESCRIPTION","en","Mages\' bolts have a chance to ignore magic resistance.");
         Locale.setString("UPGRADE_13_NAME","en","Eldritch Power");
         Locale.setString("UPGRADE_13_DESCRIPTION","en","Increases mages\' attack damage.");
         Locale.setString("UPGRADE_14_NAME","en","Wizard Academy");
         Locale.setString("UPGRADE_14_DESCRIPTION","en","Reduces mages\' special abilities costs.");
         Locale.setString("UPGRADE_15_NAME","en","Brilliance");
         Locale.setString("UPGRADE_15_DESCRIPTION","en","For every other mage tower built, each mage tower gets a bonus to damage.");
         Locale.setString("UPGRADE_16_NAME","en","Smoothbore");
         Locale.setString("UPGRADE_16_DESCRIPTION","en","Increases artillery attack range.");
         Locale.setString("UPGRADE_17_NAME","en","Alchemical Powder");
         Locale.setString("UPGRADE_17_DESCRIPTION","en","Artilleries have a chance of dealing max damage with no splash reduction.");
         Locale.setString("UPGRADE_18_NAME","en","Improved Ordnance");
         Locale.setString("UPGRADE_18_DESCRIPTION","en","Increases artillery attack damage.");
         Locale.setString("UPGRADE_19_NAME","en","Gnomish  Tinkering");
         Locale.setString("UPGRADE_19_DESCRIPTION","en","Reduces artilleries\' special abilities reload times.");
         Locale.setString("UPGRADE_20_NAME","en","Shock and Awe");
         Locale.setString("UPGRADE_20_DESCRIPTION","en","Artillery towers have a chance of stunning their targets on every attack.");
         Locale.setString("UPGRADE_21_NAME","en","Burning Skies");
         Locale.setString("UPGRADE_21_DESCRIPTION","en","Increases meteor damage and reduces cooldown by 5 seconds.");
         Locale.setString("UPGRADE_22_NAME","en","Scorched Earth");
         Locale.setString("UPGRADE_22_DESCRIPTION","en","Meteors set the ground on fire for 5 seconds, burning enemies walking over it.");
         Locale.setString("UPGRADE_23_NAME","en","Hellfire");
         Locale.setString("UPGRADE_23_DESCRIPTION","en","Adds 2 additional meteors and reduces cooldown by 5 seconds.");
         Locale.setString("UPGRADE_24_NAME","en","Conflagration");
         Locale.setString("UPGRADE_24_DESCRIPTION","en","Increases meteor damage and explosion radius while doubling scorched earth effects.");
         Locale.setString("UPGRADE_25_NAME","en","Cataclysm");
         Locale.setString("UPGRADE_25_DESCRIPTION","en","Increases meteor damage and rains additional meteors at random locations all over the battlefield.");
         Locale.setString("UPGRADE_26_NAME","en","Trained Volunteers");
         Locale.setString("UPGRADE_26_DESCRIPTION","en","Trained volunteers have additional health and deal a little more damage.");
         Locale.setString("UPGRADE_27_NAME","en","Men-at-arms");
         Locale.setString("UPGRADE_27_DESCRIPTION","en","Men-at-arms have more health and wear good armor.");
         Locale.setString("UPGRADE_28_NAME","en","Champion");
         Locale.setString("UPGRADE_28_DESCRIPTION","en","Champions have even more health and wield great weapons.");
         Locale.setString("UPGRADE_29_NAME","en","Sworn Blades");
         Locale.setString("UPGRADE_29_DESCRIPTION","en","Sworn blades have the most health and wield dual weapons.");
         Locale.setString("UPGRADE_30_NAME","en","Recurve Bow");
         Locale.setString("UPGRADE_30_DESCRIPTION","en","Gives reinforcements a ranged weapon that can target ground and flying enemies.");
         Locale.setString("ACHIEVEMENT_UPGRADE_LEVEL3_NAME","en","Home Improvement");
         Locale.setString("ACHIEVEMENT_UPGRADE_LEVEL3_DESCRIPTION","en","Upgrade all basic tower types to level 3.");
         Locale.setString("ACHIEVEMENT_EASY_TOWER_BUILDER_NAME","en","Constructor");
         Locale.setString("ACHIEVEMENT_EASY_TOWER_BUILDER_DESCRIPTION","en","Build 30 towers.");
         Locale.setString("ACHIEVEMENT_DARING_NAME","en","Daring");
         Locale.setString("ACHIEVEMENT_DARING_DESCRIPTION","en","Call 10 early waves.");
         Locale.setString("ACHIEVEMENT_FIRST_BLOOD_NAME","en","First Blood");
         Locale.setString("ACHIEVEMENT_FIRST_BLOOD_DESCRIPTION","en","Kill one enemy.");
         Locale.setString("ACHIEVEMENT_BLOODLUST_NAME","en","Bloodlust");
         Locale.setString("ACHIEVEMENT_BLOODLUST_DESCRIPTION","en","Kill 500 enemies.");
         Locale.setString("ACHIEVEMENT_WHATS_THAT_NAME","en","What\'s that?");
         Locale.setString("ACHIEVEMENT_WHATS_THAT_DESCRIPTION","en","Open 10 enemy information cards.");
         Locale.setString("ACHIEVEMENT_ARMAGGEDON_NAME","en","Armageddon");
         Locale.setString("ACHIEVEMENT_ARMAGGEDON_DESCRIPTION","en","Use Rain of Fire 5 times in a single stage.");
         Locale.setString("ACHIEVEMENT_EARN15_STARS_NAME","en","Starry");
         Locale.setString("ACHIEVEMENT_EARN15_STARS_DESCRIPTION","en","Earn 15 stars.");
         Locale.setString("ACHIEVEMENT_MEDIUM_TOWER_BUILDER_NAME","en","Engineer");
         Locale.setString("ACHIEVEMENT_MEDIUM_TOWER_BUILDER_DESCRIPTION","en","Build 100 towers.");
         Locale.setString("ACHIEVEMENT_SPECIALIZATION_NAME","en","Specialist");
         Locale.setString("ACHIEVEMENT_SPECIALIZATION_DESCRIPTION","en","Build all 8 tower specializations.");
         Locale.setString("ACHIEVEMENT_DEFEAT_JUGGERNAUT_NAME","en","Nuts and Bolts");
         Locale.setString("ACHIEVEMENT_DEFEAT_JUGGERNAUT_DESCRIPTION","en","Defeat The Juggernaut.");
         Locale.setString("ACHIEVEMENT_DEFEAT_MOUNTAIN_BOSS_NAME","en","Is he dead yeti?");
         Locale.setString("ACHIEVEMENT_DEFEAT_MOUNTAIN_BOSS_DESCRIPTION","en","Defeat J.T.");
         Locale.setString("ACHIEVEMENT_SLAYER_NAME","en","Slayer");
         Locale.setString("ACHIEVEMENT_SLAYER_DESCRIPTION","en","Kill 2500 enemies.");
         Locale.setString("ACHIEVEMENT_DEATH_FROM_ABOVE_NAME","en","Death from Above");
         Locale.setString("ACHIEVEMENT_DEATH_FROM_ABOVE_DESCRIPTION","en","Kill 100 enemies with meteor shower.");
         Locale.setString("ACHIEVEMENT_TACTICIAN_NAME","en","Tactician");
         Locale.setString("ACHIEVEMENT_TACTICIAN_DESCRIPTION","en","Change soldiers\' rally point 200 times.");
         Locale.setString("ACHIEVEMENT_EARN30_STARS_NAME","en","Supermario");
         Locale.setString("ACHIEVEMENT_EARN30_STARS_DESCRIPTION","en","Earn 30 stars.");
         Locale.setString("ACHIEVEMENT_DEFEAT_END_BOSS_NAME","en","This is the end!");
         Locale.setString("ACHIEVEMENT_DEFEAT_END_BOSS_DESCRIPTION","en","Defeat Vez\'nan.");
         Locale.setString("ACHIEVEMENT_MULTIKILL_NAME","en","Terminator");
         Locale.setString("ACHIEVEMENT_MULTIKILL_DESCRIPTION","en","Kill 10.000 enemies.");
         Locale.setString("ACHIEVEMENT_HARD_TOWER_BUILDER_NAME","en","The Architect");
         Locale.setString("ACHIEVEMENT_HARD_TOWER_BUILDER_DESCRIPTION","en","Build 150 towers.");
         Locale.setString("ACHIEVEMENT_DIE_HARD_NAME","en","Die Hard");
         Locale.setString("ACHIEVEMENT_DIE_HARD_DESCRIPTION","en","Have your soldiers regenerate a total of 50.000 life.");
         Locale.setString("ACHIEVEMENT_CANNON_FODDER_NAME","en","Cannon Fodder");
         Locale.setString("ACHIEVEMENT_CANNON_FODDER_DESCRIPTION","en","Send 1000 soldiers to their deaths.");
         Locale.setString("ACHIEVEMENT_GI_JOE_NAME","en","G.I. Joe");
         Locale.setString("ACHIEVEMENT_GI_JOE_DESCRIPTION","en","Train 1000 soldiers.");
         Locale.setString("ACHIEVEMENT_EARN45_STARS_NAME","en","Superstar");
         Locale.setString("ACHIEVEMENT_EARN45_STARS_DESCRIPTION","en","Earn 45 stars.");
         Locale.setString("ACHIEVEMENT_FEARLESS_NAME","en","Fearless");
         Locale.setString("ACHIEVEMENT_FEARLESS_DESCRIPTION","en","Call all waves early in a single mission.");
         Locale.setString("ACHIEVEMENT_REAL_STATE_NAME","en","Real Estate");
         Locale.setString("ACHIEVEMENT_REAL_STATE_DESCRIPTION","en","Sell 30 Towers");
         Locale.setString("ACHIEVEMENT_IMPATIENT_NAME","en","Impatient");
         Locale.setString("ACHIEVEMENT_IMPATIENT_DESCRIPTION","en","Call an early wave within 3 seconds of the icon showing up.");
         Locale.setString("ACHIEVEMENT_INDECISIVE_NAME","en","Indecisive");
         Locale.setString("ACHIEVEMENT_INDECISIVE_DESCRIPTION","en","Sell 5 towers in a single mission.");
         Locale.setString("ACHIEVEMENT_MAX_ELVES_NAME","en","Forest Diplomacy");
         Locale.setString("ACHIEVEMENT_MAX_ELVES_DESCRIPTION","en","Recruit max elves at The Silveroak Outpost.");
         Locale.setString("ACHIEVEMENT_IMPERIAL_SAVIOUR_NAME","en","Imperial Saviour");
         Locale.setString("ACHIEVEMENT_IMPERIAL_SAVIOUR_DESCRIPTION","en","Complete The Citadel with at least 3 surviving imperial guards.");
         Locale.setString("ACHIEVEMENT_HENDERSON_NAME","en","Like a Henderson");
         Locale.setString("ACHIEVEMENT_HENDERSON_DESCRIPTION","en","Free the sasquatch on the Icewind Pass.");
         Locale.setString("ACHIEVEMENT_SUN_BURNER_NAME","en","Sunburner!");
         Locale.setString("ACHIEVEMENT_SUN_BURNER_DESCRIPTION","en","Fire the sunray 20 times.");
         Locale.setString("ACHIEVEMENT_BEAM_ME_UP_NAME","en","Beam Me Up Scotty");
         Locale.setString("ACHIEVEMENT_BEAM_ME_UP_DESCRIPTION","en","Teleport 250 or more enemies.");
         Locale.setString("ACHIEVEMENT_AXE_RAINER_NAME","en","Axe Rain!");
         Locale.setString("ACHIEVEMENT_AXE_RAINER_DESCRIPTION","en","Throw 500 or more axes!.");
         Locale.setString("ACHIEVEMENT_SNIPER_NAME","en","50 shots 50 kills");
         Locale.setString("ACHIEVEMENT_SNIPER_DESCRIPTION","en","Snipe 50 enemies.");
         Locale.setString("ACHIEVEMENT_TOXICITY_NAME","en","Toxicity");
         Locale.setString("ACHIEVEMENT_TOXICITY_DESCRIPTION","en","Kill 50 enemies by poison damage.");
         Locale.setString("ACHIEVEMENT_ROCKETEER_NAME","en","Rocketeer");
         Locale.setString("ACHIEVEMENT_ROCKETEER_DESCRIPTION","en","Shoot 100 Missiles.");
         Locale.setString("ACHIEVEMENT_SHEPARD_NAME","en","Shepherd");
         Locale.setString("ACHIEVEMENT_SHEPARD_DESCRIPTION","en","Polymorph 50 enemies into sheeps.");
         Locale.setString("ACHIEVEMENT_DUST_TO_DUST_NAME","en","Dust to Dust!");
         Locale.setString("ACHIEVEMENT_DUST_TO_DUST_DESCRIPTION","en","Desintegrate 50 or more enemies.");
         Locale.setString("ACHIEVEMENT_ENTANGLED_NAME","en","Entangled");
         Locale.setString("ACHIEVEMENT_ENTANGLED_DESCRIPTION","en","Hold 500 or more enemies with Wrath of the Forest.");
         Locale.setString("ACHIEVEMENT_ENERGY_NETWORK_NAME","en","Energy Network");
         Locale.setString("ACHIEVEMENT_ENERGY_NETWORK_DESCRIPTION","en","Build 4 Tesla towers in any stage.");
         Locale.setString("ACHIEVEMENT_ELEMENTALIST_NAME","en","Elementalist");
         Locale.setString("ACHIEVEMENT_ELEMENTALIST_DESCRIPTION","en","Summon 5 rock elementals in any one stage.");
         Locale.setString("ACHIEVEMENT_BARBARIAN_RUSH_NAME","en","Are you not entertained?");
         Locale.setString("ACHIEVEMENT_BARBARIAN_RUSH_SHORT_NAME","en","Not entertained?");
         Locale.setString("ACHIEVEMENT_BARBARIAN_RUSH_DESCRIPTION","en","Have a single barbarian kill 10 enemies.");
         Locale.setString("ACHIEVEMENT_CLUSTERED_NAME","en","Clustered");
         Locale.setString("ACHIEVEMENT_CLUSTERED_DESCRIPTION","en","Drop 1000 or more bomblets with the cluster bomb.");
         Locale.setString("ACHIEVEMENT_ACDC_NAME","en","AC/DC");
         Locale.setString("ACHIEVEMENT_ACDC_DESCRIPTION","en","Kill 300 enemies with electricity.");
         Locale.setString("ACHIEVEMENT_MEDIC_NAME","en","Medic!");
         Locale.setString("ACHIEVEMENT_MEDIC_DESCRIPTION","en","Have your Paladins heal a total of 7.000 life.");
         Locale.setString("ACHIEVEMENT_HOLY_CHORUS_NAME","en","Holy Chorus");
         Locale.setString("ACHIEVEMENT_HOLY_CHORUS_DESCRIPTION","en","Have your Paladins perform 100 Holy Strikes.");
         Locale.setString("ACHIEVEMENT_SHEEP_KILLER_NAME","en","Ovinophobia");
         Locale.setString("ACHIEVEMENT_SHEEP_KILLER_DESCRIPTION","en","Kill 10 or more sheep with your hands!");
         Locale.setString("ACHIEVEMENT_CATCH_A_FISH_NAME","en","Twin Rivers Angler");
         Locale.setString("ACHIEVEMENT_CATCH_A_FISH_DESCRIPTION","en","Catch a fish.");
         Locale.setString("ACHIEVEMENT_GREAT_DEFENDER_NAME","en","Great Defender");
         Locale.setString("ACHIEVEMENT_GREAT_DEFENDER_DESCRIPTION","en","Complete all campaign stages in Normal difficulty.");
         Locale.setString("ACHIEVEMENT_HEROIC_DEFENDER_NAME","en","Heroic Defender");
         Locale.setString("ACHIEVEMENT_HEROIC_DEFENDER_DESCRIPTION","en","Complete all Heroic stages in Normal difficulty.");
         Locale.setString("ACHIEVEMENT_IRON_DEFENDER_NAME","en","Iron Defender");
         Locale.setString("ACHIEVEMENT_IRON_DEFENDER_DESCRIPTION","en","Complete all Iron stages in Normal difficulty.");
         Locale.setString("SV_ACHIEVEMENT_ALIBABA_NAME","en","Ali Baba");
         Locale.setString("SV_ACHIEVEMENT_ALIBABA_DESCRIPTION","en","Have your assassins steal 10.000 gold.");
         Locale.setString("SV_ACHIEVEMENT_DODGETHIS_NAME","en","Dodge This!");
         Locale.setString("SV_ACHIEVEMENT_DODGETHIS_DESCRIPTION","en","Have your assassins dodge 1000 attacks.");
         Locale.setString("SV_ACHIEVEMENT_HIGHLANDER_NAME","en","Highlander");
         Locale.setString("SV_ACHIEVEMENT_HIGHLANDER_DESCRIPTION","en","Have one templar revive 5 times in a row.");
         Locale.setString("SV_ACHIEVEMENT_LETITBLEED_NAME","en","Let it bleed!");
         Locale.setString("SV_ACHIEVEMENT_LETITBLEED_DESCRIPTION","en","Kill 100 enemies by letting them bleed to death.");
         Locale.setString("SV_ACHIEVEMENT_FUJITA5_NAME","en","Fujita #5");
         Locale.setString("SV_ACHIEVEMENT_FUJITA5_DESCRIPTION","en","Pick up 500 enemies with the Twister spell.");
         Locale.setString("SV_ACHIEVEMENT_OVERCHARGED_NAME","en","Overcharged");
         Locale.setString("SV_ACHIEVEMENT_OVERCHARGED_DESCRIPTION","en","Deal over 30.000 damage with Critical Mass explosions.");
         Locale.setString("SV_ACHIEVEMENT_NECROPOLIS_NAME","en","Necropolis");
         Locale.setString("SV_ACHIEVEMENT_NECROPOLIS_DESCRIPTION","en","Have 20 skeleton minions active at the same time.");
         Locale.setString("SV_ACHIEVEMENT_GRIMREAPER_NAME","en","Grim Reaper");
         Locale.setString("SV_ACHIEVEMENT_GRIMREAPER_DESCRIPTION","en","Have your Death Knights claim 99 lives.");
         Locale.setString("SV_ACHIEVEMENT_MECHWARRIOR_NAME","en","Mechwarrior");
         Locale.setString("SV_ACHIEVEMENT_MECHWARRIOR_DESCRIPTION","en","Build 3 Mechas on any one stage.");
         Locale.setString("SV_ACHIEVEMENT_OPTIMUSPRIME_NAME","en","Optimus Prime");
         Locale.setString("SV_ACHIEVEMENT_OPTIMUSPRIME_DESCRIPTION","en","Have your Mechas defeat 500 enemies.");
         Locale.setString("SV_ACHIEVEMENT_DEADFROMBELOW_NAME","en","Death from below");
         Locale.setString("SV_ACHIEVEMENT_DEADFROMBELOW_DESCRIPTION","en","Kill over 100 enemies with the drill.");
         Locale.setString("SV_ACHIEVEMENT_POPULARBBQ_NAME","en","Popular BBQ");
         Locale.setString("SV_ACHIEVEMENT_POPULARBBQ_DESCRIPTION","en","Set 20 enemies on fire at the same time.");
         Locale.setString("SV_ACHIEVEMENT_HAWKEYE_NAME","en","Hawkeye");
         Locale.setString("SV_ACHIEVEMENT_HAWKEYE_DESCRIPTION","en","Apply one Falconer bonus to 4 towers.");
         Locale.setString("SV_ACHIEVEMENT_BOLTOFTHESUN_NAME","en","Bolt out the Sun");
         Locale.setString("SV_ACHIEVEMENT_BOLTOFTHESUN_DESCRIPTION","en","Have the Crossbow forts shoot 10.000 bolts.");
         Locale.setString("SV_ACHIEVEMENT_SILENCEPLEASE_NAME","en","Silence please!");
         Locale.setString("SV_ACHIEVEMENT_SILENCEPLEASE_DESCRIPTION","en","Silence 70 spellcasters with the Spirit Totem.");
         Locale.setString("SV_ACHIEVEMENT_NOCOUNTRYFORWEAKMAN_NAME","en","Cull the weak");
         Locale.setString("SV_ACHIEVEMENT_NOCOUNTRYFORWEAKMAN_DESCRIPTION","en","Weaken 100 enemies with the Totem of Weakness.");
         Locale.setString("SV_ACHIEVEMENT_ANDSOITBEGINS_NAME","en","And so it begins");
         Locale.setString("SV_ACHIEVEMENT_ANDSOITBEGINS_DESCRIPTION","en","Complete Stage 1.");
         Locale.setString("SV_ACHIEVEMENT_ORGANICPROPULSION_NAME","en","Organic Impulse");
         Locale.setString("SV_ACHIEVEMENT_ORGANICPROPULSION_DESCRIPTION","en","Make a Desert Bantah move.");
         Locale.setString("SV_ACHIEVEMENT_ONEFROGGYEVENING_NAME","en","One Froggy Evening");
         Locale.setString("SV_ACHIEVEMENT_ONEFROGGYEVENING_DESCRIPTION","en","Find the singing frog.");
         Locale.setString("SV_ACHIEVEMENT_MUADIB_NAME","en","Mua’dib");
         Locale.setString("SV_ACHIEVEMENT_MUADIB_DESCRIPTION","en","Complete Campaign stage 4 without losing any soldiers to the Sandworm.");
         Locale.setString("SV_ACHIEVEMENT_STUFFOMAKER_NAME","en","Stuff ’o’ maker");
         Locale.setString("SV_ACHIEVEMENT_STUFFOMAKER_DESCRIPTION","en","Have a genie polymorph 10 enemies.");
         Locale.setString("SV_ACHIEVEMENT_SPLASH_NAME","en","Splash");
         Locale.setString("SV_ACHIEVEMENT_SPLASH_DESCRIPTION","en","Find a mermaid.");
         Locale.setString("SV_ACHIEVEMENT_THEBLACKPEARL_NAME","en","The Black Pearl");
         Locale.setString("SV_ACHIEVEMENT_THEBLACKPEARL_DESCRIPTION","en","Kill 30  enemies with the pirate ship\'s cannons.");
         Locale.setString("SV_ACHIEVEMENT_SOSTOTHEWORLD_NAME","en","SOS to the world");
         Locale.setString("SV_ACHIEVEMENT_SOSTOTHEWORLD_DESCRIPTION","en","Find the secret message.");
         Locale.setString("SV_ACHIEVEMENT_MONEYTALKS_NAME","en","Money talks");
         Locale.setString("SV_ACHIEVEMENT_MONEYTALKS_DESCRIPTION","en","Hire 10 or more mercenaries.");
         Locale.setString("SV_ACHIEVEMENT_TWISTANDSHOUT_NAME","en","Twist and shout");
         Locale.setString("SV_ACHIEVEMENT_TWISTANDSHOUT_DESCRIPTION","en","Have the Spear maidens perform 50 whirlwinds.");
         Locale.setString("SV_ACHIEVEMENT_YOUAREONEUGLYMOTHERFUCKER_NAME","en","One *ugly* $%@#");
         Locale.setString("SV_ACHIEVEMENT_YOUAREONEUGLYMOTHERFUCKER_DESCRIPTION","en","Find all 3 alien hunters.");
         Locale.setString("SV_ACHIEVEMENT_FEEDMESEYMOUR_NAME","en","Feed me, Seymour");
         Locale.setString("SV_ACHIEVEMENT_FEEDMESEYMOUR_DESCRIPTION","en","Feed over 50 creatures to the Snapvines.");
         Locale.setString("SV_ACHIEVEMENT_LANDMANAGER_NAME","en","Land manager");
         Locale.setString("SV_ACHIEVEMENT_LANDMANAGER_DESCRIPTION","en","Clean debris from 10 holders.");
         Locale.setString("SV_ACHIEVEMENT_THEWALKINGDEAD_NAME","en","The Walking Dead");
         Locale.setString("SV_ACHIEVEMENT_THEWALKINGDEAD_DESCRIPTION","en","Kill 100 Tribal zombies.");
         Locale.setString("SV_ACHIEVEMENT_ISTHATWILHELM_NAME","en","Is that Wilhelm?");
         Locale.setString("SV_ACHIEVEMENT_ISTHATWILHELM_DESCRIPTION","en","Defeat 10 climbing enemies.");
         Locale.setString("SV_ACHIEVEMENT_COLONIALMARINE_NAME","en","Colonial Marine");
         Locale.setString("SV_ACHIEVEMENT_COLONIALMARINE_DESCRIPTION","en","Kill 30 Parasytes or Reapers.");
         Locale.setString("SV_ACHIEVEMENT_LANDOWNER_NAME","en","Land Owner");
         Locale.setString("SV_ACHIEVEMENT_LANDOWNER_DESCRIPTION","en","Build on all holders on any given campaign stage.");
         Locale.setString("SV_ACHIEVEMENT_MUMMYATTHEGATES_NAME","en","Mummy at the Gates");
         Locale.setString("SV_ACHIEVEMENT_MUMMYATTHEGATES_DESCRIPTION","en","Kill a Sandwraith before it summons any Fallen.");
         Locale.setString("SV_ACHIEVEMENT_DIVIDEANDCONQUER_NAME","en","Divide and conquer");
         Locale.setString("SV_ACHIEVEMENT_DIVIDEANDCONQUER_DESCRIPTION","en","Build a specialist tower of each type on any stage.");
         Locale.setString("SV_ACHIEVEMENT_SANDWARRIOR_NAME","en","Sand Warrior");
         Locale.setString("SV_ACHIEVEMENT_SANDWARRIOR_DESCRIPTION","en","Complete a desert stage without the hero dying.");
         Locale.setString("SV_ACHIEVEMENT_TARZANBOY_NAME","en","Tarzan Boy");
         Locale.setString("SV_ACHIEVEMENT_TARZANBOY_DESCRIPTION","en","Complete a jungle stage without the hero dying.");
         Locale.setString("SV_ACHIEVEMENT_CAVEMAN_NAME","en","Caveman");
         Locale.setString("SV_ACHIEVEMENT_CAVEMAN_DESCRIPTION","en","Complete an underground stage without the hero dying.");
         Locale.setString("SV_ACHIEVEMENT_GENIEINABOTTLE_NAME","en","Genie in a Bottle");
         Locale.setString("SV_ACHIEVEMENT_GENIEINABOTTLE_DESCRIPTION","en","Defeat Nazeru, the red efreeti.");
         Locale.setString("SV_ACHIEVEMENT_KONGICIDE_NAME","en","Kongicide");
         Locale.setString("SV_ACHIEVEMENT_KONGICIDE_DESCRIPTION","en","Defeat Quincon, the Jungle King.");
         Locale.setString("SV_ACHIEVEMENT_YOUSHALLNOTPASS_NAME","en","You shall not pass!");
         Locale.setString("SV_ACHIEVEMENT_YOUSHALLNOTPASS_DESCRIPTION","en","Defeat the Dark Lord and save the realm!");
         Locale.setString("SV_ACHIEVEMENT_SAVETHEPRINCESS_NAME","en","Save the princess!");
         Locale.setString("SV_ACHIEVEMENT_SAVETHEPRINCESS_DESCRIPTION","en","Save a captive princess.");
         Locale.setString("SV_ACHIEVEMENT_DEFEAT_COMPLETE_HARD_NAME","en","Supreme Defender");
         Locale.setString("SV_ACHIEVEMENT_DEFEAT_COMPLETE_HARD_DESCRIPTION","en","Complete the campaign in Veteran mode.");
         Locale.setString("SV_ACHIEVEMENT_HERO_OF_THE_DAY_NAME","en","Hero of the Day");
         Locale.setString("SV_ACHIEVEMENT_HERO_OF_THE_DAY_DESCRIPTION","en","Level up any hero to level 5.");
         Locale.setString("SV_ACHIEVEMENT_LEGENDARY_NAME","en","Legen (wait for it) dary");
         Locale.setString("SV_ACHIEVEMENT_LEGENDARY_DESCRIPTION","en","Level up any hero to max level.");
         Locale.setString("SV_ACHIEVEMENT_INDIANAJONES_NAME","en","Dr. Henry Walton");
         Locale.setString("SV_ACHIEVEMENT_INDIANAJONES_DESCRIPTION","en","Help Indiana find the secret passage.");
         Locale.setString("SV_ACHIEVEMENT_HEROLEVELUP_NAME","en","Birth of a Hero");
         Locale.setString("SV_ACHIEVEMENT_HEROLEVELUP_DESCRIPTION","en","Level up any hero.");
         Locale.setString("MENU_BOTTOM_ATTACK_NAME","en","Attack");
         Locale.setString("MENU_BOTTOM_ATTACK_DESCRIPTION","en","Attack Damage");
         Locale.setString("MENU_BOTTOM_RELOAD_NAME","en","Reload Time");
         Locale.setString("MENU_BOTTOM_RELOAD_DESCRIPTION","en","Reload Time");
         Locale.setString("MENU_BOTTOM_RANGE_NAME","en","Range");
         Locale.setString("MENU_BOTTOM_RANGE_DESCRIPTION","en","Attack Range");
         Locale.setString("MENU_BOTTOM_HEALTH_SINGLE_NAME","en","Health");
         Locale.setString("MENU_BOTTOM_HEALTH_SINGLE_DESCRIPTION","en","Unit Health");
         Locale.setString("MENU_BOTTOM_HEALTH_NAME","en","Health");
         Locale.setString("MENU_BOTTOM_HEALTH_DESCRIPTION","en","Current Health / Total Health");
         Locale.setString("MENU_BOTTOM_ARMOR_NAME","en","Physical Armor");
         Locale.setString("MENU_BOTTOM_ARMOR_DESCRIPTION","en","Physical Armor");
         Locale.setString("MENU_BOTTOM_MAGIC_ARMOR_NAME","en","Magic Resistance");
         Locale.setString("MENU_BOTTOM_MAGIC_ARMOR_DESCRIPTION","en","Magic Resistance");
         Locale.setString("MENU_BOTTOM_RESPAWN_NAME","en","Respawn");
         Locale.setString("MENU_BOTTOM_RESPAWN_DESCRIPTION","en","Respawn Time");
         Locale.setString("MENU_BOTTOM_ARMOR_ENEMY_NAME","en","Armor Enemy");
         Locale.setString("MENU_BOTTOM_ARMOR_ENEMY_DESCRIPTION","en","Physical Armor");
         Locale.setString("MENU_BOTTOM_COST_NAME","en","Cost");
         Locale.setString("MENU_BOTTOM_COST_DESCRIPTION","en","Life cost if enemy escapes");
         Locale.setString("ENCYCLOPEDIA_ENEMY_HEALTH_NAME","en","Health");
         Locale.setString("ENCYCLOPEDIA_ENEMY_HEALTH_DESCRIPTION","en","Amount of damage a unit can withstand.");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ATTACK_NAME","en","Attack Damage");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ATTACK_DESCRIPTION","en","The amount of damage dealt per attack.");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ARMOR_NAME","en","Armor Rating");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ARMOR_DESCRIPTION","en","Armor reduces physical damage.");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ARMOR_MAGIC_NAME","en","Magic Resistance");
         Locale.setString("ENCYCLOPEDIA_ENEMY_ARMOR_MAGIC_DESCRIPTION","en","Magic resistance reduces magic damage.");
         Locale.setString("ENCYCLOPEDIA_ENEMY_SPEED_NAME","en","Speed");
         Locale.setString("ENCYCLOPEDIA_ENEMY_SPEED_DESCRIPTION","en","How quick the unit moves.");
         Locale.setString("ENCYCLOPEDIA_ENEMY_COST_NAME","en","Cost");
         Locale.setString("ENCYCLOPEDIA_ENEMY_COST_DESCRIPTION","en","How many lives are lost if the enemy gets through.");
         Locale.setString("ENCYCLOPEDIA_TOWER_ATTACK_NAME","en","Attack Damage");
         Locale.setString("ENCYCLOPEDIA_TOWER_ATTACK_DESCRIPTION","en","Damage it deals when attacking.");
         Locale.setString("ENCYCLOPEDIA_TOWER_RELOAD_NAME","en","Reload");
         Locale.setString("ENCYCLOPEDIA_TOWER_RELOAD_DESCRIPTION","en","Time between attacks.");
         Locale.setString("ENCYCLOPEDIA_TOWER_RANGE_NAME","en","Attack Range");
         Locale.setString("ENCYCLOPEDIA_TOWER_RANGE_DESCRIPTION","en","How far the tower can attack.");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_HEALTH_NAME","en","Health");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_HEALTH_DESCRIPTION","en","Amount of damage a unit can withstand.");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_ATTACK_NAME","en","Attack Damage");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_ATTACK_DESCRIPTION","en","The amount of damage dealt per attack.");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_ARMOR_NAME","en","Armor Rating");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_ARMOR_DESCRIPTION","en","Armor reduces physical damage.");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_RESPAWN_NAME","en","Training Time");
         Locale.setString("ENCYCLOPEDIA_TOWER_SOLDIER_RESPAWN_DESCRIPTION","en","Time it takes to train a new soldier.");
         Locale.setString("LEVEL_SELECT_TOOLTIP_WAVE_HEROIC_NAME","en","Waves");
         Locale.setString("LEVEL_SELECT_TOOLTIP_WAVE_HEROIC_DESCRIPTION","en","Six elite enemy waves.");
         Locale.setString("LEVEL_SELECT_TOOLTIP_WAVE_IRON_NAME","en","Waves");
         Locale.setString("LEVEL_SELECT_TOOLTIP_WAVE_IRON_DESCRIPTION","en","One super wave.");
         Locale.setString("LEVEL_SELECT_TOOLTIP_LIVES_NAME","en","Lives");
         Locale.setString("LEVEL_SELECT_TOOLTIP_LIVES_DESCRIPTION","en","Lives you start the challenge with.");
         Locale.setString("LEVEL_SELECT_TOOLTIP_UPGRADES_NAME","en","Global upgrades");
         Locale.setString("LEVEL_SELECT_TOOLTIP_UPGRADES_DESCRIPTION","en","Upgrades beyond this level are disabled in this challenge");
         Locale.setString("LEVEL_SELECT_TOOLTIP_TOWERS_NAME","en","Towers");
         Locale.setString("LEVEL_SELECT_TOOLTIP_TOWERS_DESCRIPTION","en","Towers you can or cannot build in this challenge.");
         Locale.setString("HERO_PALADIN_NAME","en","Sir Gerald");
         Locale.setString("HERO_RIFLEMAN_NAME","en","Bolin Farslayer");
         Locale.setString("HERO_ARCHER_NAME","en","Alleria Swiftwind");
         Locale.setString("HERO_REINFORCEMENT_NAME","en","Malik Hammerfury");
         Locale.setString("HERO_MAGE_NAME","en","Magnus Spellbane");
         Locale.setString("HERO_FIRE_NAME","en","Ignus");
         Locale.setString("HERO_ARCHER_WILDCAT_NAME","en","Wildcat");
         Locale.setString("HERO_MAGE_SHADOW_NAME","en","Magnus Shadow");
         Locale.setString("HERO_DENAS_NAME","en","King Denas");
         Locale.setString("HERO_SAND_WARRIOR_NAME","en","Sand Warrior");
         Locale.setString("HERO_PALADIN_DESCRIPTION","en","Defender of the righteous, punisher of the dark, protector of the innocent, crusher of evil beings, Gerald Lightseeker is the uncanny of Linirea\'s armed forces!");
         Locale.setString("HERO_RIFLEMAN_DESCRIPTION","en","Thunder and lightning have nothing on this crackshot!\nLet loose a hail of bullets, and make them fear where they step with an arsenal of mines!");
         Locale.setString("HERO_ARCHER_DESCRIPTION","en","Silent as the night, light as a feather and deadly beautiful. Too many have fallen by her charming gaze and many more by her fatal bow.");
         Locale.setString("HERO_REINFORCEMENT_DESCRIPTION","en","From a land far, far away, a Hero with unmatched strength, untamed mind, and unbroken will. A destructive force, an unleashed fury, a bullet train attitude!");
         Locale.setString("HERO_MAGE_DESCRIPTION","en","Unleash the arcane forces of Linirea, let loose a mystical storm, and spellbind your enemies! With his arcane arts and thirst for knowledge.");
         Locale.setString("HERO_FIRE_DESCRIPTION","en","Burn the kingdom\'s enemies with the blaze of a thousand stars! Forge victory in his raging flames, consuming evil in fire and brimstone!");
         Locale.setString("HERO_DENAS_DESCRIPTION","en","Your majesty itself brings an arsenal of power and courage to the battlefield. Long live the king!");
         Locale.setString("HERO_PALADIN_SPECIAL","en","Courage, Shield of Retribution");
         Locale.setString("HERO_RIFLEMAN_SPECIAL","en","Mine Layer, Tar Bomb");
         Locale.setString("HERO_ARCHER_SPECIAL","en","Multishot, Call of the Wild");
         Locale.setString("HERO_REINFORCEMENT_SPECIAL","en","Hammer Smash, Earthquake");
         Locale.setString("HERO_MAGE_SPECIAL","en","Mirage, Arcane Storm");
         Locale.setString("HERO_FIRE_SPECIAL","en","Surge of Flame, Flaming Frenzy");
         Locale.setString("HERO_DENAS_SPECIAL","en","Buff Towers, Catapult");
         Locale.setString("HERO_ALRIC_NAME","en","Alric");
         Locale.setString("HERO_MIRAGE_NAME","en","Mirage");
         Locale.setString("HERO_DWARF_NAME","en","Rurin Longbeard");
         Locale.setString("HERO_CAPTAIN_NAME","en","Capt. Blackthorne");
         Locale.setString("HERO_CRONAN_NAME","en","Cronan");
         Locale.setString("HERO_DIERDRE_NAME","en","Dierdre");
         Locale.setString("HERO_NIVUS_NAME","en","Nivus");
         Locale.setString("HERO_GRAWL_NAME","en","Grawl");
         Locale.setString("HERO_SHATRA_NAME","en","Sha\'Tra");
         Locale.setString("HERO_ASHBITE_NAME","en","Ashbite");
         Locale.setString("HERO_BEASTMASTER_BOAR_NAME","en","Wild Boar");
         Locale.setString("HERO_BEASTMASTER_FALCON_NAME","en","Falcon");
         Locale.setString("TOWER_BARRACKS_NAME","es","Barracas");
         Locale.setString("TOWER_BARRACKS_DESCRIPTION","es","Esta es la barracaaa del de mkombat");
         Locale.setString("TOWER_ARCHERS_NAME","es","Arqueros");
         Locale.setString("TOWER_ARCHERS_DESCRIPTION","es","Esta tira flechitas");
         Locale.setString("TOWER_ENGINEERS_NAME","es","Ingenieros");
         Locale.setString("TOWER_ENGINEERS_DESCRIPTION","es","Son los genieros que estan re in");
         Locale.setString("TOWER_MAGES_NAME","es","Magos");
         Locale.setString("TOWER_MAGES_DESCRIPTION","es","Esta es la torre de los magos viteh");
         Locale.setDefaultLang("en");
      }
      
      public function §_-hn§() : void
      {
         var _loc1_:§_-yD§ = null;
         this.§_-FU§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§_-Vz§)
         {
            _loc1_ = new §_-yD§();
            this.§_-FU§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §override class§() : void
      {
         var _loc1_:§implements const var§ = null;
         this.necromancerParticlesPool = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.necromancerParticlesMax)
         {
            _loc1_ = new §implements const var§();
            this.necromancerParticlesPool[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §_-MI§() : void
      {
         var _loc1_:§use get§ = null;
         this.§set for const§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§_-HM§)
         {
            _loc1_ = new §use get§();
            this.§set for const§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §_-cF§() : void
      {
         var _loc1_:§override const return§ = null;
         this.§function for function§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§var with§)
         {
            _loc1_ = new §override const return§();
            this.§function for function§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §_-IV§() : void
      {
         var _loc1_:§if for switch§ = null;
         this.§_-uS§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§const const dynamic§)
         {
            _loc1_ = new §if for switch§();
            this.§_-uS§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §_-fH§() : void
      {
         var _loc1_:§_-uD§ = null;
         this.§_-V4§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§_-LA§)
         {
            _loc1_ = new §_-uD§();
            this.§_-V4§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §try for for§() : void
      {
         var _loc1_:§get include§ = null;
         this.fireballParticlesPool = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.fireballParticlesMax)
         {
            _loc1_ = new §get include§();
            this.fireballParticlesPool[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §_-Zv§() : void
      {
         var _loc1_:§_-Kv§ = null;
         this.§_-R8§ = new Dictionary();
         var _loc2_:int = 0;
         while(_loc2_ < this.§in for throw§)
         {
            _loc1_ = new §_-Kv§();
            this.§_-R8§[_loc1_] = _loc1_;
            _loc2_++;
         }
      }
      
      public function §import§() : void
      {
         var _loc1_:int = 0;
         var _loc2_:* = undefined;
         var _loc3_:* = undefined;
         var _loc4_:* = undefined;
         var _loc5_:* = undefined;
         this.magicMissileParticlesAltPool = new Dictionary();
         this.magicMissileParticlesAPool = new Dictionary();
         this.magicMissileParticlesBPool = new Dictionary();
         this.magicMissileParticlesCPool = new Dictionary();
         _loc1_ = 0;
         while(_loc1_ < this.magicMissileParticlesMaxAlt)
         {
            _loc2_ = new §_-y§();
            this.magicMissileParticlesAltPool[_loc2_] = _loc2_;
            _loc1_++;
         }
         _loc1_ = 0;
         while(_loc1_ < this.magicMissileParticlesMaxTail)
         {
            _loc3_ = new §if const set§();
            this.magicMissileParticlesAPool[_loc3_] = _loc3_;
            _loc1_++;
         }
         _loc1_ = 0;
         while(_loc1_ < this.magicMissileParticlesMaxTail)
         {
            _loc4_ = new §_-Tr§();
            this.magicMissileParticlesBPool[_loc4_] = _loc4_;
            _loc1_++;
         }
         _loc1_ = 0;
         while(_loc1_ < this.magicMissileParticlesMaxTail)
         {
            _loc5_ = new §_-dR§();
            this.magicMissileParticlesCPool[_loc5_] = _loc5_;
            _loc1_++;
         }
      }
   }
}

