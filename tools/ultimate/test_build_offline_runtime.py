#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import build_offline_runtime as offline


class OfflineRuntimeTests(unittest.TestCase):
    def test_obsolete_services_and_ad_loader_are_removed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            main = '''package {
public class Test {
public static var localOnly:Boolean = false;
public function Test() {
§each const each§.onlineHandler = new AgiV2Handler();
MochiServices.connect("id",root,onError);
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
}}}
'''
            (scripts / offline.MAIN_CLASS).write_text(main, encoding="utf-8")
            (scripts / offline.HANDLER_CLASS).write_text("old", encoding="utf-8")
            upgrades = '''package {
public class MenuUpgrades {
public function init():void {
         var _loc2_:Array = ["armorgames.com","kongregate.com"];
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
}}}
'''
            defeat = '''package {
public class Defeat {
public function Defeat():void {
         var _loc2_:Array = ["armorgames.com","kongregate.com"];
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
}}}
'''
            (scripts / offline.UPGRADES_CLASS).write_text(upgrades, encoding="utf-8")
            (scripts / offline.DEFEAT_CLASS).write_text(defeat, encoding="utf-8")
            offline.patch_source(Path(tmp))
            patched = (scripts / offline.MAIN_CLASS).read_text(encoding="utf-8")
            patched_upgrades = (scripts / offline.UPGRADES_CLASS).read_text(encoding="utf-8")
            patched_defeat = (scripts / offline.DEFEAT_CLASS).read_text(encoding="utf-8")
            self.assertIn("localOnly:Boolean = true", patched)
            self.assertNotIn("MochiServices.connect", patched)
            self.assertNotIn("10016QAA25A02F", patched)
            self.assertNotIn("new §var const class§", patched)
            self.assertEqual(patched.count("mobile_add_intro.visible = true"), 1)
            self.assertIn("return \"Offline\"", (scripts / offline.HANDLER_CLASS).read_text(encoding="utf-8"))
            self.assertNotIn("10017Q8F664641", patched_upgrades)
            self.assertNotIn("CPM Stars Ads", patched_upgrades)
            self.assertIn("new §in package§(new Point(108,98))", patched_upgrades)
            self.assertNotIn("10017Q8F664641", patched_defeat)
            self.assertNotIn("CPM Stars Ads", patched_defeat)
            self.assertIn("new §_-Cu§(new Point(46,188))", patched_defeat)


if __name__ == "__main__":
    unittest.main()
