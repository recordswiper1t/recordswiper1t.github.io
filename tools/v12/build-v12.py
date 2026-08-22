from pathlib import Path
import re, sys

if len(sys.argv)!=2: raise SystemExit('usage: build-v12.py <exported-v11-scripts-dir>')
scripts=Path(sys.argv[1])

def read(n): return (scripts/n).read_text(encoding='utf-8-sig')
def write(n,s): (scripts/n).write_text(s,encoding='utf-8',newline='\n')
def rep(s,old,new,label):
    c=s.count(old)
    if c!=1: raise SystemExit(f'{label}: expected 1 got {c}')
    return s.replace(old,new,1)

# ---------------- Level: scoring + adaptive quality ----------------
level=read('Level.as')
level=rep(level,
'''      private var qolDiagFps:Number = 0;
''',
'''      private var qolDiagFps:Number = 0;
      
      private var qolVirtualLivesLost:int = 0;
      
      private var qolBestLivesLost:int = -1;
      
      private var qolBestCombined:Number = -1;
      
      private var qolRunStartMs:int = 0;
      
      private var qolAdaptiveQuality:Boolean = true;
      
      private var qolLastStageQuality:String = "";
''','score/perf state')
level=rep(level,
'''         this.qolTimerLabel.height = 42;''',
'''         this.qolTimerLabel.height = 66;''','timer height')
level=rep(level,
'''         this.qolDiagLastMs = getTimer();
         this.qolLoadBestTime();''',
'''         this.qolDiagLastMs = getTimer();
         this.qolRunStartMs = getTimer();
         this.qolLoadBestTime();''','run start')
level=rep(level,
'''      private function qolTimeAttackKey() : String
      {
         return getQualifiedClassName(this) + ":" + String(this.mode);
      }
''',
'''      private function qolTimeAttackKey() : String
      {
         var key:String = getQualifiedClassName(this) + ":" + String(this.mode);
         if(this is Level15 && Level15.qolV12PostBossActive)
         {
            key += ":postboss";
         }
         return key;
      }
''','score key')
level=rep(level,
'''            if(save.data.hasOwnProperty(key))
            {
               stored = Number(save.data[key]);
               if(!isNaN(stored) && stored > 0)
               {
                  this.qolBestTime = stored;
               }
            }
''',
'''            if(save.data.hasOwnProperty(key))
            {
               stored = Number(save.data[key]);
               if(!isNaN(stored) && stored > 0)
               {
                  this.qolBestTime = stored;
               }
            }
            if(save.data.hasOwnProperty(key + ":lost"))
            {
               this.qolBestLivesLost = int(save.data[key + ":lost"]);
            }
            if(save.data.hasOwnProperty(key + ":combined"))
            {
               this.qolBestCombined = Number(save.data[key + ":combined"]);
            }
''','load score bests')
level=rep(level,
'''            save.data[this.qolTimeAttackKey()] = this.qolBestTime;
            save.flush();''',
'''            var key:String = this.qolTimeAttackKey();
            save.data[key] = this.qolBestTime;
            save.data[key + ":lost"] = this.qolBestLivesLost;
            save.data[key + ":combined"] = this.qolBestCombined;
            save.flush();''','save score bests')
