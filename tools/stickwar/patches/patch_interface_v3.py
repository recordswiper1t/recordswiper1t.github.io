#!/usr/bin/env python3
"""Native-looking clickable sandbox cards and truthful speed feedback for V3."""

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


def replace_function(text: str, signature: str, next_signature: str, replacement: str) -> str:
    start = text.index(signature)
    end = text.index(next_signature, start)
    return text[:start] + replacement + text[end:]


def patch_game_screen(path: Path) -> None:
    text = read(path)
    if "_superEffectiveSpeed" not in text:
        text = once(text, "      private var _superSpeed:int = 1;\n", "      private var _superSpeed:int = 1;\n      \n      private var _superEffectiveSpeed:int = 1;\n", "effective speed field")
        text = once(text, "            var superEffectiveSpeed:int = this._superSpeed;\n", "            var superEffectiveSpeed:int = this._superSpeed;\n", "speed local")
        text = once(text, "            this._isFastForwardFrame = superEffectiveSpeed > 1;\n", "            this._superEffectiveSpeed = superEffectiveSpeed;\n            this._isFastForwardFrame = superEffectiveSpeed > 1;\n", "effective speed capture")
        text = once(
            text,
            """      public function get superSpeed() : int
      {
         return this._superSpeed;
      }
""",
            """      public function get superSpeed() : int
      {
         return this._superSpeed;
      }

      public function get superEffectiveSpeed() : int
      {
         return this._superEffectiveSpeed;
      }
""",
            "effective speed getter",
        )
    write(path, text)


INSTALL = r'''      private function sandboxUnitRole(index:int) : String
      {
         var roles:Array = ["ECONOMY","FRONTLINE","RANGED","TANK","ASSASSIN","AIR","SUPPORT","MAGIC","TITAN"];
         return String(roles[index]);
      }

      private function sandboxUnitCard(index:int,xPos:Number,yPos:Number) : Sprite
      {
         var card:Sprite = new Sprite();
         card.name = "sandbox_unit_" + index;
         card.x = xPos;
         card.y = yPos;
         var selected:Boolean = index == this._sandboxUnitIndex;
         card.graphics.lineStyle(selected ? 3 : 1,selected ? 16763904 : 13870409,1);
         card.graphics.beginFill(selected ? 3289650 : 1183245,0.98);
         card.graphics.drawRoundRect(0,0,116,70,9,9);
         card.graphics.endFill();
         // A readable Stick War silhouette: head, body, legs and role-specific weapon.
         card.graphics.lineStyle(3,selected ? 16774620 : 14540253,1);
         card.graphics.drawCircle(21,17,7);
         card.graphics.moveTo(21,24); card.graphics.lineTo(21,44);
         card.graphics.moveTo(21,30); card.graphics.lineTo(9,39);
         card.graphics.moveTo(21,30); card.graphics.lineTo(34,37);
         card.graphics.moveTo(21,44); card.graphics.lineTo(12,57);
         card.graphics.moveTo(21,44); card.graphics.lineTo(31,57);
         if(index == 2) { card.graphics.moveTo(32,23); card.graphics.lineTo(42,51); card.graphics.drawCircle(37,37,10); }
         else if(index == 3 || index == 4) { card.graphics.moveTo(34,37); card.graphics.lineTo(52,15); }
         else if(index == 7) { card.graphics.moveTo(35,37); card.graphics.lineTo(35,12); card.graphics.drawCircle(35,9,3); }
         else if(index == 8) { card.graphics.drawCircle(21,29,17); }
         card.addChild(this.sandboxPaletteText(this.sandboxNameForIndex(index),43,9,68,32,9));
         card.addChild(this.sandboxPaletteText(this.sandboxUnitRole(index),43,43,68,17,8));
         card.buttonMode = true;
         card.mouseChildren = false;
         card.addEventListener(MouseEvent.CLICK,this.sandboxPaletteClick,false,0,true);
         return card;
      }

      private function sandboxNameForIndex(index:int) : String
      {
         var names:Array = ["Miner","Swordwrath","Archidon","Spearton","Shadowrath","Albowtross","Meric","Magikill","Giant"];
         return String(names[index]);
      }

      private function installSandboxPalette() : void
      {
         this._sandboxButton = this.sandboxPaletteButton("SANDBOX","sandbox_toggle",704,14,132);
         addChild(this._sandboxButton);
         this._sandboxPanel = new Sprite();
         this._sandboxPanel.x = 414;
         this._sandboxPanel.y = 48;
         this._sandboxPanel.graphics.lineStyle(4,13870409,1);
         this._sandboxPanel.graphics.beginFill(394500,0.985);
         this._sandboxPanel.graphics.drawRoundRect(0,0,424,410,15,15);
         this._sandboxPanel.graphics.endFill();
         this._sandboxPanel.graphics.lineStyle(1,16774620,0.65);
         this._sandboxPanel.graphics.drawRoundRect(7,7,410,396,11,11);
         this._sandboxPanel.addChild(this.sandboxPaletteText("WAR COUNCIL • SANDBOX",15,11,394,26,17));
         this._sandboxStatus = this.sandboxPaletteText("",15,39,394,38,10);
         this._sandboxStatus.multiline = true;
         this._sandboxStatus.wordWrap = true;
         this._sandboxPanel.addChild(this._sandboxStatus);
         var i:int = 0;
         while(i < 9)
         {
            this._sandboxPanel.addChild(this.sandboxUnitCard(i,15 + i % 3 * 132,81 + int(i / 3) * 76));
            i++;
         }
         this._sandboxPanel.addChild(this.sandboxPaletteButton("DEPLOY ALLY","sandbox_ally",15,313,122));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("DEPLOY ENEMY","sandbox_enemy",151,313,122));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("BATCH " + this._sandboxCount,"sandbox_batch",287,313,122));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("SPEED","sandbox_speed",15,351,90));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("+ GOLD","sandbox_gold",113,351,90));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("+ MANA","sandbox_mana",211,351,90));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("MORE","sandbox_more",309,351,100));
         addChild(this._sandboxPanel);
         this._sandboxPanel.visible = false;
         this.refreshSandboxPalette();
      }

'''


