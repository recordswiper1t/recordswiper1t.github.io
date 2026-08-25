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
| **Kingdom Rush Ultimate (KR + KRF)** | **Released V17 combined runtime** | Direct native-map entry, 19 sourced Kingdom Rush stages plus 15 Frontiers stages, map switching, unified stars/system access, game-styled war rooms and bidirectional guest tower/hero armories |
| **Super Stick War (SW1 + SW2)** | **Released V3.1** | 65-stage combined campaign, seven-chapter atlas, real objective state machines, direct Battle Lab, soldier-card sandbox, 108 mastery nodes, possession and adaptive performance patches |
| **Epic War 5** | **Released Expansion V4.3** | Repaired direct access and Continue flow, polished bronze/crimson soldier-card Battle Forge, compact circular slots 7–12, moving spawned armies, adaptive 8× speed, immediate Instant Win, expanded progression and large-battle performance work |

The repository is deliberately fail-closed: a generated SWF is not described as a release merely because it serializes. Build pipelines re-decompile and verify required gameplay/mod markers before publication.

## Kingdom Rush Frontiers — current expansion

Frontiers V12 keeps the V11 sandbox/performance feature set and adds **The Last Rift**, post-boss scoring, renderer hardening and additional performance work. V12.1 contains the current audio/pop-up polish. V12.2 preserves all of it and removes the obsolete online-service startup gate that could loop on fresh browsers.

The in-level sandbox includes heroes, enemy spawning, Send All, Time Attack, recycle/loop play, tower clipboard, cleanup/cheat controls, diagnostics and adaptive load controls. Native Ruffle is recommended for large swarms because it avoids browser/WebAssembly overhead.

## Kingdom Rush Ultimate — KR + KRF

The browser launcher under `ultimate/` defaults to the verified V17 combined runtime and enters the saved native map directly, bypassing the obsolete promotional and slot-selection gates. It exposes 19 sourced Kingdom Rush stages and all 15 Frontiers campaign stages on their native maps. Each campaign has a game-styled armory that deploys the other game's eight tier-four towers and source-ready hero roster through an explicit host-compatible guest combat mode. The original Kingdom Rush and cleaned Frontiers V12.2 engines remain available as isolated-save recovery paths.

The combined release was verified through Southport's complete seven-wave victory loop, Frontiers stage launches and enemy movement, shared-map return routing, and all five selector pages. Retired Mochi and CPMStar requests are removed from the combined and standalone Frontiers startup paths.

## Super Stick War — SW1 + SW2

**V3.1 is the current release.** The verified binary is `assets/stick-war-complete-v31.swf`, with matching V3.1 build and SHA-256 records in `assets/`. The playable web shell is under `stickwar-complete/`; its Battle Lab button now enters a battle directly instead of hiding the sandbox behind the original title and difficulty screens.

V3.1 includes a 65-stage campaign, playable Order/Chaos progression, seven chapter atlas, objective-specific escort/siege/assassination/interruption/defense logic, 108 mastery nodes, direct possession, Battle Lab presets, explicit sandbox controls, diagnostics and performance optimization without lowering combat simulation rate. The release SWF passed strict FFDec import and fresh re-decompile verification before publication.

## Epic War 5

Released assets and build records live under `assets/`; the game pages are under `epicwar5/` and `epicwar5-expansion/`. V4.3 repairs the original empty Continue handler, routes the dedicated Expansion launcher directly to hero/save selection, opens the authored 25-stage panel automatically, keeps the wider battlefield and compact slots 7–12, replaces the old debug palette with a dark bronze/crimson animated roster-card Battle Forge, and gives spawned armies explicit forward orders.

The V3.x toolchain lives under `tools/epicwar5/expansion/`, including the V3.8 UI/sandbox patch, frozen invariant checks, and reproducible FFDec rebuild workflow.

## Release verification

Verified releases use matching build/checksum records in `assets/`. GitHub Actions workflows under `.github/workflows/` perform source pinning where applicable, FFDec import/re-export checks and release-marker validation before publication.
