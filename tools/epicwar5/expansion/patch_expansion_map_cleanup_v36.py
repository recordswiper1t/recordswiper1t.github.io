#!/usr/bin/env python3
"""Epic War 5 Expansion V3.6 world-map cleanup patch.

Baseline: the exact released Expansion V3.5 binary. V3.5 safely deferred
Expansion battle construction to WorldMap.frameHandle, but it initialized the
battle before destroying the map. That lets the battle begin behind the map
display layer in Ruffle. V3.6 destroys the map first and then initializes the
queued battle with a saved GameFramework reference.
"""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_expansion_map_cleanup_v36.py <ffdec-export-root>")

path = Path(sys.argv[1]) / "scripts" / "Game" / "Interface" / "WorldMap.as"
if not path.is_file():
    raise SystemExit(f"missing {path}")

text = path.read_text(encoding="utf-8-sig")
old = """         if(this.expansionPendingStage > 0)
         {
            clip = new battle_mc();
            clip.init(this.mGF,this.expansionPendingStage);
            this.expansionPendingStage = 0;
            this.destroy();
            return;
         }
"""
new = """         if(this.expansionPendingStage > 0)
         {
            var expansionGame:* = this.mGF;
            var expansionStageId:int = this.expansionPendingStage;
            this.expansionPendingStage = 0;
            this.destroy();
            clip = new battle_mc();
            clip.init(expansionGame,expansionStageId);
            return;
         }
"""

matches = text.count(old)
if matches != 1:
    raise SystemExit(f"WorldMap deferred transition: expected 1 match, got {matches}")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8", newline="\n")
print("Epic War 5 Expansion V3.6 map-before-battle cleanup applied")

