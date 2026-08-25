# Super Stick War V3.1 release and reproducible patch stack

The published release is `assets/stick-war-complete-v31.swf`. It opens the
Battle Lab directly, automatically exposes the in-game War Council sandbox,
and retains the normal campaign as a separate launch choice.

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

## Current release artifact

The checked and published files are:

- `assets/stick-war-complete-v31.swf`
- `assets/STICKWAR-COMPLETE-V31-BUILD.txt`
- `assets/STICKWAR-COMPLETE-V31-SHA256SUMS.txt`

V3.1 is produced from the mapped baseline with the V3 gameplay/interface
passes followed by `patch_entry_v31.py`. The repository release tests pin the
exact SHA-256 and reject stale player references.
