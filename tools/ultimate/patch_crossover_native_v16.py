#!/usr/bin/env python3
"""Harden V15 crossover guests into interactive, stateful V16 combat adapters.

The games have unrelated AS3 type hierarchies, so a foreign hero cannot be
inserted into the host's typed Soldier collection.  V16 supplies the missing
host adapter explicitly: shared target snapshots, distinct unit statistics,
click upgrades/stances, health, incoming pressure, death/respawn, levelling,
skills, cleanup, and truthful UI.  Native campaign classes remain untouched
when they are running in their own game.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def replace_function(text: str, signature: str, next_signature: str, replacement: str) -> str:
    start = text.index(signature)
    end = text.index(next_signature, start)
    return text[:start] + replacement + text[end:]


TOWER_METHODS = r'''      public function ultimateInitGuest(ROOT:Object, KIND:String) : void
      {
         this.ultimateGuestRoot = ROOT;
         this.ultimateGuestKind = KIND;
         this.ultimateGuestLevel = 1;
         this.ultimateGuestRange = 245;
         this.ultimateGuestPower = 58;
         this.ultimateGuestReload = 24;
         if(KIND.indexOf("crossbow") >= 0 || KIND.indexOf("rangers") >= 0) { this.ultimateGuestRange = 290; this.ultimateGuestReload = 15; this.ultimateGuestPower = 44; }
         else if(KIND.indexOf("musketeer") >= 0 || KIND.indexOf("totem") >= 0) { this.ultimateGuestRange = 325; this.ultimateGuestReload = 30; this.ultimateGuestPower = 92; }
         else if(KIND.indexOf("mage") >= 0 || KIND.indexOf("arcane") >= 0 || KIND.indexOf("necro") >= 0 || KIND.indexOf("sorcerer") >= 0 || KIND.indexOf("archmage") >= 0) { this.ultimateGuestRange = 275; this.ultimateGuestReload = 26; this.ultimateGuestPower = 105; }
         else if(KIND.indexOf("tesla") >= 0 || KIND.indexOf("bertha") >= 0 || KIND.indexOf("dwaarp") >= 0 || KIND.indexOf("mecha") >= 0) { this.ultimateGuestRange = 235; this.ultimateGuestReload = 34; this.ultimateGuestPower = 88; }
         else { this.ultimateGuestRange = 205; this.ultimateGuestReload = 20; this.ultimateGuestPower = 66; }
         this.building = false;
         this.buttonMode = true;
         this.mouseChildren = false;
         this.addEventListener(MouseEvent.CLICK,this.ultimateGuestUpgrade,false,0,true);
         this.alpha = 1;
         try { this.gotoAndStop("idle"); } catch(errorIdle:Error) { try { this.gotoAndStop(1); } catch(errorFrame:Error) { } }
      }

      private function ultimateGuestUpgrade(event:MouseEvent) : void
      {
         if(this.ultimateGuestRoot == null) return;
         this.ultimateGuestLevel = this.ultimateGuestLevel >= 3 ? 1 : this.ultimateGuestLevel + 1;
         this.scaleX = this.scaleY = 1 + 0.05 * this.ultimateGuestLevel;
      }

      public function ultimateGuestTick() : Boolean
      {
         if(this.ultimateGuestRoot == null) return false;
         this.ultimateGuestCooldown++;
         if(this.ultimateGuestCooldown % Math.max(8,this.ultimateGuestReload - this.ultimateGuestLevel * 2) != 0) return true;
         var list:Array = this.ultimateGuestRoot.ultimateGuestEnemySnapshot();
         var enemy:Object = null;
         var best:Object = null;
         var dx:Number = 0;
         var dy:Number = 0;
         var distance2:Number = 0;
         var bestDistance2:Number = this.ultimateGuestRange * this.ultimateGuestRange;
         for each(enemy in list)
         {
            if(enemy != null && Boolean(enemy.isActive))
            {
               dx = Number(enemy.x) - this.x;
               dy = Number(enemy.y) - this.y;
               distance2 = dx * dx + dy * dy;
               if(distance2 < bestDistance2) { bestDistance2 = distance2; best = enemy; }
            }
         }
         if(best == null) { this.alpha = 1; return true; }
         var power:int = int(this.ultimateGuestPower * (1 + (this.ultimateGuestLevel - 1) * 0.35));
         var splash:Boolean = this.ultimateGuestKind.indexOf("tesla") >= 0 || this.ultimateGuestKind.indexOf("bertha") >= 0 || this.ultimateGuestKind.indexOf("dwaarp") >= 0 || this.ultimateGuestKind.indexOf("mecha") >= 0;
         var chain:Boolean = this.ultimateGuestKind.indexOf("arcane") >= 0 || this.ultimateGuestKind.indexOf("archmage") >= 0 || this.ultimateGuestKind.indexOf("necro") >= 0 || this.ultimateGuestKind.indexOf("sorcerer") >= 0;
         if(splash || chain)
         {
            var hits:int = 0;
            var radius2:Number = splash ? 12500 : 20000;
            for each(enemy in list)
            {
               if(enemy != null && Boolean(enemy.isActive))
               {
                  dx = Number(enemy.x) - Number(best.x); dy = Number(enemy.y) - Number(best.y);
                  if(dx * dx + dy * dy <= radius2 && hits < (splash ? 8 : 4)) { enemy.setDamage(power,3); hits++; }
               }
            }
         }
         else best.setDamage(power,3);
         this.alpha = 0.72;
         return true;
      }

'''


HERO_METHODS = r'''      public function ultimateInitGuest(ROOT:Object, KIND:String) : void
      {
         this.ultimateGuestRoot = ROOT;
         this.ultimateGuestKind = KIND;
         this.ultimateGuestOriginX = this.x;
         this.ultimateGuestOriginY = this.y;
         this.ultimateGuestLevel = 1;
         this.ultimateGuestXP = 0;
         this.ultimateGuestHealthMax = KIND.indexOf("dragon") >= 0 || KIND.indexOf("grawl") >= 0 || KIND.indexOf("malik") >= 0 || KIND.indexOf("viking") >= 0 ? 1250 : 850;
         this.ultimateGuestHealth = this.ultimateGuestHealthMax;
         this.ultimateGuestHolding = false;
         this.isActive = true;
         this.isDead = false;
         this.isRespawning = false;
         this.isWalking = false;
         this.isFighting = false;
         this.buttonMode = true;
         this.mouseChildren = false;
         this.addEventListener(MouseEvent.CLICK,this.ultimateGuestToggleStance,false,0,true);
         this.ultimateGuestHealthBar = new Sprite();
         this.ultimateGuestHealthBar.y = -48;
         this.addChild(this.ultimateGuestHealthBar);
         this.ultimateGuestDrawHealth();
         try { this.gotoAndPlay("idle"); } catch(errorIdle:Error) { try { this.gotoAndPlay(1); } catch(errorFrame:Error) { } }
      }

      private function ultimateGuestToggleStance(event:MouseEvent) : void
      {
         if(this.ultimateGuestRoot == null) return;
         this.ultimateGuestHolding = !this.ultimateGuestHolding;
         this.alpha = this.ultimateGuestHolding ? 0.78 : 1;
      }

      private function ultimateGuestDrawHealth() : void
      {
         if(this.ultimateGuestHealthBar == null) return;
         var ratio:Number = Math.max(0,Math.min(1,this.ultimateGuestHealth / this.ultimateGuestHealthMax));
         this.ultimateGuestHealthBar.graphics.clear();
         this.ultimateGuestHealthBar.graphics.beginFill(0,0.85); this.ultimateGuestHealthBar.graphics.drawRect(-22,-3,44,6); this.ultimateGuestHealthBar.graphics.endFill();
         this.ultimateGuestHealthBar.graphics.beginFill(ratio > 0.35 ? 3381555 : 13382451,1); this.ultimateGuestHealthBar.graphics.drawRect(-21,-2,42 * ratio,4); this.ultimateGuestHealthBar.graphics.endFill();
      }

      private function ultimateGuestFall() : void
      {
         this.isDead = true;
         this.isActive = false;
         this.isRespawning = true;
         this.ultimateGuestRespawn = 300;
         this.visible = false;
      }

      public function ultimateGuestHeroTick() : Boolean
      {
         if(this.ultimateGuestRoot == null) return false;
         if(this.isRespawning)
         {
            this.ultimateGuestRespawn--;
            if(this.ultimateGuestRespawn <= 0)
            {
               this.x = this.ultimateGuestOriginX; this.y = this.ultimateGuestOriginY;
               this.ultimateGuestHealth = this.ultimateGuestHealthMax;
               this.isDead = false; this.isRespawning = false; this.isActive = true; this.visible = true;
               this.ultimateGuestDrawHealth();
            }
            return true;
         }
         this.ultimateGuestCooldown++;
         var list:Array = this.ultimateGuestRoot.ultimateGuestEnemySnapshot();
         var enemy:Object = null;
         var best:Object = null;
         var dx:Number = 0;
         var dy:Number = 0;
         var distance2:Number = 0;
         var bestDistance2:Number = 810000;
         var nearby:int = 0;
         for each(enemy in list)
         {
            if(enemy != null && Boolean(enemy.isActive))
            {
               dx = Number(enemy.x) - this.x; dy = Number(enemy.y) - this.y; distance2 = dx * dx + dy * dy;
               if(distance2 < bestDistance2) { bestDistance2 = distance2; best = enemy; }
               if(distance2 < 3600) nearby++;
            }
         }
         if(nearby > 0 && this.ultimateGuestCooldown % 18 == 0)
         {
            this.ultimateGuestHealth -= nearby * Math.max(5,12 - this.ultimateGuestLevel * 2);
            this.ultimateGuestDrawHealth();
            if(this.ultimateGuestHealth <= 0) { this.ultimateGuestFall(); return true; }
         }
         if(best == null) return true;
         var range:Number = this.ultimateGuestKind.indexOf("alleria") >= 0 || this.ultimateGuestKind.indexOf("bolin") >= 0 || this.ultimateGuestKind.indexOf("mirage") >= 0 || this.ultimateGuestKind.indexOf("nivus") >= 0 || this.ultimateGuestKind.indexOf("magnus") >= 0 || this.ultimateGuestKind.indexOf("dragon") >= 0 ? 145 : 48;
         var range2:Number = range * range;
         dx = Number(best.x) - this.x; dy = Number(best.y) - this.y;
         if(bestDistance2 > range2 && !this.ultimateGuestHolding)
         {
            var distance:Number = Math.sqrt(bestDistance2);
            var step:Number = Math.min(2.2 + this.ultimateGuestLevel * 0.18,distance - range);
            this.x += dx / distance * step; this.y += dy / distance * Math.min(step,1.5);
            this.scaleX = dx < 0 ? -Math.abs(this.scaleX) : Math.abs(this.scaleX);
         }
         else if(bestDistance2 <= range2 && this.ultimateGuestCooldown % Math.max(12,22 - this.ultimateGuestLevel) == 0)
         {
            var power:int = int((this.ultimateGuestKind.indexOf("dragon") >= 0 || this.ultimateGuestKind.indexOf("ignus") >= 0 ? 105 : 62) * (1 + (this.ultimateGuestLevel - 1) * 0.28));
            best.setDamage(power,3);
            this.ultimateGuestXP++;
            if(this.ultimateGuestXP >= this.ultimateGuestLevel * 10 && this.ultimateGuestLevel < 10)
            {
               this.ultimateGuestLevel++; this.ultimateGuestHealthMax += 90; this.ultimateGuestHealth = Math.min(this.ultimateGuestHealthMax,this.ultimateGuestHealth + 180); this.ultimateGuestDrawHealth();
            }
            if(this.ultimateGuestXP % 5 == 0)
            {
               var hits:int = 0;
               for each(enemy in list)
               {
                  if(enemy != null && Boolean(enemy.isActive))
                  {
                     dx = Number(enemy.x) - Number(best.x); dy = Number(enemy.y) - Number(best.y);
                     if(dx * dx + dy * dy < 14400 && hits < 6) { enemy.setDamage(int(power * 0.7),3); hits++; }
                  }
               }
            }
         }
         return true;
      }

'''


def patch_tower(path: Path) -> None:
    text = read(path)
    if "ultimateGuestLevel:int" not in text:
        text = once(
            text,
            "      private var ultimateGuestCooldown:int = 0;\n",
            """      private var ultimateGuestCooldown:int = 0;

      private var ultimateGuestLevel:int = 1;

      private var ultimateGuestRange:Number = 245;

      private var ultimateGuestPower:int = 58;

      private var ultimateGuestReload:int = 24;
