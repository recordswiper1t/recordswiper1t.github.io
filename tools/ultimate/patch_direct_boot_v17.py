#!/usr/bin/env python3
"""Boot the combined release directly into its native map instead of ad/title gates."""

from __future__ import annotations

import argparse
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    path = args.source
    text = read(path)
    if "ultimateDirect" not in text:
        text = once(
            text,
            """      private function §_-Ea§(param1:Event) : void
      {
         this.§override do§.removeEventListener(Event.COMPLETE,this.§_-Ea§);
         §in extends§(this.§override do§).addPlayListeners();
      }
""",
            """      private function §_-Ea§(param1:Event) : void
      {
         this.§override do§.removeEventListener(Event.COMPLETE,this.§_-Ea§);
         if(this.loaderInfo != null && String(this.loaderInfo.parameters.ultimateDirect) == "1")
         {
            this.§import for§();
         }
         else
         {
            §in extends§(this.§override do§).addPlayListeners();
         }
      }
""",
            "preloader bypass",
        )
        text = once(
            text,
            """      public function initGame() : void
      {
         this.tooltipsStatus = true;
         this.§do§();
         this.§_-1z§();
         this.showMainMenu();
      }
""",
            """      public function initGame() : void
      {
         this.tooltipsStatus = true;
         this.§do§();
         this.§_-1z§();
         if(this.loaderInfo != null && String(this.loaderInfo.parameters.ultimateDirect) == "1")
         {
            this.loadGame("krslot1");
         }
         else
         {
            this.showMainMenu();
         }
      }
""",
            "direct map boot",
        )
    write(path, text)
    final = read(path)
    for needle in ["ultimateDirect", 'this.loadGame("krslot1")', "this.§import for§();"]:
        if needle not in final:
            raise SystemExit(f"validation failed: {needle!r}")
    print("Kingdom Rush Ultimate V17 direct native-map boot applied")


if __name__ == "__main__":
    main()
