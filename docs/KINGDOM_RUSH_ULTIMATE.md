# Kingdom Rush Ultimate

> Historical design target. It has been superseded by the verified V17 combined release: direct native-map entry, two native campaign maps containing the 19 Kingdom Rush and 15 Frontiers stages available in the audited Flash sources, unified progression surfaces, game-styled war rooms, and bidirectional guest armories. See `KINGDOM_RUSH_ULTIMATE_STATUS.md` for the released artifact and verification evidence.

Goal: one Frontiers-based runtime containing the original **Kingdom Rush** and **Kingdom Rush: Frontiers** campaigns, their post-campaign stages, both games' towers and heroes, and the complete V11/V12 sandbox/performance feature set.

## Runtime rule

**Kingdom Rush Frontiers V12/V11 is the authoritative engine.**

Do not stitch two SWFs together as independent games and do not replace Frontiers' global managers with KR1 versions. KR1 content is imported into a collision-safe namespace and then selectively rebound to the Frontiers shared core. This keeps the existing mod infrastructure intact:

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

`tools/ultimate/tower_registry.py` is the runtime source of truth for these branches. It records the audited classes, including `KR1__TowerEngineerBfg` for Big Bertha, and provides stable `ultimate_*` action IDs. The eight current Frontiers branches retain their existing V11/V12 `qol_*` actions as implementation aliases while the eight KR1 branches get new actions. The existing V11 blueprint/copy-paste layer should be extended to KR1 tier-4 classes rather than replaced.

## Hero target

Frontiers' hero lifecycle remains authoritative. The stable roster manifest targets **29 selectable heroes**: 13 from KR1 and 16 from Frontiers, plus the three Frontiers stage-secondary heroes as map content. KR1 heroes should be adapted behind a compatibility layer so both rosters can be selected/spawned on either campaign without changing Frontiers' existing hero implementation or sandbox toggles.

Required compatibility work:

1. stable combined hero IDs independent of obfuscated class names
2. spawn/move/death/respawn adapters
3. KR1 ability cooldown and level semantics mapped to the Frontiers runtime
4. save data namespaced so KR1 and KRF progress never overwrite each other
5. sandbox "all heroes" and individual toggles extended to both rosters

## Campaign/save architecture

Use stable IDs from the manifest, not `Level15`-style class names, as save keys. `tools/ultimate/campaign_registry.py` maps those stable IDs to runtime identities only when source is actually available.

Suggested model:

- `campaign = kr1 | krf | bonus`
- `stageId = kr1-southport`, `krf-hammerhold`, etc.
- stars/challenges keyed by `stageId`
- difficulty/challenge mode stays separate from stage identity
- unlock graph comes from the manifest
- sandbox can bypass unlocks without mutating campaign completion

The world-map UI can initially be a simple combined stage selector. A visually merged world map is later polish and must not block playable levels.

## Verified KR1 publisher-source audit

The V13 CI can fetch the historical Armor Games publisher build **ephemerally for structural/build work**. The source binary and decompiled scripts are not committed or uploaded as artifacts.

Publisher endpoint used by the audit:

`https://cache.armorgames.com/files/games/kingdom-rush-12141.swf`

Verified SHA-256:

`7b5467a3eccc17f6dd001ff2d41bdf1b03d79fd515a2a9586c42bfd982bb1e23`

FFDec 26.2.1 structural inventory from that source versus the enhanced Frontiers runtime found:

- KR1: 995 ActionScript classes
- Frontiers: 1103 ActionScript classes in the audited base
- 203 same-name class collisions
- KR1 publisher build contains `Level1` through `Level19`
- `Level1`-`Level12` are the main campaign
- verified extra publisher-build levels cover Sarelgaz's Lair, Ruins of Acaroth, Rotten Forest, Hushwood, Bandit's Lair, Glacial Heights and Ha'Kraj Plateau
- later KR1 additions not present in that publisher build remain reconstruction/source-port work

The collision profile is favourable: most collisions are shared engine/UI/base classes (`Level`, `Enemy`, `Wave`, base tower/soldier/power classes, etc.), while most KR1-specific enemies, heroes and tier-4 towers have distinct identities.

## Binary merge strategy

FFDec's CLI `-importScript` can replace an existing AS3 script pack but cannot simply create all missing KR1 classes in the Frontiers SWF. V13 therefore uses a two-stage approach.

### Stage 1 — collision-safe structural import

1. Convert KR1 and the enhanced Frontiers base to FFDec SWF XML.
2. Prefix every KR1 class/linkage as `KR1__*` for the initial structural proof.
3. Offset KR1 character IDs into a non-overlapping range and fail if the combined UI16 character-ID space would exceed 65535.
4. Import reusable `Define*` tags, ABC tags and linkage metadata before Frontiers' `EndTag`.
5. Drop the KR1 document-class binding so Frontiers remains the executable document/runtime.
6. Rebuild with `-xml2swf` and re-export with FFDec.
7. Require both Frontiers mod classes/markers and namespaced KR1 levels/towers to be visible after the round trip.

`tools/ultimate/merge_swf_xml.py` implements the streaming XML merge so the large XML files do not need to be held in memory at once.

### Stage 2 — rebind playable KR1 content to Frontiers core

