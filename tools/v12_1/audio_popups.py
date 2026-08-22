#!/usr/bin/env python3
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: audio_popups.py <exported-v12-scripts-dir>')
root=Path(sys.argv[1])
def read(p): return (root/p).read_text(encoding='utf-8-sig')
def write(p,s):
    q=root/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(s,encoding='utf-8',newline='\n')
def rep(s,a,b,label):
    n=s.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    return s.replace(a,b,1)
def sub1(s,pat,repl,label,flags=re.S):
    out,n=re.subn(pat,repl,s,count=1,flags=flags)
    if n!=1: raise SystemExit(f'{label}: expected 1 regex match, got {n}')
    return out

# ---------------- Sound manager ----------------
sm_path='§_-aQ§/§for for dynamic§.as'; sm=read(sm_path)
sm=rep(sm,
'''      public function §_-In§() : void
      {
         this.§_-8o§ = true;
      }
      
      public function §throw extends§() : void
      {
         this.§_-8o§ = false;
      }
      
      public function §with do§() : void
      {
         this.§_-3i§ = true;
      }
      
      public function §dynamic for set§() : void
      {
         this.§_-3i§ = false;
      }
''',
'''      public function §_-In§() : void
      {
         this.§_-8o§ = true;
         this.qolApplyCategoryVolumes();
      }
      
      public function §throw extends§() : void
      {
         this.§_-8o§ = false;
         this.qolApplyCategoryVolumes();
      }
      
      public function §with do§() : void
      {
         this.§_-3i§ = true;
         this.qolApplyCategoryVolumes();
      }
      
      public function §dynamic for set§() : void
      {
         this.§_-3i§ = false;
         this.qolApplyCategoryVolumes();
      }
      
      private function qolApplyCategoryVolumes() : void
      {
         var item:§_-ac§ = null;
         var soundName:String = null;
         var i:int = 0;
         while(i < this.§_-YH§.length)
         {
            item = this.§_-YH§[i] as §_-ac§;
            if(item != null)
            {
               soundName = item.name;
               if(this.§do for set§ || this.§_-8o§ && this.§_-eA§(soundName) || this.§_-3i§ && this.§_-Q5§(soundName))
               {
                  item.setVolume(0);
               }
               else
               {
                  item.setVolume(item.§_-Dh§);
               }
            }
            i++;
         }
      }
''','category mute methods')
sm=rep(sm,
'''      public function playSound(param1:String, param2:Number = 1, param3:Number = 0, param4:int = 0, param5:Boolean = true) : void
      {
         var _loc6_:int = int(this.§_-YH§.length);
''',
'''      public function playSound(param1:String, param2:Number = 1, param3:Number = 0, param4:int = 0, param5:Boolean = true) : void
      {
         var requestedVolume:Number = param2;
         var _loc6_:int = int(this.§_-YH§.length);
''','requested volume local')
sm=rep(sm,
'''         if(_loc9_.channel != null)
         {
            _loc9_.play(param3,param4,param2,param5);
            dispatchEvent(new SoundManagerEvent(SoundManagerEvent.§_-A7§,_loc9_));
''',
'''         if(_loc9_.channel != null)
         {
            _loc9_.play(param3,param4,param2,param5);
            _loc9_.§_-Dh§ = requestedVolume;
            dispatchEvent(new SoundManagerEvent(SoundManagerEvent.§_-A7§,_loc9_));
''','preserve requested volume')

mute_fn='''      public function §_-u2§() : void
      {
         var item:§_-ac§ = null;
         var soundName:String = null;
         this.§do for set§ = true;
         var i:int = 0;
         while(i < this.§_-YH§.length)
         {
            item = this.§_-YH§[i] as §_-ac§;
            if(item != null)
            {
               soundName = item.name;
               if(!(this.§_-8o§ && this.§_-eA§(soundName)) && !(this.§_-3i§ && this.§_-Q5§(soundName)) && item.channel != null && item.channel.soundTransform != null)
               {
                  item.§_-Dh§ = item.channel.soundTransform.volume;
               }
               item.§_-Wa§ = true;
               item.setVolume(0);
            }
            i++;
         }
         dispatchEvent(new SoundManagerEvent(SoundManagerEvent.§_-Fh§));
      }
      
'''
unmute_fn='''      public function §final const function§() : void
      {
         var item:§_-ac§ = null;
         var soundName:String = null;
         this.§do for set§ = false;
         var i:int = 0;
         while(i < this.§_-YH§.length)
         {
            item = this.§_-YH§[i] as §_-ac§;
            if(item != null)
            {
               soundName = item.name;
               item.§_-Wa§ = false;
               if(this.§_-8o§ && this.§_-eA§(soundName) || this.§_-3i§ && this.§_-Q5§(soundName))
               {
                  item.setVolume(0);
               }
               else
               {
                  item.setVolume(item.§_-Dh§);
               }
            }
            i++;
         }
         dispatchEvent(new SoundManagerEvent(SoundManagerEvent.§_-VG§));
      }
      
'''
sm=sub1(sm,r'      public function §_-u2§\(\) : void\n      \{.*?\n      \}\n      \n(?=      public function §final const function§)',mute_fn,'global mute function')
sm=sub1(sm,r'      public function §final const function§\(\) : void\n      \{.*?\n      \}\n      \n(?=      public function §switch finally§)',unmute_fn,'global unmute function')
write(sm_path,sm)

