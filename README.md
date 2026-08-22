# Flash strategy mod lab

This repository contains three performance-first Flash/ActionScript mod projects. Release binaries are built through pinned-source/FFDec workflows and are only promoted when their release checks pass.

## Project status

| Project | Current state | Main features |
| --- | --- | --- |
| **Kingdom Rush Frontiers** | Released on `main` through V12/V12.1 | Full sandbox, tower clipboard, hero/enemy controls, Time Attack/loop scoring, diagnostics, adaptive performance controls, **The Last Rift** expansion |
| **Kingdom Rush Ultimate (KR + KRF)** | Active V13 integration in PR #42 | Frontiers V12 runtime + KR1 campaign/content import, combined campaign routing, 16 tier-4 targets, combined hero target, inherited V11/V12 sandbox/performance systems |
| **Super Stick War (SW1 + SW2)** | V1 release candidate in PR #39 | 65-stage combined campaign, Order/Chaos progression, 108 mastery nodes, possession, Battle Lab, F2 sandbox, F1 diagnostics and performance patches |
| **Epic War 5** | Released on `main` through Expansion V3.3.1 | Sandbox builds, expanded campaign/equipment/progression, large-battle performance pass, release-candidate verification and sitelock hotfix |

The repository is deliberately fail-closed: a generated SWF is not described as a release merely because it serializes. Build pipelines re-decompile and verify required gameplay/mod markers before publication.

## Kingdom Rush Frontiers — current released desktop mod

The recommended laptop version is native Ruffle from `desktop/`.

### Windows

Download the repository as a ZIP, extract it, then run:

`desktop\run-native.bat`

The launcher downloads Ruffle on first use and automatically selects the newest verified Frontiers SWF in `assets/`.

### macOS / Linux

Run:

`sh desktop/run-native.sh`

See [`desktop/README.md`](desktop/README.md) for renderer troubleshooting, sandbox controls, scoring and performance settings.

Current Frontiers V12 keeps the V11 sandbox/performance feature set and adds **The Last Rift**, post-boss scoring, renderer hardening and additional performance work. V12.1 contains the current audio/pop-up polish.

## Kingdom Rush Ultimate — V13

Development lives in [PR #42](../../pull/42). The architecture keeps Frontiers V12 as the authoritative runtime and imports KR1 content through a collision-safe namespace/rebind layer so existing sandbox/performance systems remain intact.

The branch is not promoted to a release until imported KR stages, KR tower/hero compatibility, combined campaign saves/UI and final FFDec round-trip/runtime gates pass. See `docs/KINGDOM_RUSH_ULTIMATE.md` on that branch for the detailed compatibility plan.

## Super Stick War — SW1 + SW2

The release candidate lives in [PR #39](../../pull/39). Its build is based on a pinned official Stick War 2 baseline and remasters SW1 content into that runtime rather than pretending to merge two unrelated binaries.

Target V1 includes a 65-stage campaign, playable Order/Chaos progression, 108 mastery nodes, direct possession, authored expansion objectives, Battle Lab presets, sandbox controls, diagnostics and performance optimization without lowering combat simulation rate.

## Epic War 5

Released assets and build records live under `assets/`; the game pages are under `epicwar5/` and `epicwar5-expansion/`. The expansion line progressed through V3/V3.1/V3.2 to the V3.3 performance/quality release and V3.3.1 site-hosting hotfix.

The V3.x toolchain lives under `tools/epicwar5/expansion/`, including the dedicated V3.3 performance patch and validation/rebuild workflows.

## Release verification

Verified releases use matching build/checksum records in `assets/`. GitHub Actions workflows under `.github/workflows/` perform source pinning where applicable, FFDec import/re-export checks and release-marker validation before publication.
