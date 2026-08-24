from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ThreeGameReleaseTests(unittest.TestCase):
    RELEASES = {
        "kingdom-rush-ultimate-v14.swf": "938d42e985f96875c9aae7c90ca8c0fcc63f3bfb2939750e5c39082208907fcc",
        "epic-war-5-expansion-v39.swf": "4efc930562f1d82f3df32bc63a379f7fc58d8a79415596658396b38840869e2d",
        "stick-war-complete-v2.swf": "7ca1ba4b46c677ae9100b1251fd55f64079e64d4230a0abe01a1317e8ae1610a",
    }

    def text(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_release_hashes_are_exact(self) -> None:
        for name, expected in self.RELEASES.items():
            digest = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()
            self.assertEqual(expected, digest, name)

    def test_central_hub_reaches_all_three_real_launchers(self) -> None:
        hub = self.text("index.html")
        for route in (
            "/ultimate/play.html?campaign=ultimate",
            "/stickwar-complete/",
            "/epicwar5-expansion/",
        ):
            self.assertIn(route, hub)
        self.assertIn("KR + KRF V14", hub)
        self.assertIn("Complete Expansion V2", hub)
        self.assertIn("V3.9", hub)

    def test_every_player_uses_the_current_binary(self) -> None:
        pages = {
            "ultimate/play.html": "kingdom-rush-ultimate-v14.swf",
            "stickwar-complete/index.html": "stick-war-complete-v2.swf",
            "iphone/stickwar.html": "stick-war-complete-v2.swf",
            "epicwar5-expansion/index.html": "epic-war-5-expansion-v39.swf",
            "iphone/epicwar5.html": "epic-war-5-expansion-v39.swf",
        }
        for page, asset in pages.items():
            self.assertIn(asset, self.text(page), page)

    def test_live_html_has_no_stale_release_references(self) -> None:
        html = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.html"))
        for stale in (
            "kingdom-rush-ultimate-v13.swf",
            "epic-war-5-expansion-v38.swf",
            "stick-war-complete-v1.swf",
            "Expansion V3.8",
        ):
            self.assertNotIn(stale, html)

    def test_requested_interface_contracts_are_published(self) -> None:
        ultimate = self.text("ultimate/play.html")
        self.assertIn("TWO NATIVE MAPS + SHARED SYSTEMS", ultimate)
        self.assertIn("shared star wallet", ultimate)

        stick = self.text("stickwar-complete/index.html")
        self.assertIn("850 / 700", stick)
        self.assertIn("Visible SANDBOX button", stick)
        self.assertIn("12×", stick)

        ew5 = self.text("epicwar5-expansion/index.html")
        self.assertIn("46-pixel circular sockets", ew5)
        self.assertIn("1×/2×/4×/6×/8×", ew5)
        self.assertIn("opens the result screen immediately", ew5)

    def test_desktop_launchers_use_current_binaries(self) -> None:
        powershell = self.text("desktop/run-native.ps1")
        python = self.text("desktop/run_native.py")
        self.assertIn("stick-war-complete-v2.swf", powershell)
        self.assertIn("stick-war-complete-v2.swf", python)
        self.assertIn("epic-war-5-expansion-v39.swf", powershell)
        self.assertIn("epic-war-5-expansion-v39.swf", python)


if __name__ == "__main__":
    unittest.main()