anchor='''      private function qolTimeText(param1:Number) : String
'''
helpers=r'''      private function qolCurrentRunSeconds() : Number
      {
         if(this.qolTimerRunning)
         {
            return Math.max(0,(getTimer() - this.qolTimerStartMs) / 1000);
         }
         if(this.qolTimerLast >= 0)
         {
            return this.qolTimerLast;
         }
         return Math.max(0,(getTimer() - this.qolRunStartMs) / 1000);
      }
      
      private function qolCombinedScore(param1:Number, param2:int) : Number
      {
         return Math.max(0,param1) + Math.max(0,param2) * 15;
      }
      
      public function qolRecordVirtualLivesLost(param1:int) : void
      {
         if(!Level.qolRecycleEnemies)
         {
            return;
         }
         this.qolVirtualLivesLost += Math.max(1,param1);
         this.qolUpdateTimerHud();
      }
      
      public function qolResetRunTracking(param1:Boolean = false) : void
      {
         this.qolVirtualLivesLost = 0;
         this.qolRunStartMs = getTimer();
         this.qolTimerLast = -1;
         this.qolBestTimeLoaded = false;
         this.qolBestTime = -1;
         this.qolBestLivesLost = -1;
         this.qolBestCombined = -1;
         this.qolLoadBestTime();
         if(param1 && Level.qolTimeAttackEnabled)
         {
            this.qolTimerRunning = true;
            this.qolTimerStartMs = getTimer();
            this.qolTimeAttackLaunched = true;
         }
         this.qolUpdateTimerHud();
      }
      
      private function qolBankRun() : void
      {
         var elapsed:Number = this.qolCurrentRunSeconds();
         var combined:Number = this.qolCombinedScore(elapsed,this.qolVirtualLivesLost);
         this.qolLoadBestTime();
         if(elapsed > 0 && (this.qolBestTime < 0 || elapsed < this.qolBestTime))
         {
            this.qolBestTime = elapsed;
         }
         if(this.qolBestLivesLost < 0 || this.qolVirtualLivesLost < this.qolBestLivesLost)
         {
            this.qolBestLivesLost = this.qolVirtualLivesLost;
         }
         if(this.qolBestCombined < 0 || combined < this.qolBestCombined)
         {
            this.qolBestCombined = combined;
         }
         this.qolSaveBestTime();
         this.qolUpdateTimerHud();
      }
      
      private function qolScoreText() : String
      {
         this.qolLoadBestTime();
         var bestLost:String = this.qolBestLivesLost < 0 ? "--" : String(this.qolBestLivesLost);
         var bestCombined:String = this.qolBestCombined < 0 ? "--" : this.qolBestCombined.toFixed(2);
         return "LOST " + this.qolVirtualLivesLost + " / BEST " + bestLost + "\nSCORE " + this.qolCombinedScore(this.qolCurrentRunSeconds(),this.qolVirtualLivesLost).toFixed(2) + " / BEST " + bestCombined;
      }
      
'''+anchor
level=rep(level,anchor,helpers,'score helpers')
level=rep(level,
'''         this.qolTimerLabel.visible = Level.qolTimeAttackEnabled;
         if(!Level.qolTimeAttackEnabled)
         {
            return;
         }
''',
'''         this.qolTimerLabel.visible = Level.qolTimeAttackEnabled || Level.qolRecycleEnemies;
         if(!Level.qolTimeAttackEnabled && !Level.qolRecycleEnemies)
         {
            return;
         }
''','score hud visible')
level=rep(level,
'''         this.qolTimerLabel.text = "TIME  " + currentText + "\nBEST  " + this.qolBestTimeText();''',
'''         this.qolTimerLabel.text = "TIME " + currentText + " / BEST " + this.qolBestTimeText() + "\n" + this.qolScoreText();''','score hud text')
level=rep(level,
'''         this.qolTimeAttackLaunched = true;
         this.qolTimerRunning = true;
         this.qolTimerLast = -1;
         this.qolTimerStartMs = getTimer();''',
'''         this.qolTimeAttackLaunched = true;
         this.qolVirtualLivesLost = 0;
         this.qolRunStartMs = getTimer();
         this.qolTimerRunning = true;
         this.qolTimerLast = -1;
         this.qolTimerStartMs = getTimer();''','TA score reset')
level=rep(level,
'''         if(this.qolTimerLast > 0 && (this.qolBestTime < 0 || this.qolTimerLast < this.qolBestTime))
         {
            this.qolBestTime = this.qolTimerLast;
            this.qolSaveBestTime();
         }
         this.qolUpdateTimerHud();''',
'''         if(this.qolTimerLast > 0 && (this.qolBestTime < 0 || this.qolTimerLast < this.qolBestTime))
         {
            this.qolBestTime = this.qolTimerLast;
         }
         this.qolBankRun();
         this.qolUpdateTimerHud();''','TA bank')
anchor='''      private function qolGameTick() : void
'''
adapt=r'''      private function qolAdaptiveQualityTick(param1:Boolean, param2:Boolean, param3:Boolean) : void
      {
         if(!this.qolAdaptiveQuality || this.stage == null || this.qolPerfFrame % 30 != 0)
         {
            return;
         }
         var desired:String = param3 ? StageQuality.LOW : (param2 ? StageQuality.MEDIUM : StageQuality.HIGH);
         if(desired != this.qolLastStageQuality)
         {
            this.stage.quality = desired;
            this.qolLastStageQuality = desired;
         }
      }
      
'''+anchor
level=rep(level,anchor,adapt,'adaptive helper')
level=rep(level,
'''            var ultra:Boolean = entityCount > this.qolUltraEntities || bulletCount > this.qolUltraBullets;
            this.updateEntities();''',
'''            var ultra:Boolean = entityCount > this.qolUltraEntities || bulletCount > this.qolUltraBullets;
            this.qolAdaptiveQualityTick(heavy,extreme,ultra);
            this.updateEntities();''','adaptive call')
