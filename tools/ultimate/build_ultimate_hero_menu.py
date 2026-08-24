#!/usr/bin/env python3
"""Add nine source-ready KR1 heroes to the enhanced Frontiers sandbox.

The existing Frontiers hero system remains authoritative. KR1 publisher heroes
are optional extra heroes, default OFF, and are resolved by class name so this
patch still compiles on an unmerged V11/V12 SWF. Hacksaw, Oni, Thor and Ten'Shí
remain locked in scope but are not exposed until compatible source exists.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

KRF = [
    ("alric","Alric"),("mirage","Mirage"),("captain","Blackthorne"),
    ("cronan","Cronan"),("shatra","Sha'tra"),("grawl","Grawl"),
    ("nivus","Nivus"),("dierdre","Dierdre"),("ashbite","Ashbite"),
    ("rurin","Rurin Longbeard"),
]
KR1 = [
    ("kr1_gerald","Gerald","KR1__SoldierHeroGerald"),
    ("kr1_alleria","Alleria","KR1__SoldierHeroAlleria"),
    ("kr1_malik","Malik","KR1__SoldierHeroMalik"),
    ("kr1_bolin","Bolin","KR1__SoldierHeroBolin"),
    ("kr1_magnus","Magnus","KR1__SoldierHeroMagnus"),
    ("kr1_ignus","Ignus","KR1__SoldierHeroIgnus"),
    ("kr1_denas","King Denas","KR1__SoldierHeroDenas"),
    ("kr1_elora","Elora","KR1__SoldierHeroFrost"),
    ("kr1_ingvar","Ingvar","KR1__SoldierHeroViking"),
]
PAGE_SIZE=8


def read(p:Path)->str:
    if not p.is_file(): raise SystemExit(f"missing source: {p}")
    return p.read_text(encoding="utf-8-sig")

def write(p:Path,s:str)->None:
    p.write_text(s,encoding="utf-8",newline="\n")

def rep(s:str,old:str,new:str,label:str)->str:
    n=s.count(old)
    if n!=1: raise SystemExit(f"{label}: expected 1 anchor, found {n}")
    return s.replace(old,new,1)

def replace_function(s:str,signature:str,replacement:str,label:str)->str:
    start=s.find(signature)
    if start<0: raise SystemExit(f"{label}: signature missing")
    brace=s.find("{",start); depth=0; i=brace; ins=False; esc=False; q=""
    while i<len(s):
        c=s[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c==q: ins=False
        else:
            if c in ('"',"'"): ins=True; q=c
            elif c=="{": depth+=1
            elif c=="}":
                depth-=1
                if depth==0: return s[:start]+replacement+s[i+1:]
        i+=1
    raise SystemExit(f"{label}: unterminated")


def patch(s:str)->tuple[str,dict]:
    if "private function ultimateMakeKR1Hero" in s:
        return s,{"already_patched":True,"kr1_ready":9}

    s=rep(s,"      private var qolEnemyPage:int = 0;\n",
          "      private var qolEnemyPage:int = 0;\n      \n      private var qolHeroPage:int = 0;\n",
          "hero page state")

    rows=KRF+[(k,t) for k,t,_ in KR1]
    row_literal=",".join('["%s","%s"]'%(k,t.replace('"','\\"')) for k,t in rows)
    old='''         else if(this.qolSettingsPage == 2)\n         {\n            this.qolEnsureHeroSelection();\n            this.qolSettings.addChild(this.qolLabel("HEROES",28,16,22));\n            var heroNames:Array = [["alric","Alric"],["mirage","Mirage"],["captain","Blackthorne"],["cronan","Cronan"],["shatra","Sha\\'tra"],["grawl","Grawl"],["nivus","Nivus"],["dierdre","Dierdre"],["ashbite","Ashbite"],["rurin","Rurin Longbeard"]];\n            var hi:int = 0;\n            while(hi < heroNames.length)\n            {\n               this.qolSettings.addChild(this.qolButton(this.qolHeroLabel(heroNames[hi][0],heroNames[hi][1]),hi % 2 == 0 ? 28 : 302,72 + int(hi / 2) * 47,250,"hero_" + heroNames[hi][0]));\n               hi++;\n            }\n            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();\n            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL HEROES OFF" : "TURN ALL HEROES ON",28,320,524,"heroes_all"));\n            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES NOW",28,374,250,"heroes_remove"));\n            this.qolSettings.addChild(this.qolButton("← Dashboard",302,374,250,"page_main"));\n         }\n'''
    new=f'''         else if(this.qolSettingsPage == 2)\n         {{\n            this.qolEnsureHeroSelection();\n            var heroNames:Array = [{row_literal}];\n            var heroPages:int = Math.ceil(heroNames.length / {PAGE_SIZE});\n            this.qolHeroPage = Math.max(0,Math.min(heroPages - 1,this.qolHeroPage));\n            this.qolSettings.addChild(this.qolLabel("HEROES — PAGE " + (this.qolHeroPage + 1) + "/" + heroPages,28,16,22));\n            var heroFirst:int = this.qolHeroPage * {PAGE_SIZE};\n            var hi:int = 0;\n            while(hi < {PAGE_SIZE} && heroFirst + hi < heroNames.length)\n            {{\n               var heroRow:Array = heroNames[heroFirst + hi] as Array;\n               this.qolSettings.addChild(this.qolButton(this.qolHeroLabel(String(heroRow[0]),String(heroRow[1])),hi % 2 == 0 ? 28 : 302,68 + int(hi / 2) * 47,250,"hero_" + String(heroRow[0])));\n               hi++;\n            }}\n            this.qolSettings.addChild(this.qolButton("← Hero page",28,264,150,"hero_page_prev"));\n            this.qolSettings.addChild(this.qolButton("Hero page →",402,264,150,"hero_page_next"));\n            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();\n            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL HEROES OFF" : "TURN ALL HEROES ON",28,318,524,"heroes_all"));\n            this.qolSettings.addChild(this.qolLabel("KR1 heroes default OFF; Hacksaw / Oni / Thor / Ten'Shí need later source.",28,369,13));\n            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES NOW",28,400,250,"heroes_remove"));\n            this.qolSettings.addChild(this.qolButton("← Dashboard",302,400,250,"page_main"));\n         }}\n'''
    s=rep(s,old,new,"hero settings page")

    # Page actions MUST precede the generic hero_* handler because their names
    # themselves begin with hero_.
    generic='''         else if(action.indexOf("hero_") == 0) this.qolToggleHero(action.substr(5));\n'''
    generic_braced='''         else if(action.indexOf("hero_") == 0)\n         {\n            this.qolToggleHero(action.substr(5));\n         }\n'''
    if generic in s: anchor=generic
    elif generic_braced in s: anchor=generic_braced
    else: raise SystemExit("generic hero click handler missing")
    paging=f'''         else if(action == "hero_page_prev")\n         {{\n            this.qolHeroPage = (this.qolHeroPage + Math.ceil({len(rows)} / {PAGE_SIZE}) - 1) % Math.ceil({len(rows)} / {PAGE_SIZE});\n         }}\n         else if(action == "hero_page_next")\n         {{\n            this.qolHeroPage = (this.qolHeroPage + 1) % Math.ceil({len(rows)} / {PAGE_SIZE});\n         }}\n'''
    s=rep(s,anchor,paging+anchor,"hero pagination action ordering")

    cases="\n".join(f'''            case "{k}":\n               return this.ultimateMakeKR1Hero("{cls}",p);''' for k,_t,cls in KR1)
    factory=f'''      private function ultimateMakeKR1Hero(param1:String, param2:Point) : §dynamic const class§\n      {{\n         var heroClass:Class = null;\n         var candidate:Object = null;\n         try {{ heroClass = Class(getDefinitionByName(param1)); }}\n         catch(errorLookup:Error) {{ return null; }}\n         try {{ candidate = new heroClass(param2,param2,null,param2); }}\n         catch(errorFour:Error)\n         {{\n            try {{ candidate = new heroClass(param2,param2,null); }}\n            catch(errorThree:Error)\n            {{\n               try {{ candidate = new heroClass(param2,param2); }}\n               catch(errorTwo:Error) {{ return null; }}\n            }}\n         }}\n         return candidate is §dynamic const class§ ? §dynamic const class§(candidate) : null;\n      }}\n      \n      private function qolMakeHero(param1:String, param2:int) : §dynamic const class§\n      {{\n         var p:Point = new Point(this.§_-R4§[0].x + param2 % 3 * 28 - 28,this.§_-R4§[0].y + int(param2 / 3) * 28);\n         switch(param1)\n         {{\n            case "alric": return new SoldierHeroAlric(p,p,null,p);\n            case "mirage": return new SoldierHeroMirage(p,p,null,p);\n            case "captain": return new SoldierHeroCaptain(p,p,null,p);\n            case "cronan": return new SoldierHeroCronan(p,p,null,p);\n            case "shatra": return new SoldierHeroAlien(p,p,null,p);\n            case "grawl": return new §else const static§(p,p,null,p);\n            case "nivus": return new SoldierHeroNivus(p,p,null,p);\n            case "dierdre": return new SoldierHeroDierdre(p,p,null,p);\n            case "ashbite": return new SoldierHeroDragon(p,p,null,p);\n            case "rurin": return new §switch for super§(p,p,null,p);\n{cases}\n            default: return null;\n         }}\n      }}\n'''
    s=replace_function(s,"      private function qolMakeHero(param1:String, param2:int) : §dynamic const class§\n",factory,"hero factory")

    legacy='var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"];'
    combined='var roster:Array = ['+','.join('"'+k+'"' for k,_ in KRF)+','+','.join('"'+k+'"' for k,_t,_c in KR1)+'];'
    if s.count(legacy)!=2: raise SystemExit(f"hero roster arrays: expected 2, found {s.count(legacy)}")
    s=s.replace(legacy,combined,1) # spawn extras

    ensure='''var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"];\n         for each(var heroName in roster)\n         {\n            Level.qolHeroEnabled[heroName] = true;\n         }'''
    ensure_new=ensure+'''\n         var kr1Roster:Array = ['''+','.join('"'+k+'"' for k,_t,_c in KR1)+'''];\n         for each(heroName in kr1Roster)\n         {\n            Level.qolHeroEnabled[heroName] = false;\n         }'''
    s=rep(s,ensure,ensure_new,"KR1 default-off hero state")

    return s,{"already_patched":False,"frontiers_toggles":10,"kr1_ready":9,"toggle_total":19,"pages":3,"kr1_default_on":False}


def main()->None:
    p=argparse.ArgumentParser(); p.add_argument("scripts",type=Path); p.add_argument("--report",type=Path)
    a=p.parse_args(); path=a.scripts/"Level.as"; text,stats=patch(read(path)); write(path,text)
    result={"stats":stats,"kr1_ready":[{"key":k,"title":t,"runtime_class":c} for k,t,c in KR1],
            "later_or_missing":["Hacksaw","Oni","Thor","Ten'Shí"],
            "primary_hero_persistence_changed":False,
            "runtime_compatibility_requires_merged_probe":True}
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
