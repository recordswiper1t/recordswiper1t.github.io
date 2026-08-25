#!/usr/bin/env python3
"""Epic War 5 V4.1 gameplay, Forge, controls and spatial-performance pass."""

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


def function_block(text: str, signature: str, next_signature: str) -> tuple[int, int, str]:
    start = text.index(signature)
    end = text.index(next_signature, start)
    return start, end, text[start:end]


def patch_spatial(path: Path) -> None:
    text = read(path)
    if "expansionSpatialCandidates" in text:
        return
    text = once(text, "   import flash.geom.ColorTransform;\n", "   import flash.geom.ColorTransform;\n   import flash.utils.getTimer;\n", "spatial timer import")
    text = once(
        text,
        "   public class CharacterBase extends MovieClip\n   {\n",
        """   public class CharacterBase extends MovieClip
   {

      private static var expansionSpatialBuckets:Object = {};

      private static var expansionSpatialStamp:int = -1000;

      private static var expansionSpatialCount:int = -1;

      private static var expansionSpatialContainer:Object = null;

      private static const EXPANSION_BUCKET_SIZE:int = 240;
""",
        "spatial fields",
    )
    helper = r'''      private function expansionSpatialCandidates(CENTER:Number,RADIUS:Number) : Array
      {
         var now:int = getTimer();
         var count:int = int(this.mGF.contUNIT.numChildren);
         var child:* = null;
         var key:int = 0;
         var bucket:Array = null;
         var i:int = 0;
         if(now - expansionSpatialStamp >= 80 || count != expansionSpatialCount || expansionSpatialContainer != this.mGF.contUNIT)
         {
            expansionSpatialBuckets = {};
            expansionSpatialStamp = now;
            expansionSpatialCount = count;
            expansionSpatialContainer = this.mGF.contUNIT;
            i = 0;
            while(i < count)
            {
               child = this.mGF.contUNIT.getChildAt(i);
               key = Math.floor(Number(child.x) / EXPANSION_BUCKET_SIZE);
               bucket = expansionSpatialBuckets[key] as Array;
               if(bucket == null) { bucket = []; expansionSpatialBuckets[key] = bucket; }
               bucket.push(child);
               i++;
            }
         }
         var result:Array = [];
         var first:int = Math.floor((CENTER - RADIUS) / EXPANSION_BUCKET_SIZE);
         var last:int = Math.floor((CENTER + RADIUS) / EXPANSION_BUCKET_SIZE);
         key = first;
         while(key <= last)
         {
            bucket = expansionSpatialBuckets[key] as Array;
            if(bucket != null) result = result.concat(bucket);
            key++;
         }
         return result;
      }

'''
    text = once(text, "      public function setHitRegen(VAL:int = 0) : Boolean\n", helper + "      public function setHitRegen(VAL:int = 0) : Boolean\n", "spatial helper")

    replacements = [
        ("      public function setHitRegen(", "      public function setHitTest(", "this.clip.x", "900"),
        ("      public function setHitTest(", "      public function setHitState(", "myClip.x", "900"),
        ("      public function getTargetInSightRange(", "      public function getTargetInHitBox(", "this._x_move_target_pos", "sight_range"),
        ("      public function getTargetInHitBox(", "      public function getTargetChildInHitBox(", "this.clip.x", "900"),
        ("      public function getTargetChildInHitBox(", "      public function getTargetAlignment(", "this.clip.x", "900"),
        ("      public function isTargetInHitBox(", "      public function isEnableDestroy(", "this.clip.x", "900"),
    ]
    for signature, next_signature, center, radius in replacements:
        start, end, block = function_block(text, signature, next_signature)
        old = """         var numChildren:int = int(this.mGF.contUNIT.numChildren);
         i = 0;
         while(i < numChildren)
         {
            child = this.mGF.contUNIT.getChildAt(i);
"""
        new = f"""         var expansionCandidates:Array = this.expansionSpatialCandidates({center},{radius});
         var numChildren:int = expansionCandidates.length;
         i = 0;
         while(i < numChildren)
         {{
            child = expansionCandidates[i];
"""
        if old not in block:
            raise SystemExit(f"{path.name} spatial loop anchor missing in {signature}")
        block = block.replace(old, new, 1)
        text = text[:start] + block + text[end:]
    write(path, text)


