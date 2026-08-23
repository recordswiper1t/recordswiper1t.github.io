#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: persisted_popup_state.py <patched-v12.1-scripts-dir>')

root = Path(sys.argv[1])


def read(path):
    return (root / path).read_text(encoding='utf-8-sig')


def write(path, text):
    return (root / path).write_text(text, encoding='utf-8', newline='\n')


def rep(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, got {count}')
    return text.replace(old, new, 1)


# The original SWF initializes game.main.tooltipsStatus=true on every fresh
# session, and its built-in Tooltip ON/OFF handler never persists that field.
# V12.1 added Level.qolPopupsEnabled as another in-memory master. Persist one
# explicit KRF QoL preference and keep both runtime values synchronized.
level = read('Level.as')

level = rep(
    level,
    '''         this.qolDiagLastMs = getTimer();
         this.qolRunStartMs = getTimer();
         this.qolLoadBestTime();''',
    '''         this.qolDiagLastMs = getTimer();
         this.qolRunStartMs = getTimer();
         this.qolLoadPopupPreference();
         this.qolLoadBestTime();''',
    'load popup preference during level init',
)

anchor = '''      private function qolTimeAttackKey() : String
'''
helpers = r'''      private function qolLoadPopupPreference() : void
      {
         var save:SharedObject = null;
         try
         {
            save = SharedObject.getLocal("krf_qol_settings");
            if(save.data.hasOwnProperty("popupsEnabled"))
            {
               Level.qolPopupsEnabled = Boolean(save.data.popupsEnabled);
            }
            else
            {
               Level.qolPopupsEnabled = this.game.main.tooltipsStatus;
            }
            this.game.main.tooltipsStatus = Level.qolPopupsEnabled;
            save.close();
         }
         catch(err:Error)
         {
            Level.qolPopupsEnabled = this.game.main.tooltipsStatus;
         }
      }
      
      public function qolSavePopupPreference(param1:Boolean) : void
      {
         var save:SharedObject = null;
         Level.qolPopupsEnabled = param1;
         this.game.main.tooltipsStatus = param1;
         try
         {
            save = SharedObject.getLocal("krf_qol_settings");
            save.data.popupsEnabled = param1;
            save.flush();
            save.close();
         }
         catch(err:Error)
         {
         }
      }
      
'''+anchor
level = rep(level, anchor, helpers, 'popup persistence helpers')

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
            this.qolSavePopupPreference(nextPopupState);
            if(!nextPopupState)
''',
    'popup toggle synchronization and persistence',
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

# The scripted Level-1 BUILD HERE sign is created outside Level itself, so it
# checks both synchronized runtime values after Level loads the saved preference.
tutorial_path = '§dynamic const function§.as'
tutorial = read(tutorial_path)
tutorial = rep(
    tutorial,
    '         if(Level.qolPopupsEnabled)\n',
    '         if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)\n',
    'build sign persisted gate',
)
write(tutorial_path, tutorial)

# The built-in settings menu must use the same persistence function. This is the
# missing link in the original SWF: it only mutated tooltipsStatus in memory.
settings_path = '§_-bK§.as'
settings = read(settings_path)
settings = rep(
    settings,
    '''                  this.cRoot.game.main.tooltipsStatus = true;
                  Level.qolPopupsEnabled = true;
                  this.§_-2O§();
''',
    '''                  this.cRoot.qolSavePopupPreference(true);
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
    '''                  this.cRoot.qolSavePopupPreference(false);
                  this.cRoot.removeToopTip();
''',
    'built-in popup off persistence',
)
write(settings_path, settings)

checks = {
    'Level.as': [
        'SharedObject.getLocal("krf_qol_settings")',
        'save.data.popupsEnabled = param1',
        'save.flush()',
        'qolLoadPopupPreference();',
        'qolSavePopupPreference(nextPopupState)',
        'Level.qolPopupsEnabled && this.game.main.tooltipsStatus ? "ON" : "OFF"',
        'if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)',
    ],
    tutorial_path: [
        'if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)',
    ],
    settings_path: [
        'this.cRoot.qolSavePopupPreference(true)',
        'this.cRoot.qolSavePopupPreference(false)',
    ],
}
for path, needles in checks.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{path}: missing {needle}')

print('V12.1 persisted popup preference applied')
