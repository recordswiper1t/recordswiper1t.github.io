# Kingdom Rush Ultimate V17 — release status

V17 enters the player's saved combined slot and native map directly, keeps both native campaign maps and unified star wallet/system access, uses bronze/parchment war rooms, and retains the stateful bidirectional crossover armories.

## Released artifact

- file: `assets/kingdom-rush-ultimate-v17.swf`
- size: **91,103,485 bytes**
- SHA-256: **5C7BEE6A283D3F2FF5B5E23A9FE73D57FF64A3C6051B7148FC4D012C4779C26E**
- Kingdom Rush stages: all **19** stages embedded in the verified publisher Flash source
- Frontiers stages: all **15** campaign stages in the enhanced Flash runtime
- native map switching: persistent **KR MAP**, **KRF MAP**, and **SHARED HUB** controls
- shared systems: stars, upgrade rooms, hero rooms, achievements, and encyclopedias
- speed and victory tools: adaptive 1×/2×/4×/8×/12× plus immediate result-screen Instant Win

## V17 crossover armories and access

The Kingdom Rush war room can deploy all eight Frontiers tier-four towers and ten source-ready Frontiers heroes. The Frontiers war room can deploy all eight original Kingdom Rush tier-four towers and nine heroes present in the publisher Flash source.

Guest objects use their real linked tower/hero timelines. Their native-only initialization is bypassed when they enter the other campaign, then a stateful host-compatible combat branch provides health, death/respawn, hero leveling and skills, tower upgrades, movement stances, cached targeting, and damage through the shared `setDamage` contract. Native instances still follow their original code paths. Combined mode bypasses the old promotional Play screen and slot picker; standalone recovery modes preserve them.

## Verification

- strict FFDec import completed with abort-on-error, including the direct-boot root and the native crossover classes;
- the resulting 91 MB SWF freshly re-decompiled;
- fresh output contains both armory pages, all guest-spawn routes, both guest tower bases, both guest hero bases, and the inherited V14 map/speed/Instant Win markers;
- normal native constructors are guarded only when the parent level belongs to the other campaign;
- launchers and checksum tests point exclusively to V17.

## Later Kingdom Rush stages

The available Flash source ends at Level19 (Ha'Kraj Plateau). Pit of Fire, Pandaemonium, Fungal Forest, Rotwick, Ancient Necropolis, Nightfang Swale, and Castle Blackburn were released in later Steam/mobile builds and are not present in the audited SWF. This repository does not fabricate or mislabel those stages. They require a compatible source from a copy the user owns, or a full reconstruction of maps, paths, waves, art, enemies, and specials.

## Access paths

- central hub: `/`
- combined release: `/ultimate/play.html?campaign=ultimate`
- mobile hub: `/games/`
- standalone recovery choices: `/ultimate/play.html?campaign=kr` and `/ultimate/play.html?campaign=krf`
