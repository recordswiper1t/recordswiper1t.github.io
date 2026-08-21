# Full-content Frontiers Steam port

This directory is the migration path from the 15-stage Flash/SWF mod to the complete desktop release of Kingdom Rush Frontiers.

## Why this port exists

The current browser build is based on the older Flash SWF and does not contain the post-campaign elite stages. The official Steam release is a different game build: its game logic is Lua-based and its packaged assets/scripts live inside the installed game archive. The existing ActionScript patchers therefore cannot be applied directly.

This port intentionally does **not** commit or redistribute the paid game, decrypted game scripts, art, audio, or other proprietary assets. It only contains patch/inventory tooling and a feature manifest. Supply files from a copy of Kingdom Rush Frontiers you own.

## Input

Use either:

- the installed `Kingdom Rush Frontiers.exe` from Steam, or
- an already extracted `kr2` directory from that installation.

Typical Windows install location:

`C:\Program Files (x86)\Steam\steamapps\common\Kingdom Rush Frontiers\Kingdom Rush Frontiers.exe`

Do not commit the extracted game directory to GitHub.

## First pass

Run:

```bash
python tools/steam-port/prepare_owned_game.py "C:\Program Files (x86)\Steam\steamapps\common\Kingdom Rush Frontiers\Kingdom Rush Frontiers.exe" --out C:\krf-port-work
```

or:

```bash
python tools/steam-port/prepare_owned_game.py C:\path\to\extracted\kr2 --out C:\krf-port-work
```

The script creates an inventory with hashes and identifies candidate Lua files for each V7 feature. It does not upload the game or modify the original installation.

## Port target

The port should preserve the complete Steam campaign/elite-stage content and reimplement the browser mod set in Lua:

- unlock campaign content / challenge availability
- max/default upgrades and configurable upgrade reset
- hero availability and hero level/skill controls
- 1x / 3x speed control
- numeric add-gold control
- numeric add-lives control
- custom enemy/unit spawning
- send-all-waves with boss/special entrance handling
- direct/special building placement tools
- unlimited mode
- instant win
- high-entity performance/back-pressure safeguards where applicable
- Time Attack: immediately activate all authored waves, wall-clock timer, per-stage best time
- enemy exit recycling without life loss or exit rewards, preserving remaining enemy state where the engine allows it

See `PORT-MANIFEST.json` for the implementation checklist.

## Browser/iPhone note

The Steam build is not a SWF and cannot simply replace the file loaded by Ruffle on the GitHub Pages site. This port targets the legitimate desktop game first. A browser/iPhone version would require a separately authorized/runtime-compatible game build; the Steam executable and paid assets should not be republished on GitHub Pages.
