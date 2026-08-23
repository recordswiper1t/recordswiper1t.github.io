#!/usr/bin/env python3
"""Epic War 5 Expansion V3.5 direct-entry patch.

The expansion-specific web launcher may expose stage 26 immediately without
rewriting campaign saves. Normal/native progression still requires the stock
12 story + 8 extra clears because the opt-in is delivered as a FlashVar.
"""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_direct_expansion_v35.py <ffdec-export-root>")

path = Path(sys.argv[1]) / "scripts" / "Game" / "Interface" / "WorldMap.as"
text = path.read_text(encoding="utf-8-sig")

def once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, got {count}")
    text = text.replace(old, new, 1)

helper = '''      private function expansionDirectAvailable() : Boolean
      {
         if(this.mGF.datMgr.expansionOriginalCampaignComplete())
         {
            return true;
         }
         try
         {
            var rootClip:* = this.mGF.stageRoot.root;
            if(rootClip != null && rootClip.loaderInfo != null && String(rootClip.loaderInfo.parameters.ew5ExpansionDirect) == "1")
            {
               return true;
            }
         }
         catch(error:Error)
         {
         }
         return false;
      }
      
'''
count = text.count("this.mGF.datMgr.expansionOriginalCampaignComplete()")
if count != 3:
    raise SystemExit(f"availability callsites: expected 3 matches, got {count}")
text = text.replace("this.mGF.datMgr.expansionOriginalCampaignComplete()", "this.expansionDirectAvailable()")
once("      private function expansionInstallButton() : void\n", helper + "      private function expansionInstallButton() : void\n", "direct-entry helper")

path.write_text(text, encoding="utf-8", newline="\n")

for marker in ("expansionDirectAvailable", "parameters.ew5ExpansionDirect", "this.expansionPendingStage = 100 + id"):
    if marker not in text:
        raise SystemExit(f"missing {marker}")
print("Epic War 5 Expansion V3.5 direct-entry patch applied")