A fully prefixed binary is safe but would otherwise carry a second KR1 engine. `tools/ultimate/port_plan.py` classifies collisions, and `tools/ultimate/rebind_namespaced_scripts.py` performs the bridge:

- KR1 content identities such as `KR1__Level1` remain namespaced.
- KR1 stage graphics such as `KR1__GLevel1` remain namespaced so their imported art/timelines are used.
- references from KR1 content to shared colliding core types are rewritten back to authoritative Frontiers classes.
- explicit compatibility identities can be excluded from that rewrite; the first is `KR1__Level`.
- because the content classes already exist after Stage 1, FFDec `-importScript` can replace/recompile them.

## KR1 Level compatibility adapter

A direct `KR1__Level1 extends Level` rewrite is useful as a diagnostic but too brittle as the final design. Imported KR1 stages legitimately use inherited names that may not exist under the same API in Frontiers.

The preferred architecture is:

1. KR1 stages retain `extends KR1__Level`.
2. The already-imported `KR1__Level` definition is replaced with a thin `KR1__Level extends Level` compatibility class.
3. `tools/ultimate/level_api_diff.py` computes only the inherited KR1 `Level` members a stage references that Frontiers lacks.
4. `tools/ultimate/build_level_adapter.py` can generate typed-neutral compile stubs for those missing names. Those stubs are diagnostic only and must be replaced with explicit Frontiers-backed semantics or proven irrelevant before gameplay certification.
5. `rebind_namespaced_scripts.py --exclude-rebind KR1__Level` rebinds other shared-core references while preserving the adapter inheritance identity.

`tools/ultimate/build_southport_adapter.py` turns the complete Southport sequence into a reproducible local build: structural merged SWF -> API contract -> adapter -> Southport rebind -> FFDec replacement -> re-export verification.

`tools/ultimate/stage_api_matrix.py` generalises the same API analysis across all publisher-source `Level1`-`Level19`. The `probe-kr1-stage-adapter-matrix.yml` CI job attempts to compile all 19 stage classes against one union adapter. This determines whether one compatibility superclass can support the complete source-ready KR1 campaign/post-campaign set.

## Port order

### Gate A — source inventory — substantially complete

- Frontiers V12/V11 ActionScript export and source audit.
- Ephemeral official-publisher KR1 fetch and FFDec audit.
- Class-collision inventory and stable content manifest.
- Binary/XML schema probes and class namespace policy.

### Gate B — first real imported level — active

Port **Southport** into the Frontiers runtime with Frontiers towers/heroes first. It must pass:

- structural SWF round-trip with both code sets present
- `KR1__Level` compatibility class compilation over Frontiers `Level`
- Southport recompilation through that adapter
- paths and wave timing
- enemy exits/lives
- build spots
- powers
- campaign win/loss
- Heroic/Iron modes
- V11/V12 sandbox and Time Attack controls

The compiler matrix can prove the class layer for Level1–Level19 early, but runtime certification remains stage-by-stage.

### Gate C — combined towers

Implement four tier-4 choices per family using `tower_registry.py` and extend clipboard/ability-rank handling to the KR1 branches. Test all 16 tier-4 towers on Southport and Hammerhold.

### Gate D — KR1 roster and campaign

Import/rebind KR1 enemies, bosses, map specials and heroes, then port all 12 main stages and all available post-campaign content. Reconstruct/source-port the later KR1 stages absent from the publisher Flash build.

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
- re-exported SWF structurally verified with FFDec 26.2.1
- native desktop/browser launchers prefer the verified Ultimate SWF only after these checks pass

## Current branch status

`agent/v13-kingdom-rush-ultimate-clean` is based directly on current `main` and preserves the verified V12 Last Rift runtime.

Implemented/under CI proof:

- complete 51-stage original-game manifest plus V12 bonus stage metadata
- complete 16-tier-4-tower / 29-selectable-hero target manifest
- canonical runtime tower class/action registry for all 16 branches
- source/preflight validation with SHA-256 recording
- official-publisher KR1 structural audit
- ActionScript collision reporting and import policy generation
- FFDec XML schema/round-trip probes
- streaming character-ID/linkage/ABC definition merger
- fully namespaced KR1 binary-coexistence proof workflow
- shared-core rebind tooling with explicit compatibility exclusions
- Southport API-diff and Frontiers-backed `KR1__Level` compile-bridge tooling
- reproducible Southport adapter build pipeline
- Level1-Level19 union adapter matrix/probe
- stable campaign/save runtime registry
- expensive audit workflows narrowed so unrelated Ultimate commits do not continuously refetch/re-export both games
- ignored local binary inputs/work directories

Not yet claimable as complete:

- a gameplay-verified Southport inside the enhanced Frontiers runtime
- semantic implementations for any generated `KR1__Level` adapter stubs
- combined tier-4 upgrade UI/behavior
- KR1 hero compatibility adapters and combined hero selector
- all KR1 campaign/post-campaign stages runtime-tested
- later Frontiers post-campaign/endless maps
- final combined campaign/save UI and launcher promotion

The build remains **fail-closed**: a generated SWF is not called V13/Ultimate merely because it can be serialized. Required class coexistence, Frontiers enhancement markers, stage recompilation and gameplay compatibility gates must pass first.
