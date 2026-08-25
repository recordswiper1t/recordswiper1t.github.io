#!/usr/bin/env python3
"""Epic War 5 Expansion V4.2 access-path repair.

The stock cover's large Continue button has an empty handler.  The dedicated
Expansion launcher also needlessly routes through the sponsor animation and
cover before the save/hero selector.  This patch makes Continue useful, uses
the existing FlashVar to enter the native hero/save selector directly, skips
the prologue only for the dedicated Expansion launcher, and opens the authored
25-stage panel as soon as the native world map exists.
"""
from pathlib import Path
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: patch_access_v42.py <ffdec-export-root>")

scripts = Path(sys.argv[1]) / "scripts"


def read(relative: str) -> str:
    path = scripts / relative
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    return path.read_text(encoding="utf-8-sig")


def write(relative: str, value: str) -> None:
    (scripts / relative).write_text(value, encoding="utf-8", newline="\n")


def once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, got {count}")
    return value.replace(old, new, 1)


direct_helper = '''      private function expansionDirect() : Boolean
      {
         try
         {
            var rootClip:* = this.mGF.stageRoot.root;
            return rootClip != null && rootClip.loaderInfo != null && String(rootClip.loaderInfo.parameters.ew5ExpansionDirect) == "1";
         }
         catch(error:Error)
         {
         }
         return false;
      }

'''

main = read("Game/Main.as")
main = once(
    main,
'''         else
         {
            clipS = new intro_splash_mc();
            clipS.init(this.mGF);
         }
''',
'''         else
         {
            try
            {
               var rootClip:* = this.mGF.stageRoot.root;
               if(rootClip != null && rootClip.loaderInfo != null && String(rootClip.loaderInfo.parameters.ew5ExpansionDirect) == "1")
               {
                  clipS = new cover_hero_select_mc();
                  clipS.init(this.mGF);
                  return;
               }
            }
            catch(error:Error)
            {
            }
            clipS = new intro_splash_mc();
            clipS.init(this.mGF);
         }
''',
    "direct Expansion entry",
)
write("Game/Main.as", main)

cover = read("Game/Interface/Cover.as")
cover = once(
    cover,
'''      private function continueClick(event:MouseEvent) : void
      {
      }
''',
'''      private function continueClick(event:MouseEvent) : void
      {
         var clip:* = new cover_hero_select_mc();
         clip.init(this.mGF);
         this.destroy();
      }
''',
    "working Continue button",
)
write("Game/Interface/Cover.as", cover)

hero = read("Game/Interface/CoverHeroSelect.as")
hero = once(
    hero,
    "      private function startClick(event:MouseEvent) : void\n",
    direct_helper + "      private function startClick(event:MouseEvent) : void\n",
    "hero selector direct helper",
)
hero = once(
    hero,
'''         if(this.btn_erase.visible == false)
         {
            if(this.mGF.datMgr.hero_select_id == 1)
            {
               clipPrologue = new prologue_hero1_mc();
            }
            else if(this.mGF.datMgr.hero_select_id == 2)
            {
               clipPrologue = new prologue_hero2_mc();
            }
            else
            {
               clipPrologue = new prologue_hero3_mc();
            }
            clipPrologue.init(this.mGF);
         }
''',
'''         if(this.btn_erase.visible == false && !this.expansionDirect())
         {
            if(this.mGF.datMgr.hero_select_id == 1)
            {
               clipPrologue = new prologue_hero1_mc();
            }
            else if(this.mGF.datMgr.hero_select_id == 2)
            {
               clipPrologue = new prologue_hero2_mc();
            }
            else
            {
               clipPrologue = new prologue_hero3_mc();
            }
            clipPrologue.init(this.mGF);
         }
''',
    "Expansion prologue bypass",
)
write("Game/Interface/CoverHeroSelect.as", hero)

world = read("Game/Interface/WorldMap.as")
world = once(
    world,
'''         this.expansionInstallButton();
         this.area2.visible = false;
''',
'''         this.expansionInstallButton();
         if(this.expansionDirectAvailable())
         {
            this.expansionOpenPanel();
         }
         this.area2.visible = false;
''',
    "automatic Expansion campaign panel",
)
write("Game/Interface/WorldMap.as", world)

checks = {
    "Game/Main.as": ["parameters.ew5ExpansionDirect", "new cover_hero_select_mc()"],
    "Game/Interface/Cover.as": ["continueClick", "clip.init(this.mGF)", "this.destroy()"],
    "Game/Interface/CoverHeroSelect.as": ["expansionDirect()", "!this.expansionDirect()"],
    "Game/Interface/WorldMap.as": ["this.expansionOpenPanel();"],
}
for relative, markers in checks.items():
    value = read(relative)
    for marker in markers:
        if marker not in value:
            raise SystemExit(f"validation failed: {marker!r} missing from {relative}")

print("Epic War 5 Expansion V4.2 direct-access repair applied")
