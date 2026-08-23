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

old = '''         this.mc.mainPanel.stickWarButton.addEventListener(MouseEvent.CLICK,this.stickWarButton);
         this.mc.introBrokenMc.addEventListener(MouseEvent.CLICK,this.openIntroLink);
         this.mc.creditsScreen.visible = false;
      }
      
      private function skipButton() : void
'''
new = '''         this.mc.mainPanel.stickWarButton.addEventListener(MouseEvent.CLICK,this.stickWarButton);
         this.mc.introBrokenMc.addEventListener(MouseEvent.CLICK,this.openIntroLink);
         this.mc.creditsScreen.visible = false;
         if(this.main.loaderInfo != null && String(this.main.loaderInfo.parameters.swcLab) == "1")
         {
            // Battle Lab FlashVars were previously consumed only after entering a battle,
            // so the web launcher could not actually launch the configured lab. Route the
            // fresh, unsaved campaign instance into level 0 on the next frame.
            this.main.campaign.setDifficulty(Campaign.D_NORMAL);
            addEventListener(Event.ENTER_FRAME,this.startBattleLabOnce,false,0,true);
         }
      }
      
      private function startBattleLabOnce(evt:Event) : void
      {
         removeEventListener(Event.ENTER_FRAME,this.startBattleLabOnce);
         this.main.showScreen("campaignMap",false,true);
      }
      
      private function skipButton() : void
'''
if t.count(old) != 1:
    raise SystemExit(f'CampaignMenuScreen Battle Lab routing: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)

old = '''         this.buttons = [];
         this.keyboard.cleanUp();
         this.youtubeLoader.stopVideo();
         this.mouseState.cleanUp();
'''
new = '''         this.buttons = [];
         this.keyboard.cleanUp();
         if(this.youtubeLoader != null)
         {
            this.youtubeLoader.stopVideo();
         }
         this.mouseState.cleanUp();
'''
if t.count(old) != 1:
    raise SystemExit(f'CampaignMenuScreen leave loader guard: expected 1 match, got {t.count(old)}')
t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8', newline='\n')
print('patched', p.relative_to(root))
