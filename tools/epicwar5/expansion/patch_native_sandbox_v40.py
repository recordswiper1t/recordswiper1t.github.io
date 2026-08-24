#!/usr/bin/env python3
"""Epic War 5 V4.0: replace the debug palette with a native unit-card forge."""

from __future__ import annotations

import argparse
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
    b = text.find(end, a + 1)
    if a < 0 or b < 0:
        raise SystemExit(f"{label}: block anchors missing")
    return text[:a] + replacement + text[b:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_root", type=Path)
    args = parser.parse_args()
    path = args.export_root / "scripts" / "Game" / "System" / "Battle" / "BattleSystem.as"
    text = read(path)

    text = once(
        text,
        "   import flash.text.TextFormat;\n",
        "   import flash.text.TextFormat;\n   import flash.utils.getDefinitionByName;\n",
        "preview reflection import",
    )
    text = once(
        text,
        "      private var sandboxSpeedIndex:int = 0;\n",
        "      private var sandboxSpeedIndex:int = 0;\n      \n      private var sandboxRosterPage:int = 0;\n",
        "roster page field",
    )

    native_methods = r'''      private function sandboxText(LABEL:String, SIZE:int, COLOR:uint, WIDTH:Number, HEIGHT:Number, X:Number = 0, Y:Number = 0) : TextField
      {
         var label:TextField = new TextField();
         label.defaultTextFormat = new TextFormat("_sans",SIZE,COLOR,true);
         label.text = LABEL;
         label.width = WIDTH;
         label.height = HEIGHT;
         label.x = X;
         label.y = Y;
         label.selectable = false;
         label.mouseEnabled = false;
         return label;
      }

      private function sandboxMakeButton(LABEL:String, ACTION:String, X:Number, Y:Number, WIDTH:Number = 86) : MovieClip
      {
         var button:MovieClip = new MovieClip();
         button.name = ACTION;
         button.x = X;
         button.y = Y;
         button.graphics.lineStyle(2,11377354,1);
         button.graphics.beginFill(4203014,0.99);
         button.graphics.drawRoundRect(0,0,WIDTH,29,7,7);
         button.graphics.endFill();
         button.graphics.lineStyle(1,15837487,0.55);
         button.graphics.moveTo(5,4);
         button.graphics.lineTo(WIDTH - 5,4);
         var label:TextField = this.sandboxText(LABEL,10,16774620,WIDTH,21,0,6);
         label.defaultTextFormat = new TextFormat("_sans",10,16774620,true,null,null,null,null,null,"center");
         button.addChild(label);
         button.buttonMode = true;
         button.mouseChildren = false;
         button.addEventListener(MouseEvent.CLICK,this.sandboxClick,false,0,true);
         return button;
      }

      private function sandboxMakeUnitCard(NAME:String, INDEX:int, X:Number, Y:Number) : MovieClip
      {
         var card:MovieClip = new MovieClip();
         var selected:Boolean = INDEX == this.sandboxIndex;
         var previewClass:Class = null;
         var preview:MovieClip = null;
         card.name = "sandbox_pick_" + INDEX;
         card.x = X;
         card.y = Y;
         card.graphics.lineStyle(selected ? 4 : 2,selected ? 16763904 : 8272407,1);
         card.graphics.beginFill(selected ? 5387546 : 2169361,0.98);
         card.graphics.drawRoundRect(0,0,116,104,12,12);
         card.graphics.endFill();
         card.graphics.beginFill(0,0.32);
         card.graphics.drawEllipse(17,64,82,21);
         card.graphics.endFill();
         try
         {
            previewClass = Class(getDefinitionByName(NAME + "_mc"));
            preview = new previewClass() as MovieClip;
            preview.scaleX = preview.scaleY = NAME == "dragon" || NAME == "baal" || NAME == "gaia" ? 0.28 : 0.38;
            preview.x = 58;
            preview.y = 70;
            preview.mouseEnabled = false;
            preview.mouseChildren = false;
            try { preview.gotoAndPlay("standby"); } catch(errorFrame:Error) { }
            card.addChild(preview);
         }
         catch(errorPreview:Error)
         {
            card.graphics.beginFill(16763904,0.9);
            card.graphics.drawCircle(58,43,18);
            card.graphics.endFill();
         }
         var title:TextField = this.sandboxText(NAME.toUpperCase(),10,16774620,110,18,3,84);
         title.defaultTextFormat = new TextFormat("_sans",10,16774620,true,null,null,null,null,null,"center");
         card.addChild(title);
         card.buttonMode = true;
         card.mouseChildren = false;
         card.addEventListener(MouseEvent.CLICK,this.sandboxClick,false,0,true);
         return card;
      }

      private function sandboxPanelStatus(MSG:String = "") : String
      {
         var name:String = String(this.sandboxNames[this.sandboxIndex]).toUpperCase();
         return name + "  •  batch " + this.sandboxCount + "  •  mana +" + this.sandboxManaAmount + "  •  speed " + this.sandboxSpeedText() +
            "\nFREE " + this.sandboxOnOff(sandboxFreeSpells) + "  •  BUILD∞ " + this.sandboxOnOff(sandboxUnlimitedBuildings) + "  •  FAST " + this.sandboxOnOff(sandboxFastUnits) + "  •  POP " + this.sandboxOnOff(sandboxPopBoost) + (MSG == "" ? "" : "  •  " + MSG);
      }

      private function sandboxRenderPanel(MSG:String = "") : void
      {
         if(this.sandboxPanel == null)
         {
            return;
         }
         while(this.sandboxPanel.numChildren > 0)
         {
            this.sandboxPanel.removeChildAt(0);
         }
         this.sandboxPanel.graphics.clear();
         this.sandboxPanel.graphics.lineStyle(4,11377354,1);
         this.sandboxPanel.graphics.beginFill(1111560,0.985);
         this.sandboxPanel.graphics.drawRoundRect(0,0,550,466,17,17);
         this.sandboxPanel.graphics.endFill();
         this.sandboxPanel.graphics.lineStyle(2,15837487,0.72);
         this.sandboxPanel.graphics.drawRoundRect(7,7,536,452,13,13);
         this.sandboxPanel.addChild(this.sandboxText("BATTLE FORGE",20,16763904,250,27,18,12));
         var pageCount:int = Math.ceil(this.sandboxNames.length / 8);
         this.sandboxRosterPage = Math.max(0,Math.min(pageCount - 1,this.sandboxRosterPage));
         var page:TextField = this.sandboxText("ROSTER " + (this.sandboxRosterPage + 1) + " / " + pageCount,12,13877213,180,21,350,17);
         page.defaultTextFormat = new TextFormat("_sans",12,13877213,true,null,null,null,null,null,"right");
         this.sandboxPanel.addChild(page);
         var first:int = this.sandboxRosterPage * 8;
         var slot:int = 0;
         while(slot < 8 && first + slot < this.sandboxNames.length)
         {
            this.sandboxPanel.addChild(this.sandboxMakeUnitCard(String(this.sandboxNames[first + slot]),first + slot,18 + slot % 4 * 130,49 + int(slot / 4) * 112));
            slot++;
         }
         this.sandboxStatus = this.sandboxText(this.sandboxPanelStatus(MSG),10,15856113,514,43,18,276);
         this.sandboxStatus.multiline = true;
         this.sandboxStatus.wordWrap = true;
         this.sandboxPanel.addChild(this.sandboxStatus);
         this.sandboxPanel.addChild(this.sandboxMakeButton("◀ ROSTER","sandbox_page_prev",18,321,94));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPAWN ALLY","sandbox_ally",124,321,140));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPAWN ENEMY","sandbox_enemy",276,321,140));
         this.sandboxPanel.addChild(this.sandboxMakeButton("ROSTER ▶","sandbox_page_next",428,321,104));
         this.sandboxPanel.addChild(this.sandboxMakeButton("BATCH ×" + this.sandboxCount,"sandbox_batch",18,357,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("+ MANA","sandbox_mana",121,357,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPEED " + this.sandboxSpeedText(),"sandbox_speed",224,357,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("HEAL","sandbox_heal",327,357,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("WIPE","sandbox_wipe",430,357,102));
         this.sandboxPanel.addChild(this.sandboxMakeButton("FREE " + this.sandboxOnOff(sandboxFreeSpells),"sandbox_free",18,393,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("BUILD∞ " + this.sandboxOnOff(sandboxUnlimitedBuildings),"sandbox_build",121,393,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("FAST " + this.sandboxOnOff(sandboxFastUnits),"sandbox_fast",224,393,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("POP " + this.sandboxOnOff(sandboxPopBoost),"sandbox_pop",327,393,95));
         this.sandboxPanel.addChild(this.sandboxMakeButton("WIN NOW","sandbox_win",430,393,102));
         this.sandboxPanel.addChild(this.sandboxMakeButton("CLOSE FORGE","sandbox_toggle",18,429,250));
         this.sandboxPanel.addChild(this.sandboxMakeButton("DISABLE SANDBOX","sandbox_disable",282,429,250));
      }

      private function sandboxInstall() : void
      {
         this.mGF.stageRoot.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey,false,0,true);
         this.sandboxToggleButton = this.sandboxMakeButton("BATTLE FORGE","sandbox_toggle",641,17,151);
         this.mGF.stageRoot.addChild(this.sandboxToggleButton);
         this.sandboxPanel = new MovieClip();
         this.sandboxPanel.x = 125;
         this.sandboxPanel.y = 55;
         this.mGF.stageRoot.addChild(this.sandboxPanel);
         this.sandboxPanel.visible = false;
         this.sandboxRenderPanel("Ready");
      }

'''
    text = between(
        text,
        "      private function sandboxMakeButton",
        "      private function sandboxOnOff",
        native_methods,
        "native forge methods",
    )

    refresh_start = text.index("      private function sandboxRefresh")
    refresh_end = text.index("      private function sandboxCycle", refresh_start)
    refresh = r'''      private function sandboxRefresh(MSG:String = "") : void
      {
         if(this.sandboxPanel == null || this.sandboxToggleButton == null)
         {
            return;
         }
         this.sandboxPanel.visible = sandboxMaster && this.sandboxHudVisible;
         TextField(this.sandboxToggleButton.getChildAt(0)).text = sandboxMaster ? (this.sandboxHudVisible ? "FORGE OPEN" : "BATTLE FORGE") : "BATTLE FORGE";
         if(this.sandboxPanel.visible)
         {
            this.sandboxRenderPanel(MSG);
         }
      }

'''
    text = text[:refresh_start] + refresh + text[refresh_end:]

    text = once(
        text,
        '''         if(action == "sandbox_prev")
         {
            this.sandboxCycle(-1);
         }
''',
        '''         if(action.indexOf("sandbox_pick_") == 0)
         {
            this.sandboxIndex = int(action.substr(13));
            this.sandboxRefresh("Selected " + String(this.sandboxNames[this.sandboxIndex]).toUpperCase());
            return;
         }
         if(action == "sandbox_page_prev")
         {
            this.sandboxRosterPage = (this.sandboxRosterPage + Math.ceil(this.sandboxNames.length / 8) - 1) % Math.ceil(this.sandboxNames.length / 8);
            this.sandboxRefresh("Roster page changed");
         }
         else if(action == "sandbox_page_next")
         {
            this.sandboxRosterPage = (this.sandboxRosterPage + 1) % Math.ceil(this.sandboxNames.length / 8);
            this.sandboxRefresh("Roster page changed");
         }
         else if(action == "sandbox_prev")
         {
            this.sandboxCycle(-1);
         }
''',
        "card and roster click actions",
    )

    checks = [
        "private function sandboxMakeUnitCard",
        'getDefinitionByName(NAME + "_mc")',
        '"BATTLE FORGE"',
        'action.indexOf("sandbox_pick_")',
        'this.sandboxMakeButton("SPAWN ALLY"',
        'this.sandboxMakeButton("WIN NOW"',
        "sandboxApplySpeed",
        "sandboxWinCommitted",
    ]
    for needle in checks:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r}")
    write(path, text)
    print("Epic War 5 V4.0 native animated roster-card sandbox applied")


if __name__ == "__main__":
    main()
