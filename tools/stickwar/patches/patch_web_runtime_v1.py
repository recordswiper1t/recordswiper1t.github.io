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

old = '''      private function normalButton() : void
      {
         this.checkCheatMode();
         this.switchToIntro();
         this.main.campaign.setDifficulty(Campaign.D_NORMAL);
      }
      
      private function hardButton() : void
      {
         this.checkCheatMode();
         this.switchToIntro();
         this.main.campaign.setDifficulty(Campaign.D_HARD);
      }
      
      private function insaneButton() : void
      {
         this.checkCheatMode();
         this.switchToIntro();
         this.main.campaign.setDifficulty(Campaign.D_INSANE);
      }
'''
new = '''      private function normalButton() : void
      {
         this.checkCheatMode();
         this.main.campaign.setDifficulty(Campaign.D_NORMAL);
         this.switchToIntro();
      }
      
      private function hardButton() : void
      {
         this.checkCheatMode();
         this.main.campaign.setDifficulty(Campaign.D_HARD);
         this.switchToIntro();
      }
      
      private function insaneButton() : void
      {
         this.checkCheatMode();
         this.main.campaign.setDifficulty(Campaign.D_INSANE);
         this.switchToIntro();
      }
'''
if t.count(old) != 1:
    raise SystemExit(f'CampaignMenuScreen difficulty ordering: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8', newline='\n')
print('patched', p.relative_to(root))

# Battle Lab parameters were originally consumed only by CampaignGameScreen, so the web
# launcher's "Launch Battle Lab" button still landed on the ordinary title menu. Route
# swcLab launches through the normal campaign-map/game-screen lifecycle without loading a
# saved campaign. This keeps lab sessions isolated from the persistent campaign save.
p = root / 'com/brockw/stickwar/stickwar2.as'
t = p.read_text(encoding='utf-8-sig')
old = '''         showScreen("mainMenu");
         tracker = null;
'''
new = '''         paramObj = LoaderInfo(stage.root.loaderInfo).parameters;
         if(paramObj != null && String(paramObj.swcLab) == "1")
         {
            this.campaign.setDifficulty(Campaign.D_NORMAL);
            showScreen("campaignMap");
         }
         else
         {
            showScreen("mainMenu");
         }
         tracker = null;
'''
if t.count(old) != 1:
    raise SystemExit(f'stickwar2 Battle Lab routing: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8', newline='\n')
print('patched', p.relative_to(root))
