#!/usr/bin/env python3
"""Patch the Ultimate runtime to use an existing, fully offline service class.

FFDec can reliably replace an existing AS3 script pack but cannot add a brand-new
class to this obfuscated SWF.  Reusing the existing AgiV2Handler QName avoids a
runtime #1065 while removing every dependency on the retired AGI/Mochi services.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MAIN_CLASS = "§each const each§.as"
HANDLER_CLASS = "AgiV2Handler.as"
UPGRADES_CLASS = "MenuUpgrades.as"
DEFEAT_CLASS = "§native for var§.as"

OFFLINE_HANDLER = """package
{
   import flash.display.Stage;

   public class AgiV2Handler implements §for const break§
   {
      public function AgiV2Handler()
      {
         super();
      }

      public function loadSystem(param1:Stage = null) : void
      {
      }

      public function retrieveHeroesPurchased(param1:§if const function§ = null) : void
      {
      }

      public function showSingleHeroStoreForSku(param1:String, param2:§if const function§) : void
      {
      }

      public function callQuest(param1:String, param2:* = null) : void
      {
      }

      public function retrieveAllProductPrices() : void
      {
      }

      public function isLoggedIn() : Boolean
      {
         return false;
      }

      public function getAvatarUrl() : *
      {
         return "";
      }

      public function getUserName() : String
      {
         return "Player";
      }

      public function retrieveOnlineData(param1:*) : void
      {
      }

      public function submitSave(param1:*, param2:*, param3:*) : void
      {
      }

      public function deleteSave(param1:*, param2:*) : void
      {
      }

      public function getService() : String
      {
         return "Offline";
      }

      public function openLogin() : void
      {
      }
   }
}
"""


def replace_once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(before, after, 1)


def patch_source(source_root: Path) -> None:
    scripts = source_root / "scripts"
    main_path = scripts / MAIN_CLASS
    handler_path = scripts / HANDLER_CLASS
    upgrades_path = scripts / UPGRADES_CLASS
    defeat_path = scripts / DEFEAT_CLASS

    main = main_path.read_text(encoding="utf-8")
    if "new UltimateOfflineHandler()" in main:
        main = replace_once(
            main,
            "new UltimateOfflineHandler()",
            "new AgiV2Handler()",
            "offline handler constructor",
        )
    elif "new AgiV2Handler()" not in main:
        raise SystemExit("offline handler constructor: no supported constructor found")

    if "public static var localOnly:Boolean = false;" in main:
        main = replace_once(
            main,
            "public static var localOnly:Boolean = false;",
            "public static var localOnly:Boolean = true;",
            "local-only field",
        )
    elif "§each const each§.localOnly = false;" in main:
        main = replace_once(
            main,
            "§each const each§.localOnly = false;",
            "§each const each§.localOnly = true;",
            "local-only assignment",
        )
    elif not (
        "public static var localOnly:Boolean = true;" in main
        or "§each const each§.localOnly = true;" in main
    ):
        raise SystemExit("local-only mode: no supported field or assignment found")

    # The obsolete advertising API must never gate startup.
    main, connect_count = re.subn(
        r"^[ \t]*MochiServices\.connect\([^\n;]+\);\r?\n",
        "",
        main,
        flags=re.MULTILINE,
    )
    if "MochiServices.connect(" in main:
        raise SystemExit("obsolete Mochi startup: unsupported connect call remains")

    ad_branch = '''         if(!this.§static const super§(_loc2_))
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
'''
    if ad_branch in main:
        main = replace_once(
            main,
            ad_branch,
            "         this.§override do§.§dynamic const import§.mobile_add_intro.visible = true;\n",
            "obsolete CPMStar startup",
        )
    elif "10016QAA25A02F" in main or "new §var const class§" in main:
        raise SystemExit("obsolete CPMStar startup: unsupported ad branch remains")

    upgrades = upgrades_path.read_text(encoding="utf-8")
    upgrades_ad_branch = '''         var _loc2_:Array = ["armorgames.com","kongregate.com"];
         if(!this.game.main.§static const super§(_loc2_))
         {
            trace("load CPM Stars Ads inside Upgrades");
            _loc3_ = "10017Q8F664641";
            _loc4_ = new §var const class§(_loc3_);
            this.§_-EY§(_loc4_);
         }
         else
         {
            this.addChild(new §in package§(new Point(108,98)));
         }
'''
    if upgrades_ad_branch in upgrades:
        upgrades = replace_once(
            upgrades,
            upgrades_ad_branch,
            "         this.addChild(new §in package§(new Point(108,98)));\n",
            "obsolete CPMStar upgrades panel",
        )
    elif "10017Q8F664641" in upgrades or "CPM Stars Ads inside Upgrades" in upgrades:
        raise SystemExit("obsolete CPMStar upgrades panel: unsupported ad branch remains")

    defeat = defeat_path.read_text(encoding="utf-8")
    defeat_ad_branch = '''         var _loc2_:Array = ["armorgames.com","kongregate.com"];
         if(!this.cRoot.game.main.§static const super§(_loc2_))
         {
            trace("load CPM Stars Ads inside Defeat");
            _loc3_ = "10017Q8F664641";
            _loc4_ = new §var const class§(_loc3_);
            this.§_-EY§(_loc4_);
         }
         else
         {
            this.addChild(new §_-Cu§(new Point(46,188)));
         }
'''
    if defeat_ad_branch in defeat:
        defeat = replace_once(
            defeat,
            defeat_ad_branch,
            "         this.addChild(new §_-Cu§(new Point(46,188)));\n",
            "obsolete CPMStar defeat panel",
        )
    elif "10017Q8F664641" in defeat or "CPM Stars Ads inside Defeat" in defeat:
        raise SystemExit("obsolete CPMStar defeat panel: unsupported ad branch remains")

    main_path.write_text(main, encoding="utf-8", newline="\n")
    handler_path.write_text(OFFLINE_HANDLER, encoding="utf-8", newline="\n")
    upgrades_path.write_text(upgrades, encoding="utf-8", newline="\n")
    defeat_path.write_text(defeat, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    patch_source(args.source_root.resolve())
    print("patched Ultimate runtime for deterministic offline startup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
