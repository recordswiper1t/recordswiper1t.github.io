#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: persisted_popup_state.py <patched-v12.1-scripts-dir>')

root = Path(sys.argv[1])


def read(path):
    return (root / path).read_text(encoding='utf-8-sig')


def write(path, text):
    (root / path).write_text(text, encoding='utf-8', newline='\n')


def rep(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, got {count}')
    return text.replace(old, new, 1)


# V12.1 introduced a second popup master (Level.qolPopupsEnabled), while the
# original game keeps tooltipsStatus only in memory and resets it to true on a
# fresh SWF session. Persist the preference in a dedicated QOL SharedObject so
# campaign saves and Time Attack records remain untouched.
level = read('Level.as')
level = rep(
    level,
    '''      public function Level(param1:Array, param2:Array, param3:int = 0, param4:Boolean = false)
      {
         super();
         this.mode = param3;
''',
    '''      public function Level(param1:Array, param2:Array, param3:int = 0, param4:Boolean = false)
      {
         super();
         this.qolLoadPopupPreference();
         this.mode = param3;
''',
    'load popup preference at Level construction',
)
level = rep(
    level,
    '''      private function qolTimeAttackKey() : String
''',
    '''      private function qolLoadPopupPreference() : void
      {
         var save:SharedObject = null;
         var enabled:Boolean = true;
         if(this.game != null && this.game.main != null)
         {
            enabled = this.game.main.tooltipsStatus;
         }
         try
         {
            save = SharedObject.getLocal("krf_qol_settings");
            if(save.data.hasOwnProperty("popupsEnabled"))
            {
               enabled = Boolean(save.data.popupsEnabled);
            }
         }
         catch(error:Error)
         {
         }
         Level.qolPopupsEnabled = enabled;
         if(this.game != null && this.game.main != null)
         {
            this.game.main.tooltipsStatus = enabled;
         }
      }

      public function qolSetPopupPreference(param1:Boolean) : void
      {
         var save:SharedObject = null;
         Level.qolPopupsEnabled = param1;
         if(this.game != null && this.game.main != null)
         {
            this.game.main.tooltipsStatus = param1;
         }
         try
         {
            save = SharedObject.getLocal("krf_qol_settings");
            save.data.popupsEnabled = param1;
            save.flush();
         }
         catch(error:Error)
         {
         }
      }

      private function qolTimeAttackKey() : String
''',
    'popup preference persistence methods',
)
level = rep(
    level,
    'this.qolSettings.addChild(this.qolButton("POP-UP HINTS: " + (Level.qolPopupsEnabled ? "ON" : "OFF"),28,386,524,"popup_hints"));',
    'this.qolSettings.addChild(this.qolButton("POP-UP HINTS: " + (Level.qolPopupsEnabled && this.game.main.tooltipsStatus ? "ON" : "OFF"),28,386,524,"popup_hints"));',
    'popup button persisted state',
)
level = rep(
    level,
    '''         else if(action == "popup_hints")
         {
            Level.qolPopupsEnabled = !Level.qolPopupsEnabled;
            this.game.main.tooltipsStatus = Level.qolPopupsEnabled;
            if(!Level.qolPopupsEnabled)
''',
    '''         else if(action == "popup_hints")
         {
            var nextPopupState:Boolean = !(Level.qolPopupsEnabled && this.game.main.tooltipsStatus);
            this.qolSetPopupPreference(nextPopupState);
            if(!nextPopupState)
''',
    'popup toggle persistence',
)
level = rep(
    level,
    '''      public function sendPauseNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled)
''',
    '''      public function sendPauseNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)
''',
    'pause notification persisted gate',
)
level = rep(
    level,
    '''      public function sendSecondLevelNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled)
''',
    '''      public function sendSecondLevelNotification(param1:String) : void
      {
         if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)
''',
    'second notification persisted gate',
)
level = rep(
    level,
    '''      public function §_-gU§() : void
      {
         if(!Level.qolPopupsEnabled)
''',
    '''      public function §_-gU§() : void
      {
         if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)
''',
    'generic notification persisted gate',
)
write('Level.as', level)

# The scripted Level 1 BUILD HERE sign is created outside Level itself, so it
# must check the restored Tooltips value in addition to the session master.
tutorial_path = '§dynamic const function§.as'
tutorial = read(tutorial_path)
tutorial = rep(
    tutorial,
    '         if(Level.qolPopupsEnabled)\n',
    '         if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)\n',
    'build sign persisted gate',
)
write(tutorial_path, tutorial)

# Route the original settings panel through the same public setter. Its stock
# tooltip toggle only redraws the buttons and otherwise has no persistence.
settings_path = '§_-bK§.as'
settings = read(settings_path)
settings = rep(
    settings,
    '''                  this.cRoot.game.main.tooltipsStatus = true;
                  Level.qolPopupsEnabled = true;
                  this.§_-2O§();
''',
    '''                  this.cRoot.qolSetPopupPreference(true);
                  this.§_-2O§();
''',
    'built-in popup on persistence',
)
settings = rep(
    settings,
    '''                  this.cRoot.game.main.tooltipsStatus = false;
                  Level.qolPopupsEnabled = false;
                  this.cRoot.removeToopTip();
''',
    '''                  this.cRoot.qolSetPopupPreference(false);
                  this.cRoot.removeToopTip();
''',
    'built-in popup off persistence',
)
write(settings_path, settings)

checks = {
    'Level.as': [
        'this.qolLoadPopupPreference();',
        'qolLoadPopupPreference',
        'qolSetPopupPreference',
        'SharedObject.getLocal("krf_qol_settings")',
        'save.data.popupsEnabled = param1',
        'save.flush()',
        'nextPopupState',
        'Level.qolPopupsEnabled && this.game.main.tooltipsStatus ? "ON" : "OFF"',
        'if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)',
    ],
    tutorial_path: [
        'if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)',
    ],
    settings_path: [
        'this.cRoot.qolSetPopupPreference(true)',
        'this.cRoot.qolSetPopupPreference(false)',
    ],
}
for path, needles in checks.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{path}: missing {needle}')

print('V12.1 persisted popup preference integration applied')