CLICK = r'''      private function sandboxPaletteClick(evt:MouseEvent) : void
      {
         var action:String = Sprite(evt.currentTarget).name;
         if(action == "sandbox_toggle")
         {
            this._sandboxMode = true;
            this._sandboxPanel.visible = !this._sandboxPanel.visible;
            this.refreshSandboxPalette("Clickable unit cards ready");
            return;
         }
         if(action.indexOf("sandbox_unit_") == 0)
         {
            this._sandboxUnitIndex = int(action.substr(13));
            this.rebuildSandboxPalette(true,"Selected " + this.sandboxUnitName());
            return;
         }
         if(!this._sandboxMode) this._sandboxMode = true;
         if(action == "sandbox_batch") this._sandboxCount = this._sandboxCount == 1 ? 5 : (this._sandboxCount == 5 ? 10 : (this._sandboxCount == 10 ? 20 : 1));
         else if(action == "sandbox_speed") this.gameScreen.superSpeed = this.gameScreen.superSpeed == 1 ? 2 : (this.gameScreen.superSpeed == 2 ? 4 : (this.gameScreen.superSpeed == 4 ? 8 : (this.gameScreen.superSpeed == 8 ? 12 : 1)));
         else if(action == "sandbox_gold") this.team.gold += 1000;
         else if(action == "sandbox_mana") this.team.mana += 1000;
         else if(action == "sandbox_more")
         {
            this._sandboxNoPop = !this._sandboxNoPop;
            if(this.keyBoardState.isShift)
            {
               var victims:Array = this.team.enemyTeam.units.slice();
               for each(var victim:Unit in victims) if(victim.isAlive()) victim.damage(0,100000000,null);
            }
         }
         else if(action == "sandbox_ally" || action == "sandbox_enemy")
         {
            var target:Team = action == "sandbox_ally" ? this.team : this.team.enemyTeam;
            var i:int = 0;
            while(i < this._sandboxCount)
            {
               this.spawnSuperUnit(this.sandboxTypeForKey(this._sandboxUnitIndex,target),target);
               i++;
            }
            target.attack(false);
         }
         this.rebuildSandboxPalette(true,action == "sandbox_speed" ? "Requested " + this.gameScreen.superSpeed + "x" : "Updated");
      }

'''


def patch_ui(path: Path) -> None:
    text = read(path)
    if "WAR COUNCIL • SANDBOX" in text:
        return
    install_start = "      private function installSandboxPalette() : void"
    install_end = "      private function sandboxUnitName() : String"
    text = replace_function(text, install_start, install_end, INSTALL)
    text = once(
        text,
        """      private function sandboxUnitName() : String
      {
         var names:Array = ["Miner","Swordwrath","Archidon","Spearton","Shadowrath","Albowtross","Meric","Magikill","Giant"];
         return String(names[this._sandboxUnitIndex]);
      }
""",
        """      private function sandboxUnitName() : String
      {
         return this.sandboxNameForIndex(this._sandboxUnitIndex);
      }

      private function rebuildSandboxPalette(open:Boolean, message:String = "") : void
      {
         if(this._sandboxPanel != null && this._sandboxPanel.parent != null) this._sandboxPanel.parent.removeChild(this._sandboxPanel);
         this._sandboxPanel = null;
         this.installSandboxPalette();
         this._sandboxPanel.visible = open;
         this.refreshSandboxPalette(message);
      }
""",
        "unit name and rebuild",
    )
    text = text.replace(
        'this._sandboxStatus.text = this.sandboxUnitName().toUpperCase() + " • batch " + this._sandboxCount + " • speed " + this.gameScreen.superSpeed + "x\\nPop safety " + (this._sandboxNoPop ? "OFF" : "ON") + (MSG == "" ? "" : "\\n" + MSG);',
        'this._sandboxStatus.text = this.sandboxUnitName().toUpperCase() + " • batch " + this._sandboxCount + " • requested " + this.gameScreen.superSpeed + "x • running " + this.gameScreen.superEffectiveSpeed + "x\\nPopulation safety " + (this._sandboxNoPop ? "OFF" : "ON") + (MSG == "" ? "" : " • " + MSG);',
        1,
    )
    click_start = "      private function sandboxPaletteClick(evt:MouseEvent) : void"
    click_end = "      private function updateSuperControls() : void"
    text = replace_function(text, click_start, click_end, CLICK)
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    args = parser.parse_args()
    root = args.scripts / "com" / "brockw" / "stickwar"
    game = root / "GameScreen.as"
    ui = root / "engine" / "UserInterface.as"
    patch_game_screen(game)
    patch_ui(ui)
    checks = {
        game: ["_superEffectiveSpeed", "get superEffectiveSpeed"],
        ui: ["WAR COUNCIL • SANDBOX", "sandboxUnitCard", 'action.indexOf("sandbox_unit_")', "running \" + this.gameScreen.superEffectiveSpeed"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path}")
    print("Super Stick War V3 soldier-card sandbox and effective-speed feedback applied")


if __name__ == "__main__":
    main()
