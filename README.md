# Flash strategy mod lab

This repository contains three performance-first Flash/ActionScript mod projects. Release binaries are built through pinned-source/FFDec workflows and are only promoted when their release checks pass.

## Play now

The GitHub Pages root is the shared **laptop + iPhone game hub**. Laptop buttons open the full browser shells; iPhone buttons use the lighter touch-first players.

For the highest laptop performance, download/extract the repository and use native Ruffle:

```text
# Windows
desktop\run-native.bat --game krf
desktop\run-native.bat --game stickwar
desktop\run-native.bat --game epicwar5
desktop\run-native.bat --game epicwar5-expansion

# macOS / Linux
sh desktop/run-native.sh --game krf
sh desktop/run-native.sh --game stickwar
sh desktop/run-native.sh --game epicwar5
sh desktop/run-native.sh --game epicwar5-expansion
```

The launcher downloads native Ruffle on first use and reuses the cached executable. See [`desktop/README.md`](desktop/README.md) for renderer fallback, stable/nightly selection and performance notes.

## Project status

| Project | Current state | Main features |
| --- | --- | --- |
| **Kingdom Rush Frontiers** | Released on `main` through V12/V12.1 | Full sandbox, tower clipboard, hero/enemy controls, Time Attack/loop scoring, diagnostics, adaptive performance controls, **The Last Rift** expansion |
| **Kingdom Rush Ultimate (KR + KRF)** | Active V13 integration in PR #42 | Frontiers V12.1 runtime + KR1 campaign/content import, combined campaign routing, 16 tier-4 targets, combined hero target, inherited V11/V12 sandbox/performance systems |
| **Super Stick War (SW1 + SW2)** | **Released V1 on `main`** | 65-stage combined campaign, Order/Chaos progression, 108 mastery nodes, possession, Battle Lab, F2 sandbox, F1 diagnostics and performance patches |
| **Epic War 5** | Released on `main` through Expansion V3.4 | Expanded campaign/equipment/progression, repaired battle transitions, optional battle sandbox, large-battle performance and release verification |

The repository is deliberately fail-closed: a generated SWF is not described as a release merely because it serializes. Build pipelines re-decompile and verify required gameplay/mod markers before publication.

## Kingdom Rush Frontiers — current released mod

Current Frontiers V12 keeps the V11 sandbox/performance feature set and adds **The Last Rift**, post-boss scoring, renderer hardening and additional performance work. V12.1 contains the current audio/pop-up polish, and its POP-UP HINTS / Tooltips preference is stored separately from campaign saves so the choice persists across fresh Ruffle sessions. Level 15 records are finalized only after all 30 Last Rift waves, so the original boss transition cannot save a partial expansion run.

The in-level sandbox includes heroes, enemy spawning, Send All, Time Attack, recycle/loop play, tower clipboard, cleanup/cheat controls, diagnostics and adaptive load controls. Native Ruffle is recommended for large swarms because it avoids browser/WebAssembly overhead.

## Kingdom Rush Ultimate — V13

Development lives in [PR #42](../../pull/42). The architecture keeps Frontiers V12.1 as the authoritative runtime and imports KR1 content through a collision-safe namespace/rebind layer so existing sandbox/performance systems remain intact.

The branch is not promoted to a release until imported KR stages, KR tower/hero compatibility, combined campaign saves/UI and final FFDec round-trip/runtime gates pass. See `docs/KINGDOM_RUSH_ULTIMATE.md` and `docs/KINGDOM_RUSH_ULTIMATE_STATUS.md` on that branch for the detailed compatibility/release plan.

## Super Stick War — SW1 + SW2

**V1 is released on `main`.** The verified binary is `assets/stick-war-complete-v1.swf`, with matching `STICKWAR-COMPLETE-V1-BUILD.txt` and SHA-256 manifest in `assets/`. The playable web shell is under `stickwar-complete/`.

V1 includes a 65-stage campaign, playable Order/Chaos progression, 108 mastery nodes, direct possession, authored expansion objectives, Battle Lab presets, sandbox controls, diagnostics and performance optimization without lowering combat simulation rate. The release SWF passed FFDec import and fresh re-decompile verification before publication.

## Epic War 5

Released assets and build records live under `assets/`; the stable game page remains under `epicwar5/` and the completed expansion is under `epicwar5-expansion/`. V3.4 retains the V3.3.1 performance/sitelock stack, repairs Expansion battle entry, and adds a default-off battle sandbox.

The V3.x toolchain lives under `tools/epicwar5/expansion/`, including the V3.3 performance work, V3.4 runtime/sandbox patch, frozen invariant validator and reproducible FFDec rebuild workflows.

## Release verification

Verified releases use matching build/checksum records in `assets/`. GitHub Actions workflows under `.github/workflows/` perform source pinning where applicable, FFDec import/re-export checks and release-marker validation before publication.
