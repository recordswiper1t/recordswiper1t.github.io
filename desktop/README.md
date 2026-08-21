# Native desktop performance mode

The web player runs Ruffle's WebAssembly build inside a browser. This folder provides a native desktop path for the same V7 SWF so gameplay does not pay the browser/DOM/WebAssembly overhead.

## Fastest way to play

1. Clone or download this repository so the V7 SWF exists at `assets/kingdom-rush-frontiers-v5.swf`.
2. Make sure Python 3 is installed.
3. Windows: double-click `desktop/run-native.bat`.
4. macOS/Linux: run `sh desktop/run-native.sh` from Terminal.

The first launch downloads a recent official Ruffle desktop build from `ruffle-rs/ruffle` into `.native/ruffle/`. Later launches reuse that native executable and start immediately.

By default the launcher uses a recent Ruffle nightly because the desktop emulator receives compatibility and performance improvements continuously. Use `--stable` if you prefer the latest stable release, or `--refresh` to force a fresh download.

Examples:

```text
desktop\run-native.bat --refresh
sh desktop/run-native.sh --stable
```

## Why this should be faster

The existing `mod/fast.html` still has to execute the emulator as WebAssembly and render through a browser tab. Native Ruffle runs the Rust desktop executable directly and removes JavaScript glue, page layout/compositing, browser throttling, extension interference, and most browser memory overhead from the hot path.

The SWF itself already contains the V6/V7 swarm-performance safeguards, so native Ruffle stacks a lower-overhead runtime underneath those game-side patches.

## Performance expectations

This is the highest-impact runtime change available without rewriting the game in another engine. A specific multiplier such as 10x cannot be guaranteed across every laptop or every enemy count; measure it on the target machine. The important target is stable frame pacing during the largest V7 time-attack swarms.

For best results:

- Plug the laptop into power and disable battery-saver mode.
- On dual-GPU laptops, assign the Ruffle executable to the high-performance GPU in the OS graphics settings.
- Close the browser version while using native mode so it does not compete for CPU/GPU time.
- If a new nightly regresses performance, run with `--stable` and compare.

## Files and saves

The launcher runs the exact repository SWF and does not alter the V7 build. Native Ruffle stores Flash local data separately from browser Ruffle, so browser saves may need to be migrated through Ruffle's save-management features if you need the same progress in both runtimes.
