#!/usr/bin/env python3
"""Finish the V13 combined runtime's map, shared-system and sandbox UX.

This patch is intentionally applied to a fresh FFDec export of the exact V13
release.  It keeps both original campaign controllers alive, exposes their
native maps through a persistent switch bar, adds one shared systems hub and a
shared star wallet, repairs user-facing KR strings polluted by namespacing,
adds a clickable KR battle sandbox, extends safe speed tiers, and makes the
Frontiers final-stage Instant Win bypass the custom post-boss sequence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"{label}: start anchor missing")
    b = text.find(end, a)
    if b < 0:
        raise SystemExit(f"{label}: end anchor missing")
    return text[:a] + replacement + text[b:]


def patch_controller(text: str) -> str:
    if "ultimateSharedRuntimeV14" in text:
        return text
    text = once(
        text,
        "   import flash.display.DisplayObject;\n",
        "   import flash.display.*;\n   import flash.text.*;\n",
        "controller display/text imports",
    )
    text = once(
        text,
        "      public var ultimateNativeKRMain:Object;\n",
        """      public var ultimateNativeKRMain:Object;
      
      public var ultimateSharedRuntimeV14:Boolean = true;
      
      private var ultimateNativeKRMapActive:Boolean = false;
      
      private var ultimateNav:Sprite;
      
      private var ultimateHub:Sprite;
      
      private var ultimateSharedStars:int = -1;
      
      private var ultimateLastKRStars:int = -1;
      
      private var ultimateLastKRFStars:int = -1;