def patch_battle_system(path: Path) -> None:
    text = read(path)
    if "sandboxEffectiveRate" in text:
        return
    text = once(text, "      private var sandboxSpeedIndex:int = 0;\n", "      private var sandboxSpeedIndex:int = 0;\n      \n      private var sandboxEffectiveRate:int = 24;\n      \n      private var sandboxPanelBuilt:Boolean = false;\n", "Forge performance fields")
    text = once(
        text,
        """            previewClass = Class(getDefinitionByName(NAME + "_mc"));
            preview = new previewClass() as MovieClip;
""",
        """            var previewName:String = NAME == "gaia" ? "guardian" : NAME;
            previewClass = Class(getDefinitionByName(previewName + "_mc"));
            preview = new previewClass() as MovieClip;
""",
        "preview aliases",
    )
    text = once(
        text,
        """         title = this.sandboxText(NAME.toUpperCase(),10,16774620,110,18,3,84);
         title.defaultTextFormat = new TextFormat("_sans",10,16774620,true,null,null,null,null,null,"center");
         card.addChild(title);
""",
        """         title = this.sandboxText(NAME.toUpperCase(),10,16774620,110,18,3,80);
         title.defaultTextFormat = new TextFormat("_sans",10,16774620,true,null,null,null,null,null,"center");
         card.addChild(title);
         var role:TextField = this.sandboxText(this.sandboxUnitRole(NAME),8,13877213,110,15,3,94);
         role.defaultTextFormat = new TextFormat("_sans",8,13877213,true,null,null,null,null,null,"center");
         card.addChild(role);
""",
        "Forge roles",
    )
    role_helper = r'''      private function sandboxUnitRole(NAME:String) : String
      {
         if(NAME == "wizard" || NAME == "witch" || NAME == "lich" || NAME == "diablos") return "MAGIC • CONTROL";
         if(NAME == "elf" || NAME == "dwarf" || NAME == "dwarfenginer" || NAME == "bomber") return "RANGED • SUPPORT";
         if(NAME == "dragon" || NAME == "phoenix" || NAME == "angel" || NAME == "succubus") return "AIR • ASSAULT";
         if(NAME == "gaia" || NAME == "golem" || NAME == "troll" || NAME == "tank") return "TANK • GUARD";
         if(NAME.indexOf("hero") == 0 || NAME == "baal" || NAME == "devil") return "HERO • LEGEND";
         return "MELEE • ASSAULT";
      }

'''
    text = once(text, "      private function sandboxPanelStatus(MSG:String = \"\") : String\n", role_helper + "      private function sandboxPanelStatus(MSG:String = \"\") : String\n", "Forge role helper")
    text = text.replace(
        'return name + "  •  batch " + this.sandboxCount + "  •  mana +" + this.sandboxManaAmount + "  •  speed " + this.sandboxSpeedText() +',
        'return name + "  •  " + this.sandboxUnitRole(String(this.sandboxNames[this.sandboxIndex])) + "  •  batch " + this.sandboxCount + "  •  speed " + this.sandboxSpeedText() +',
        1,
    )
    text = once(text, "         this.mGF.stageRoot.stage.frameRate = rate;\n", "         this.sandboxEffectiveRate = rate;\n         this.mGF.stageRoot.stage.frameRate = rate;\n", "effective rate capture")
    old_speed = '         return this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "2x" : (this.sandboxSpeedIndex == 2 ? "4x" : (this.sandboxSpeedIndex == 3 ? "6x" : "8x")));\n'
    new_speed = '         var requested:String = this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "2x" : (this.sandboxSpeedIndex == 2 ? "4x" : (this.sandboxSpeedIndex == 3 ? "6x" : "8x")));\n         var effective:String = String(Math.max(1,int(this.sandboxEffectiveRate / 24))) + "x";\n         return requested == effective ? requested : requested + "→" + effective;\n'
    text = once(text, old_speed, new_speed, "truthful speed label")

    refresh_start, refresh_end, _ = function_block(text, "      private function sandboxRefresh", "      private function sandboxCycle")
    refresh = r'''      private function sandboxRefresh(MSG:String = "") : void
      {
         if(this.sandboxPanel == null || this.sandboxToggleButton == null) return;
         this.sandboxPanel.visible = sandboxMaster && this.sandboxHudVisible;
         TextField(this.sandboxToggleButton.getChildAt(0)).text = sandboxMaster ? (this.sandboxHudVisible ? "FORGE OPEN" : "BATTLE FORGE") : "BATTLE FORGE";
         if(!this.sandboxPanel.visible) return;
         var structural:Boolean = !this.sandboxPanelBuilt || MSG.indexOf("Selected") == 0 || MSG.indexOf("Roster") == 0 || MSG.indexOf("Batch") == 0;
         if(structural)
         {
            this.sandboxRenderPanel(MSG);
            this.sandboxPanelBuilt = true;
         }
         else if(this.sandboxStatus != null)
         {
            this.sandboxStatus.text = this.sandboxPanelStatus(MSG);
         }
      }

'''
    text = text[:refresh_start] + refresh + text[refresh_end:]

    text = once(
        text,
        """         if(this.mGF.keyMgr.getKeyPress().KEY_7)
         {
            this.playerMgr.selectGroupUnit(7);
         }
""",
        """         if(this.mGF.keyMgr.getKeyPress().KEY_7)
         {
            this.playerMgr.selectGroupUnit(7);
         }
         if(this.mGF.keyMgr.getKeyPress().KEY_8) this.playerMgr.selectGroupUnit(8);
         if(this.mGF.keyMgr.getKeyPress().KEY_9) this.playerMgr.selectGroupUnit(9);
         if(this.mGF.keyMgr.getKeyPress().KEY_0) this.playerMgr.selectGroupUnit(10);
         if(this.mGF.keyMgr.getKeyHold().KEY_SHIFT && this.mGF.keyMgr.getKeyPress().KEY_1) this.playerMgr.selectGroupUnit(11);
         if(this.mGF.keyMgr.getKeyHold().KEY_SHIFT && this.mGF.keyMgr.getKeyPress().KEY_2) this.playerMgr.selectGroupUnit(12);
""",
        "slots 8-12 hotkeys",
    )
    write(path, text)


