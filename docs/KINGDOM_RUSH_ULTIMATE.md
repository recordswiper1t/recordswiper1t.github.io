# Kingdom Rush Ultimate

Goal: one Frontiers-based runtime containing the original **Kingdom Rush** and **Kingdom Rush: Frontiers** campaigns, their post-campaign stages, both games' towers and heroes, and the complete V11/V12 sandbox/performance feature set.

## Runtime rule

**Kingdom Rush Frontiers V12/V11 is the authoritative engine.**

Do not stitch two SWFs together and do not replace Frontiers' global managers with KR1 versions. KR1 content is imported/namespaced into the Frontiers runtime. This keeps the existing mod infrastructure intact:

- sandbox menu and direct enemy spawning
- all current Frontiers hero toggles
- Time Attack / Send All / recycling
- exact tower clipboard and invested-cost reconciliation
- map-special selling/copy support
- diagnostics and swarm thresholds
- V8-V11 performance work
- V12 scoring/adaptive-quality work and The Last Rift bonus act

## Original-game content target

The canonical list lives in `tools/ultimate/content_manifest.py`.

| Game | Main | Post-campaign | Endless | Total |
| --- | ---: | ---: | ---: | ---: |
| Kingdom Rush | 12 | 14 | 1 | 27 |
| Frontiers | 15 | 7 | 2 | 24 |
| **Combined** | **27** | **21** | **3** | **51** |

That is **48 normal campaign/post-campaign stages**, plus **3 endless maps**. The custom V12 `The Last Rift` stays as an additional bonus mode/stage and is not counted in the 51 originals.

### Kingdom Rush post-campaign

Sarelgaz's Lair; Ruins of Acaroth; Rotten Forest; Fungal Forest; Hushwood; Bandit's Lair; Glacial Heights; Ha'Kraj Plateau; Pit of Fire; Pandaemonium; Rotwick; Ancient Necropolis; Nightfang Swale; Castle Blackburn.

Endless target: Rage Valley.

### Frontiers post-campaign

Port Tortuga; Storm Atoll; The Sunken Citadel; Bonesburg; Desecrated Grove; Dusk Chateau; Darklight Depths.

Endless targets: Ruins of Nas'de and Temple of Evil / Temple of Ethereal Evil.

## Tower target

All basic tiers remain shared. At tier 4, every build spot should expose all four specialisations in that family:

- Archer: Ranger's Hideout, Musketeer Garrison, Crossbow Fort, Tribal Axethrowers
- Barracks: Holy Order, Barbarian Mead Hall, Knights Templar, Assassin's Guild
- Mage: Arcane Wizard, Sorcerer Mage, Archmage Tower, Necromancer Tower
- Artillery: Tesla x104, 500mm Big Bertha, DWAARP, Battle-Mecha T200

The existing V11 blueprint/copy-paste layer should be extended to KR1 tier-4 classes rather than replaced.

## Hero target

Frontiers' hero lifecycle remains authoritative. KR1 heroes should be adapted behind a compatibility layer so both rosters can be selected/spawned on either campaign without changing Frontiers' existing hero implementation or sandbox toggles.

Required compatibility work:

1. stable combined hero IDs independent of obfuscated class names
2. spawn/move/death/respawn adapters
3. KR1 ability cooldown and level semantics mapped to the Frontiers runtime
4. save data namespaced so KR1 and KRF progress never overwrite each other
5. sandbox "all heroes" and individual toggles extended to both rosters

## Campaign/save architecture

Use stable IDs from the manifest, not `Level15`-style class names, as save keys.

Suggested model:

- `campaign = kr1 | krf | bonus`
- `stageId = kr1-southport`, `krf-hammerhold`, etc.
- stars/challenges keyed by `stageId`
- difficulty/challenge mode stays separate from stage identity
- unlock graph comes from the manifest
- sandbox can bypass unlocks without mutating campaign completion

The world-map UI can initially be a simple combined stage selector. A visually merged world map is a later polish item and must not block playable levels.

## Port order

### Gate A — source inventory

- Export Frontiers V12/V11 ActionScript with FFDec.
- Export a user-supplied KR1 source SWF with FFDec.
- Run `audit_exports.py` to find class collisions and build the KR1 namespace plan.
- Inventory binary symbols/timelines needed by KR1 levels/towers/heroes/enemies.

### Gate B — first real imported level

Port **Southport** into the Frontiers runtime with Frontiers towers/heroes first. It must pass:

- paths and wave timing
- enemy exits/lives
- build spots
- powers
- campaign win/loss
- Heroic/Iron modes
- V11 sandbox and Time Attack controls

### Gate C — combined towers

Implement four tier-4 choices per family and extend clipboard/ability-rank handling to the KR1 branches. Test all 16 tier-4 towers on Southport and Hammerhold.

### Gate D — KR1 roster and campaign

Import KR1 enemies, bosses, map specials and heroes, then port all 12 main stages and 14 post-campaign stages.

### Gate E — Frontiers later content

The existing Flash Frontiers source does not contain the later post-campaign/endless map set used by other releases. Those maps therefore require either:

- a compatible source/export from a release the user is entitled to use, or
- reconstruction of paths, waves, scenery, special mechanics and missing symbols inside the Flash runtime.

Do not mark Port Tortuga through Darklight Depths (or the two Frontiers endless maps) complete until this dependency is actually satisfied and re-export verified.

### Gate F — full integration

- every one of the 48 normal stages accepts both games' towers and heroes
- endless maps accept both rosters/tower sets where mechanics permit
- all V11/V12 enhancements work on imported stages
- combined campaign selector and saves work
- re-exported SWF structurally verified with the same FFDec version used by the existing pipeline
- native desktop launcher prefers the verified Ultimate SWF only after these checks pass

## Current branch status

`agent/v13-kingdom-rush-ultimate` is based on `agent/v12-postboss-expansion`, so the existing V12 work is preserved.

Implemented foundation:

- complete 51-stage original-game manifest plus V12 bonus stage metadata
- source/preflight validation with SHA-256 recording
- ActionScript export inventory and collision reporting
- deterministic KR1 namespace plan generation
- reproducible FFDec source-audit preparation script
- ignored local binary inputs/work directories

Not yet claimable as complete:

- KR1 binary/source asset import (KR1 source is not currently present in this repository)
- combined tier-4 upgrade UI/classes
- KR1 heroes/enemies/stage classes in the Frontiers SWF
- later Frontiers post-campaign/endless maps, because their source content is not embedded in the current Flash base

## Local preparation

Keep source binaries outside version control (for example under `inputs/`, which is ignored):

```text
inputs/
  kingdom-rush.swf
  frontiers-extra/   # optional later-content export/source
```

Run a quick source check:

```bash
python3 tools/ultimate/preflight.py \
  --frontiers assets/kingdom-rush-frontiers-v12.swf \
  --kingdom-rush inputs/kingdom-rush.swf \
  --frontiers-extra-export inputs/frontiers-extra
```

Then prepare deterministic exports/audit data:

```bash
python3 tools/ultimate/build_ultimate.py \
  --ffdec /path/to/ffdec.jar \
  --frontiers assets/kingdom-rush-frontiers-v12.swf \
  --kingdom-rush inputs/kingdom-rush.swf \
  --frontiers-extra-export inputs/frontiers-extra \
  --work work/ultimate \
  --keep-temp
```

The build must remain fail-closed: if required source/symbols are missing, report the missing dependency rather than silently substituting a different level or marking the merge verified.