""",
        "shared runtime fields",
    )

    replacement = r'''      private function ultimateEnsureNativeKR() : void
      {
         if(this.ultimateNativeKRGame != null)
         {
            return;
         }
         this.ultimateNativeKRMain = new (getDefinitionByName("KR1__Defense") as Class)();
         this.ultimateNativeKRMain["_-5I"]();
         this.ultimateNativeKRMain["_-GL"]();
         this.ultimateNativeKRMain["_-1s"]();
         this.ultimateNativeKRMain["_-Q5"]();
         this.ultimateNativeKRGame = new (getDefinitionByName("KR1__Game") as Class)(this.ultimateNativeKRMain,"krultimate_slot1");
         this.ultimateNativeKRMain["addChildAt"](this.ultimateNativeKRGame,0);
         (this.ultimateNativeKRMain as DisplayObject).x = 50;
         this.ultimateLoadSharedStars();
         this.addEventListener(Event.ENTER_FRAME,this.ultimateMonitorNativeKR,false,0,true);
      }

      private function ultimateLoadSharedStars() : void
      {
         if(this.ultimateNativeKRGame == null || this.ultimateSharedStars >= 0)
         {
            return;
         }
         var so:SharedObject = null;
         try
         {
            so = SharedObject.getLocal("kingdomRushUltimateSharedV14");
            if(so.data.stars != undefined)
            {
               this.ultimateSharedStars = Math.max(0,int(so.data.stars));
            }
            so.close();
         }
         catch(errorLoad:Error)
         {
         }
         if(this.ultimateSharedStars < 0)
         {
            this.ultimateSharedStars = Math.max(0,int(this.stars) + int(this.ultimateNativeKRGame["stars"]));
         }
         this.stars = this.ultimateSharedStars;
         this.ultimateNativeKRGame["stars"] = this.ultimateSharedStars;
         this.ultimateLastKRFStars = this.stars;
         this.ultimateLastKRStars = int(this.ultimateNativeKRGame["stars"]);
         this.ultimateSaveSharedStars();
      }

      private function ultimateSaveSharedStars() : void
      {
         var so:SharedObject = null;
         try
         {
            so = SharedObject.getLocal("kingdomRushUltimateSharedV14");
            so.data.stars = this.ultimateSharedStars;
            so.flush();
            so.close();
         }
         catch(errorSave:Error)
         {
         }
      }

      private function ultimateSyncSharedStars() : void
      {
         if(this.ultimateNativeKRGame == null)
         {
            return;
         }
         this.ultimateLoadSharedStars();
         var krStars:int = Math.max(0,int(this.ultimateNativeKRGame["stars"]));
         var krfStars:int = Math.max(0,int(this.stars));
         if(this.ultimateLastKRStars >= 0 && krStars != this.ultimateLastKRStars)
         {
            this.ultimateSharedStars = Math.max(0,this.ultimateSharedStars + krStars - this.ultimateLastKRStars);
         }
         else if(this.ultimateLastKRFStars >= 0 && krfStars != this.ultimateLastKRFStars)
         {
            this.ultimateSharedStars = Math.max(0,this.ultimateSharedStars + krfStars - this.ultimateLastKRFStars);
         }
         this.stars = this.ultimateSharedStars;
         this.ultimateNativeKRGame["stars"] = this.ultimateSharedStars;
         this.ultimateLastKRFStars = this.ultimateSharedStars;
         this.ultimateLastKRStars = this.ultimateSharedStars;
         this.ultimateSaveSharedStars();
      }

      private function ultimateText(param1:String, param2:Number, param3:Number, param4:Number, param5:Number, param6:int = 14, param7:uint = 16777215) : TextField
      {
         var text:TextField = new TextField();
         text.defaultTextFormat = new TextFormat("_sans",param6,param7,true);
         text.text = param1;
         text.x = param2;
         text.y = param3;
         text.width = param4;
         text.height = param5;
         text.selectable = false;
         text.mouseEnabled = false;
         return text;
      }

      private function ultimateButton(param1:String, param2:Number, param3:Number, param4:Number, param5:Number, param6:String) : Sprite
      {
         var button:Sprite = new Sprite();
         button.name = param6;
         button.x = param2;
         button.y = param3;
         button.graphics.beginFill(1710618,0.97);
         button.graphics.lineStyle(1,15647579,0.9);
         button.graphics.drawRoundRect(0,0,param4,param5,9,9);
         button.graphics.endFill();
         button.addChild(this.ultimateText(param1,8,6,param4 - 16,param5 - 8,12));
         button.buttonMode = true;
         button.mouseChildren = false;
         button.addEventListener(MouseEvent.CLICK,this.ultimateNavClick,false,0,true);
         return button;
      }

      private function ultimateInstallNav() : void
      {
         if(this.ultimateNav == null)
         {
            this.ultimateNav = new Sprite();
            this.ultimateNav.x = 238;
            this.ultimateNav.y = 6;
            this.ultimateNav.addChild(this.ultimateButton("KR MAP",0,0,100,32,"ultimate_map_kr"));
            this.ultimateNav.addChild(this.ultimateButton("KRF MAP",106,0,100,32,"ultimate_map_krf"));
            this.ultimateNav.addChild(this.ultimateButton("SHARED HUB",212,0,118,32,"ultimate_hub"));
         }
         if(this.ultimateNav.parent != this)
         {
            this.addChild(this.ultimateNav);
         }
         else
         {
            this.setChildIndex(this.ultimateNav,this.numChildren - 1);
         }
      }

      private function ultimateSetNavVisible(param1:Boolean) : void
      {
         this.ultimateInstallNav();
         this.ultimateNav.visible = param1;
         if(!param1)
         {
            this.ultimateCloseHub();
         }
      }

      public function ultimateShowKRMap() : void
      {
         this.ultimateCloseHub();
         this.ultimateEnsureNativeKR();
         this.ultimateSyncSharedStars();
         if(this.ultimateNativeKRGame["map"] == null)
         {
            this.ultimateNativeKRGame["_-IL"](null);
         }
         if((this.ultimateNativeKRMain as DisplayObject).parent != this)
         {
            this.addChild(this.ultimateNativeKRMain as DisplayObject);
         }
         if(this.§_-6X§ != null)
         {
            this.§_-6X§.visible = false;
         }
         this.ultimateNativeKRMapActive = true;
         this.ultimateSetNavVisible(true);
      }

      public function ultimateShowKRFMap() : void
      {
         this.ultimateCloseHub();
         this.ultimateSyncSharedStars();
         if(this.ultimateNativeKRMain != null && (this.ultimateNativeKRMain as DisplayObject).parent == this)
         {
            this.removeChild(this.ultimateNativeKRMain as DisplayObject);
         }
         if(this.§_-6X§ != null)
         {
            this.§_-6X§.visible = true;
         }
         this.ultimateNativeKRMapActive = false;
         this.ultimateSetNavVisible(true);
      }

      private function ultimateCloseHub() : void
      {
         if(this.ultimateHub != null && this.ultimateHub.parent != null)
         {
            this.ultimateHub.parent.removeChild(this.ultimateHub);
         }
         this.ultimateHub = null;
      }

      private function ultimateRenderHub() : void
      {
         this.ultimateEnsureNativeKR();
         this.ultimateSyncSharedStars();
         this.ultimateCloseHub();
         var panel:Sprite = new Sprite();
         panel.x = 55;
         panel.y = 50;
         panel.graphics.beginFill(592137,0.985);
         panel.graphics.lineStyle(2,15647579,0.95);
         panel.graphics.drawRoundRect(0,0,690,470,17,17);
         panel.graphics.endFill();
         panel.addChild(this.ultimateText("KINGDOM RUSH ULTIMATE — SHARED SYSTEMS",22,14,645,30,20,15647579));
         panel.addChild(this.ultimateText("One star wallet across both upgrade trees: " + this.ultimateSharedStars + " available",22,47,645,22,14,14540253));
         panel.addChild(this.ultimateText("Choose either campaign's native screen below. Selections and progress stay saved when maps switch.",22,70,645,25,12,12566463));
         panel.addChild(this.ultimateText("KINGDOM RUSH",30,108,285,25,16,15647579));
         panel.addChild(this.ultimateText("FRONTIERS",376,108,285,25,16,7531748));
         panel.addChild(this.ultimateButton("KR HERO ROOM",25,140,300,42,"ultimate_sys_kr_hero"));
         panel.addChild(this.ultimateButton("KRF HERO ROOM",365,140,300,42,"ultimate_sys_krf_hero"));
         panel.addChild(this.ultimateButton("KR STAR UPGRADES",25,191,300,42,"ultimate_sys_kr_upgrades"));
         panel.addChild(this.ultimateButton("KRF STAR UPGRADES",365,191,300,42,"ultimate_sys_krf_upgrades"));
         panel.addChild(this.ultimateButton("KR ACHIEVEMENTS",25,242,300,42,"ultimate_sys_kr_achievements"));
         panel.addChild(this.ultimateButton("KRF ACHIEVEMENTS",365,242,300,42,"ultimate_sys_krf_achievements"));
         panel.addChild(this.ultimateButton("KR ENCYCLOPEDIA",25,293,300,42,"ultimate_sys_kr_encyclopedia"));
         panel.addChild(this.ultimateButton("KRF ENCYCLOPEDIA",365,293,300,42,"ultimate_sys_krf_encyclopedia"));
         panel.addChild(this.ultimateText("SANDBOX + SPEED",25,353,200,22,14,15647579));
         panel.addChild(this.ultimateText("Clickable panels in both games · adaptive 1×/2×/4×/8×/12× speed · immediate Instant Win.",25,377,640,48,12,14540253));
         panel.addChild(this.ultimateButton("CLOSE",245,430,200,32,"ultimate_hub_close"));
         this.ultimateHub = panel;
         this.addChild(panel);
         this.ultimateInstallNav();
      }

      private function ultimateOpenKRSystem(param1:String) : void
      {
         this.ultimateShowKRMap();
         var map:Object = this.ultimateNativeKRGame["map"];
         if(map != null)
         {
            map[param1](null);
         }
         this.ultimateInstallNav();
      }

      private function ultimateOpenKRFSystem(param1:String) : void
      {
         this.ultimateShowKRFMap();
         if(this.§_-6X§ != null)
         {
            this.§_-6X§[param1](null);
         }
         this.ultimateInstallNav();
      }

      private function ultimateNavClick(param1:MouseEvent) : void
      {
         var action:String = Sprite(param1.currentTarget).name;
         if(action == "ultimate_map_kr") this.ultimateShowKRMap();
         else if(action == "ultimate_map_krf") this.ultimateShowKRFMap();
         else if(action == "ultimate_hub") this.ultimateRenderHub();
         else if(action == "ultimate_hub_close") this.ultimateCloseHub();
         else if(action == "ultimate_sys_kr_hero") this.ultimateOpenKRSystem("§_-Nq§");
         else if(action == "ultimate_sys_kr_upgrades") this.ultimateOpenKRSystem("clickUpgrades");
         else if(action == "ultimate_sys_kr_achievements") this.ultimateOpenKRSystem("clickAchievements");
         else if(action == "ultimate_sys_kr_encyclopedia") this.ultimateOpenKRSystem("clickEncyclopedia");
         else if(action == "ultimate_sys_krf_hero") this.ultimateOpenKRFSystem("§_-WS§");
         else if(action == "ultimate_sys_krf_upgrades") this.ultimateOpenKRFSystem("clickUpgrades");
         else if(action == "ultimate_sys_krf_achievements") this.ultimateOpenKRFSystem("§_-EN§");
         else if(action == "ultimate_sys_krf_encyclopedia") this.ultimateOpenKRFSystem("§_-Br§");
      }

      public function ultimateStartStage(param1:String, param2:String, param3:int, param4:int = 0, param5:Boolean = false, param6:String = "kr1") : void
      {
         this.ultimateStageId = param2;
         this.ultimateStageGame = param6;
         this.ultimateSourceLevel = param3;
         this.currentLevel = param3;
         this.ultimateCloseHub();
         this.ultimateSetNavVisible(false);
         if(param6 == "kr1")
         {
            this.ultimateEnsureNativeKR();
            if(this.ultimateNativeKRGame["map"] != null)
            {
               this.ultimateNativeKRGame["_-Ax"]();
            }
            this.ultimateNativeKRGame["startLevel"](param3,param4);
            if((this.ultimateNativeKRMain as DisplayObject).parent != this)
            {
               this.addChild(this.ultimateNativeKRMain as DisplayObject);
            }
            this.ultimateNativeKRMapActive = true;
            return;
         }
         var levelClass:Class = getDefinitionByName(param1) as Class;
         if(levelClass != null)
         {
            this.addChildAt(new levelClass(this,param4,param5),0);
         }
      }

      private function ultimateMonitorNativeKR(param1:Event) : void
      {
         if(this.ultimateNativeKRGame == null)
         {
            return;
         }
         this.ultimateSyncSharedStars();
         if(this.ultimateNativeKRMapActive)
         {
            this.ultimateSetNavVisible(this.ultimateNativeKRGame["map"] != null);
         }
      }

'''
    text = between(
        text,
        "      public function ultimateStartStage(",
        "      public function ultimateKrfMainStageId(",
        replacement,
        "persistent KR controller and shared hub",
    )
    text = once(
        text,
        "         this.addChildAt(new _loc19_(this,param2,param3),0);\n",
        "         this.ultimateCloseHub();\n         this.ultimateSetNavVisible(false);\n         this.addChildAt(new _loc19_(this,param2,param3),0);\n",
        "hide nav for native KRF stage",
    )
    text = once(
        text,
        "         this.§_-6X§ = new §class const for§(this);\n         this.addChild(this.§_-6X§);\n",
        "         this.§_-6X§ = new §class const for§(this);\n         this.addChild(this.§_-6X§);\n         this.ultimateNativeKRMapActive = false;\n         this.ultimateSetNavVisible(true);\n",
        "show nav on KRF map",
    )
    return text


def patch_krf_map(text: str) -> str:
    if 'ultimateMakeButton("KR MAP"' in text:
        return text
    text = once(
        text,
        'this.ultimateMakeButton("ULTIMATE",690,500,96,40,"ultimate_open")',
        'this.ultimateMakeButton("KR MAP",690,500,96,40,"ultimate_open")',
        "replace stage selector label",
    )
    text = once(
        text,
        '''         if(action == "ultimate_open")
         {
            this.ultimateCampaignPage = 0;
            this.ultimateRenderCampaignPanel();
            return;
         }
''',
        '''         if(action == "ultimate_open")
         {
            this.ultimateCloseCampaignPanel();
            this.game.ultimateShowKRMap();
            return;
         }
''',
        "replace selector opening with native KR map switch",
    )
    return text


def patch_kr_level(text: str) -> str:
    if "ultimateKRSandboxV14" in text:
        return text
    text = once(
        text,
        "   import flash.text.TextField;" if "   import flash.text.TextField;" in text else "   import flash.ui.Keyboard;\n",
        "   import flash.text.TextField;" if "   import flash.text.TextField;" in text else "   import flash.text.*;\n   import flash.ui.Keyboard;\n",
        "KR level text import",
    )
    # The branch above is deliberately idempotent for exports that already
    # contain explicit text imports.  Fresh V13 enters the second arm.
    text = once(
        text,
        "      public var mode:int;\n",
        """      public static var ultimateSpeed:int = 1;
      
      public var ultimateKRSandboxV14:Boolean = true;
      
      private var ultimateSandboxButton:Sprite;
      
      private var ultimateSandboxPanel:Sprite;
      
      public var ultimateSandboxCommitted:Boolean = false;
      
      public var mode:int;