level=rep(level,
'''         return "PAUSED | " + (Level.qolSpeed == 3 ? "3x" : "1x") + " | TA " + (Level.qolTimeAttackEnabled ? "ON" : "off") + " | recycle " + (Level.qolRecycleEnemies ? "ON" : "off") + " | unlimited " + (this.qolUnlimitedMode ? "ON" : "off");''',
'''         return "PAUSED | " + (Level.qolSpeed == 3 ? "3x" : "1x") + " | TA " + (Level.qolTimeAttackEnabled ? "ON" : "off") + " | recycle " + (Level.qolRecycleEnemies ? "ON" : "off") + " | lost " + this.qolVirtualLivesLost + " | unlimited " + (this.qolUnlimitedMode ? "ON" : "off");''','status score')
old='''            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,200,250,"instant_win"));
            this.qolSettings.addChild(this.qolLabel("Best: " + this.qolBestTimeText(),28,272,18));
            this.qolSettings.addChild(this.qolLabel("Send All and Time Attack remain paused until this menu closes.",28,314,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,390,250,"page_main"));'''
new='''            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,200,250,"instant_win"));
            this.qolSettings.addChild(this.qolButton("BANK CURRENT LOOP RUN",28,260,524,"bank_run"));
            this.qolSettings.addChild(this.qolLabel("Best time: " + this.qolBestTimeText() + "   Best lost: " + (this.qolBestLivesLost < 0 ? "--" : String(this.qolBestLivesLost)),28,322,16));
            this.qolSettings.addChild(this.qolLabel("Combined score = seconds + 15 × virtual lives lost. Lower is better.",28,352,14));
            this.qolSettings.addChild(this.qolLabel("Send All and Time Attack remain paused until this menu closes.",28,380,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,422,250,"page_main"));'''
level=rep(level,old,new,'waves scoring UI')
level=rep(level,
'''         else if(action == "unlimited")
         {''',
'''         else if(action == "bank_run")
         {
            this.qolBankRun();
         }
         else if(action == "unlimited")
         {''','bank action')
level=rep(level,
'''         else if(action == "recycle_exits")
         {
            Level.qolRecycleEnemies = !Level.qolRecycleEnemies;
         }''',
'''         else if(action == "recycle_exits")
         {
            Level.qolRecycleEnemies = !Level.qolRecycleEnemies;
            if(Level.qolRecycleEnemies)
            {
               this.qolResetRunTracking(false);
            }
         }''','recycle reset')
old='''            this.qolSettings.addChild(this.qolLabel("Adjusts only cosmetic cadence/back-pressure; attacks and movement stay full-rate.",28,334,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,408,250,"page_main"));'''
new='''            this.qolSettings.addChild(this.qolButton("Adaptive render quality: " + (this.qolAdaptiveQuality ? "ON" : "OFF"),28,330,524,"adaptive_quality"));
            this.qolSettings.addChild(this.qolLabel("Adaptive LOW/MEDIUM/HIGH render quality follows swarm load; combat stays full-rate.",28,382,14));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,422,250,"page_main"));'''
level=rep(level,old,new,'performance adaptive UI')
level=rep(level,
'''         else if(action == "perf_aggressive")
         {''',
'''         else if(action == "adaptive_quality")
         {
            this.qolAdaptiveQuality = !this.qolAdaptiveQuality;
            if(!this.qolAdaptiveQuality && this.stage != null)
            {
               this.stage.quality = StageQuality.HIGH;
               this.qolLastStageQuality = StageQuality.HIGH;
            }
         }
         else if(action == "perf_aggressive")
         {''','adaptive action')
write('Level.as',level)

# ------------ Enemy virtual lives lost ------------
for n in ['Enemy.as','EnemyCanibalBeast.as','EnemyTremor.as']:
    s=read(n)
    if n=='Enemy.as':
        old='''         if(Level.qolRecycleEnemies)
         {
            this.isActive = false;'''
    elif n=='EnemyCanibalBeast.as':
        old='''            if(Level.qolRecycleEnemies)
            {
               this.isActive = false;'''
    else:
        old='''         if(Level.qolRecycleEnemies)
         {
            this.isActive = false;'''
    if n=='EnemyCanibalBeast.as':
        new='''            if(Level.qolRecycleEnemies)
            {
               if(this.cRoot != null)
               {
                  this.cRoot.qolRecordVirtualLivesLost(this.cost);
               }
               this.isActive = false;'''
    else:
        new='''         if(Level.qolRecycleEnemies)
         {
            if(this.cRoot != null)
            {
               this.cRoot.qolRecordVirtualLivesLost(this.cost);
            }
            this.isActive = false;'''
    s=rep(s,old,new,n+' virtual loss')
    write(n,s)

