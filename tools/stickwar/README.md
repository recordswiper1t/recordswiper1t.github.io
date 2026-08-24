# Stick War Complete V1 foundation

This branch creates the expansion framework and data model. It does **not** contain a Stick War game binary because none exists in the repository yet.

## Required baseline

Place a legitimately obtained canonical Stick War 2 SWF at:

`tools/stickwar/baseline/stick-war-2.swf`

Do not rename it after mapping. Run:

```bash
python3 tools/stickwar/analyze_baseline.py
python3 tools/stickwar/build_v1.py
```

`analyze_baseline.py` verifies the SWF, exports scripts through FFDec, builds a source inventory and writes candidate symbol mappings. `build_v1.py` validates the content data and refuses to claim a playable release until the required symbol mapping is complete.

## What is already defined

- 65-stage unified campaign/war-game progression.
- Order + Chaos six-tier expansion trees.
- Hybrid unlock rules.
- Low-level performance plan and benchmark thresholds.
- Web player/Expansion Lab shell at `/stickwar-complete/`.
- Deterministic baseline/hash/mapping workflow.

## Non-negotiable performance rule

Combat, movement, targeting, projectiles and cooldowns stay full-rate. Under load, the game reduces cosmetic cadence, UI redraws and transient effects first.

## Expected release artifact

When the baseline is mapped and patched, the build publishes:

`assets/stick-war-complete-v2.swf`

plus a build manifest and SHA-256 file. The player shell automatically tries that asset.