# ---------------- Popup master switch ----------------
level=read('Level.as')
level=rep(level,'      public static var qolRecycleEnemies:Boolean = false;\n','      public static var qolRecycleEnemies:Boolean = false;\n      \n      public static var qolPopupsEnabled:Boolean = true;\n','popup static')
level=rep(level,
'''            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,330,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,410,250,"page_main"));
''',
'''            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,330,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("POP-UP HINTS: " + (Level.qolPopupsEnabled ? "ON" : "OFF"),28,386,524,"popup_hints"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,442,250,"page_main"));
''','popup button')
level=rep(level,'         else if(action == "unlimited")\n         {\n',
'''         else if(action == "popup_hints")
         {
            Level.qolPopupsEnabled = !Level.qolPopupsEnabled;
            this.game.main.tooltipsStatus = Level.qolPopupsEnabled;
            if(!Level.qolPopupsEnabled)
            {
               this.removeToopTip();
               if(this is Level1 && Level1(this).buildSign != null)
               {
                  Level1(this).buildSign.closeMe();
               }
               if(this is Level1 && Level1(this).notificationSign != null)
               {
                  Level1(this).notificationSign.destroyThis();
               }
            }
         }
         else if(action == "unlimited")
         {
''','popup action')
level=rep(level,'      public function sendPauseNotification(param1:String) : void\n      {\n',
'''      public function sendPauseNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled)
         {
            return;
         }
''','pause notification gate')
level=rep(level,
'''      public function sendSecondLevelNotification(param1:String) : void
      {
         this.§include return§.addNotification(param1);
      }
''',
'''      public function sendSecondLevelNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled)
         {
            return;
         }
         this.§include return§.addNotification(param1);
      }
''','second notification gate')
level=rep(level,
'''      public function §_-gU§() : void
      {
         this.§include return§.addNotification(not);
      }
''',
'''      public function §_-gU§() : void
      {
         if(!Level.qolPopupsEnabled)
         {
            return;
         }
         this.§include return§.addNotification(not);
      }
''','generic notification gate')
level=rep(level,'      public function addToopTip(param1:Tooltip) : void\n      {\n         this.removeToopTip();\n',
'''      public function addToopTip(param1:Tooltip) : void
      {
         if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)
         {
            if(param1 != null)
            {
               param1.destroyThis();
            }
            return;
         }
         this.removeToopTip();
''','tooltip gate')
write('Level.as',level)

# Scripted level-1 BUILD HERE sign.
tp='§dynamic const function§.as'; t=read(tp)
t=rep(t,
'''         Level1(this.level).buildSign = new §import const switch§(new Point(485,259),Level1(this.level));
         this.level.bullets.addChild(Level1(this.level).buildSign);
''',
'''         if(Level.qolPopupsEnabled)
         {
            Level1(this.level).buildSign = new §import const switch§(new Point(485,259),Level1(this.level));
            this.level.bullets.addChild(Level1(this.level).buildSign);
         }
''','build sign gate')
write(tp,t)

# Built-in Tooltips switch mirrors the same master setting.
sp='§_-bK§.as'; st=read(sp)
st=rep(st,'                  this.cRoot.game.main.tooltipsStatus = true;\n                  this.§_-2O§();\n',
'''                  this.cRoot.game.main.tooltipsStatus = true;
                  Level.qolPopupsEnabled = true;
                  this.§_-2O§();
''','builtin popup on')
st=rep(st,'                  this.cRoot.game.main.tooltipsStatus = false;\n                  this.§_-2O§();\n',
'''                  this.cRoot.game.main.tooltipsStatus = false;
                  Level.qolPopupsEnabled = false;
                  this.cRoot.removeToopTip();
                  if(this.cRoot is Level1 && Level1(this.cRoot).buildSign != null)
                  {
                     Level1(this.cRoot).buildSign.closeMe();
                  }
                  this.§_-2O§();
''','builtin popup off')
write(sp,st)

for p,needles in {
 'Level.as':['qolPopupsEnabled','POP-UP HINTS:','popup_hints'],
 sm_path:['qolApplyCategoryVolumes','requestedVolume','public function §_-u2§','public function §final const function§'],
 tp:['if(Level.qolPopupsEnabled)'],
 sp:['Level.qolPopupsEnabled = false','Level.qolPopupsEnabled = true']}.items():
    x=read(p)
    for needle in needles:
        if needle not in x: raise SystemExit(f'{p}: missing {needle}')
print('V12.1 audio/popup patch applied')
