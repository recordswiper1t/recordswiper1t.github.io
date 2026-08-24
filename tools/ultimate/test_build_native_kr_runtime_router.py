#!/usr/bin/env python3
from __future__ import annotations

import unittest

import build_native_kr_runtime_router as router


class NativeKrRuntimeRouterTests(unittest.TestCase):
    def test_native_launch_and_shared_map_return_are_installed(self) -> None:
        source = '''package
{
   import flash.events.*;
   public class Test
   {
      public var ultimateSourceLevel:int = 0;

      public function ultimateStartStage(param1:String, param2:String, param3:int, param4:int = 0, param5:Boolean = false, param6:String = "kr1") : void
      {
         var levelClass:Class = getDefinitionByName(param1) as Class;
         if(levelClass == null)
         {
            return;
         }
         this.ultimateStageId = param2;
         this.ultimateStageGame = param6;
         this.ultimateSourceLevel = param3;
         this.currentLevel = param3;
         this.addChildAt(new levelClass(this,param4,param5),0);
      }
   }
}
'''
        patched = router.patch(source)
        self.assertIn('getDefinitionByName("KR1__Defense")', patched)
        self.assertIn('getDefinitionByName("KR1__Game")', patched)
        self.assertIn('Event.ENTER_FRAME,this.ultimateMonitorNativeKR', patched)
        self.assertIn('this.ultimateNativeKRGame["map"] == null', patched)
        self.assertIn('this.removeChild(this.ultimateNativeKRMain as DisplayObject)', patched)
        self.assertIn('this.§var const finally§(null);', patched)
        self.assertIn('import flash.display.DisplayObject;', patched)


if __name__ == "__main__":
    unittest.main()
