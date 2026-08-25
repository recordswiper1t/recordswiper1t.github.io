#!/usr/bin/env python3
"""Make Battle Lab direct, and make every sandbox utility discoverable."""

from __future__ import annotations

import argparse
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


def patch_menu(path: Path) -> None:
    text = read(path)
    if "launchDirectBattleLab" in text:
        return
    text = once(
        text,
        """      private function skipButton() : void
      {
         this.main.showScreen("campaignMap",false,true);
      }
""",
        """      private function launchDirectBattleLab(evt:Event) : void
      {
         removeEventListener(Event.ENTER_FRAME,this.launchDirectBattleLab);
         var params:Object = this.main.loaderInfo == null ? null : this.main.loaderInfo.parameters;
         var requested:String = params == null ? "normal" : String(params.swcDifficulty).toLowerCase();
         this.main.campaign.setDifficulty(requested == "insane" ? Campaign.D_INSANE : (requested == "hard" ? Campaign.D_HARD : Campaign.D_NORMAL));
         this.main.campaign.currentLevel = params != null && int(params.swcStage) > 0 ? Math.min(this.main.campaign.levels.length - 1,int(params.swcStage) - 1) : 0;
         this.main.showScreen("campaignMap",false,true);
      }

      private function skipButton() : void
      {
         this.main.showScreen("campaignMap",false,true);
      }
""",
        "direct lab helper",
    )
    text = once(
        text,
        """         this.mc.creditsScreen.visible = false;
      }
""",
        """         this.mc.creditsScreen.visible = false;
         var launchParams:Object = this.main.loaderInfo == null ? null : this.main.loaderInfo.parameters;
         if(launchParams != null && String(launchParams.swcLab) == "1")
         {
            addEventListener(Event.ENTER_FRAME,this.launchDirectBattleLab,false,1000,true);
         }
      }
""",
        "direct lab enter hook",
    )
    text = once(
        text,
        """         removeEventListener(Event.ENTER_FRAME,this.update);
""",
        """         removeEventListener(Event.ENTER_FRAME,this.update);
         removeEventListener(Event.ENTER_FRAME,this.launchDirectBattleLab);
""",
        "direct lab cleanup",
    )
    write(path, text)


def patch_ui(path: Path) -> None:
    text = read(path)
    if "sandbox_wipe" in text:
        if "enableSandbox" not in text:
            text = once(
                text,
                """      public function enableDiagnostics() : void
      {
         this._diagnostics = true;
         this._diagText.visible = true;
      }
""",
                """      public function enableSandbox() : void
      {
         this._sandboxMode = true;
         this._sandboxPanel.visible = true;
         this.refreshSandboxPalette("Battle Lab ready");
      }

      public function enableDiagnostics() : void
      {
         this._diagnostics = true;
         this._diagText.visible = true;
      }
""",
                "direct sandbox helper",
            )
            write(path, text)
        return
    text = once(text, "this._sandboxPanel.graphics.drawRoundRect(0,0,424,410,15,15);", "this._sandboxPanel.graphics.drawRoundRect(0,0,424,450,15,15);", "panel height")
    text = once(text, "this._sandboxPanel.graphics.drawRoundRect(7,7,410,396,11,11);", "this._sandboxPanel.graphics.drawRoundRect(7,7,410,436,11,11);", "inner panel height")
    text = once(
        text,
        """         this._sandboxPanel.addChild(this.sandboxPaletteButton("MORE","sandbox_more",309,351,100));
         addChild(this._sandboxPanel);
""",
        """         this._sandboxPanel.addChild(this.sandboxPaletteButton("POP SAFE","sandbox_more",309,351,100));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("CLEAR ENEMIES","sandbox_wipe",15,392,190));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("CLOSE","sandbox_close",219,392,190));
         addChild(this._sandboxPanel);
""",
        "utility buttons",
    )
    utility_start = text.index('         else if(action == "sandbox_more")')
    utility_end = text.index('         else if(action == "sandbox_ally" || action == "sandbox_enemy")', utility_start)
    text = text[:utility_start] + """         else if(action == "sandbox_more")
         {
            this._sandboxNoPop = !this._sandboxNoPop;
         }
         else if(action == "sandbox_wipe")
         {
            var victims:Array = this.team.enemyTeam.units.slice();
            for each(var victim:Unit in victims) if(victim.isAlive()) victim.damage(0,100000000,null);
         }
         else if(action == "sandbox_close")
         {
            this._sandboxPanel.visible = false;
            return;
         }
""" + text[utility_end:]
    text = once(
        text,
        """      public function enableDiagnostics() : void
      {
         this._diagnostics = true;
         this._diagText.visible = true;
      }
""",
        """      public function enableSandbox() : void
      {
         this._sandboxMode = true;
         this._sandboxPanel.visible = true;
         this.refreshSandboxPalette("Battle Lab ready");
      }

      public function enableDiagnostics() : void
      {
         this._diagnostics = true;
         this._diagText.visible = true;
      }
""",
        "direct sandbox helper",
    )
    write(path, text)


def patch_gameplay(path: Path) -> None:
    text = read(path)
    text = once(
        text,
        """         if(this._superLabParams != null && String(this._superLabParams.swcLab) == "1")
         {
            userInterface.enableDiagnostics();
            this.applyBattleLabPreset(String(this._superLabParams.swcPreset));
""",
        """         if(this._superLabParams != null && String(this._superLabParams.swcLab) == "1")
         {
            userInterface.enableSandbox();
            this.applyBattleLabPreset(String(this._superLabParams.swcPreset));
""",
        "battle lab default panel",
    )
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    args = parser.parse_args()
    root = args.scripts / "com" / "brockw" / "stickwar"
    menu = root / "campaign" / "CampaignMenuScreen.as"
    gameplay = root / "campaign" / "CampaignGameScreen.as"
    ui = root / "engine" / "UserInterface.as"
    patch_menu(menu)
    patch_ui(ui)
    patch_gameplay(gameplay)
    checks = {
        menu: ["launchDirectBattleLab", "swcDifficulty", "swcStage"],
        ui: ["sandbox_wipe", "CLEAR ENEMIES", "sandbox_close", "enableSandbox"],
        gameplay: ["userInterface.enableSandbox()"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path}")
    print("Super Stick War V3.1 direct Battle Lab and explicit utility controls applied")


if __name__ == "__main__":
    main()