AUTHORED = r'''         // V4.1 authored encounter layer: each expedition changes the battlefield,
         // not merely the health multiplier.
         switch(tier)
         {
            case 1: this.bSys.charMgr.createEnemyUnit("unit","goblinred",900,0,50,eliteHP,eliteATK,"fire",1.1); break;
            case 2: this.bSys.charMgr.createEnemyUnit("object","towerarrow",1500,0,50,portalHP); this.bSys.charMgr.createEnemyUnit("object","towerice",2050,0,50,portalHP); break;
            case 3: this.bSys.charMgr.createEnemyPortal("portalcave",850,53,portalHP,0,"goblin",4); break;
            case 4: this.bSys.charMgr.createEnemyUnit("unit","bomber",1000,0,50,eliteHP,eliteATK,"fire",1.2); this.bSys.charMgr.createEnemyUnit("unit","bomber",1350,0,50,eliteHP,eliteATK,"fire",1.2); break;
            case 5: this.bSys.charMgr.createEnemyUnit("object","wall2",1700,0,50,int(portalHP * 1.8)); break;
            case 6: this.bSys.charMgr.createEnemyPortal("portalwarp",900,53,portalHP,0,"mystic",5); break;
            case 7: this.bSys.charMgr.createEnemyUnit("boss","troll",1300,0,50,int(bossHP * 0.38),int(bossATK * 0.7),"",1); break;
            case 8: this.bSys.charMgr.createEnemyUnit("object","towerfire",1200,0,50,portalHP); this.bSys.charMgr.createEnemyUnit("object","towerthunder",1900,0,50,portalHP); break;
            case 9: this.bSys.charMgr.createEnemyPortal("portalhell",750,53,portalHP,0,"brute",4); this.bSys.charMgr.createEnemyPortal("portalcave",1450,53,portalHP,0,"goblin",5); break;
            case 10: this.bSys.charMgr.createEnemyUnit("boss","phoenix",1200,0,50,int(bossHP * 0.45),int(bossATK * 0.65),"fire",1); break;
            case 11: this.bSys.charMgr.createEnemyUnit("unit","succubus",900,0,50,eliteHP,eliteATK,"dark",1.3); this.bSys.charMgr.createEnemyUnit("unit","vampire",1400,0,50,eliteHP,eliteATK,"dark",1.2); break;
            case 12: this.bSys.charMgr.createEnemyUnit("object","towerice",1000,0,50,portalHP); this.bSys.charMgr.createEnemyUnit("object","wall2",1600,0,50,int(portalHP * 1.5)); break;
            case 13: this.bSys.charMgr.createEnemyPortal("portalwarp",750,53,portalHP,0,"archer",5); this.bSys.charMgr.createEnemyPortal("portalhell",1750,53,portalHP,0,"mystic",5); break;
            case 14: this.bSys.charMgr.createEnemyUnit("boss","anubis",1100,0,50,int(bossHP * 0.5),int(bossATK * 0.75),"poison",1); break;
            case 15: this.bSys.charMgr.createEnemyUnit("object","towerthunder",900,0,50,portalHP); this.bSys.charMgr.createEnemyUnit("object","towerfire",1450,0,50,portalHP); this.bSys.charMgr.createEnemyUnit("object","towerice",2000,0,50,portalHP); break;
            case 16: this.bSys.charMgr.createEnemyPortal("portalcave",700,53,portalHP,0,"giant",3); break;
            case 17: this.bSys.charMgr.createEnemyUnit("boss","gaia",1250,0,50,int(bossHP * 0.55),int(bossATK * 0.7),"ice",1); break;
            case 18: this.bSys.charMgr.createEnemyUnit("object","wall2",1100,0,50,int(portalHP * 2)); this.bSys.charMgr.createEnemyUnit("object","wall2",1850,0,50,int(portalHP * 2)); break;
            case 19: this.bSys.charMgr.createEnemyPortal("portalhell",650,53,portalHP,0,"brute",5); this.bSys.charMgr.createEnemyPortal("portalwarp",1350,53,portalHP,0,"bomber",5); break;
            case 20: this.bSys.charMgr.createEnemyUnit("boss","dragon",1050,0,50,int(bossHP * 0.6),int(bossATK * 0.78),"fire",1); break;
            case 21: this.bSys.charMgr.createEnemyUnit("unit","angelevil",800,0,50,int(eliteHP * 1.6),int(eliteATK * 1.2),"dark",1.4); break;
            case 22: this.bSys.charMgr.createEnemyUnit("object","towerfire",800,0,50,int(portalHP * 1.5)); this.bSys.charMgr.createEnemyUnit("object","towerthunder",1400,0,50,int(portalHP * 1.5)); this.bSys.charMgr.createEnemyUnit("object","towerice",2000,0,50,int(portalHP * 1.5)); break;
            case 23: this.bSys.charMgr.createEnemyPortal("portalhell",600,53,int(portalHP * 1.4),0,"giant",4); this.bSys.charMgr.createEnemyPortal("portalwarp",1300,53,int(portalHP * 1.4),0,"mystic",5); break;
            case 24: this.bSys.charMgr.createEnemyUnit("boss","baal",1000,0,50,int(bossHP * 0.7),int(bossATK * 0.82),"fire",1); break;
            case 25: this.bSys.charMgr.createEnemyUnit("boss","gaia",900,0,50,int(bossHP * 0.45),int(bossATK * 0.72),"thunder",1); this.bSys.charMgr.createEnemyUnit("boss","dragon",1500,0,50,int(bossHP * 0.45),int(bossATK * 0.72),"fire",1); break;
         }
'''


