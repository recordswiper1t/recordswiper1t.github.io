#!/usr/bin/env python3
"""Add a visible Stick War sandbox palette and adaptive 1x-12x simulation."""

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


def patch_game_screen(path: Path) -> None:
    text = read(path)
    text = once(
        text,
        "      private var _isFastForwardFrame:Boolean;\n",
        "      private var _isFastForwardFrame:Boolean;\n      \n      private var _superSpeed:int = 1;\n",
        "Stick speed field",
    )
    text = once(
        text,
        "         this.isFastForward = false;\n         this._isFastForwardFrame = false;\n",
        "         this.isFastForward = false;\n         this._isFastForwardFrame = false;\n         this._superSpeed = 1;\n",
        "Stick speed init",
    )
    text = once(
        text,
        '''            this.simulation.update(this);
            if(this.isFastForward)
            {
               this._isFastForwardFrame = true;
               this.simulation.update(this);
               this._isFastForwardFrame = false;
            }
''',
        '''            var superActorLoad:int = this.game.teamA.units.length + this.game.teamB.units.length + this.game.projectileManager.projectiles.length + this.game.projectileManager.airEffects.length;
            var superEffectiveSpeed:int = this._superSpeed;
            if(superActorLoad >= 420) superEffectiveSpeed = Math.min(superEffectiveSpeed,2);
            else if(superActorLoad >= 280) superEffectiveSpeed = Math.min(superEffectiveSpeed,4);
            else if(superActorLoad >= 170) superEffectiveSpeed = Math.min(superEffectiveSpeed,8);
            this.simulation.update(this);
            var superTick:int = 1;
            this._isFastForwardFrame = superEffectiveSpeed > 1;
            while(superTick < superEffectiveSpeed)
            {
               this.simulation.update(this);
               superTick++;
            }
            this._isFastForwardFrame = false;
''',
        "adaptive multi-tick Stick speed",
    )
    text = once(
        text,
        "      public function get isFastForward() : Boolean\n",
        '''      public function get superSpeed() : int
      {
         return this._superSpeed;
      }

      public function set superSpeed(value:int) : void
      {
         this._superSpeed = value <= 1 ? 1 : (value <= 2 ? 2 : (value <= 4 ? 4 : (value <= 8 ? 8 : 12)));
         this.isFastForward = this._superSpeed > 1;
      }

      public function get isFastForward() : Boolean
''',
        "Stick speed property",
    )
    write(path, text)