""",
            f"{path.name} tower fields",
        )
    text = replace_function(text, "      public function ultimateInitGuest(", "      public function onFrameUpdate() : void", TOWER_METHODS)
    write(path, text)


def patch_soldier(path: Path) -> None:
    text = read(path)
    if "import flash.display.Sprite;" not in text:
        text = once(text, "   import flash.events.*;\n", "   import flash.display.Sprite;\n   import flash.events.*;\n", f"{path.name} Sprite import")
    if "ultimateGuestHealthMax:int" not in text:
        text = once(
            text,
            "      private var ultimateGuestCooldown:int = 0;\n",
            """      private var ultimateGuestCooldown:int = 0;

      private var ultimateGuestLevel:int = 1;

      private var ultimateGuestXP:int = 0;

      private var ultimateGuestHealth:int = 850;

      private var ultimateGuestHealthMax:int = 850;

      private var ultimateGuestRespawn:int = 0;

      private var ultimateGuestOriginX:Number = 0;

      private var ultimateGuestOriginY:Number = 0;

      private var ultimateGuestHolding:Boolean = false;

      private var ultimateGuestHealthBar:Sprite;
""",
            f"{path.name} hero fields",
        )
    text = replace_function(text, "      public function ultimateInitGuest(", "      public function onFrameUpdate() : void", HERO_METHODS)
    write(path, text)


SNAPSHOT = r'''      public function ultimateGuestEnemySnapshot() : Array
      {
         this.ultimateGuestCacheTick++;
         if(this.ultimateGuestEnemyCache.length == 0 || this.ultimateGuestCacheTick >= 10)
         {
            this.ultimateGuestCacheTick = 0;
            this.ultimateGuestEnemyCache.length = 0;
            var enemy:Object = null;
            for each(enemy in this.enemies) if(enemy != null && Boolean(enemy.isActive)) this.ultimateGuestEnemyCache.push(enemy);
         }
         return this.ultimateGuestEnemyCache;
      }

      private function ultimateClearCrossoverGuests() : void
      {
         var guest:Object = null;
         for each(guest in this.ultimateCrossoverGuests)
         {
            if(guest != null)
            {
               try { delete this.towers[guest]; } catch(errorTower:Error) { }
               try { if((guest as DisplayObject).parent != null) (guest as DisplayObject).parent.removeChild(guest as DisplayObject); } catch(errorDisplay:Error) { }
            }
         }
         this.ultimateCrossoverGuests.length = 0;
      }

'''


def patch_level(path: Path, kr: bool) -> None:
    text = read(path)
    marker = "      public var ultimateKRArmoryV15:Boolean = true;\n" if kr else "      public var ultimateCrossoverArmoryV15:Boolean = true;\n"
    if "ultimateCrossoverGuests:Array" not in text:
        text = once(
            text,
            marker,
            marker + "      \n      public var ultimateCrossoverNativeV16:Boolean = true;\n      \n      private var ultimateCrossoverGuests:Array = [];\n      \n      private var ultimateGuestEnemyCache:Array = [];\n      \n      private var ultimateGuestCacheTick:int = 0;\n",
            f"{path.name} crossover collections",
        )
    helper_marker = "      private function ultimateSpawnKRFGuest" if kr else "      private function ultimateSpawnKRGuest"
    if "public function ultimateGuestEnemySnapshot" not in text:
        text = once(text, helper_marker, SNAPSHOT + helper_marker, f"{path.name} target snapshot")
    if "this.ultimateCrossoverGuests.push(guest);" not in text:
        pattern = re.compile(r"(\s*this\.entities\.addChild\(guest as DisplayObject\);\s*)if\(!hero\)\s*\{\s*this\.towers\[guest\] = guest;\s*\}")
        text, count = pattern.subn(r"\1this.ultimateCrossoverGuests.push(guest);\n         if(!hero)\n         {\n            this.towers[guest] = guest;\n         }", text, count=1)
        if count != 1:
            raise SystemExit(f"{path.name} guest registry: expected one anchor, found {count}")
    if kr:
        text = once(
            text,
            '            panel.addChild(this.ultimateSandboxMakeButton("◀ ARMORY PAGE",18,330,170,"ultimate_armory_prev"));\n',
            '            panel.addChild(this.ultimateSandboxMakeButton("◀ ARMORY PAGE",18,330,170,"ultimate_armory_prev"));\n            panel.addChild(this.ultimateSandboxMakeButton("CLEAR GUESTS",185,372,170,"ultimate_clear_guests"));\n',
            "KR clear button",
        )
        click_anchor = '         else if(action.indexOf("guest_krf_") == 0)\n         {\n            this.ultimateSpawnKRFGuest(action);\n            this.ultimateRenderSandbox();\n         }\n'
    else:
        text = once(
            text,
            '            this.qolSettings.addChild(this.qolButton("◀ ARMORY PAGE",28,338,170,"armory_prev"));\n',
            '            this.qolSettings.addChild(this.qolButton("◀ ARMORY PAGE",28,338,170,"armory_prev"));\n            this.qolSettings.addChild(this.qolButton("CLEAR GUESTS",205,382,170,"ultimate_clear_guests"));\n',
            "KRF clear button",
        )
        click_anchor = '         else if(action.indexOf("guest_kr_") == 0)\n         {\n            this.ultimateSpawnKRGuest(action);\n         }\n'
    text = once(text, click_anchor, click_anchor + '         else if(action == "ultimate_clear_guests")\n         {\n            this.ultimateClearCrossoverGuests();\n         }\n', f"{path.name} clear action")
    write(path, text)


def patch_star_sync(path: Path) -> None:
    text = read(path)
    old = r'''         if(this.ultimateLastKRStars >= 0 && krStars != this.ultimateLastKRStars)
         {
            this.ultimateSharedStars = Math.max(0,this.ultimateSharedStars + krStars - this.ultimateLastKRStars);
         }
         else if(this.ultimateLastKRFStars >= 0 && krfStars != this.ultimateLastKRFStars)
         {
            this.ultimateSharedStars = Math.max(0,this.ultimateSharedStars + krfStars - this.ultimateLastKRFStars);
         }
'''
    new = r'''         var krDelta:int = this.ultimateLastKRStars < 0 ? 0 : krStars - this.ultimateLastKRStars;
         var krfDelta:int = this.ultimateLastKRFStars < 0 ? 0 : krfStars - this.ultimateLastKRFStars;
         if(krDelta != 0 || krfDelta != 0)
         {
            this.ultimateSharedStars = Math.max(0,this.ultimateSharedStars + krDelta + krfDelta);
         }
'''
    text = once(text, old, new, "transactional shared stars")
    text = text.replace("KINGDOM RUSH ULTIMATE — SHARED SYSTEMS", "KINGDOM RUSH ULTIMATE — UNIFIED WAR TABLE", 1)
    text = text.replace("Choose either campaign's native screen below. Selections and progress stay saved when maps switch.", "Both campaigns share this war table and star ledger. Open either native collection without leaving the combined profile.", 1)
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.scripts
    patch_tower(root / "KR1__Tower.as")
    patch_tower(root / "§_-5u§.as")
    patch_soldier(root / "KR1__Soldier.as")
    patch_soldier(root / "Soldier.as")
    patch_level(root / "KR1__Level.as", True)
    patch_level(root / "Level.as", False)
    patch_star_sync(root / "§_-BQ§.as")
    checks = {
        root / "KR1__Tower.as": ["ultimateGuestLevel", "ultimateGuestUpgrade", "ultimateGuestEnemySnapshot"],
        root / "Soldier.as": ["ultimateGuestHealthMax", "ultimateGuestFall", "ultimateGuestToggleStance"],
        root / "KR1__Level.as": ["ultimateCrossoverNativeV16", "ultimateClearCrossoverGuests", "CLEAR GUESTS"],
        root / "Level.as": ["ultimateCrossoverNativeV16", "ultimateGuestEnemySnapshot", "CLEAR GUESTS"],
        root / "§_-BQ§.as": ["krDelta", "krfDelta", "UNIFIED WAR TABLE"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path.name}")
    report = {
        "version": 16,
        "shared_enemy_snapshots": True,
        "tower_stat_families": True,
        "click_tower_upgrades": 3,
        "hero_health_death_respawn": True,
        "hero_levels": 10,
        "hero_click_stances": ["advance", "hold"],
        "clear_guests": True,
        "transactional_star_deltas": True,
    }
    if args.report:
        import json
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