# ---------------- Level15: The Last Rift ----------------
l15=read('Level15.as')
l15=rep(l15,
'''      private var §_-G0§:Boolean = false;
''',
'''      private var §_-G0§:Boolean = false;
      
      public static var qolV12PostBossActive:Boolean = false;
      
      private var qolV12PostBossStarted:Boolean = false;
      
      private var qolV12PostBossComplete:Boolean = false;
      
      private var qolV12Tick:int = 0;
      
      private var qolV12EnemySeen:Dictionary = new Dictionary(true);
      
      private var qolV12Raged:Dictionary = new Dictionary(true);
      
      private var qolV12Boss:Enemy = null;
      
      private var qolV12Hero:MovieClip = null;
      
      private var qolV12Tower:MovieClip = null;
      
      private var qolV12Overlay:Sprite = null;
      
      private var qolV12BannerField:TextField = null;
      
      private var qolV12BannerUntil:int = 0;
      
      private var qolV12LastMilestone:int = -1;
''','postboss state')
l15=rep(l15,
'''         this.§_-Hs§ = new §_-39§();''',
'''         Level15.qolV12PostBossActive = false;
         this.§_-Hs§ = new §_-39§();''','reset postboss')
l15=rep(l15,
'''         this.addChild(this.§_-Hs§);''',
'''         this.addChild(this.§_-Hs§);
         this.addEventListener(Event.ENTER_FRAME,this.qolV12Frame,false,0,true);''','postboss frame listener')
l15=rep(l15,
'''         if(this.§_-nx§ && !this.§_-v0§)''',
'''         if(!this.qolV12PostBossStarted && this.§_-nx§ && !this.§_-v0§)''','original boss force send all')
l15=rep(l15,
'''      override protected function hasEnemies() : Boolean
      {
         if(!this.§_-v0§ && this.§_-nx§ || this.§_-He§.numChildren > 0)
''',
'''      override protected function hasEnemies() : Boolean
      {
         if(this.qolV12PostBossStarted)
         {
            return super.hasEnemies();
         }
         if(!this.§_-v0§ && this.§_-nx§ || this.§_-He§.numChildren > 0)
''','postboss hasEnemies')
l15=rep(l15,
'''      override public function §super const finally§() : void
      {
      }
      
      override public function §_-pp§() : void
      {
      }
''',
'''      override public function §super const finally§() : void
      {
         if(this.qolV12PostBossComplete)
         {
            super.§super const finally§();
         }
      }
      
      override public function §_-pp§() : void
      {
         if(this.qolV12PostBossComplete)
         {
            super.§_-pp§();
         }
      }
      
      override public function onPreWin() : void
      {
         if(this.mode == §_-Mm§.MODE_CAMPAIGN && !this.qolV12PostBossStarted)
         {
            this.qolV12BeginPostBoss();
            return;
         }
         if(this.qolV12PostBossStarted)
         {
            this.qolV12PostBossComplete = true;
            Level15.qolV12PostBossActive = false;
         }
      }
''','postboss win hook')

waves=[]
def wave(parts,path,interval=110):
    sp=[]
    for cls,count,delay in parts:
        sp.append(f'new §_-VY§("{cls}","",0,{count},{delay},0,false,0)')
    waves.append('new Wave(new Array('+','.join(sp)+f'),{interval},{path},"","",false)')
