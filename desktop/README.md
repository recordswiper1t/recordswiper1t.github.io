# Kingdom Rush Frontiers — native desktop mod

This is the recommended way to play the mod on a laptop. It runs the newest verified SWF directly in native Ruffle instead of the browser/WebAssembly player.

## Fastest way to play

### Windows

1. Download the repository ZIP and extract it.
2. Open the `desktop` folder.
3. Double-click `run-native.bat`.
4. The first launch downloads native Ruffle automatically; later launches reuse `.native\ruffle\ruffle.exe`.

No Python installation is required on Windows.

### macOS / Linux

Run:

```text
sh desktop/run-native.sh
```

Python 3 is required for the macOS/Linux bootstrap launcher.

## Build selection

The launchers always choose the newest verified game file present, currently preferring:

`V12 → V11 → V10 → V9 → V8 → V7 fallback`

V12 is **The Last Rift** audit release. It keeps every V11 sandbox/performance feature and adds the post-final-boss act, loop-run scoring, renderer hardening and additional performance work.

## Windows graphics crash protection

Some Windows systems can hit a native Ruffle/wgpu Vulkan panic. The launcher therefore does **not** use Vulkan by default.

- Default: DirectX 12 (`dx12`)
- If DX12 exits unsuccessfully: automatically retry OpenGL
- Force OpenGL: `desktop\run-native.bat --gl`
- Explicit Vulkan test only: `desktop\run-native.bat --vulkan`
- Force DX12: `desktop\run-native.bat --dx12`

If a cached Ruffle build itself appears broken, run `desktop\run-native.bat --refresh`.

## Ruffle channel

The default is a recent Ruffle nightly because Flash compatibility/performance fixes land there first. To use the newest stable release instead:

```text
desktop\run-native.bat --stable
sh desktop/run-native.sh --stable
```

## Current sandbox features

The in-level sandbox is organized into Heroes, Enemies, Waves/Time Attack, Towers/Clipboard, Cheats/Cleanup and Performance pages. Opening the sandbox pauses the level.

Highlights include:

- all playable hero implementations in this SWF, including Rurin Longbeard;
- direct enemy catalog/spawning with count steps of 1, 5 and 25;
- Send All, Time Attack and recycle/loop play;
- persistent fastest-time, fewest-virtual-lives-lost and combined loop-run records;
- map-special building placement and selling;
- Ctrl+C/Ctrl+V tower blueprints with standard tier and purchased tier-4 ability ranks preserved where the SWF exposes permanent upgrade state;
- exact affordability checks before paste;
- Clear All Enemies, Remove All Heroes, Sell All Map Specials and clipboard reset;
- Normal, Chaos, Benchmark and Time Attack presets;
- FPS/entity/bullet diagnostics and configurable heavy/extreme/ultra swarm thresholds.

Live hired units, projectiles and one-shot action state are intentionally not copied with tower blueprints. They are runtime objects rather than permanent tower upgrades.

## The Last Rift

After the original Level 15 campaign boss is defeated, V12 continues into a 30-wave post-boss act instead of immediately ending the level. It uses three new runtime-built routes, additional tower locations, evolved enemy archetypes, a final Rift Sovereign boss, and map-only allied hero/tower roles while reusing safe embedded animation assets from the original SWF.

This approach is deliberate: the current FFDec import pipeline can reliably replace existing ActionScript classes but cannot safely add completely new classes/assets to this old SWF.

## Performance

The mod keeps combat simulation full-rate: attacks, targeting and movement are not skipped for performance. Optimization is concentrated on allocations, UI redraws, cosmetic cadence, Send-All back-pressure and adaptive render quality under extreme swarm load.

For best laptop performance:

- plug into power and disable battery saver;
- close the browser copy while using native Ruffle;
- on dual-GPU Windows laptops, assign `.native\ruffle\ruffle.exe` to the high-performance GPU;
- use the Performance page to enable diagnostics and tune thresholds;
- compare nightly vs `--stable` if one Ruffle build regresses on your hardware.

## Saves and records

Native Ruffle stores Flash local data separately from browser Ruffle. The mod's Time Attack/loop records use Flash local shared storage as well, so browser and desktop records may be separate unless their local data is migrated.

## Build verification

Release SWFs are built from the previous verified binary, imported with FFDec, re-exported, and checked for required ActionScript markers before they are published. SHA-256 files in `assets/` identify the exact verified binaries.
