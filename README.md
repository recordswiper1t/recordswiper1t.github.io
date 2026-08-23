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

# macOS / Linux
sh desktop/run-native.sh --game krf
sh desktop/run-native.sh --game stickwar
sh desktop/run-native.sh --game epicwar5
```

The launcher downloads native Ruffle on first use and reuses the cached executable. See [`desktop/README.md`](desktop/README.md) for renderer fallback, stable/nightly selection and performance notes.

## Project status

| Project | Current state | Main features |
| --- | --- | --- |
| **Kingdom Rush Ultimate (KR + KRF)** | **Release-ready two-campaign launcher** | Complete original KR publisher runtime plus offline-ready Frontiers V12.2, separate saves, campaign switching, sandbox/performance systems and **The Last Rift** |
| **Super Stick War (SW1 + SW2)** | **Released V1 on `main`** | 65-stage combined campaign, Order/Chaos progression, 108 mastery nodes, possession, Battle Lab, F2 sandbox, F1 diagnostics and performance patches |
| **Epic War 5** | **Expansion V3.8 complete locally** | 12 readable unit slots, redesigned sandbox dashboard, moving spawned armies, expanded campaign/equipment/progression and large-battle performance work |

The repository is deliberately fail-closed: a generated SWF is not described as a release merely because it serializes. Build pipelines re-decompile and verify required gameplay/mod markers before publication.

## Kingdom Rush Frontiers — current expansion

Frontiers V12 keeps the V11 sandbox/performance feature set and adds **The Last Rift**, post-boss scoring, renderer hardening and additional performance work. V12.1 contains the current audio/pop-up polish. V12.2 preserves all of it and removes the obsolete online-service startup gate that could loop on fresh browsers.

The in-level sandbox includes heroes, enemy spawning, Send All, Time Attack, recycle/loop play, tower clipboard, cleanup/cheat controls, diagnostics and adaptive load controls. Native Ruffle is recommended for large swarms because it avoids browser/WebAssembly overhead.

## Kingdom Rush Ultimate — KR + KRF

The browser launcher under `ultimate/` exposes both complete, tested campaigns from one access point. Original Kingdom Rush runs in its publisher engine and Frontiers runs in the enhanced V12.2 engine; the two runtimes and save namespaces stay isolated so switching campaigns cannot trigger the class collisions found in the abandoned single-SWF experiments.

The earlier shared-engine V13 work remains documented under `docs/` as development history, but no broken composed SWF is exposed by the site.

## Super Stick War — SW1 + SW2

**V1 is released on `main`.** The verified binary is `assets/stick-war-complete-v1.swf`, with matching `STICKWAR-COMPLETE-V1-BUILD.txt` and SHA-256 manifest in `assets/`. The playable web shell is under `stickwar-complete/`.

V1 includes a 65-stage campaign, playable Order/Chaos progression, 108 mastery nodes, direct possession, authored expansion objectives, Battle Lab presets, sandbox controls, diagnostics and performance optimization without lowering combat simulation rate. The release SWF passed FFDec import and fresh re-decompile verification before publication.

## Epic War 5

Released assets and build records live under `assets/`; the game pages are under `epicwar5/` and `epicwar5-expansion/`. The expansion line progressed through V3/V3.1/V3.2 to the V3.3 performance/quality release and V3.3.1 site-hosting hotfix.

The V3.x toolchain lives under `tools/epicwar5/expansion/`, including the dedicated V3.3 performance patch and validation/rebuild workflows.

## Release verification

Verified releases use matching build/checksum records in `assets/`. GitHub Actions workflows under `.github/workflows/` perform source pinning where applicable, FFDec import/re-export checks and release-marker validation before publication.
