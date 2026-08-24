#!/usr/bin/env python3
"""Remove obsolete title-screen network dependencies from Super Stick War V1."""

from pathlib import Path
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: patch_offline_startup_v1.py <scripts-root>")

root = Path(sys.argv[1])


def replace_once(relative_path: str, old: str, new: str, label: str) -> None:
    path = root / relative_path
    text = path.read_text(encoding="utf-8-sig")
    matches = text.count(old)
    if matches != 1:
        raise SystemExit(
            f"{relative_path} {label}: expected 1 match, got {matches}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


MENU = "com/brockw/stickwar/campaign/CampaignMenuScreen.as"
replace_once(
    MENU,
    '''         Security.allowDomain("stickempires.com");
         urlRequest = new URLRequest("http://www.stickempires.com/getIntroLink");
         urlLoader = new URLLoader();
         urlLoader.dataFormat = URLLoaderDataFormat.TEXT;
         urlLoader.addEventListener(Event.COMPLETE,this.handleComplete);
         urlLoader.load(urlRequest);
         this.youtubeLoader = new YoutubeLoader("w6q9EoFmu0w");
''',
    '''         // The original intro endpoints were retired years ago. Keep the
         // loader object for the menu lifecycle, but never perform a network load.
         this.youtubeLoader = new YoutubeLoader("");
''',
    "remove eager title network requests",
)

replace_once(
    MENU,
    '''         if(this.isFirst)
         {
            this.switchToFadeIn();
         }
         else
         {
            this.switchToMainMenu();
         }
         this.isFirst = false;
''',
    '''         // The website already provides the campaign/lab launcher. Open the
         // playable campaign setup directly instead of a second legacy link menu.
         this.switchToNewOrContinue();
         this.isFirst = false;
''',
    "open campaign setup directly",
)

for difficulty, constant in (
    ("normal", "D_NORMAL"),
    ("hard", "D_HARD"),
    ("insane", "D_INSANE"),
):
    replace_once(
        MENU,
        f'''      private function {difficulty}Button() : void
      {{
         this.checkCheatMode();
         this.switchToIntro();
         this.main.campaign.setDifficulty(Campaign.{constant});
      }}
''',
        f'''      private function {difficulty}Button() : void
      {{
         this.checkCheatMode();
         this.main.campaign.setDifficulty(Campaign.{constant});
         this.skipButton();
      }}
''',
        f"offline {difficulty} campaign start",
    )

YOUTUBE = "com/brockw/stickwar/campaign/YoutubeLoader.as"
replace_once(
    YOUTUBE,
    '''         Security.allowDomain("www.youtube.com");
         this.ready = false;
         my_loader = new Loader();
         my_loader.load(new URLRequest("http://www.youtube.com/apiplayer?version=3"));
         my_loader.contentLoaderInfo.addEventListener(Event.INIT,onLoaderInit);
         this.hadError = false;
''',
    '''         // YouTube's Flash player no longer exists. This deliberately inert
         // object preserves callers that stop/hide the former intro player.
         this.ready = false;
         this.hadError = true;
''',
    "disable retired YouTube Flash player",
)

print("Offline title startup V1 applied")
