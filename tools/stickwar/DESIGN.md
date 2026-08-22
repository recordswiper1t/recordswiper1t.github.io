# Stick War Complete — master expansion design

## Goal

Build one definitive Stick War game on a Stick War 2 baseline: remaster the Stick War 1 conquest as Chapter I, continue through Stick War 2-style Order/Chaos content, then extend into a large original postgame. Campaign progression and sandbox/debug state stay separate.

## Release ceiling

- 65 authored campaign/war-game definitions in `data/campaign.json`.
- 18 playable Order/Chaos unit families with six-step expansion trees in `data/tech.json`.
- Order campaign, unlockable Chaos campaign, late-game limited hybrid armies.
- Direct unit possession restored as a first-class mechanic.
- Boss framework, survival, escort, assassination, economy, siege, interrupt and benchmark objectives.
- Battle Lab with presets and share-code scenario serialization.
- Sandbox pages for units, factions, economy, technology, bosses, battlefield, AI, cleanup, diagnostics and performance.
- Performance designed for 100–200 actor real battles and a 250–300+ actor benchmark path without slowing the combat simulation.

## Progression

Chapter I deliberately starts smaller than Stick War 2. Units/tech are earned through conquest. Mana and the broader SW2 vocabulary arrive only near the end of Chapter I. Order advanced units enter in Chapter II. Chaos becomes the central enemy in Chapter III and becomes playable after the Medusa arc. Hybrid slots are endgame rewards rather than permanent cheats.

Campaign progression owns unlocks, technology ranks, clear state and medals. Sandbox uses a separate save namespace and may expose everything without contaminating campaign saves.

## Possession

Possession must work for all normal combat units. The possession controller owns input, camera follow, selected-unit HUD, attack/ability dispatch, escape back to RTS mode and safe cleanup on death. It must never create a second simulation path; possession issues the same state transitions/abilities the AI or RTS command layer uses.

## Performance architecture

The expansion is allowed to change low-level internals aggressively so long as behavior stays deterministic enough for authored stages and combat logic remains full-rate.

1. Maintain typed active vectors for units/projectiles/buildings/effects.
2. Maintain an x/y spatial hash once per simulation tick.
3. Target acquisition queries nearby buckets before exact distance/hit tests.
4. Reuse candidate buffers and squared-distance math; avoid per-frame Points, Rectangles and temporary arrays.
5. Pool projectiles, impact effects and short-lived particles.
6. Insert actors incrementally into render depth; do not sort the entire battlefield on every spawn.
7. UI is dirty-flagged and cadence-limited. Combat state is not.
8. Health bars are staggered across frames.
9. Strategic AI decisions may run at 4–8 Hz; unit movement/attacks remain full-rate.
10. Dead actors are retired from active containers promptly.
11. Cosmetic budgets fall as actor count rises.
12. Benchmark counters expose frame time, entities, projectiles, target checks and pool sizes.

See `data/performance.json` for thresholds and acceptance targets.

## Build rule

The release is built from one user-supplied canonical Stick War 2 SWF. The baseline hash is recorded before modification. Every patch must be reproducible from exported source, reimported by FFDec, re-decompiled, then checked for required markers. No release should depend on hand-edited binary state.

## Implementation order

1. Acquire/verify canonical SW2 baseline.
2. Export ActionScript and run `analyze_baseline.py`.
3. Freeze a symbol mapping for game root, battle loop, unit base, projectile base, selection, production, technology, save, campaign, AI and HUD.
4. Land performance foundation first: active vectors, spatial hash, pools, cadence utilities and counters.
5. Add possession using existing unit ability paths.
6. Expand save schema and campaign storage.
7. Import Chapter I definitions and progression gates.
8. Add expansion tech trees and Chaos/hybrid unlocks.
9. Add Chapters IV–VII and boss/objective controllers.
10. Add Battle Lab/sandbox bindings.
11. Balance and benchmark every release profile.
