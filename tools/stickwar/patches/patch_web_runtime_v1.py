#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_web_runtime_v1.py <scripts-root>')
root = Path(sys.argv[1])

p = root / 'com/brockw/stickwar/campaign/CampaignMenuScreen.as'
t = p.read_text(encoding='utf-8-sig')

old = '''         Security.allowDomain("stickempires.com");
         urlRequest = new URLRequest("http://www.stickempires.com/getIntroLink");
         urlLoader = new URLLoader();
         urlLoader.dataFormat = URLLoaderDataFormat.TEXT;
         urlLoader.addEventListener(Event.COMPLETE,this.handleComplete);
         urlLoader.load(urlRequest);
         this.youtubeLoader = new YoutubeLoader("w6q9EoFmu0w");
         addChild(this.youtubeLoader);
'''
new = '''         // SUPER STICK WAR WEB RUNTIME V1: the original SW2 menu tried two Flash-era
         // HTTP services at startup (StickEmpires getIntroLink + YouTube AS3 player).
         // Modern HTTPS browsers/Ruffle cannot use either endpoint. Keep the expansion
         // self-contained and do not let dead cross-origin loaders interfere with play.
         this.youtubeLoader = null;
'''
if t.count(old) != 1:
    raise SystemExit(f'CampaignMenuScreen startup networking: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)

old = '''      private function switchToIntro() : void
      {
         this.mc.gotoAndStop("mainMenu");
         this.state = S_INTRO;
         this.main.soundManager.playSoundInBackground("");
         this.timeSinceTriedToStartYoutube = getTimer();
      }
'''
new = '''      private function switchToIntro() : void
      {
         // SUPER STICK WAR WEB RUNTIME V1: the original intro was a remote YouTube
         // Flash player which no longer exists. Continue directly to the campaign map
         // after difficulty selection instead of entering a permanently broken loader.
         this.main.soundManager.playSoundInBackground("");
         this.main.showScreen("campaignMap",false,true);
      }
'''
if t.count(old) != 1:
    raise SystemExit(f'CampaignMenuScreen intro transition: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8', newline='\n')
print('patched', p.relative_to(root))
