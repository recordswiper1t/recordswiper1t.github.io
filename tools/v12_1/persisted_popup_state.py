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
# built-in Tooltips preference is stored on game.main.tooltipsStatus. The static
# master resets to true on every fresh SWF session, so a saved Tooltips=OFF
# preference could still allow notification cards until the settings UI was
# touched. Keep both controls in lockstep and always honor the persisted value.
level = read('Level.as')
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
            Level.qolPopupsEnabled = nextPopupState;
            this.game.main.tooltipsStatus = nextPopupState;
            if(!nextPopupState)
''',
    'popup toggle synchronization',
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
# must check the saved Tooltips value in addition to the session master.
tutorial_path = '§dynamic const function§.as'
tutorial = read(tutorial_path)
tutorial = rep(
    tutorial,
    '         if(Level.qolPopupsEnabled)\n',
    '         if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)\n',
    'build sign persisted gate',
)
write(tutorial_path, tutorial)

checks = {
    'Level.as': [
        'nextPopupState',
        'Level.qolPopupsEnabled && this.game.main.tooltipsStatus ? "ON" : "OFF"',
        'if(!Level.qolPopupsEnabled || !this.game.main.tooltipsStatus)',
    ],
    tutorial_path: [
        'if(Level.qolPopupsEnabled && this.level.game.main.tooltipsStatus)',
    ],
}
for path, needles in checks.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{path}: missing {needle}')

print('V12.1 persisted popup-state integration applied')
