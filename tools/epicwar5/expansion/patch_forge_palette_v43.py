#!/usr/bin/env python3
"""Epic War 5 Expansion V4.3 Battle Forge palette correction."""
from pathlib import Path
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: patch_forge_palette_v43.py <ffdec-export-root>")

path = Path(sys.argv[1]) / "scripts" / "Game" / "System" / "Battle" / "BattleSystem.as"
text = path.read_text(encoding="utf-8-sig")


def once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, got {count}")
    text = text.replace(old, new, 1)


# Dark iron/wood surfaces, bronze framing, crimson selection and parchment text.
once("button.graphics.lineStyle(2,11377354,1);", "button.graphics.lineStyle(2,12094020,1);", "button bronze frame")
once("button.graphics.beginFill(4203014,0.99);", "button.graphics.beginFill(3875868,0.99);", "button dark wood")
once("button.graphics.lineStyle(1,15837487,0.55);", "button.graphics.lineStyle(1,7754545,0.72);", "button inner bevel")
once(
    "card.graphics.lineStyle(selected ? 4 : 2,selected ? 16763904 : 8272407,1);",
    "card.graphics.lineStyle(selected ? 4 : 2,selected ? 15779690 : 7754545,1);",
    "card bronze frame",
)
once(
    "card.graphics.beginFill(selected ? 5387546 : 2169361,0.98);",
    "card.graphics.beginFill(selected ? 5906458 : 2365972,0.98);",
    "card crimson/dark fill",
)
once("card.graphics.beginFill(16763904,0.9);", "card.graphics.beginFill(12094020,0.9);", "selected card crest")
once("this.sandboxPanel.graphics.lineStyle(4,11377354,1);", "this.sandboxPanel.graphics.lineStyle(4,12094020,1);", "panel bronze frame")
once("this.sandboxPanel.graphics.beginFill(1111560,0.985);", "this.sandboxPanel.graphics.beginFill(1512207,0.985);", "panel dark iron")
once("this.sandboxPanel.graphics.lineStyle(2,15837487,0.72);", "this.sandboxPanel.graphics.lineStyle(2,7754545,0.9);", "panel inner bronze")
once(
    'this.sandboxPanel.addChild(this.sandboxText("BATTLE FORGE",20,16763904,250,27,18,12));',
    'this.sandboxPanel.addChild(this.sandboxText("BATTLE FORGE",20,15779690,250,27,18,12));',
    "Forge gold title",
)
once(
    "this.sandboxStatus = this.sandboxText(this.sandboxPanelStatus(MSG),10,15856113,514,43,18,276);",
    "this.sandboxStatus = this.sandboxText(this.sandboxPanelStatus(MSG),10,15193261,514,43,18,276);",
    "Forge parchment status",
)

path.write_text(text, encoding="utf-8", newline="\n")

for marker in ("beginFill(1512207,0.985)", "lineStyle(4,12094020,1)", "selected ? 5906458 : 2365972", "10,15193261,514"):
    if marker not in text:
        raise SystemExit(f"validation failed: {marker}")

print("Epic War 5 Expansion V4.3 dark bronze/crimson Forge palette applied")
