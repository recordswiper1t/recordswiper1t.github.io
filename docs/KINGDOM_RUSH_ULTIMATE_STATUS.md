# Kingdom Rush Ultimate V15 — release status

V15 keeps the two native campaign maps and V14 shared systems, replaces the custom sandbox surfaces with bronze/parchment war rooms, and adds bidirectional crossover armories.

## Released artifact

- file: `assets/kingdom-rush-ultimate-v15.swf`
- size: **91,100,192 bytes**
- SHA-256: **76B4848E3FC8268F8A5CB30916AEB6DB18A80691383E87F5E70EAC4FCE769AD0**
- Kingdom Rush stages: all **19** stages embedded in the verified publisher Flash source
- Frontiers stages: all **15** campaign stages in the enhanced Flash runtime
- native map switching: persistent **KR MAP**, **KRF MAP**, and **SHARED HUB** controls
- shared systems: stars, upgrade rooms, hero rooms, achievements, and encyclopedias
- speed and victory tools: adaptive 1×/2×/4×/8×/12× plus immediate result-screen Instant Win

## V15 crossover armories

The Kingdom Rush war room can deploy all eight Frontiers tier-four towers and ten source-ready Frontiers heroes. The Frontiers war room can deploy all eight original Kingdom Rush tier-four towers and nine heroes present in the publisher Flash source.

Guest objects use their real linked tower/hero timelines. Their native-only initialization is bypassed when they enter the other campaign, then a host-compatible combat branch moves heroes, targets the host level's live enemies, and applies damage through the shared `setDamage` contract. Native instances still follow their original code paths.

## Verification

- strict FFDec import completed with abort-on-error for all 49 modified Ultimate classes;
- the resulting 91 MB SWF freshly re-decompiled;
- fresh output contains both armory pages, all guest-spawn routes, both guest tower bases, both guest hero bases, and the inherited V14 map/speed/Instant Win markers;
- normal native constructors are guarded only when the parent level belongs to the other campaign;
- launchers and checksum tests point exclusively to V15.

## Later Kingdom Rush stages

The available Flash source ends at Level19 (Ha'Kraj Plateau). Pit of Fire, Pandaemonium, Fungal Forest, Rotwick, Ancient Necropolis, Nightfang Swale, and Castle Blackburn were released in later Steam/mobile builds and are not present in the audited SWF. This repository does not fabricate or mislabel those stages. They require a compatible source from a copy the user owns, or a full reconstruction of maps, paths, waves, art, enemies, and specials.

## Access paths

- central hub: `/`
- combined release: `/ultimate/play.html?campaign=ultimate`
- mobile hub: `/games/`
- standalone recovery choices: `/ultimate/play.html?campaign=kr` and `/ultimate/play.html?campaign=krf`
