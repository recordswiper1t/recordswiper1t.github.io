from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ThreeGameReleaseTests(unittest.TestCase):
    RELEASES = {
        "kingdom-rush-ultimate-v17.swf": "5c7bee6a283d3f2ff5b5e23a9fe73d57ff64a3c6051b7148fc4d012c4779c26e",
        "epic-war-5-expansion-v43.swf": "8f5b1cde585868205b62b44c606be6073d6cd709868bf5a69d0c36224e7eab74",
        "stick-war-complete-v31.swf": "dc20743d230b221d09e9cce599df1ca02ebff7de9dfd7f6fd0b72997bfa4b342",
    }

    def text(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_release_hashes_are_exact(self) -> None:
        for name, expected in self.RELEASES.items():
            digest = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()
            self.assertEqual(expected, digest, name)

    def test_manifests_pin_the_same_release_hashes(self) -> None:
        manifests = {
            "kingdom-rush-ultimate-v17.swf": "KINGDOM-RUSH-ULTIMATE-V17-SHA256SUMS.txt",
            "stick-war-complete-v31.swf": "STICKWAR-COMPLETE-V31-SHA256SUMS.txt",
            "epic-war-5-expansion-v43.swf": "EPICWAR5-EXPANSION-V43-SHA256SUMS.txt",
        }
        for asset, manifest in manifests.items():
            self.assertEqual(
                f"{self.RELEASES[asset]}  {asset}",
                self.text(f"assets/{manifest}").strip(),
                manifest,
            )

    def test_central_hub_reaches_all_three_real_launchers(self) -> None:
        hub = self.text("index.html")
        for route in (
            "/ultimate/play.html?campaign=ultimate",
            "/stickwar-complete/",
            "/epicwar5-expansion/",
        ):
            self.assertIn(route, hub)
        self.assertIn("KR + KRF V17", hub)
        self.assertIn("Complete Expansion V3.1", hub)
        self.assertIn("V4.3", hub)

    def test_every_player_uses_the_current_binary(self) -> None:
        pages = {
            "ultimate/play.html": "kingdom-rush-ultimate-v17.swf",
            "stickwar-complete/index.html": "stick-war-complete-v31.swf",
            "iphone/stickwar.html": "stick-war-complete-v31.swf",
            "epicwar5-expansion/index.html": "epic-war-5-expansion-v43.swf",
            "iphone/epicwar5.html": "epic-war-5-expansion-v43.swf",
        }
        for page, asset in pages.items():
            self.assertIn(asset, self.text(page), page)

    def test_live_html_has_no_stale_release_references(self) -> None:
        html = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.html"))
        for stale in (
            "kingdom-rush-ultimate-v13.swf",
            "kingdom-rush-ultimate-v14.swf",
            "kingdom-rush-ultimate-v15.swf",
            "kingdom-rush-ultimate-v16.swf",
            "epic-war-5-expansion-v38.swf",
            "epic-war-5-expansion-v39.swf",
            "epic-war-5-expansion-v40.swf",
            "epic-war-5-expansion-v41.swf",
            "epic-war-5-expansion-v42.swf",
            "stick-war-complete-v1.swf",
            "stick-war-complete-v2.swf",
            "stick-war-complete-v3.swf",
            "Expansion V3.8",
        ):
            self.assertNotIn(stale, html)

    def test_requested_interface_contracts_are_published(self) -> None:
        ultimate = self.text("ultimate/play.html")
        self.assertIn("TWO NATIVE MAPS + CROSSOVER ARMORIES", ultimate)
        self.assertIn("stateful crossover", ultimate)
        self.assertIn('ultimateDirect:"1"', ultimate)

        stick = self.text("stickwar-complete/index.html")
        self.assertIn("850 / 700", stick)
        self.assertIn("Visible SANDBOX button", stick)
        self.assertIn("12×", stick)
        self.assertIn("31-direct-lab", stick)

        ew5 = self.text("epicwar5-expansion/index.html")
        self.assertIn("Animated soldier cards", ew5)
        self.assertIn("Battle Forge", ew5)
        self.assertIn("1×/2×/4×/6×/8×", ew5)
        self.assertIn("opens the result screen immediately", ew5)

    def test_desktop_launchers_use_current_binaries(self) -> None:
        powershell = self.text("desktop/run-native.ps1")
        python = self.text("desktop/run_native.py")
        self.assertIn("stick-war-complete-v31.swf", powershell)
        self.assertIn("stick-war-complete-v31.swf", python)
        self.assertIn("epic-war-5-expansion-v43.swf", powershell)
        self.assertIn("epic-war-5-expansion-v43.swf", python)

    def test_self_hosted_runtime_and_quality_controls(self) -> None:
        self.assertTrue((ROOT / "vendor/ruffle/0.5.0/ruffle.js").is_file())
        for page in ("ultimate/play.html", "stickwar-complete/index.html", "epicwar5-expansion/index.html"):
            html = self.text(page)
            self.assertIn("/vendor/ruffle/0.5.0/ruffle.js", html, page)
            self.assertNotIn("unpkg.com/@ruffle-rs/ruffle", html, page)
        self.assertIn("stickwar-quality", self.text("stickwar-complete/index.html"))
        self.assertIn("ew5-quality", self.text("epicwar5-expansion/index.html"))

    def test_gameplay_patch_sources_cover_audited_gaps(self) -> None:
        stick = self.text("tools/stickwar/patches/patch_gameplay_v3.py")
        for objective in ("escort", "siege", "assassinate", "interrupt", "defend"):
            self.assertIn(f'return "{objective}"', stick)
        self.assertIn("CAMPAIGN ATLAS", stick)
        stick_entry = self.text("tools/stickwar/patches/patch_entry_v31.py")
        for marker in ("launchDirectBattleLab", "enableSandbox", "CLEAR ENEMIES", "sandbox_close"):
            self.assertIn(marker, stick_entry)

        kr = self.text("tools/ultimate/patch_crossover_native_v16.py")
        for marker in ("ultimateGuestHealthMax", "ultimateGuestEnemySnapshot", "krDelta + krfDelta"):
            self.assertIn(marker, kr)
        self.assertIn("ultimateDirect", self.text("tools/ultimate/patch_direct_boot_v17.py"))

        kr_runtime = self.text("tools/ultimate/patch_shared_runtime_v14.py")
        for marker in (
            "qolInstantWinCommitted",
            "Level15(this).qolInstantWinFinalStage()",
            "qolV12PostBossComplete = true",
            "gotoAndStop(99)",
        ):
            self.assertIn(marker, kr_runtime)

        ew5 = self.text("tools/epicwar5/expansion/patch_gameplay_v41.py")
        for marker in ("expansionSpatialCandidates", "selectGroupUnit(12)", "case 25:"):
            self.assertIn(marker, ew5)
        ew5_runtime = self.text("tools/epicwar5/expansion/patch_hud_speed_v39.py")
        self.assertIn('this.battle_result = "win"', ew5_runtime)
        self.assertIn("truly immediate Epic War victory result", ew5_runtime)
        ew5_access = self.text("tools/epicwar5/expansion/patch_access_v42.py")
        for marker in ("working Continue button", "parameters.ew5ExpansionDirect", "automatic Expansion campaign panel"):
            self.assertIn(marker, ew5_access)
        ew5_palette = self.text("tools/epicwar5/expansion/patch_forge_palette_v43.py")
        for marker in ("panel dark iron", "card crimson/dark fill", "Forge parchment status"):
            self.assertIn(marker, ew5_palette)


if __name__ == "__main__":
    unittest.main()