D='EnemySaurianDarter'; B='EnemySaurianBroodguard'; N='EnemySaurianNightscale'; R='EnemySaurianRazorwing'; M='EnemySaurianMyrmidon'; S='EnemySaurianSavant'; F='EnemySaurianBlazefang'; T='EnemySaurianBrute'
for spec in [
 ([(D,12,22)],0,70), ([(D,10,20),(B,5,42)],1,75), ([(D,14,18),(N,4,55)],2,80),
 ([(B,8,34),(R,5,58)],0,85), ([(D,18,15),(M,4,60)],1,85), ([(N,8,32),(S,2,100)],2,90),
 ([(R,9,35),(B,7,40)],0,90), ([(M,7,45),(D,16,16)],1,90), ([(F,6,50),(N,8,30)],2,95),
 ([(T,2,120),(B,10,32)],0,100), ([(S,4,80),(D,20,15)],1,100), ([(R,12,28),(N,10,28)],2,100),
 ([(M,10,38),(F,7,45)],0,105), ([(T,3,100),(S,3,80),(D,18,14)],1,105), ([(B,14,27),(R,10,32),(N,8,30)],2,110),
 ([(F,10,38),(M,10,38)],0,110), ([(S,5,65),(N,14,24),(D,15,14)],1,110), ([(T,4,90),(R,12,26)],2,115),
 ([(M,14,34),(B,12,30),(S,4,70)],0,115), ([(N,20,20),(F,10,34)],1,115), ([(T,5,80),(M,12,34)],2,120),
 ([(R,18,22),(S,6,60),(D,20,12)],0,120), ([(F,14,30),(N,18,20)],1,120), ([(T,6,75),(B,16,26),(S,5,65)],2,125),
 ([(M,18,28),(R,16,24)],0,125), ([(S,8,50),(F,16,28),(D,22,11)],1,130), ([(T,8,65),(N,20,19)],2,130),
 ([(M,20,25),(B,20,24),(R,15,22)],0,135), ([(S,10,45),(F,18,25),(N,18,19)],1,140),
 ([(T,1,1),(M,16,25),(R,16,22),(S,8,45)],2,160)
]: wave(*spec)
wave_literal=',\n            '.join(waves)