""",
        "KR sandbox fields",
    )
    text = once(
        text,
        "         this.loadGrid();\n         this.addEventListener(Event.DEACTIVATE,this.onDeactivate,false,0,true);\n",
        "         this.loadGrid();\n         this.ultimateInstallSandbox();\n         this.addEventListener(Event.DEACTIVATE,this.onDeactivate,false,0,true);\n",
        "install KR sandbox",
    )
    methods = r'''      private function ultimateSandboxText(param1:String, param2:Number, param3:Number, param4:Number, param5:Number, param6:int = 12) : TextField
      {
         var text:TextField = new TextField();
         text.defaultTextFormat = new TextFormat("_sans",param6,16777215,true);
         text.text = param1;
         text.x = param2;
         text.y = param3;
         text.width = param4;
         text.height = param5;
         text.selectable = false;
         text.mouseEnabled = false;
         return text;
      }

      private function ultimateSandboxMakeButton(param1:String, param2:Number, param3:Number, param4:Number, param5:String) : Sprite
      {
         var button:Sprite = new Sprite();
         button.name = param5;
         button.x = param2;
         button.y = param3;
         button.graphics.beginFill(1710618,0.97);
         button.graphics.lineStyle(1,15647579,0.9);
         button.graphics.drawRoundRect(0,0,param4,34,8,8);
         button.graphics.endFill();
         button.addChild(this.ultimateSandboxText(param1,7,7,param4 - 14,22,11));
         button.buttonMode = true;
         button.mouseChildren = false;
         button.addEventListener(MouseEvent.CLICK,this.ultimateSandboxClick,false,0,true);
         return button;
      }

      private function ultimateInstallSandbox() : void
      {
         this.ultimateSandboxButton = this.ultimateSandboxMakeButton("SANDBOX",684,8,108,"ultimate_sandbox_toggle");
         this.gui.addChild(this.ultimateSandboxButton);
      }

      private function ultimateCloseSandbox() : void
      {
         if(this.ultimateSandboxPanel != null && this.ultimateSandboxPanel.parent != null)
         {
            this.ultimateSandboxPanel.parent.removeChild(this.ultimateSandboxPanel);
         }
         this.ultimateSandboxPanel = null;
      }

      private function ultimateRenderSandbox() : void
      {
         this.ultimateCloseSandbox();
         var panel:Sprite = new Sprite();
         panel.x = 528;
         panel.y = 48;
         panel.graphics.beginFill(526344,0.975);
         panel.graphics.lineStyle(2,15647579,0.95);
         panel.graphics.drawRoundRect(0,0,262,270,13,13);
         panel.graphics.endFill();
         panel.addChild(this.ultimateSandboxText("KR SANDBOX",14,10,230,25,16));
         panel.addChild(this.ultimateSandboxText("Speed " + KR1__Level.ultimateSpeed + "× — adaptive under heavy load",14,38,230,22,11));
         panel.addChild(this.ultimateSandboxMakeButton("SPEED: " + KR1__Level.ultimateSpeed + "×",12,69,238,"ultimate_speed"));
         panel.addChild(this.ultimateSandboxMakeButton("+ 1,000 GOLD",12,109,114,"ultimate_gold"));
         panel.addChild(this.ultimateSandboxMakeButton("+ 10 LIVES",136,109,114,"ultimate_lives"));
         panel.addChild(this.ultimateSandboxMakeButton("INSTANT WIN",12,149,238,"ultimate_win"));
         panel.addChild(this.ultimateSandboxText("Instant Win uses the normal victory/save screen. Map progression, stars and achievements remain intact.",14,191,230,45,11));
         panel.addChild(this.ultimateSandboxMakeButton("CLOSE",72,231,118,"ultimate_close"));
         this.ultimateSandboxPanel = panel;
         this.gui.addChild(panel);
      }

      private function ultimateSandboxClick(param1:MouseEvent) : void
      {
         var action:String = Sprite(param1.currentTarget).name;
         if(action == "ultimate_sandbox_toggle")
         {
            if(this.ultimateSandboxPanel == null) this.ultimateRenderSandbox(); else this.ultimateCloseSandbox();
            return;
         }
         if(action == "ultimate_close") this.ultimateCloseSandbox();
         else if(action == "ultimate_gold") { this.updateCash(1000); this.ultimateRenderSandbox(); }
         else if(action == "ultimate_lives") { this.lives += 10; this.hud.updateLives(this.lives); this.ultimateRenderSandbox(); }
         else if(action == "ultimate_speed")
         {
            KR1__Level.ultimateSpeed = KR1__Level.ultimateSpeed == 1 ? 2 : (KR1__Level.ultimateSpeed == 2 ? 4 : (KR1__Level.ultimateSpeed == 4 ? 8 : (KR1__Level.ultimateSpeed == 8 ? 12 : 1)));
            this.ultimateRenderSandbox();
         }
         else if(action == "ultimate_win") this.ultimateInstantWin();
      }

      private function ultimateInstantWin() : void
      {
         if(this.ultimateSandboxCommitted || this.§_-7D§ == LEVEL_WIN)
         {
            return;
         }
         this.ultimateSandboxCommitted = true;
         this.ultimateCloseSandbox();
         this.indexWaves = this.waves == null ? this.indexWaves : this.waves.length;
         this.activeWaves = new Dictionary(true);
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.onPreWin();
         this.checkLevelAchievements();
         this.§_-7D§ = LEVEL_WIN;
         this.addMenuVictory();
      }

      private function ultimateExtraSpeedTicks() : void
      {
         var requested:int = KR1__Level.ultimateSpeed;
         var load:int = this.entities == null || this.bullets == null ? 0 : this.entities.numChildren + this.bullets.numChildren;
         var effective:int = load > 420 ? Math.min(requested,2) : (load > 260 ? Math.min(requested,4) : (load > 150 ? Math.min(requested,8) : requested));
         var tick:int = 1;
         while(tick < effective && (this.§_-7D§ == LEVEL_NORMAL || this.§_-7D§ == LEVEL_PRE_WIN))
         {
            if(this.§_-7D§ == LEVEL_NORMAL) this.§_-Ad§();
            this.updateEntities();
            this.updateBullets();
            if((tick & 1) == 0 || load < 150)
            {
               this.updateBulletsDecals();
               this.updateDecals();
               this.updateBackground();
               this.§_-Bw§();
            }
            this.menu.updateMenu();
            this.notificationHolder.update();
            tick++;
         }
      }

'''
    text = once(
        text,
        "      public function loadGrid() : void\n",
        methods + "      public function loadGrid() : void\n",
        "KR sandbox methods",
    )
    text = once(
        text,
        "               this.updatePointers();\n            }\n            if(this.§_-7D§ == LEVEL_PRE_WIN)\n",
        "               this.updatePointers();\n               this.ultimateExtraSpeedTicks();\n            }\n            if(this.§_-7D§ == LEVEL_PRE_WIN)\n",
        "KR extra speed ticks",
    )
    return text


def sanitize_kr_locale(text: str) -> tuple[str, int]:
    pattern = re.compile(r'(KR1__Locale\.setString\("(?:[^"\\]|\\.)*","(?:[^"\\]|\\.)*",")((?:[^"\\]|\\.)*)("\);)')
    count = 0

    def clean(match: re.Match[str]) -> str:
        nonlocal count
        value = match.group(2)
        if "KR1__" not in value:
            return match.group(0)
        count += value.count("KR1__")
        return match.group(1) + value.replace("KR1__", "") + match.group(3)

    return pattern.sub(clean, text), count


def patch_krf_level(text: str) -> str:
    if "qolInstantWinCommitted" not in text:
        text = once(
            text,
            "      private var qolSendAllAfterMenu:Boolean = false;\n",
            "      private var qolSendAllAfterMenu:Boolean = false;\n      \n      public var qolInstantWinCommitted:Boolean = false;\n",
            "Frontiers Instant Win guard",
        )
    old = '''      private function qolInstantWin() : void
      {
         this.qolUnlimitedMode = false;
         this.qolSendAllPending = false;
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.qolHideSettings();
         this.§_-BF§ = LEVEL_PRE_WIN;
         this.onPreWin();
         this.§try each§();
      }
'''
    new = '''      private function qolInstantWin() : void
      {
         if(this.qolInstantWinCommitted || this.§_-BF§ == LEVEL_WIN)
         {
            return;
         }
         this.qolInstantWinCommitted = true;
         this.qolUnlimitedMode = false;
         this.qolSendAllPending = false;
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.qolHideSettings();
         if(this is Level15)
         {
            Level15(this).qolInstantWinFinalStage();
            return;
         }
         this.onPreWin();
         this.§try each§();
         this.§_-BF§ = LEVEL_WIN;
         this.§_-pp§();
         this.§super const finally§();
      }
'''
    if old in text:
        text = once(text, old, new, "safe Frontiers Instant Win")

    # Five requested tiers.  The actual simulation budget is reduced under
    # extreme entity/effect load, keeping input and teardown responsive.
    text = text.replace(
        "Level.qolSpeed = Level.qolSpeed == 1 ? 3 : 1;",
        "Level.qolSpeed = Level.qolSpeed == 1 ? 2 : (Level.qolSpeed == 2 ? 4 : (Level.qolSpeed == 4 ? 8 : (Level.qolSpeed == 8 ? 12 : 1)));",
    )
    text = text.replace('Level.qolSpeed == 3 ? "3x" : "1x"', 'Level.qolSpeed + "x"')
    text = text.replace('(Level.qolSpeed == 3 ? "3x" : "1x")', '(Level.qolSpeed + "x")')
    text = text.replace("Level.qolSpeed = 3;", "Level.qolSpeed = 4;")
    text = once(
        text,
        "         var qolTick:int = 0;\n",
        "         var qolTick:int = 0;\n         var qolEffectiveSpeed:int = Level.qolSpeed;\n",
        "Frontiers effective speed local",
    )
    text = once(
        text,
        "            qolTick = 0;\n            while(qolTick < Level.qolSpeed && (this.§_-BF§ == LEVEL_NORMAL || this.§_-BF§ == LEVEL_PRE_WIN))\n",
        "            qolEffectiveSpeed = this.entities.numChildren > this.qolUltraEntities || this.bullets.numChildren > this.qolUltraBullets ? Math.min(Level.qolSpeed,2) : (this.entities.numChildren > this.qolExtremeEntities || this.bullets.numChildren > this.qolExtremeBullets ? Math.min(Level.qolSpeed,4) : (this.entities.numChildren > this.qolHeavyEntities || this.bullets.numChildren > this.qolHeavyBullets ? Math.min(Level.qolSpeed,8) : Level.qolSpeed));\n            qolTick = 0;\n            while(qolTick < qolEffectiveSpeed && (this.§_-BF§ == LEVEL_NORMAL || this.§_-BF§ == LEVEL_PRE_WIN))\n",
        "Frontiers adaptive speed budget",
    )
    text = text.replace("this.§_-WR§ += Level.qolSpeed;", "this.§_-WR§ += qolEffectiveSpeed;")
    return text


def patch_level15(text: str) -> str:
    if "qolInstantWinFinalStage" in text:
        return text
    method = '''      public function qolInstantWinFinalStage() : void
      {
         this.qolV12PostBossStarted = true;
         this.qolV12PostBossComplete = true;
         Level15.qolV12PostBossActive = false;
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.onPreWin();
         this.§try each§();
         this.§_-BF§ = LEVEL_WIN;
         this.§_-pp§();
         this.§super const finally§();
      }
      
'''
    return once(text, "      override public function onPreWin() : void\n", method + "      override public function onPreWin() : void\n", "final-stage Instant Win bypass")


def patch_kr_victory(text: str) -> str:
    if "ultimateSandboxCommitted" in text:
        return text
    return once(
        text,
        "         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);\n",
        """         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);
         if(this.§_-9c§.ultimateSandboxCommitted)
         {
            this.gotoAndStop(99);
            this.starsEnded = true;
            this.§_-2I§ = 99;
         }
