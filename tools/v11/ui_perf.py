#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit("usage: patch.py <scripts-dir>")
scripts=Path(sys.argv[1])
def read(name): return (scripts/name).read_text(encoding="utf-8-sig")
def write(name,text): (scripts/name).write_text(text,encoding="utf-8",newline="\n")
def replace_once(text,old,new,label):
 n=text.count(old)
 if n!=1: raise SystemExit(f"{label}: expected 1 match, found {n}")
 return text.replace(old,new,1)
def replace_function(text,signature,replacement,label):
 start=text.find(signature)
 if start<0: raise SystemExit(f"{label}: signature missing")
 brace=text.find("{",start); depth=0; i=brace; ins=False; esc=False; q=""
 while i<len(text):
  c=text[i]
  if ins:
   if esc: esc=False
   elif c=="\\": esc=True
   elif c==q: ins=False
  else:
   if c in ("\"","'"): ins=True; q=c
   elif c=="{": depth+=1
   elif c=="}":
    depth-=1
    if depth==0: return text[:start]+replacement+text[i+1:]
  i+=1
 raise SystemExit(f"{label}: unterminated")

level=read('Level.as')
render=r'''      private function qolRenderSettings() : void
      {
         if(this.qolSettings == null) return;
         while(this.qolSettings.numChildren > 0) this.qolSettings.removeChildAt(0);
         this.qolSettings.graphics.clear();
         this.qolSettings.graphics.beginFill(1118481,0.97);
         this.qolSettings.graphics.lineStyle(2,13983051,0.8);
         this.qolSettings.graphics.drawRoundRect(0,0,580,515,18,18);
         this.qolSettings.graphics.endFill();
         this.qolSettings.addChild(this.qolLabel(this.qolStatusText(),28,48,13));
         if(this.qolSettingsPage == 0)
         {
            this.qolSettings.addChild(this.qolLabel("V11 SANDBOX",28,16,24));
            this.qolSettings.addChild(this.qolButton("Heroes",28,78,250,"page_heroes"));
            this.qolSettings.addChild(this.qolButton("Enemies",302,78,250,"page_enemy"));
            this.qolSettings.addChild(this.qolButton("Waves / Time Attack",28,136,250,"page_waves"));
            this.qolSettings.addChild(this.qolButton("Towers / Clipboard",302,136,250,"page_towers"));
            this.qolSettings.addChild(this.qolButton("Cheats / Cleanup",28,194,250,"page_cheats"));
            this.qolSettings.addChild(this.qolButton("Performance",302,194,250,"page_perf"));
            this.qolSettings.addChild(this.qolLabel("Presets",28,260,16));
            this.qolSettings.addChild(this.qolButton("Normal",28,286,120,"preset_normal"));
            this.qolSettings.addChild(this.qolButton("Chaos",162,286,120,"preset_chaos"));
            this.qolSettings.addChild(this.qolButton("Benchmark",296,286,120,"preset_benchmark"));
            this.qolSettings.addChild(this.qolButton("Time Attack",430,286,122,"preset_timeattack"));
            this.qolSettings.addChild(this.qolButton("HIDE SANDBOX",165,382,250,"hide"));
         }
         else if(this.qolSettingsPage == 1)
         {
            var enemyPages:int = Math.ceil(this.qolEnemies.length / 8);
            this.qolEnemyPage = Math.max(0,Math.min(enemyPages - 1,this.qolEnemyPage));
            this.qolSettings.addChild(this.qolLabel("ENEMIES — PAGE " + (this.qolEnemyPage + 1) + "/" + enemyPages,28,16,22));
            var firstEnemy:int = this.qolEnemyPage * 8;
            var slot:int = 0;
            while(slot < 8 && firstEnemy + slot < this.qolEnemies.length)
            {
               var enemyIndex:int = firstEnemy + slot;
               var shortName:String = String(this.qolEnemies[enemyIndex]).replace("Enemy","");
               var selectedPrefix:String = enemyIndex == this.qolEnemyIndex ? "▶ " : "";
               var bx:Number = slot % 2 == 0 ? 28 : 302;
               var by:Number = 72 + int(slot / 2) * 45;
               this.qolSettings.addChild(this.qolButton(selectedPrefix + shortName,bx,by,250,"enemy_pick_" + enemyIndex));
               slot++;
            }
            this.qolSettings.addChild(this.qolButton("← Page",28,258,120,"enemy_page_prev"));
            this.qolSettings.addChild(this.qolButton("Page →",432,258,120,"enemy_page_next"));
            this.qolSettings.addChild(this.qolLabel("Count " + this.qolEnemyCount + " | Path " + (this.qolEnemyPath + 1),176,270,16));
            this.qolSettings.addChild(this.qolButton("-25",28,312,78,"count_m25"));
            this.qolSettings.addChild(this.qolButton("-5",116,312,78,"count_m5"));
            this.qolSettings.addChild(this.qolButton("-1",204,312,78,"count_m1"));
            this.qolSettings.addChild(this.qolButton("+1",298,312,78,"count_p1"));
            this.qolSettings.addChild(this.qolButton("+5",386,312,78,"count_p5"));
            this.qolSettings.addChild(this.qolButton("+25",474,312,78,"count_p25"));
            this.qolSettings.addChild(this.qolButton("Prev path",28,366,120,"path_prev"));
            this.qolSettings.addChild(this.qolButton("SEND SELECTED",162,366,256,"send_custom"));
            this.qolSettings.addChild(this.qolButton("Next path",432,366,120,"path_next"));
            this.qolSettings.addChild(this.qolButton("CLEAR ALL ENEMIES",28,420,250,"clear_enemies"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",302,420,250,"page_main"));
         }
         else if(this.qolSettingsPage == 2)
         {
            this.qolEnsureHeroSelection();
            this.qolSettings.addChild(this.qolLabel("HEROES",28,16,22));
            var heroNames:Array = [["alric","Alric"],["mirage","Mirage"],["captain","Blackthorne"],["cronan","Cronan"],["shatra","Sha'tra"],["grawl","Grawl"],["nivus","Nivus"],["dierdre","Dierdre"],["ashbite","Ashbite"],["rurin","Rurin Longbeard"]];
            var hi:int = 0;
            while(hi < heroNames.length)
            {
               this.qolSettings.addChild(this.qolButton(this.qolHeroLabel(heroNames[hi][0],heroNames[hi][1]),hi % 2 == 0 ? 28 : 302,72 + int(hi / 2) * 47,250,"hero_" + heroNames[hi][0]));
               hi++;
            }
            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();
            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL HEROES OFF" : "TURN ALL HEROES ON",28,320,524,"heroes_all"));
            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES NOW",28,374,250,"heroes_remove"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",302,374,250,"page_main"));
         }
         else if(this.qolSettingsPage == 3)
         {
            this.qolSettings.addChild(this.qolLabel("WAVES / TIME ATTACK",28,16,22));
            this.qolSettings.addChild(this.qolButton(this.qolSendAllPending ? "Sending all waves…" : "SEND ALL WAVES",28,80,524,"all_waves"));
            this.qolSettings.addChild(this.qolButton("Time Attack: " + (Level.qolTimeAttackEnabled ? "ON" : "OFF"),28,140,250,"time_attack"));
            this.qolSettings.addChild(this.qolButton("Recycle exits: " + (Level.qolRecycleEnemies ? "ON" : "OFF"),302,140,250,"recycle_exits"));
            this.qolSettings.addChild(this.qolButton("Unlimited: " + (this.qolUnlimitedMode ? "ON" : "OFF"),28,200,250,"unlimited"));
            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,200,250,"instant_win"));
            this.qolSettings.addChild(this.qolLabel("Best: " + this.qolBestTimeText(),28,272,18));
            this.qolSettings.addChild(this.qolLabel("Send All and Time Attack remain paused until this menu closes.",28,314,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,390,250,"page_main"));
         }
         else if(this.qolSettingsPage == 4)
         {
            this.qolSettings.addChild(this.qolLabel("CHEATS / CLEANUP",28,16,22));
            this.qolSettings.addChild(this.qolButton("Speed: " + (Level.qolSpeed == 3 ? "3x" : "1x"),28,80,250,"speed"));
            this.qolSettings.addChild(this.qolButton(this.game.qolTreesMaxed ? "RESET UPGRADES" : "MAX ALL UPGRADES",302,80,250,"trees_toggle"));
            this.qolSettings.addChild(this.qolLabel("Gold",28,150,16));
            this.qolGoldInput = this.qolInput("0",90,138,190);
            this.qolSettings.addChild(this.qolGoldInput);
            this.qolSettings.addChild(this.qolButton("ADD",302,136,250,"gold_add"));
            this.qolSettings.addChild(this.qolLabel("Lives",28,210,16));
            this.qolLivesInput = this.qolInput("0",90,198,190);
            this.qolSettings.addChild(this.qolLivesInput);
            this.qolSettings.addChild(this.qolButton("ADD",302,196,250,"lives_add"));
            this.qolSettings.addChild(this.qolButton("CLEAR ALL ENEMIES",28,270,250,"clear_enemies"));
            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES",302,270,250,"heroes_remove"));
            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,330,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,410,250,"page_main"));
         }
         else if(this.qolSettingsPage == 5)
         {
            this.qolSettings.addChild(this.qolLabel("PERFORMANCE",28,16,22));
            this.qolSettings.addChild(this.qolLabel("FPS " + this.qolDiagFps.toFixed(1) + " | entities " + this.entities.numChildren + " | bullets " + this.bullets.numChildren,28,78,18));
            this.qolSettings.addChild(this.qolButton("Live diagnostics: " + (this.qolDiagEnabled ? "ON" : "OFF"),28,112,524,"diag_toggle"));
            this.qolSettings.addChild(this.qolLabel("Heavy  E" + this.qolHeavyEntities + " / B" + this.qolHeavyBullets,28,178,16));
            this.qolSettings.addChild(this.qolButton("-",302,164,110,"perf_heavy_minus"));
            this.qolSettings.addChild(this.qolButton("+",442,164,110,"perf_heavy_plus"));
            this.qolSettings.addChild(this.qolLabel("Extreme  E" + this.qolExtremeEntities + " / B" + this.qolExtremeBullets,28,238,16));
            this.qolSettings.addChild(this.qolButton("-",302,224,110,"perf_extreme_minus"));
            this.qolSettings.addChild(this.qolButton("+",442,224,110,"perf_extreme_plus"));
            this.qolSettings.addChild(this.qolLabel("Ultra  E" + this.qolUltraEntities + " / B" + this.qolUltraBullets,28,298,16));
            this.qolSettings.addChild(this.qolButton("-",302,284,110,"perf_ultra_minus"));
            this.qolSettings.addChild(this.qolButton("+",442,284,110,"perf_ultra_plus"));
            this.qolSettings.addChild(this.qolButton("DEFAULT THRESHOLDS",28,350,250,"perf_default"));
            this.qolSettings.addChild(this.qolButton("AGGRESSIVE LAPTOP",302,350,250,"perf_aggressive"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,414,250,"page_main"));
         }
         else
         {
            this.qolSettings.addChild(this.qolLabel("TOWERS / CLIPBOARD",28,16,22));
            this.qolSettings.addChild(this.qolLabel("Ctrl+C copies exact standard tier or tier-4 branch + purchased abilities.",28,88,15));
            this.qolSettings.addChild(this.qolLabel("Ctrl+V on an empty build spot pays the source tower's full invested cost.",28,118,15));
            this.qolSettings.addChild(this.qolLabel("Map-special building types are also copyable; live hired units are not cloned.",28,148,15));
            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,210,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("CLEAR CLIPBOARD",28,270,524,"clipboard_clear"));
            this.qolSettings.addChild(this.qolLabel("Build advanced and map-special towers from any empty TowerHolder radial menu.",28,344,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,402,250,"page_main"));
         }
      }
'''
level=replace_function(level,'      private function qolRenderSettings() : void\n',render,'categorized settings UI')
click=r'''      private function qolSettingsClick(param1:MouseEvent) : void
      {
         var action:String = Sprite(param1.currentTarget).name;
         if(action == "speed") Level.qolSpeed = Level.qolSpeed == 1 ? 3 : 1;
         else if(action == "trees_toggle") this.game.qolSetTreesMaxed(!this.game.qolTreesMaxed);
         else if(action == "gold_add")
         {
            var amount:Number = this.qolGoldInput == null ? 0 : Number(this.qolGoldInput.text);
            if(isNaN(amount) || amount < 0) amount = 0;
            this.updateCash(int(Math.min(2000000000,amount)));
         }
         else if(action == "lives_add")
         {
            var livesAmount:Number = this.qolLivesInput == null ? 0 : Number(this.qolLivesInput.text);
            if(isNaN(livesAmount) || livesAmount < 0) livesAmount = 0;
            this.lives = Math.min(2000000000,this.lives + livesAmount);
            if(this.§_-rd§ != null) this.§_-rd§.updateLives(this.lives);
         }
         else if(action == "page_main") this.qolSettingsPage = 0;
         else if(action == "page_enemy") this.qolSettingsPage = 1;
         else if(action == "page_heroes") this.qolSettingsPage = 2;
         else if(action == "page_waves") this.qolSettingsPage = 3;
         else if(action == "page_cheats") this.qolSettingsPage = 4;
         else if(action == "page_perf") this.qolSettingsPage = 5;
         else if(action == "page_towers") this.qolSettingsPage = 6;
         else if(action.indexOf("hero_") == 0) this.qolToggleHero(action.substr(5));
         else if(action == "heroes_all") this.qolSetAllHeroes(!this.qolAllHeroesEnabled());
         else if(action == "heroes_remove") this.qolSetAllHeroes(false);
         else if(action == "recycle_exits") Level.qolRecycleEnemies = !Level.qolRecycleEnemies;
         else if(action == "time_attack")
         {
            Level.qolTimeAttackEnabled = !Level.qolTimeAttackEnabled;
            this.qolTimeAttackPending = Level.qolTimeAttackEnabled && this.indexWaves == 0 && !this.qolTimeAttackLaunched;
            if(!Level.qolTimeAttackEnabled) { this.qolTimeAttackPending = false; this.qolTimerRunning = false; }
            this.qolUpdateTimerHud();
         }
         else if(action == "unlimited") { this.qolUnlimitedMode = !this.qolUnlimitedMode; this.isReadyToWin = false; this.readyToWinTimeCounter = 0; }
         else if(action == "all_waves") this.qolSendAllAfterMenu = true;
         else if(action == "instant_win") { this.qolInstantWin(); return; }
         else if(action == "enemy_page_prev") this.qolEnemyPage = (this.qolEnemyPage + Math.ceil(this.qolEnemies.length / 8) - 1) % Math.ceil(this.qolEnemies.length / 8);
         else if(action == "enemy_page_next") this.qolEnemyPage = (this.qolEnemyPage + 1) % Math.ceil(this.qolEnemies.length / 8);
         else if(action.indexOf("enemy_pick_") == 0) this.qolEnemyIndex = int(action.substr(11));
         else if(action == "count_m25") this.qolEnemyCount = Math.max(1,this.qolEnemyCount - 25);
         else if(action == "count_m5") this.qolEnemyCount = Math.max(1,this.qolEnemyCount - 5);
         else if(action == "count_m1") this.qolEnemyCount = Math.max(1,this.qolEnemyCount - 1);
         else if(action == "count_p1") this.qolEnemyCount = Math.min(1000,this.qolEnemyCount + 1);
         else if(action == "count_p5") this.qolEnemyCount = Math.min(1000,this.qolEnemyCount + 5);
         else if(action == "count_p25") this.qolEnemyCount = Math.min(1000,this.qolEnemyCount + 25);
         else if(action == "path_prev") this.qolEnemyPath = Math.max(0,this.qolEnemyPath - 1);
         else if(action == "path_next") this.qolEnemyPath = Math.min(Math.max(0,this.§_-V8§.length - 1),this.qolEnemyPath + 1);
         else if(action == "send_custom") this.qolSendCustomRound();
         else if(action == "clear_enemies") this.qolClearAllEnemies();
         else if(action == "sell_specials") this.qolSellAllMapSpecials();
         else if(action == "clipboard_clear") { this.qolTowerClipboard = null; this.qolTowerClipboardAction = ""; }
         else if(action == "diag_toggle") this.qolDiagEnabled = !this.qolDiagEnabled;
         else if(action == "perf_heavy_minus") { this.qolHeavyEntities = Math.max(60,this.qolHeavyEntities - 20); this.qolHeavyBullets = Math.max(80,this.qolHeavyBullets - 25); }
         else if(action == "perf_heavy_plus") { this.qolHeavyEntities += 20; this.qolHeavyBullets += 25; }
         else if(action == "perf_extreme_minus") { this.qolExtremeEntities = Math.max(this.qolHeavyEntities + 20,this.qolExtremeEntities - 40); this.qolExtremeBullets = Math.max(this.qolHeavyBullets + 30,this.qolExtremeBullets - 50); }
         else if(action == "perf_extreme_plus") { this.qolExtremeEntities += 40; this.qolExtremeBullets += 50; }
         else if(action == "perf_ultra_minus") { this.qolUltraEntities = Math.max(this.qolExtremeEntities + 40,this.qolUltraEntities - 80); this.qolUltraBullets = Math.max(this.qolExtremeBullets + 60,this.qolUltraBullets - 100); }
         else if(action == "perf_ultra_plus") { this.qolUltraEntities += 80; this.qolUltraBullets += 100; }
         else if(action == "perf_default") this.qolApplyPreset("normal");
         else if(action == "perf_aggressive") this.qolApplyPreset("chaos");
         else if(action.indexOf("preset_") == 0) this.qolApplyPreset(action.substr(7));
         else if(action == "hide") { this.qolHideSettings(); return; }
         this.qolRenderSettings();
      }
'''
level=replace_function(level,'      private function qolSettingsClick(param1:MouseEvent) : void\n',click,'V11 settings actions')
level=replace_once(level,'''            var heavy:Boolean = this.entities.numChildren > 160 || this.bullets.numChildren > 200;
            var extreme:Boolean = this.entities.numChildren > 260 || this.bullets.numChildren > 330;
            var ultra:Boolean = this.entities.numChildren > 520 || this.bullets.numChildren > 680;''','''            this.qolProcessTowerPaste();
            var entityCount:int = this.entities.numChildren;
            var bulletCount:int = this.bullets.numChildren;
            var heavy:Boolean = entityCount > this.qolHeavyEntities || bulletCount > this.qolHeavyBullets;
            var extreme:Boolean = entityCount > this.qolExtremeEntities || bulletCount > this.qolExtremeBullets;
            var ultra:Boolean = entityCount > this.qolUltraEntities || bulletCount > this.qolUltraBullets;''','configurable swarm thresholds')
level=level.replace('this.entities.numChildren > 340 || this.bullets.numChildren > 420','this.entities.numChildren > this.qolExtremeEntities + 80 || this.bullets.numChildren > this.qolExtremeBullets + 90')
level=level.replace('this.entities.numChildren > 240 || this.bullets.numChildren > 300','this.entities.numChildren > this.qolHeavyEntities + 80 || this.bullets.numChildren > this.qolHeavyBullets + 100')
level=replace_once(level,'            this.game.gameSounds.onFrameUpdate();\n            qolTick = 0;','            this.qolDiagnosticsFrame();\n            this.game.gameSounds.onFrameUpdate();\n            qolTick = 0;','diagnostics frame hook')
write('Level.as',level)
print('V11 UI/performance patches applied')
