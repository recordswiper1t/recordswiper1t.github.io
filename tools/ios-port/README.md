# Full-content Frontiers iOS port

This directory is the migration path from the 15-stage Flash/SWF browser mod to the full-content iPhone App Store release of Kingdom Rush Frontiers.

## Target

The source target is the user's legitimately purchased **Kingdom Rush Frontiers TD** iPhone app. The current App Store release is a different build from the old Flash SWF used by this repository and contains the later mobile content that the SWF build does not.

The existing V1-V7 ActionScript patchers cannot be assumed to apply directly. The first step is to inventory the owned iOS app bundle and determine which game logic/resources are stored as patchable data and which logic is compiled into the signed executable.

## What this repository will and will not contain

This port may contain:

- inventory/inspection tooling
- patch descriptions and patchers written against user-supplied files
- hashes and compatibility metadata
- original mod UI/logic created for this project

It must not contain or redistribute the paid App Store app, copyrighted game art/audio, a decrypted App Store executable, or instructions/tools whose purpose is to defeat Apple FairPlay/DRM.

## Accepted local input

`inspect_owned_ios.py` accepts either:

- an `.ipa` file that the user legitimately has access to, or
- an extracted `.app` / `Payload` directory from an owned copy.

The tool only opens ordinary ZIP/resource data. It does **not** decrypt an App Store executable or modify the original input.

Example:

```bash
python tools/ios-port/inspect_owned_ios.py "/path/to/Kingdom Rush Frontiers.ipa" --out "/tmp/krf-ios-inventory.json"
```

or:

```bash
python tools/ios-port/inspect_owned_ios.py "/path/to/Payload/Kingdom Rush Frontiers.app" --out "/tmp/krf-ios-inventory.json"
```

Do not commit the IPA, app bundle, extracted paid assets, or save data to GitHub.

## Port feature target

The iOS port should preserve all full-game stages and reimplement the current browser mod set where the mobile engine permits it:

- campaign / elite-stage and challenge availability controls
- max/default upgrades plus reset-for-custom behavior
- hero availability, level and skill controls for implementations in the full mobile build
- 1x / 3x speed control
- numeric add-gold control
- numeric add-lives control
- custom enemy/unit spawning
- send-all-waves with boss/special entrance handling
- special/direct building placement tools
- unlimited mode
- instant win
- high-entity performance/back-pressure safeguards where practical
- Time Attack: immediate authored-wave activation, wall-clock timer and per-stage/mode best time
- enemy exit recycling without life loss/exit rewards while preserving remaining enemy state where the engine permits

See `PORT-MANIFEST.json` for the checklist.

## Important deployment distinction

A modified iOS App Store app is not the same thing as the current GitHub Pages/Ruffle build. Even after the game logic is understood, iOS code-signing and App Store protections mean a modified native app cannot simply be hosted as a replacement SWF and opened in Safari.

The browser project can still reuse ideas/data from the full-content analysis, but making the seven extra stages playable in Safari requires a browser-compatible implementation or assets/content that can legally be redistributed. The iOS inspection phase tells us what is technically reusable without assuming that the paid native app can be republished.