def patch_encounters(path: Path) -> None:
    text = read(path)
    if "V4.1 authored encounter layer" in text:
        return
    anchor = """         this.eWave3.init(String(waveNames[(index + 5) % waveNames.length]),Math.min(5,3 + int(tier / 6)),Math.max(2,12 - int(tier / 3)));
         var waveCap:int = Math.min(22,16 + int(tier / 4));
"""
    text = once(text, anchor, "         this.eWave3.init(String(waveNames[(index + 5) % waveNames.length]),Math.min(5,3 + int(tier / 6)),Math.max(2,12 - int(tier / 3)));\n" + AUTHORED + "         var waveCap:int = Math.min(22,16 + int(tier / 4));\n", "authored encounters")
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_root", type=Path)
    args = parser.parse_args()
    base = args.export_root / "scripts" / "Game"
    character = base / "System" / "GameObject" / "Character" / "CharacterBase.as"
    battle = base / "System" / "Battle" / "BattleSystem.as"
    enemy = base / "System" / "Battle" / "BattleControlEnemy.as"
    patch_spatial(character)
    patch_battle_system(battle)
    patch_encounters(enemy)
    checks = {
        character: ["expansionSpatialCandidates", "EXPANSION_BUCKET_SIZE", "expansionCandidates"],
        battle: ["sandboxEffectiveRate", "sandboxUnitRole", 'previewName:String = NAME == "gaia"', "selectGroupUnit(12)", "sandboxPanelBuilt"],
        enemy: ["V4.1 authored encounter layer", "case 25:", 'createEnemyUnit("boss","gaia"'],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path}")
    print("Epic War 5 V4.1 gameplay, Forge, 12-slot controls and spatial performance applied")


if __name__ == "__main__":
    main()
