# Native desktop performance mode

This is the recommended laptop build for the Kingdom Rush Frontiers mod. It runs the verified **V8 optimized SWF** through native Ruffle instead of the browser/WebAssembly player.

## Fastest way to play

### Windows

1. Download or clone this repository.
2. Double-click `desktop\run-native.bat`.
3. The first launch downloads the correct native Ruffle desktop build automatically. No Python install is required.
4. Later launches reuse the cached Ruffle executable from `.native\ruffle\`.

### macOS / Linux

Run:

```text
sh desktop/run-native.sh
```

The shell launcher uses Python 3 to select/download the correct Ruffle build for the machine.

## Game build

The launcher prefers `assets/kingdom-rush-frontiers-v8.swf`, which has been built, re-exported, and structurally verified with FFDec 26.2.1. If that file is missing, it falls back to the historical V7 asset.

V8 includes:

- native-desktop-ready runtime path;
- amortized Time Attack completion checks instead of full enemy scans on every kill;
- 10 Hz timer HUD redraw instead of every frame;
- additional ultra-swarm cosmetic throttling while gameplay/combat remains full-rate;
- the existing V5/V6/V7 swarm throttling and Send-All back-pressure;
- Ctrl+C tower copy and Ctrl+V paste onto a selected empty build spot when you have enough cash.

Tower copy/paste supports the base Archer, Barracks, Mage and Engineer families plus Crossbow, Totem, Archmage, Necromancer, DWAARP, Battle-Mecha, Assassin and Templar branches. Special ability ranks are not duplicated because those subclasses own live soldier/projectile/effect state.

## Ruffle channel

The default is a recent Ruffle nightly because compatibility and performance fixes land there first. You can use the latest stable build instead:

```text
desktop\run-native.bat --stable
sh desktop/run-native.sh --stable
```

Force a fresh Ruffle download with `--refresh`.

## Best laptop performance

- Plug the laptop into power and turn off battery saver.
- On dual-GPU laptops, assign `.native\ruffle\ruffle.exe` to the high-performance GPU in Windows Graphics settings.
- Close the browser copy of the game while using native mode.
- Use fullscreen if your desktop compositor behaves better that way.
- If a nightly causes a regression, compare with `--stable`.

Native Ruffle removes the browser, JavaScript/DOM compositing and WebAssembly layer from the gameplay path. A fixed multiplier cannot be guaranteed across all laptops, but this is the lowest-overhead way this SWF can run without porting the entire game to another engine.

## Saves

Native Ruffle stores Flash local data separately from browser Ruffle. If you need the same progress in both, migrate the save using Ruffle's save-management features.
