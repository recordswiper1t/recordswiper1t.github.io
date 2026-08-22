#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: audio_popups.py <exported-v12-scripts-dir>')
root = Path(sys.argv[1])

def read(p):
    return (root / p).read_text(encoding='utf-8-sig')
def write(p,s):
    path = root / p
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s, encoding='utf-8', newline='\n')
def rep(s, old, new, label):
    c=s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 match, got {c}')
    return s.replace(old,new,1)

# ------------------------------------------------------------------
# SoundManager: selective FX/music mutes become authoritative.
# Preserve requested volume even when currently muted; mute/unmute
# existing channels immediately; global pause mute respects category
# preferences when restoring channels.
# ------------------------------------------------------------------
sm_path='§_-aQ§/§for for dynamic§.as'
sm=read(sm_path)

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
         var name:String = null;
         var i:int = 0;
         while(i < this.§_-YH§.length)
         {
            item = this.§_-YH§[i] as §_-ac§;
            if(item != null)
            {
               name = item.name;
               if(this.§do for set§ || this.§_-8o§ && this.§_-eA§(name) || this.§_-3i§ && this.§_-Q5§(name))
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
''','sound category methods')

sm=rep(sm,
'''      public function playSound(param1:String, param2:Number = 1, param3:Number = 0, param4:int = 0, param5:Boolean = true) : void
      {
         var _loc6_:int = int(this.§_-YH§.length);
''',
'''      public function playSound(param1:String, param2:Number = 1, param3:Number = 0, param4:int = 0, param5:Boolean = true) : void
      {
         var requestedVolume:Number = param2;
         var _loc6_:int = int(this.§_-YH§.length);
''','requested sound volume')

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
''','preserve desired sound volume')

sm=rep(sm,
'''             if(_loc3_ != null && _loc3_.channel != null && _loc3_.channel.soundTransform != null)
             {
                _loc3_.§_-Dh§ = _loc3_.channel.soundTransform.volume;
                _loc3_.§_-Wa§ = true;
             }
''',
'''             if(_loc3_ != null && _loc3_.channel != null && _loc3_.channel.soundTransform != null)
             {
                if(!(this.§_-8o§ && this.§_-eA§(_loc2_)) && !(this.§_-3i§ && this.§_-Q5§(_loc2_)))
                {
                   _loc3_.§_-Dh§ = _loc3_.channel.soundTransform.volume;
                }
                _loc3_.§_-Wa§ = true;
             }
''','global mute desired volume')

sm=rep(sm,
'''             _loc3_.§_-Wa§ = false;
             this.§switch finally§(_loc2_,_loc3_.§_-Dh§);
''',
'''             _loc3_.§_-Wa§ = false;
             if(this.§_-8o§ && this.§_-eA§(_loc2_) || this.§_-3i§ && this.§_-Q5§(_loc2_))
             {
                this.§switch finally§(_loc2_,0);
             }
             else
             {
                this.§switch finally§(_loc2_,_loc3_.§_-Dh§);
             }
''','global unmute respects categories')
write(sm_path,sm)

# ------------------------------------------------------------------
# Level: one master pop-up setting. It controls tooltip objects,
# pause notifications, second-level notification cards and current
# first-level tutorial signs. Add it to the sandbox settings too.
# ------------------------------------------------------------------
level=read('Level.as')
level=rep(level,
'''      public static var qolRecycleEnemies:Boolean = false;
''',
'''      public static var qolRecycleEnemies:Boolean = false;
      
      public static var qolPopupsEnabled:Boolean = true;
''','popup static setting')

level=rep(level,
'''            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,330,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,410,250,"page_main"));
''',
'''            this.qolSettings.addChild(this.qolButton("SELL ALL MAP SPECIALS",28,330,524,"sell_specials"));
            this.qolSettings.addChild(this.qolButton("POP-UP HINTS: " + (Level.qolPopupsEnabled ? "ON" : "OFF"),28,386,524,"popup_hints"));
            this.qolSettings.addChild(this.qolButton("← Dashboard",165,442,250,"page_main"));
''','popup settings button')

level=rep(level,
'''         else if(action == "unlimited")
         {
''',
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
''','popup settings action')

level=rep(level,
'''      public function sendPauseNotification(param1:String) : void
      {
''',
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

level=rep(level,
'''      public function addToopTip(param1:Tooltip) : void
      {
         this.removeToopTip();
''',
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

# First-level scripted BUILD HERE sign: skip the visual prompt when popups are off.
tut_path='§dynamic const function§.as'
tut=read(tut_path)
tut=rep(tut,
'''         Level1(this.level).buildSign = new §import const switch§(new Point(485,259),Level1(this.level));
         this.level.bullets.addChild(Level1(this.level).buildSign);
''',
'''         if(Level.qolPopupsEnabled)
         {
            Level1(this.level).buildSign = new §import const switch§(new Point(485,259),Level1(this.level));
            this.level.bullets.addChild(Level1(this.level).buildSign);
         }
''','build-here sign gate')
write(tut_path,tut)

# Built-in pause/settings tooltip switch controls the same master preference.
settings_path='§_-bK§.as'
settings=read(settings_path)
settings=rep(settings,
'''                  this.cRoot.game.main.tooltipsStatus = true;
                  this.§_-2O§();
''',
'''                  this.cRoot.game.main.tooltipsStatus = true;
                  Level.qolPopupsEnabled = true;
                  this.§_-2O§();
''','built-in popup on')
settings=rep(settings,
'''                  this.cRoot.game.main.tooltipsStatus = false;
                  this.§_-2O§();
''',
'''                  this.cRoot.game.main.tooltipsStatus = false;
                  Level.qolPopupsEnabled = false;
                  this.cRoot.removeToopTip();
                  if(this.cRoot is Level1 && Level1(this.cRoot).buildSign != null)
                  {
                     Level1(this.cRoot).buildSign.closeMe();
                  }
                  this.§_-2O§();
''','built-in popup off')
write(settings_path,settings)

checks={
 'Level.as':['qolPopupsEnabled','POP-UP HINTS:','if(!Level.qolPopupsEnabled)','popup_hints'],
 sm_path:['qolApplyCategoryVolumes','requestedVolume','global'],
 tut_path:['if(Level.qolPopupsEnabled)'],
 settings_path:['Level.qolPopupsEnabled = false','Level.qolPopupsEnabled = true']
}
for p,needles in checks.items():
    txt=read(p)
    for needle in needles:
        if needle not in txt:
            raise SystemExit(f'{p}: missing {needle}')
print('V12.1 audio/popup patch applied')