anchor='''      override public function destroyThis() : void
'''
postboss=f'''      private function qolV12BeginPostBoss() : void
      {{
         this.§_-BF§ = LEVEL_NORMAL;
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.§_-WR§ = 0;
         this.§_-v0§ = true;
         this.§_-G0§ = true;
         this.qolV12PostBossStarted = true;
         Level15.qolV12PostBossActive = true;
         this.qolV12PostBossComplete = false;
         this.qolV12Tick = 0;
         this.qolV12Boss = null;
         this.qolV12EnemySeen = new Dictionary(true);
         this.qolV12Raged = new Dictionary(true);
         this.qolV12InstallPaths();
         this.qolV12InstallArena();
         this.qolV12InstallTowerSpots();
         this.qolV12InstallAllies();
         this.waves = new Array(
            {wave_literal}
         );
         this.activeWaves = new Dictionary(true);
         this.indexWaves = 0;
         this.§_-g3§ = 0;
         this.§_-Wd§ = 30;
         this.getNumberOfWaves();
         this.updateCash(3500);
         if(this.lives < 20)
         {{
            this.updateLives(20 - this.lives);
         }}
         this.qolResetRunTracking(true);
         this.qolV12Banner("THE LAST RIFT — 30 WAVES",300);
      }}
      
      private function qolV12BuildPath(param1:Array) : Array
      {{
         var center:Array = [];
         var i:int = 0;
         var a:Point = null;
         var b:Point = null;
         var dx:Number = 0;
         var dy:Number = 0;
         var dist:Number = 0;
         var steps:int = 0;
         var j:int = 0;
         while(i < param1.length - 1)
         {{
            a = param1[i];
            b = param1[i + 1];
            dx = b.x - a.x;
            dy = b.y - a.y;
            dist = Math.sqrt(dx * dx + dy * dy);
            steps = Math.max(1,int(dist / 6));
            j = 0;
            while(j < steps)
            {{
               center.push(new Point(a.x + dx * j / steps,a.y + dy * j / steps));
               j++;
            }}
            i++;
         }}
         center.push(param1[param1.length - 1].clone());
         var upper:Array = [];
         var lower:Array = [];
         for each(var p:Point in center)
         {{
            upper.push(new Point(p.x,p.y - 12));
            lower.push(new Point(p.x,p.y + 12));
         }}
         return new Array(center,upper,lower);
      }}
      
      private function qolV12InstallPaths() : void
      {{
         this.§_-V8§ = new Array(
            this.qolV12BuildPath(new Array(new Point(-30,130),new Point(130,130),new Point(210,235),new Point(360,235),new Point(450,145),new Point(610,150),new Point(720,270),new Point(820,270))),
            this.qolV12BuildPath(new Array(new Point(-30,360),new Point(115,360),new Point(190,470),new Point(330,470),new Point(410,360),new Point(560,360),new Point(650,455),new Point(820,455))),
            this.qolV12BuildPath(new Array(new Point(170,-30),new Point(170,95),new Point(300,160),new Point(300,310),new Point(470,310),new Point(545,235),new Point(700,235),new Point(700,610)))
         );
         this.pathsActives = new Array(true,true,true);
      }}
      
      private function qolV12InstallArena() : void
      {{
         if(this.§_-qi§ != null)
         {{
            this.§_-qi§.transform.colorTransform = new ColorTransform(0.72,0.62,0.95,1,0,0,20,0);
         }}
         this.qolV12Overlay = new Sprite();
         this.qolV12Overlay.graphics.beginFill(2293850,0.20);
         this.qolV12Overlay.graphics.drawRect(0,0,800,600);
         this.qolV12Overlay.graphics.endFill();
         this.qolV12Overlay.graphics.lineStyle(3,7667967,0.55);
         this.qolV12Overlay.graphics.moveTo(100,0); this.qolV12Overlay.graphics.lineTo(360,230); this.qolV12Overlay.graphics.lineTo(510,0);
         this.qolV12Overlay.graphics.moveTo(800,180); this.qolV12Overlay.graphics.lineTo(520,315); this.qolV12Overlay.graphics.lineTo(800,530);
         this.qolV12Overlay.mouseEnabled = false;
         this.addChildAt(this.qolV12Overlay,Math.min(1,this.numChildren));
         this.qolV12BannerField = new TextField();
         this.qolV12BannerField.defaultTextFormat = new TextFormat("_sans",20,16777215,true,null,null,null,null,"center");
         this.qolV12BannerField.width = 620;
         this.qolV12BannerField.height = 35;
         this.qolV12BannerField.x = 90;
         this.qolV12BannerField.y = 42;
         this.qolV12BannerField.background = true;
         this.qolV12BannerField.backgroundColor = 2621500;
         this.qolV12BannerField.selectable = false;
         this.qolV12BannerField.mouseEnabled = false;
         this.qolV12BannerField.visible = false;
         this.§else const native§.addChild(this.qolV12BannerField);
      }}
      
      private function qolV12InstallTowerSpots() : void
      {{
         var spots:Array = [[80,105,120,155],[145,285,190,320],[80,390,130,430],[180,535,230,500],[280,105,310,160],[320,365,365,405],[390,105,420,155],[420,285,455,330],[485,535,535,500],[525,115,560,165],[565,335,610,370],[645,95,680,145],[655,515,700,480],[735,100,690,155],[735,390,690,420]];
         var i:int = 0;
         while(i < spots.length)
         {{
            this.entities.addChild(new TowerHolder(spots[i][0],spots[i][1],new Point(spots[i][2],spots[i][3])));
            i++;
         }}
      }}
      
      private function qolV12InstallAllies() : void
      {{
         this.qolV12Tower = new TowerDwarfRiflemen(402,78,new Point(402,128));
         this.entities.addChild(this.qolV12Tower);
         this.qolV12Hero = new §switch for super§(new Point(405,520),new Point(405,520),null,new Point(405,520));
         this.entities.addChild(this.qolV12Hero);
         this.qolV12Banner("SPECIAL ALLIES — NYRA THE RIFTWARDEN + RIFT BEACON",240);
      }}
      
      private function qolV12Banner(param1:String, param2:int = 180) : void
      {{
         if(this.qolV12BannerField == null)
         {{
            return;
         }}
         this.qolV12BannerField.text = param1;
         this.qolV12BannerField.visible = true;
         this.qolV12BannerUntil = this.qolV12Tick + param2;
      }}
      
      private function qolV12TuneEnemy(param1:Enemy) : void
      {{
         if(param1 == null || this.qolV12EnemySeen[param1])
         {{
            return;
         }}
         this.qolV12EnemySeen[param1] = true;
         var name:String = getQualifiedClassName(param1);
         var hp:Number = 1;
         var dmg:Number = 1;
         var spd:Number = 1;
         var tint:ColorTransform = new ColorTransform(0.78,0.58,1.12,1,20,0,35,0);
         if(name == "EnemySaurianDarter") {{ hp = 1.45; dmg = 1.20; spd = 1.22; tint = new ColorTransform(1.05,0.45,1.15,1,18,0,28,0); }}
         else if(name == "EnemySaurianBroodguard") {{ hp = 1.85; dmg = 1.25; param1.armor = Math.min(95,param1.armor + 18); tint = new ColorTransform(0.62,0.72,1.25,1,0,8,28,0); }}
         else if(name == "EnemySaurianMyrmidon") {{ hp = 2.20; dmg = 1.45; param1.armor = Math.min(95,param1.armor + 22); tint = new ColorTransform(0.55,0.55,0.85,1,12,0,32,0); }}
         else if(name == "EnemySaurianNightscale") {{ hp = 1.65; dmg = 1.35; spd = 1.18; tint = new ColorTransform(0.60,0.38,1.20,1,20,0,40,0); }}
         else if(name == "EnemySaurianBlazefang") {{ hp = 1.90; dmg = 1.55; tint = new ColorTransform(1.12,0.42,0.72,1,35,0,20,0); }}
         else if(name == "EnemySaurianRazorwing") {{ hp = 1.60; dmg = 1.30; spd = 1.25; tint = new ColorTransform(0.55,0.80,1.25,1,0,18,30,0); }}
         else if(name == "EnemySaurianSavant") {{ hp = 2.10; dmg = 1.30; tint = new ColorTransform(0.55,1.05,1.18,1,0,22,26,0); }}
         else if(name == "EnemySaurianBrute") {{ hp = 3.20; dmg = 1.80; param1.armor = Math.min(95,param1.armor + 15); tint = new ColorTransform(0.72,0.42,1.02,1,25,0,35,0); }}
         param1.initHealth = Math.max(1,int(param1.initHealth * hp));
         param1.health = param1.initHealth;
         param1.minDamage = Math.max(1,int(param1.minDamage * dmg));
         param1.maxDamage = Math.max(param1.minDamage,int(param1.maxDamage * dmg));
         param1.speed *= spd;
         param1.transform.colorTransform = tint;
         if(param1.lifeBar != null)
         {{
            param1.lifeBar.updateMaxHealth(param1.initHealth,param1.health);
            param1.lifeBar.updateProgress(param1.health);
         }}
         if(this.§_-g3§ >= 30 && name == "EnemySaurianBrute" && this.qolV12Boss == null)
         {{
            this.qolV12Boss = param1;
            param1.isBoss = true;
            param1.initHealth *= 6;
            param1.health = param1.initHealth;
            param1.minDamage *= 2;
            param1.maxDamage *= 2;
            param1.armor = Math.max(param1.armor,85);
            param1.magicArmor = Math.max(param1.magicArmor,60);
            param1.scaleX *= 1.28;
            param1.scaleY *= 1.28;
            if(param1.lifeBar != null)
            {{
               param1.lifeBar.updateMaxHealth(param1.initHealth,param1.health);
               param1.lifeBar.updateProgress(param1.health);
            }}
            this.qolV12Banner("WAVE 30 — VORAK, THE RIFT SOVEREIGN",360);
         }}
      }}
      
      private function qolV12SupportPulse() : void
      {{
         var hasConductor:Boolean = false;
         var e:Enemy = null;
         for each(e in this.enemies)
         {{
            if(!e.isDead && getQualifiedClassName(e) == "EnemySaurianSavant")
            {{
               hasConductor = true;
               break;
            }}
         }}
         if(!hasConductor)
         {{
            return;
         }}
         for each(e in this.enemies)
         {{
            if(!e.isDead && e.health < e.initHealth)
            {{
               e.health = Math.min(e.initHealth,e.health + Math.max(1,int(e.initHealth * 0.025)));
               if(e.lifeBar != null) e.lifeBar.updateProgress(e.health);
            }}
         }}
      }}
      
      private function qolV12BossPulse() : void
      {{
         if(this.qolV12Boss == null || this.qolV12Boss.isDead)
         {{
            return;
         }}
         this.qolV12Boss.health = Math.min(this.qolV12Boss.initHealth,this.qolV12Boss.health + Math.max(1,int(this.qolV12Boss.initHealth * 0.04)));
         if(this.qolV12Boss.lifeBar != null) this.qolV12Boss.lifeBar.updateProgress(this.qolV12Boss.health);
         var p:int = Math.max(0,Math.min(2,int(Math.random() * 3)));
         var reinforcement:Wave = new Wave([new §_-VY§("EnemySaurianDarter","",0,5,18,0,false,0),new §_-VY§("EnemySaurianNightscale","",0,2,45,120,false,0)],0,p,"","",false);
         this.activeWaves[reinforcement] = reinforcement;
         this.qolV12Banner("VORAK CASTS FRACTURE PULSE — REINFORCEMENTS",120);
      }}
      
      private function qolV12AlliedPulse() : void
      {{
         var e:Enemy = null;
         if(this.qolV12Tower != null && this.qolV12Tower.parent != null)
         {{
            this.qolV12Tower.transform.colorTransform = new ColorTransform(0.65,0.85,1.25,1,0,10,35,0);
            for each(e in this.enemies)
            {{
               if(!e.isDead && Point.distance(new Point(e.x,e.y),new Point(this.qolV12Tower.x,this.qolV12Tower.y)) < 245)
               {{
                  e.setDamage(95 + this.§_-g3§ * 3,§_-Mm§.P_ARMOR);
               }}
            }}
         }}
         if(this.qolV12Hero != null && this.qolV12Hero.parent != null)
         {{
            this.qolV12Hero.transform.colorTransform = new ColorTransform(0.60,1.05,1.30,1,0,20,35,0);
            for each(e in this.enemies)
            {{
               if(!e.isDead && Point.distance(new Point(e.x,e.y),new Point(this.qolV12Hero.x,this.qolV12Hero.y)) < 135)
               {{
                  e.setDamage(70 + this.§_-g3§ * 2,§_-Mm§.P_ARMOR);
               }}
            }}
         }}
      }}
      
      private function qolV12Milestone() : void
      {{
         if(this.§_-g3§ == this.qolV12LastMilestone)
         {{
            return;
         }}
         this.qolV12LastMilestone = this.§_-g3§;
         if(this.§_-g3§ == 1) this.qolV12Banner("RIFTLINGS + OBSIDIAN GUARD",150);
         else if(this.§_-g3§ == 6) this.qolV12Banner("NEW ENEMY — RIFT CONDUCTOR (HEALS THE HORDE)",180);
         else if(this.§_-g3§ == 10) this.qolV12Banner("NEW ENEMY — TITAN HUSK",180);
         else if(this.§_-g3§ == 15) this.qolV12Banner("THE RIFT DEEPENS — ENEMIES EVOLVE",180);
         else if(this.§_-g3§ == 20) this.qolV12Banner("VOID STALKERS ENRAGE BELOW HALF HEALTH",180);
         else if(this.§_-g3§ == 25) this.qolV12Banner("FINAL ASSAULT — HOLD THE THREE PATHS",180);
      }}
      
      private function qolV12Frame(param1:Event) : void
      {{
         if(!this.qolV12PostBossStarted || this.qolV12PostBossComplete)
         {{
            return;
         }}
         this.qolV12Tick++;
         var e:Enemy = null;
         for each(e in this.enemies)
         {{
            this.qolV12TuneEnemy(e);
            if(!e.isDead && getQualifiedClassName(e) == "EnemySaurianNightscale" && e.health < e.initHealth / 2 && !this.qolV12Raged[e])
            {{
               this.qolV12Raged[e] = true;
               e.speed *= 1.35;
               e.transform.colorTransform = new ColorTransform(1.05,0.28,1.20,1,35,0,45,0);
            }}
         }}
         this.qolV12Milestone();
         if(this.qolV12Tick % 180 == 0) this.qolV12SupportPulse();
         if(this.qolV12Tick % 150 == 0) this.qolV12AlliedPulse();
         if(this.qolV12Tick % 360 == 0) this.qolV12BossPulse();
         if(this.qolV12BannerField != null && this.qolV12Tick >= this.qolV12BannerUntil)
         {{
            this.qolV12BannerField.visible = false;
         }}
      }}
      
'''+anchor
l15=rep(l15,anchor,postboss,'postboss methods')
write('Level15.as',l15)

checks={
 'Level.as':['qolVirtualLivesLost','qolBankRun','Adaptive render quality','qolRecordVirtualLivesLost','":postboss"'],
 'Level15.as':['THE LAST RIFT','qolV12BuildPath','VORAK, THE RIFT SOVEREIGN','NYRA THE RIFTWARDEN','qolV12PostBossActive'],
 'Enemy.as':['qolRecordVirtualLivesLost(this.cost)'],
 'EnemyCanibalBeast.as':['qolRecordVirtualLivesLost(this.cost)'],
 'EnemyTremor.as':['qolRecordVirtualLivesLost(this.cost)']
}
for n,ns in checks.items():
 s=read(n)
 for x in ns:
  if x not in s: raise SystemExit(f'{n}: missing {x}')
print('V12 local patch applied successfully')