""",
        "instant KR victory screen",
    )


def patch_krf_victory(text: str) -> str:
    if "qolInstantWinCommitted" in text:
        return text
    return once(
        text,
        "         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);\n",
        """         this.addEventListener(Event.ENTER_FRAME,this.eFrameEvents,false,0,true);
         if(this.cRoot.qolInstantWinCommitted)
         {
            this.gotoAndStop(99);
            this.§_-NK§ = true;
            this.§_-tM§ = 99;
         }
""",
        "instant Frontiers victory screen",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.scripts

    controller = root / "§_-BQ§.as"
    krf_map = root / "§class const for§.as"
    kr_level = root / "KR1__Level.as"
    kr_defense = root / "KR1__Defense.as"
    krf_level = root / "Level.as"
    level15 = root / "Level15.as"
    kr_victory = root / "KR1__MenuVictory.as"
    krf_victory = root / "§override const static§.as"

    write(controller, patch_controller(read(controller)))
    write(krf_map, patch_krf_map(read(krf_map)))
    write(kr_level, patch_kr_level(read(kr_level)))
    defense, sanitized = sanitize_kr_locale(read(kr_defense))
    write(kr_defense, defense)
    write(krf_level, patch_krf_level(read(krf_level)))
    write(level15, patch_level15(read(level15)))
    write(kr_victory, patch_kr_victory(read(kr_victory)))
    write(krf_victory, patch_krf_victory(read(krf_victory)))

    checks = {
        controller: ["ultimateSharedRuntimeV14", "ultimateShowKRMap", "kingdomRushUltimateSharedV14", "KR HERO ROOM"],
        krf_map: ['ultimateMakeButton("KR MAP"', "this.game.ultimateShowKRMap()"],
        kr_level: ["ultimateKRSandboxV14", "ultimateExtraSpeedTicks", "INSTANT WIN"],
        krf_level: ["qolInstantWinCommitted", "qolEffectiveSpeed", "Level15(this).qolInstantWinFinalStage()"],
        level15: ["qolInstantWinFinalStage", "qolV12PostBossComplete = true"],
        kr_victory: ["ultimateSandboxCommitted", "gotoAndStop(99)"],
        krf_victory: ["qolInstantWinCommitted", "gotoAndStop(99)"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path.name}")
    if "KR1__Locale.setString" not in defense or re.search(r'KR1__Locale\.setString\([^\n]*"[^"\n]*KR1__', defense):
        raise SystemExit("KR locale sanitization incomplete")

    report = {
        "version": "14",
        "native_map_switch": True,
        "shared_star_wallet": True,
        "shared_system_hub": ["heroes", "upgrades", "achievements", "encyclopedia"],
        "kr_clickable_sandbox": True,
        "speed_tiers": [1, 2, 4, 8, 12],
        "adaptive_speed_budget": True,
        "final_stage_instant_win_normal_teardown": True,
        "kr_locale_prefixes_removed": sanitized,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
