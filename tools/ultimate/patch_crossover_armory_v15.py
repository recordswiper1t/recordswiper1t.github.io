#!/usr/bin/env python3
"""Kingdom Rush Ultimate V15 native sandbox and real crossover guest armory.

The two campaigns retain their native simulation cores.  Selected towers and
heroes from the other campaign run in an explicit guest-combat mode: the real
linked character/tower timeline is instantiated, moves or attacks inside the
host level, and damages the host campaign's live enemy objects through their
shared dynamic damage contract.  Native instances continue down their original
code paths unchanged.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


KRF_TOWERS = [
    ("crossbow", "Crossbow Fort", "TowerArcherCrossbow"),
    ("totem", "Tribal Axethrowers", "TowerArcherTotem"),
    ("templar", "Knights Templar", "TowerSoldierTemplar"),
    ("assassin", "Assassin's Guild", "TowerSoldierAssassin"),
    ("archmage", "Archmage Tower", "TowerMageArchmage"),
    ("necromancer", "Necromancer Tower", "TowerMageNecromancer"),
    ("dwaarp", "DWAARP", "TowerEngineerDwaarp"),
    ("mecha", "Battle-Mecha T200", "TowerEngineerMech"),
]

KR_TOWERS = [
    ("rangers", "Rangers Hideout", "KR1__TowerArcherRanger"),
    ("musketeer", "Musketeer Garrison", "KR1__TowerArcherMusketeer"),
    ("paladin", "Holy Order", "KR1__TowerSoldierPaladin"),
    ("barbarian", "Barbarian Hall", "KR1__TowerSoldierBarbarian"),
    ("arcane", "Arcane Wizard", "KR1__TowerMageArcane"),
    ("sorcerer", "Sorcerer Mage", "KR1__TowerMageSorcerer"),
    ("tesla", "Tesla x104", "KR1__TowerEngineerTesla"),
    ("bertha", "500mm Big Bertha", "KR1__TowerEngineerBfg"),
]

KRF_HEROES = [
    ("alric", "Alric", "SoldierHeroAlric"),
    ("mirage", "Mirage", "SoldierHeroMirage"),
    ("captain", "Blackthorne", "SoldierHeroCaptain"),
    ("cronan", "Cronan", "SoldierHeroCronan"),
    ("shatra", "Sha'tra", "SoldierHeroAlien"),
    ("grawl", "Grawl", "§else const static§"),
    ("nivus", "Nivus", "SoldierHeroNivus"),
    ("dierdre", "Dierdre", "SoldierHeroDierdre"),
    ("ashbite", "Ashbite", "SoldierHeroDragon"),
    ("rurin", "Rurin", "§switch for super§"),
]

KR_HEROES = [
    ("gerald", "Gerald", "KR1__SoldierHeroGerald"),
    ("alleria", "Alleria", "KR1__SoldierHeroAlleria"),
    ("malik", "Malik", "KR1__SoldierHeroMalik"),
    ("bolin", "Bolin", "KR1__SoldierHeroBolin"),
    ("magnus", "Magnus", "KR1__SoldierHeroMagnus"),
    ("ignus", "Ignus", "KR1__SoldierHeroIgnus"),
    ("denas", "King Denas", "KR1__SoldierHeroDenas"),
    ("elora", "Elora", "KR1__SoldierHeroFrost"),
    ("ingvar", "Ingvar", "KR1__SoldierHeroViking"),
]


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


def insert_function_guard(text: str, signature: str, guard: str) -> str:
    pattern = re.compile(re.escape(signature) + r"\s*\{\n")
    return pattern.sub(lambda m: m.group(0) + guard, text)


def patch_pause_guards(text: str) -> str:
    pattern = re.compile(r"((?:override\s+)?public function (?:pause|unPause)\(\) : void\s*\{\n)")
    return pattern.sub(r"\1         if(this.ultimateGuestRoot != null) { this.stop(); return; }\n", text)


def patch_tower_base(text: str, kr: bool) -> str:
    if "ultimateGuestTowerV15" in text:
        return text
    root_field = "      public var §_-9c§:KR1__Level;\n" if kr else "      public var cRoot:Level;\n"
    fields = root_field + r'''
      public var ultimateGuestTowerV15:Boolean = true;

      public var ultimateGuestRoot:Object = null;

      public var ultimateGuestKind:String = "";

      private var ultimateGuestCooldown:int = 0;
'''
    text = once(text, root_field, fields, "guest tower fields")
    marker = "      public function onFrameUpdate() : void\n"
    methods = r'''      public function ultimateInitGuest(ROOT:Object, KIND:String) : void
      {
         this.ultimateGuestRoot = ROOT;
         this.ultimateGuestKind = KIND;
         this.building = false;
         this.buttonMode = true;
         this.mouseChildren = false;
         this.alpha = 1;
         try { this.gotoAndStop("idle"); } catch(errorIdle:Error) { try { this.gotoAndStop(1); } catch(errorFrame:Error) { } }
      }

      public function ultimateGuestTick() : Boolean
      {
         if(this.ultimateGuestRoot == null)
         {
            return false;
         }
         this.scaleX = this.scaleY = 1 + Math.sin(this.ultimateGuestCooldown * 0.13) * 0.015;
         this.ultimateGuestCooldown++;
         if(this.ultimateGuestCooldown % 24 != 0)
         {
            return true;
         }
         var enemy:Object = null;
         var best:Object = null;
         var dx:Number = 0;
         var dy:Number = 0;
         var distance:Number = 0;
         var bestDistance:Number = 260;
         for each(enemy in this.ultimateGuestRoot.enemies)
         {
            if(enemy != null && Boolean(enemy.isActive))
            {
               dx = Number(enemy.x) - this.x;
               dy = Number(enemy.y) - this.y;
               distance = Math.sqrt(dx * dx + dy * dy);
               if(distance < bestDistance)
               {
                  bestDistance = distance;
                  best = enemy;
               }
            }
         }
         if(best != null)
         {
            var power:int = this.ultimateGuestKind.indexOf("mage") >= 0 || this.ultimateGuestKind.indexOf("arcane") >= 0 || this.ultimateGuestKind.indexOf("necro") >= 0 || this.ultimateGuestKind.indexOf("sorcerer") >= 0 ? 92 : 70;
            if(this.ultimateGuestKind.indexOf("tesla") >= 0 || this.ultimateGuestKind.indexOf("bertha") >= 0 || this.ultimateGuestKind.indexOf("dwaarp") >= 0 || this.ultimateGuestKind.indexOf("mecha") >= 0)
            {
               for each(enemy in this.ultimateGuestRoot.enemies)
               {
                  if(enemy != null && Boolean(enemy.isActive))
                  {
                     dx = Number(enemy.x) - Number(best.x);
                     dy = Number(enemy.y) - Number(best.y);
                     if(dx * dx + dy * dy <= 10000) enemy.setDamage(power,3);
                  }
               }
            }
            else
            {
               best.setDamage(power,3);
            }
            this.alpha = 0.72;
         }
         else
         {
            this.alpha = 1;
         }
         return true;
      }

'''
    text = once(text, marker, methods + marker, "guest tower methods")
    text = insert_function_guard(text, "      public function onFrameUpdate() : void", "         if(this.ultimateGuestTick()) { return; }\n")
    return patch_pause_guards(text)


def patch_tower_family(text: str) -> str:
    if "if(this.ultimateGuestTick())" not in text:
        text = insert_function_guard(text, "      override public function onFrameUpdate() : void", "         if(this.ultimateGuestTick()) { return; }\n")
    return patch_pause_guards(text)


def patch_tower_class(text: str, kr: bool, kind: str) -> str:
    if f'ultimateInitGuest(this.parent.parent,"{kind}")' not in text:
        assignment = "         this.§_-9c§ = KR1__Level(this.parent.parent);\n" if kr else "         this.cRoot = Level(this.parent.parent);\n"
        native_type = "KR1__Level" if kr else "Level"
        replacement = f'''         if(!(this.parent.parent is {native_type}))
         {{
            this.ultimateInitGuest(this.parent.parent,"{kind}");
            return;
         }}
''' + assignment
        text = once(text, assignment, replacement, f"{kind} guest init")
    if "override public function onFrameUpdate()" in text and "if(this.ultimateGuestTick())" not in text:
        text = insert_function_guard(text, "      override public function onFrameUpdate() : void", "         if(this.ultimateGuestTick()) { return; }\n")
    return patch_pause_guards(text)


def patch_soldier_base(text: str, kr: bool) -> str:
    if "ultimateGuestHeroV15" in text:
        return text
    field_anchor = "      public var isActive:Boolean = false;\n"
    fields = r'''      public var ultimateGuestHeroV15:Boolean = true;

      public var ultimateGuestRoot:Object = null;

      public var ultimateGuestKind:String = "";

      private var ultimateGuestCooldown:int = 0;

''' + field_anchor
    text = once(text, field_anchor, fields, "guest hero fields")
    marker = "      public function onFrameUpdate() : void\n"
    methods = r'''      public function ultimateInitGuest(ROOT:Object, KIND:String) : void
      {
         this.ultimateGuestRoot = ROOT;
         this.ultimateGuestKind = KIND;
         this.isActive = true;
         this.isDead = false;
         this.isRespawning = false;
         this.isWalking = false;
         this.isFighting = false;
         this.buttonMode = false;
         this.mouseChildren = false;
         try { this.gotoAndPlay("idle"); } catch(errorIdle:Error) { try { this.gotoAndPlay(1); } catch(errorFrame:Error) { } }
      }

      public function ultimateGuestHeroTick() : Boolean
      {
         if(this.ultimateGuestRoot == null)
         {
            return false;
         }
         var enemy:Object = null;
         var best:Object = null;
         var dx:Number = 0;
         var dy:Number = 0;
         var distance:Number = 0;
         var bestDistance:Number = 900;
         for each(enemy in this.ultimateGuestRoot.enemies)
         {
            if(enemy != null && Boolean(enemy.isActive))
            {
               dx = Number(enemy.x) - this.x;
               dy = Number(enemy.y) - this.y;
               distance = Math.sqrt(dx * dx + dy * dy);
               if(distance < bestDistance)
               {
                  bestDistance = distance;
                  best = enemy;
               }
            }
         }
         if(best == null)
         {
            return true;
         }
         dx = Number(best.x) - this.x;
         dy = Number(best.y) - this.y;
         if(bestDistance > 46)
         {
            var step:Number = Math.min(2.35,bestDistance - 46);
            this.x += dx / bestDistance * step;
            this.y += dy / bestDistance * step;
            this.scaleX = dx < 0 ? -Math.abs(this.scaleX) : Math.abs(this.scaleX);
         }
         else
         {
            this.ultimateGuestCooldown++;
            if(this.ultimateGuestCooldown % 20 == 0)
            {
               best.setDamage(this.ultimateGuestKind.indexOf("dragon") >= 0 || this.ultimateGuestKind.indexOf("ignus") >= 0 ? 105 : 62,3);
               this.alpha = 0.72;
            }
            else
            {
               this.alpha = 1;
            }
         }
         return true;
      }

'''
    text = once(text, marker, methods + marker, "guest hero methods")
    text = insert_function_guard(text, "      public function onFrameUpdate() : void", "         if(this.ultimateGuestHeroTick()) { return; }\n")
    return patch_pause_guards(text)


def patch_hero_class(text: str, kr: bool, kind: str) -> str:
    if f'ultimateInitGuest(this.parent.parent,"{kind}")' not in text:
        assignment = "         this.§_-9c§ = KR1__Level(this.parent.parent);\n" if kr else "         this.cRoot = Level(this.parent.parent);\n"
        native_type = "KR1__Level" if kr else "Level"
        replacement = f'''         if(!(this.parent.parent is {native_type}))
         {{
            this.ultimateInitGuest(this.parent.parent,"{kind}");
            return;
         }}
''' + assignment
        text = once(text, assignment, replacement, f"{kind} hero guest init")
    return patch_pause_guards(text)


def armory_literal(prefix: str, towers: list[tuple[str, str, str]], heroes: list[tuple[str, str, str]]) -> str:
    rows = [(f"guest_{prefix}_tower_{key}", "TOWER • " + title) for key, title, _ in towers]
    rows += [(f"guest_{prefix}_hero_{key}", "HERO • " + title) for key, title, _ in heroes]
    return ",".join(f'["{action}","{title}"]' for action, title in rows)


def guest_switch(prefix: str, towers: list[tuple[str, str, str]], heroes: list[tuple[str, str, str]]) -> str:
    cases = []
    for key, title, cls in towers:
        cases.append(f'''            case "guest_{prefix}_tower_{key}": className = "{cls}"; title = "{title}"; break;''')
    for key, title, cls in heroes:
        cases.append(f'''            case "guest_{prefix}_hero_{key}": className = "{cls}"; title = "{title}"; hero = true; break;''')
    return "\n".join(cases)


def patch_krf_level(text: str) -> str:
    if "ultimateCrossoverArmoryV15" in text:
        return text
    text = once(
        text,
        "      private var qolSettingsPage:int = 0;\n",
        "      private var qolSettingsPage:int = 0;\n      \n      public var ultimateCrossoverArmoryV15:Boolean = true;\n      \n      private var ultimateArmoryPage:int = 0;\n      \n      private var ultimateGuestPlacement:int = 0;\n",
        "KRF armory fields",
    )
    old_button = '''         b.graphics.beginFill(2500134,0.96);
         b.graphics.lineStyle(1,16777215,0.35);
         b.graphics.drawRoundRect(0,0,param4,42,10,10);
         b.graphics.endFill();
'''
    new_button = '''         b.graphics.lineStyle(2,12353869,1);
         b.graphics.beginFill(4469012,0.98);
         b.graphics.drawRoundRect(0,0,param4,42,9,9);
         b.graphics.endFill();
         b.graphics.lineStyle(1,16045249,0.62);
         b.graphics.moveTo(7,5);
         b.graphics.lineTo(param4 - 7,5);
'''
    text = once(text, old_button, new_button, "KRF bronze button style")
    text = text.replace('new TextFormat("_sans",16,16777215,true)', 'new TextFormat("_sans",16,16774620,true)', 1)
    old_panel = '''         this.qolSettings.graphics.beginFill(1118481,0.97);
         this.qolSettings.graphics.lineStyle(2,13983051,0.8);
         this.qolSettings.graphics.drawRoundRect(0,0,580,515,18,18);
         this.qolSettings.graphics.endFill();
'''
    new_panel = '''         this.qolSettings.graphics.lineStyle(5,11040341,1);
         this.qolSettings.graphics.beginFill(2820107,0.985);
         this.qolSettings.graphics.drawRoundRect(0,0,580,515,18,18);
         this.qolSettings.graphics.endFill();
         this.qolSettings.graphics.lineStyle(2,15837487,0.72);
         this.qolSettings.graphics.drawRoundRect(8,8,564,499,13,13);
         this.qolSettings.graphics.beginFill(8388608,0.82);
         this.qolSettings.graphics.drawCircle(18,18,8);
         this.qolSettings.graphics.drawCircle(562,18,8);
         this.qolSettings.graphics.endFill();
'''
    text = once(text, old_panel, new_panel, "KRF parchment panel style")
    text = text.replace('new TextFormat("_sans",param4,16777215,true)', 'new TextFormat("_sans",param4,16774620,true)', 1)
    text = once(
        text,
        '''            this.qolSettings.addChild(this.qolButton("Cheats / Cleanup",28,194,250,"page_cheats"));
            this.qolSettings.addChild(this.qolButton("Performance",302,194,250,"page_perf"));
            this.qolSettings.addChild(this.qolLabel("Presets",28,260,16));
            this.qolSettings.addChild(this.qolButton("Normal",28,286,120,"preset_normal"));
            this.qolSettings.addChild(this.qolButton("Chaos",162,286,120,"preset_chaos"));
            this.qolSettings.addChild(this.qolButton("Benchmark",296,286,120,"preset_benchmark"));
            this.qolSettings.addChild(this.qolButton("Time Attack",430,286,122,"preset_timeattack"));
            this.qolSettings.addChild(this.qolButton("HIDE SANDBOX",165,382,250,"hide"));
''',
        '''            this.qolSettings.addChild(this.qolButton("Cheats / Cleanup",28,194,250,"page_cheats"));
            this.qolSettings.addChild(this.qolButton("Performance",302,194,250,"page_perf"));
            this.qolSettings.addChild(this.qolButton("KINGDOM RUSH ARMORY",28,252,524,"page_armory"));
            this.qolSettings.addChild(this.qolLabel("Battle presets",28,315,16));
            this.qolSettings.addChild(this.qolButton("Normal",28,342,120,"preset_normal"));
            this.qolSettings.addChild(this.qolButton("Chaos",162,342,120,"preset_chaos"));
            this.qolSettings.addChild(this.qolButton("Benchmark",296,342,120,"preset_benchmark"));
            this.qolSettings.addChild(this.qolButton("Time Attack",430,342,122,"preset_timeattack"));
            this.qolSettings.addChild(this.qolButton("HIDE SANDBOX",165,423,250,"hide"));
''',
        "KRF dashboard armory entry",
    )
    helper_marker = "      private function qolRenderSettings() : void\n"
    armory_rows = armory_literal("kr", KR_TOWERS, KR_HEROES)
    switch = guest_switch("kr", KR_TOWERS, KR_HEROES)
    helpers = f'''      private function ultimateSpawnKRGuest(ACTION:String) : void
      {{
         var className:String = "";
         var title:String = "";
         var hero:Boolean = false;
         switch(ACTION)
         {{
{switch}
         }}
         if(className == "") return;
         var guestClass:Class = null;
         var guest:Object = null;
         var xPos:int = 205 + this.ultimateGuestPlacement % 4 * 115;
         var yPos:int = 405 - int(this.ultimateGuestPlacement % 8 / 4) * 76;
         this.ultimateGuestPlacement++;
         try {{ guestClass = Class(getDefinitionByName(className)); }} catch(errorLookup:Error) {{ return; }}
         try
         {{
            if(hero) guest = new guestClass(new Point(xPos,yPos),new Point(xPos,yPos),null,new Point(xPos,yPos));
            else guest = new guestClass(xPos,yPos,new Point(xPos + 28,yPos),0);
         }}
         catch(errorCreate:Error) {{ return; }}
         this.entities.addChild(guest as DisplayObject);
         if(!hero) this.towers[guest] = guest;
      }}

'''
    text = once(text, helper_marker, helpers + helper_marker, "KRF guest spawn helper")
    final_else = '''         else
         {
            this.qolSettings.addChild(this.qolLabel("TOWERS / CLIPBOARD",28,16,22));
'''
    armory_page = f'''         else if(this.qolSettingsPage == 7)
         {{
            var armory:Array = [{armory_rows}];
            var armoryPages:int = Math.ceil(armory.length / 8);
            this.ultimateArmoryPage = Math.max(0,Math.min(armoryPages - 1,this.ultimateArmoryPage));
            this.qolSettings.addChild(this.qolLabel("KINGDOM RUSH GUEST ARMORY — " + (this.ultimateArmoryPage + 1) + "/" + armoryPages,28,16,21));
            this.qolSettings.addChild(this.qolLabel("Real KR timelines with host-compatible guest combat. Click to deploy.",28,49,13));
            var firstArmory:int = this.ultimateArmoryPage * 8;
            var ai:int = 0;
            while(ai < 8 && firstArmory + ai < armory.length)
            {{
               var armoryRow:Array = armory[firstArmory + ai] as Array;
               this.qolSettings.addChild(this.qolButton(String(armoryRow[1]),ai % 2 == 0 ? 28 : 302,82 + int(ai / 2) * 58,250,String(armoryRow[0])));
               ai++;
            }}
            this.qolSettings.addChild(this.qolButton("◀ ARMORY PAGE",28,338,170,"armory_prev"));
            this.qolSettings.addChild(this.qolButton("ARMORY PAGE ▶",382,338,170,"armory_next"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,410,250,"page_main"));
         }}
''' + final_else
    text = once(text, final_else, armory_page, "KRF armory page")
    text = once(
        text,
        '''         else if(action == "page_towers")
         {
            this.qolSettingsPage = 6;
         }
         else if(action.indexOf("hero_") == 0)
''',
        '''         else if(action == "page_towers")
         {
            this.qolSettingsPage = 6;
         }
         else if(action == "page_armory")
         {
            this.qolSettingsPage = 7;
         }
         else if(action == "armory_prev")
         {
            this.ultimateArmoryPage = (this.ultimateArmoryPage + 2) % 3;
         }
         else if(action == "armory_next")
         {
            this.ultimateArmoryPage = (this.ultimateArmoryPage + 1) % 3;
         }
         else if(action.indexOf("guest_kr_") == 0)
         {
            this.ultimateSpawnKRGuest(action);
         }
         else if(action.indexOf("hero_") == 0)
''',
        "KRF armory click routes",
    )
    return text


def patch_kr_level(text: str) -> str:
    if "ultimateKRArmoryV15" in text:
        return text
    if "import flash.utils.getDefinitionByName;" not in text:
        text = once(text, "   import flash.utils.Dictionary;\n", "   import flash.utils.Dictionary;\n   import flash.utils.getDefinitionByName;\n", "KR guest reflection import")
    text = once(
        text,
        "      public var ultimateKRSandboxV14:Boolean = true;\n",
        "      public var ultimateKRSandboxV14:Boolean = true;\n      \n      public var ultimateKRArmoryV15:Boolean = true;\n      \n      private var ultimateSandboxPage:int = 0;\n      \n      private var ultimateArmoryPage:int = 0;\n      \n      private var ultimateGuestPlacement:int = 0;\n",
        "KR armory fields",
    )
    old_style = '''         button.graphics.beginFill(1710618,0.97);
         button.graphics.lineStyle(1,15647579,0.9);
         button.graphics.drawRoundRect(0,0,param4,34,8,8);
         button.graphics.endFill();
'''
    new_style = '''         button.graphics.lineStyle(2,12288064,1);
         button.graphics.beginFill(4203014,0.985);
         button.graphics.drawRoundRect(0,0,param4,34,8,8);
         button.graphics.endFill();
         button.graphics.lineStyle(1,16045249,0.58);
         button.graphics.moveTo(6,4);
         button.graphics.lineTo(param4 - 6,4);
'''
    text = once(text, old_style, new_style, "KR bronze button style")
    start = text.index("      private function ultimateRenderSandbox()")
    end = text.index("      private function ultimateSandboxClick", start)
    rows = armory_literal("krf", KRF_TOWERS, KRF_HEROES)
    switch = guest_switch("krf", KRF_TOWERS, KRF_HEROES)
    replacement = f'''      private function ultimateSpawnKRFGuest(action:String) : void
      {{
         var className:String = "";
         var title:String = "";
         var hero:Boolean = false;
         switch(action)
         {{
{switch}
         }}
         if(className == "") return;
         var guestClass:Class = null;
         var guest:Object = null;
         var xPos:int = 165 + this.ultimateGuestPlacement % 4 * 112;
         var yPos:int = 410 - int(this.ultimateGuestPlacement % 8 / 4) * 74;
         this.ultimateGuestPlacement++;
         try {{ guestClass = Class(getDefinitionByName(className)); }} catch(errorLookup:Error) {{ return; }}
         try
         {{
            if(hero) guest = new guestClass(new Point(xPos,yPos),new Point(xPos,yPos),null,new Point(xPos,yPos));
            else
            {{
               try {{ guest = new guestClass(xPos,yPos,new Point(xPos + 28,yPos),0,true); }}
               catch(errorFive:Error) {{ guest = new guestClass(xPos,yPos,new Point(xPos + 28,yPos),0); }}
            }}
         }}
         catch(errorCreate:Error) {{ return; }}
         this.entities.addChild(guest as DisplayObject);
         if(!hero) this.towers[guest] = guest;
      }}

      private function ultimateRenderSandbox() : void
      {{
         this.ultimateCloseSandbox();
         var panel:Sprite = new Sprite();
         panel.x = this.ultimateSandboxPage == 0 ? 440 : 250;
         panel.y = 46;
         var panelWidth:Number = this.ultimateSandboxPage == 0 ? 350 : 540;
         panel.graphics.lineStyle(5,11040341,1);
         panel.graphics.beginFill(2820107,0.985);
         panel.graphics.drawRoundRect(0,0,panelWidth,470,16,16);
         panel.graphics.endFill();
         panel.graphics.lineStyle(2,15837487,0.72);
         panel.graphics.drawRoundRect(8,8,panelWidth - 16,454,12,12);
         if(this.ultimateSandboxPage == 0)
         {{
            panel.addChild(this.ultimateSandboxText("KINGDOM RUSH WAR ROOM",18,14,320,27,17));
            panel.addChild(this.ultimateSandboxText("Speed " + KR1__Level.ultimateSpeed + "× • adaptive under heavy load",18,49,315,22,11));
            panel.addChild(this.ultimateSandboxMakeButton("SPEED: " + KR1__Level.ultimateSpeed + "×",18,82,314,"ultimate_speed"));
            panel.addChild(this.ultimateSandboxMakeButton("+ 1,000 GOLD",18,126,150,"ultimate_gold"));
            panel.addChild(this.ultimateSandboxMakeButton("+ 10 LIVES",182,126,150,"ultimate_lives"));
            panel.addChild(this.ultimateSandboxMakeButton("FRONTIERS GUEST ARMORY",18,178,314,"ultimate_page_armory"));
            panel.addChild(this.ultimateSandboxMakeButton("INSTANT WIN",18,230,314,"ultimate_win"));
            panel.addChild(this.ultimateSandboxText("Guest towers and heroes use their real Frontiers art and host-compatible combat. They do not overwrite campaign saves.",18,284,314,63,11));
            panel.addChild(this.ultimateSandboxMakeButton("CLOSE WAR ROOM",65,394,220,"ultimate_close"));
         }}
         else
         {{
            var armory:Array = [{rows}];
            var pages:int = Math.ceil(armory.length / 8);
            this.ultimateArmoryPage = Math.max(0,Math.min(pages - 1,this.ultimateArmoryPage));
            panel.addChild(this.ultimateSandboxText("FRONTIERS GUEST ARMORY — " + (this.ultimateArmoryPage + 1) + "/" + pages,18,14,500,27,17));
            panel.addChild(this.ultimateSandboxText("Click a card to deploy a combat-capable guest near the road.",18,47,500,20,11));
            var first:int = this.ultimateArmoryPage * 8;
            var ai:int = 0;
            while(ai < 8 && first + ai < armory.length)
            {{
               var row:Array = armory[first + ai] as Array;
               panel.addChild(this.ultimateSandboxMakeButton(String(row[1]),ai % 2 == 0 ? 18 : 278,80 + int(ai / 2) * 58,244,String(row[0])));
               ai++;
            }}
            panel.addChild(this.ultimateSandboxMakeButton("◀ ARMORY PAGE",18,330,170,"ultimate_armory_prev"));
            panel.addChild(this.ultimateSandboxMakeButton("ARMORY PAGE ▶",352,330,170,"ultimate_armory_next"));
            panel.addChild(this.ultimateSandboxMakeButton("← WAR ROOM",145,398,250,"ultimate_page_tools"));
         }}
         this.ultimateSandboxPanel = panel;
         this.gui.addChild(panel);
      }}

'''
    text = text[:start] + replacement + text[end:]
    text = once(
        text,
        '''         else if(action == "ultimate_gold")
         {
''',
        '''         else if(action == "ultimate_page_armory")
         {
            this.ultimateSandboxPage = 1;
            this.ultimateRenderSandbox();
         }
         else if(action == "ultimate_page_tools")
         {
            this.ultimateSandboxPage = 0;
            this.ultimateRenderSandbox();
         }
         else if(action == "ultimate_armory_prev")
         {
            this.ultimateArmoryPage = (this.ultimateArmoryPage + 2) % 3;
            this.ultimateRenderSandbox();
         }
         else if(action == "ultimate_armory_next")
         {
            this.ultimateArmoryPage = (this.ultimateArmoryPage + 1) % 3;
            this.ultimateRenderSandbox();
         }
         else if(action.indexOf("guest_krf_") == 0)
         {
            this.ultimateSpawnKRFGuest(action);
            this.ultimateRenderSandbox();
         }
         else if(action == "ultimate_gold")
         {
''',
        "KR armory click routes",
    )
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.scripts

    kr_tower_base = root / "KR1__Tower.as"
    krf_tower_base = root / "§_-5u§.as"
    write(kr_tower_base, patch_tower_base(read(kr_tower_base), True))
    write(krf_tower_base, patch_tower_base(read(krf_tower_base), False))

    for name in ("KR1__TowerArcher", "KR1__TowerSoldier", "KR1__TowerMage", "KR1__TowerEngineer", "§_-v9§", "§_-oH§", "TowerMage", "TowerEngineer"):
        path = root / f"{name}.as"
        write(path, patch_tower_family(read(path)))

    for key, _title, name in KR_TOWERS:
        path = root / f"{name}.as"
        write(path, patch_tower_class(read(path), True, key))
    for key, _title, name in KRF_TOWERS:
        path = root / f"{name}.as"
        write(path, patch_tower_class(read(path), False, key))

    kr_soldier = root / "KR1__Soldier.as"
    krf_soldier = root / "Soldier.as"
    write(kr_soldier, patch_soldier_base(read(kr_soldier), True))
    write(krf_soldier, patch_soldier_base(read(krf_soldier), False))
    for key, _title, name in KR_HEROES:
        path = root / f"{name}.as"
        write(path, patch_hero_class(read(path), True, key))
    for key, _title, name in KRF_HEROES:
        path = root / f"{name}.as"
        write(path, patch_hero_class(read(path), False, key))

    kr_level = root / "KR1__Level.as"
    krf_level = root / "Level.as"
    write(kr_level, patch_kr_level(read(kr_level)))
    write(krf_level, patch_krf_level(read(krf_level)))

    checks = {
        kr_level: ["ultimateKRArmoryV15", "FRONTIERS GUEST ARMORY", "ultimateSpawnKRFGuest", 'action.indexOf("guest_krf_")'],
        krf_level: ["ultimateCrossoverArmoryV15", "KINGDOM RUSH GUEST ARMORY", "ultimateSpawnKRGuest", 'action.indexOf("guest_kr_")'],
        kr_tower_base: ["ultimateGuestTowerV15", "ultimateGuestTick", "enemy.setDamage"],
        krf_tower_base: ["ultimateGuestTowerV15", "ultimateGuestTick", "enemy.setDamage"],
        kr_soldier: ["ultimateGuestHeroV15", "ultimateGuestHeroTick", "best.setDamage"],
        krf_soldier: ["ultimateGuestHeroV15", "ultimateGuestHeroTick", "best.setDamage"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path.name}")

    report = {
        "version": "15",
        "native_sandbox_skin": True,
        "krf_guest_towers_in_kr": len(KRF_TOWERS),
        "kr_guest_towers_in_krf": len(KR_TOWERS),
        "krf_guest_heroes_in_kr": len(KRF_HEROES),
        "kr_guest_heroes_in_krf": len(KR_HEROES),
        "guest_damage_contract": "host enemy setDamage",
        "native_campaign_paths_unchanged": True,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
