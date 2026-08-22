# Stick War Complete canonical baselines

These are the publisher-hosted Flash releases used by the deterministic build pipeline.

## Stick War (SW1)

- Source: `https://cache.armorgames.com/files/games/stick-war-4405.swf`
- Size: `7,003,484` bytes
- SHA-256: `9bff25416c98506ba01493b7e3fa523890632b4963e4f0ac33f5cbbb023c7c0b`
- Expected SWF signature: `FWS`, `CWS`, or `ZWS`

## Stick War 2 — Order Empire (SW2)

- Source: `https://cache.armorgames.com/files/games/stick-war-2-14346.swf`
- Size: `18,886,237` bytes
- SHA-256: `03aa17bc25851fb14aefbe9a7223c738f427bff22580e16ec93e5e1232b167b5`
- Expected SWF signature: `FWS`, `CWS`, or `ZWS`

Max Games also still exposes publisher-side **Download SWF** links for both games. The Armor Games URLs above are used because they are stable, directly fetchable in CI, and the exact byte sizes are independently indexed by old Flash archives.

## Build rule

The original SWFs are fetched transiently in GitHub Actions rather than committed as source assets. Every build must verify size + SHA-256 before FFDec export or patching. The modified release SWF gets its own release hash after rebuild and re-decompile verification.
