#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: add-v6-lives.py <exported-scripts-dir>")

scripts = Path(sys.argv[1])
level_path = scripts / "Level.as"
if not level_path.exists():
    raise SystemExit(f"missing exported script: {level_path}")

level = level_path.read_text(encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    return text.replace(old, new, 1)


# Add a second numeric input next to the existing cash/gold input state.
level = replace_once(
    level,
    "      private var qolGoldInput:TextField;",
    "      private var qolGoldInput:TextField;\n      \n      private var qolLivesInput:TextField;",
    "lives input state",
)

# Make enough vertical room for a full lives row and relabel the page as V6.
level = replace_once(
    level,
    "this.qolSettings.graphics.drawRoundRect(0,0,580,455,18,18);",
    "this.qolSettings.graphics.drawRoundRect(0,0,580,515,18,18);",
    "settings panel height",
)
level = replace_once(
    level,
    'this.qolSettings.addChild(this.qolLabel("V4 LEVEL SETTINGS",28,20,24));',
    'this.qolSettings.addChild(this.qolLabel("V6 LEVEL SETTINGS",28,20,24));',
    "settings title",
)

old_controls = '''            this.qolSettings.addChild(this.qolLabel("Add gold:",28,142,18));
            this.qolGoldInput = this.qolInput("0",130,130,215);
            this.qolSettings.addChild(this.qolGoldInput);
            this.qolSettings.addChild(this.qolButton("ADD",360,130,192,"gold_add"));
            this.qolSettings.addChild(this.qolButton("Hero selection  →",28,202,250,"page_heroes"));
            this.qolSettings.addChild(this.qolButton(this.qolSendAllPending ? "Sending all waves…" : "Send all waves",302,202,250,"all_waves"));
            this.qolSettings.addChild(this.qolButton("Enemy tools  →",28,262,250,"page_enemy"));
            this.qolSettings.addChild(this.qolButton("Hide V4 tools",302,262,250,"hide"));
            this.qolSettings.addChild(this.qolButton("Unlimited: " + (this.qolUnlimitedMode ? "ON" : "OFF"),28,322,250,"unlimited"));
            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,322,250,"instant_win"));
            this.qolSettings.addChild(this.qolLabel("Send-all pauses new waves while the board is overloaded.",28,382,14));'''

new_controls = '''            this.qolSettings.addChild(this.qolLabel("Add gold:",28,142,18));
            this.qolGoldInput = this.qolInput("0",130,130,215);
            this.qolSettings.addChild(this.qolGoldInput);
            this.qolSettings.addChild(this.qolButton("ADD",360,130,192,"gold_add"));
            this.qolSettings.addChild(this.qolLabel("Add lives:",28,202,18));
            this.qolLivesInput = this.qolInput("0",130,190,215);
            this.qolSettings.addChild(this.qolLivesInput);
            this.qolSettings.addChild(this.qolButton("ADD",360,190,192,"lives_add"));
            this.qolSettings.addChild(this.qolButton("Hero selection  →",28,262,250,"page_heroes"));
            this.qolSettings.addChild(this.qolButton(this.qolSendAllPending ? "Sending all waves…" : "Send all waves",302,262,250,"all_waves"));
            this.qolSettings.addChild(this.qolButton("Enemy tools  →",28,322,250,"page_enemy"));
            this.qolSettings.addChild(this.qolButton("Hide V6 tools",302,322,250,"hide"));
            this.qolSettings.addChild(this.qolButton("Unlimited: " + (this.qolUnlimitedMode ? "ON" : "OFF"),28,382,250,"unlimited"));
            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,382,250,"instant_win"));
            this.qolSettings.addChild(this.qolLabel("Send-all pauses new waves while the board is overloaded.",28,442,14));'''
level = replace_once(level, old_controls, new_controls, "settings lives row")

old_action = '''         else if(action == "gold_add")
         {
            var amount:Number = this.qolGoldInput == null ? 0 : Number(this.qolGoldInput.text);
            if(isNaN(amount) || amount < 0)
            {
               amount = 0;
            }
            this.updateCash(int(Math.min(2000000000,amount)));
         }
         else if(action == "trees_toggle")'''

new_action = '''         else if(action == "gold_add")
         {
            var amount:Number = this.qolGoldInput == null ? 0 : Number(this.qolGoldInput.text);
            if(isNaN(amount) || amount < 0)
            {
               amount = 0;
            }
            this.updateCash(int(Math.min(2000000000,amount)));
         }
         else if(action == "lives_add")
         {
            var livesAmount:Number = this.qolLivesInput == null ? 0 : Number(this.qolLivesInput.text);
            if(isNaN(livesAmount) || livesAmount < 0)
            {
               livesAmount = 0;
            }
            this.lives = int(Math.min(2000000000,Number(this.lives) + livesAmount));
            if(this.§_-rd§ != null)
            {
               this.§_-rd§.updateLives(this.lives);
            }
         }
         else if(action == "trees_toggle")'''
level = replace_once(level, old_action, new_action, "lives add action")

checks = [
    "private var qolLivesInput:TextField;",
    'qolLabel("Add lives:",28,202,18)',
    'qolButton("ADD",360,190,192,"lives_add")',
    'else if(action == "lives_add")',
    "this.§_-rd§.updateLives(this.lives);",
    'qolLabel("V6 LEVEL SETTINGS",28,20,24)',
    'qolButton("Hide V6 tools",302,322,250,"hide")',
]
for needle in checks:
    if needle not in level:
        raise SystemExit(f"validation failed: {needle!r} missing from Level.as")

level_path.write_text(level, encoding="utf-8", newline="\n")
print("V6 lives settings patch applied successfully")