def patch_ui(path: Path) -> None:
    text = read(path)
    text = once(
        text,
        "      private var _sandboxNoPop:Boolean;\n",
        """      private var _sandboxNoPop:Boolean;
      
      private var _sandboxButton:Sprite;
      
      private var _sandboxPanel:Sprite;
      
      private var _sandboxStatus:TextField;
      
      private var _sandboxUnitIndex:int = 0;
      
      private var _sandboxCount:int = 1;
""",
        "clickable sandbox fields",
    )
    text = once(
        text,
        "         addChild(this._diagText);\n         if(this.main.campaign != null)\n",
        "         addChild(this._diagText);\n         this.installSandboxPalette();\n         if(this.main.campaign != null)\n",
        "clickable sandbox install",
    )
    text = once(
        text,
        "         this._diagText = null;\n         this._hud = null;\n",
        "         this._diagText = null;\n         this._sandboxButton = null;\n         this._sandboxPanel = null;\n         this._sandboxStatus = null;\n         this._hud = null;\n",
        "clickable sandbox cleanup",
    )
    text = once(
        text,
        '''      private function clickFastForward(evt:Event) : void
      {
         this.gameScreen.isFastForward = !this.gameScreen.isFastForward;
         this.mouseState.mouseDown = false;
      }
''',
        '''      private function clickFastForward(evt:Event) : void
      {
         this.gameScreen.superSpeed = this.gameScreen.superSpeed == 1 ? 2 : (this.gameScreen.superSpeed == 2 ? 4 : 1);
         this.mouseState.mouseDown = false;
         this.refreshSandboxPalette("Battle speed " + this.gameScreen.superSpeed + "x");
      }
''',
        "native HUD speed cycling",
    )
    methods = r'''      private function sandboxPaletteText(LABEL:String, X:Number, Y:Number, WIDTH:Number, HEIGHT:Number, SIZE:int = 11) : TextField
      {
         var text:TextField = new TextField();
         text.defaultTextFormat = new TextFormat("_sans",SIZE,16777215,true);
         text.text = LABEL;
         text.x = X;
         text.y = Y;
         text.width = WIDTH;
         text.height = HEIGHT;
         text.selectable = false;
         text.mouseEnabled = false;
         return text;
      }

      private function sandboxPaletteButton(LABEL:String, ACTION:String, X:Number, Y:Number, WIDTH:Number = 104) : Sprite
      {
         var button:Sprite = new Sprite();
         button.name = ACTION;
         button.x = X;
         button.y = Y;
         button.graphics.beginFill(1183245,0.97);
         button.graphics.lineStyle(1,13870409,0.95);
         button.graphics.drawRoundRect(0,0,WIDTH,32,8,8);
         button.graphics.endFill();
         button.addChild(this.sandboxPaletteText(LABEL,7,7,WIDTH - 14,20,10));
         button.buttonMode = true;
         button.mouseChildren = false;
         button.addEventListener(MouseEvent.CLICK,this.sandboxPaletteClick,false,0,true);
         return button;
      }

      private function installSandboxPalette() : void
      {
         this._sandboxButton = this.sandboxPaletteButton("SANDBOX","sandbox_toggle",704,14,132);
         addChild(this._sandboxButton);
         this._sandboxPanel = new Sprite();
         this._sandboxPanel.x = 600;
         this._sandboxPanel.y = 54;
         this._sandboxPanel.graphics.beginFill(460551,0.98);
         this._sandboxPanel.graphics.lineStyle(2,13870409,0.95);
         this._sandboxPanel.graphics.drawRoundRect(0,0,238,334,13,13);
         this._sandboxPanel.graphics.endFill();
         this._sandboxPanel.addChild(this.sandboxPaletteText("SUPER SANDBOX",13,10,210,25,15));
         this._sandboxStatus = this.sandboxPaletteText("",13,37,210,53,10);
         this._sandboxStatus.multiline = true;
         this._sandboxStatus.wordWrap = true;
         this._sandboxPanel.addChild(this._sandboxStatus);
         this._sandboxPanel.addChild(this.sandboxPaletteButton("PREV UNIT","sandbox_prev",11,92,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("NEXT UNIT","sandbox_next",123,92,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("SPAWN ALLY","sandbox_ally",11,130,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("SPAWN ENEMY","sandbox_enemy",123,130,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("BATCH","sandbox_batch",11,168,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("SPEED","sandbox_speed",123,168,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("+ GOLD","sandbox_gold",11,206,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("+ MANA","sandbox_mana",123,206,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("WIPE ENEMY","sandbox_wipe",11,244,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("INSTANT WIN","sandbox_win",123,244,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("POP SAFETY","sandbox_pop",11,282,104));
         this._sandboxPanel.addChild(this.sandboxPaletteButton("CLOSE","sandbox_close",123,282,104));
         addChild(this._sandboxPanel);
         this._sandboxPanel.visible = false;
         this.refreshSandboxPalette();
      }

      private function sandboxUnitName() : String
      {
         var names:Array = ["Miner","Swordwrath","Archidon","Spearton","Shadowrath","Albowtross","Meric","Magikill","Giant"];
         return String(names[this._sandboxUnitIndex]);
      }

      private function refreshSandboxPalette(MSG:String = "") : void
      {
         if(this._sandboxButton != null)
         {
            TextField(this._sandboxButton.getChildAt(0)).text = this._sandboxMode ? (this._sandboxPanel.visible ? "SANDBOX ON ▲" : "SANDBOX ON ▼") : "SANDBOX";
         }
         if(this._sandboxStatus != null)
         {
            this._sandboxStatus.text = this.sandboxUnitName().toUpperCase() + " • batch " + this._sandboxCount + " • speed " + this.gameScreen.superSpeed + "x\nPop safety " + (this._sandboxNoPop ? "OFF" : "ON") + (MSG == "" ? "" : "\n" + MSG);
         }
      }

      private function sandboxPaletteClick(evt:MouseEvent) : void
      {
         var action:String = Sprite(evt.currentTarget).name;
         if(action == "sandbox_toggle")
         {
            this._sandboxMode = true;
            this._sandboxPanel.visible = !this._sandboxPanel.visible;
            this.refreshSandboxPalette("Clickable controls ready");
            return;
         }
         if(action == "sandbox_close") { this._sandboxPanel.visible = false; this.refreshSandboxPalette(); return; }
         if(!this._sandboxMode) this._sandboxMode = true;
         if(action == "sandbox_prev") this._sandboxUnitIndex = (this._sandboxUnitIndex + 8) % 9;
         else if(action == "sandbox_next") this._sandboxUnitIndex = (this._sandboxUnitIndex + 1) % 9;
         else if(action == "sandbox_batch") this._sandboxCount = this._sandboxCount == 1 ? 5 : (this._sandboxCount == 5 ? 10 : (this._sandboxCount == 10 ? 20 : 1));
         else if(action == "sandbox_speed") this.gameScreen.superSpeed = this.gameScreen.superSpeed == 1 ? 2 : (this.gameScreen.superSpeed == 2 ? 4 : (this.gameScreen.superSpeed == 4 ? 8 : (this.gameScreen.superSpeed == 8 ? 12 : 1)));
         else if(action == "sandbox_gold") this.team.gold += 1000;
         else if(action == "sandbox_mana") this.team.mana += 1000;
         else if(action == "sandbox_pop") this._sandboxNoPop = !this._sandboxNoPop;
         else if(action == "sandbox_ally" || action == "sandbox_enemy")
         {
            var target:Team = action == "sandbox_ally" ? this.team : this.team.enemyTeam;
            var i:int = 0;
            while(i < this._sandboxCount)
            {
               this.spawnSuperUnit(this.sandboxTypeForKey(this._sandboxUnitIndex,target),target);
               i++;
            }
         }
         else if(action == "sandbox_wipe")
         {
            var victims:Array = this.team.enemyTeam.units.slice();
            for each(var victim:Unit in victims) if(victim.isAlive()) victim.damage(0,100000000,null);
         }
         else if(action == "sandbox_win") this.team.enemyTeam.statue.damage(0,100000000,null);
         this.refreshSandboxPalette(action == "sandbox_win" ? "Victory triggered" : "Updated");
      }

'''
    text = once(
        text,
        "      private function updateSuperControls() : void\n",
        methods + "      private function updateSuperControls() : void\n",
        "clickable sandbox methods",
    )
    text = once(
        text,
        "            this._sandboxMode = !this._sandboxMode;\n            this.helpMessage.showMessage(this._sandboxMode ? \"SUPER SANDBOX ON — 1-9 spawn, Shift enemy, G/M resources, B swarm, Delete clear\" : \"SUPER SANDBOX OFF\");\n",
        "            this._sandboxMode = !this._sandboxMode;\n            this._sandboxPanel.visible = this._sandboxMode;\n            this.refreshSandboxPalette(this._sandboxMode ? \"Keyboard + clickable controls ready\" : \"Sandbox disabled\");\n            this.helpMessage.showMessage(this._sandboxMode ? \"SUPER SANDBOX ON — clickable panel or keyboard shortcuts\" : \"SUPER SANDBOX OFF\");\n",
        "F2 palette synchronization",
    )
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    args = parser.parse_args()
    root = args.scripts / "com" / "brockw" / "stickwar"
    game_screen = root / "GameScreen.as"
    ui = root / "engine" / "UserInterface.as"
    patch_game_screen(game_screen)
    patch_ui(ui)
    for path, needles in {
        game_screen: ["private var _superSpeed", "superEffectiveSpeed", "public function get superSpeed"],
        ui: ["installSandboxPalette", '"INSTANT WIN"', "this.gameScreen.superSpeed", "SANDBOX ON ▲"],
    }.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path}")
    print("Super Stick War clickable sandbox + adaptive 1x/2x/4x/8x/12x speed applied")


if __name__ == "__main__":
    main()
