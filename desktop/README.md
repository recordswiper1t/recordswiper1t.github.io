# Native desktop launcher — KRF, Super Stick War and Epic War 5

This is the highest-performance laptop path for the released Flash mods. It runs the selected verified SWF directly in native Ruffle instead of the browser/WebAssembly player.

## Fastest way to play

### Windows

1. Download the repository ZIP and extract it.
2. Open the `desktop` folder.
3. Double-click `run-native.bat` for Kingdom Rush Frontiers, or run one of the commands below from Command Prompt / PowerShell.
4. The first launch downloads native Ruffle automatically; later launches reuse `.native\ruffle\ruffle.exe`.

```text
desktop\run-native.bat --game krf
desktop\run-native.bat --game stickwar
desktop\run-native.bat --game epicwar5
desktop\run-native.bat --game epicwar5-expansion
```

Windows also accepts the shortcuts `--krf`, `--stickwar`, `--epicwar5` and `--epicwar5-expansion`.

No Python installation is required on Windows.

### macOS / Linux

Run:

```text
sh desktop/run-native.sh --game krf
sh desktop/run-native.sh --game stickwar
sh desktop/run-native.sh --game epicwar5
sh desktop/run-native.sh --game epicwar5-expansion
```

Python 3 is required for the macOS/Linux bootstrap launcher.

## Released game selection

- `krf` selects the newest verified Kingdom Rush Frontiers release present, currently preferring V12.1 → V12 → V11 → V10 → V9 → V8 → V5 fallback.
- `stickwar` launches `assets/stick-war-complete-v1.swf`, the released 65-stage SW1+SW2 expansion.
- `epicwar5` launches the stable V1.05-based Sandbox V2 build.
- `epicwar5-expansion` launches `assets/epic-war-5-expansion-v35.swf`, the released V3.5 Expansion with direct web/mobile entry, repaired stage transitions and a default-off battle sandbox. Native play keeps the normal campaign unlock requirement.

Kingdom Rush Frontiers V12 keeps every V11 sandbox/performance feature and adds The Last Rift, post-boss scoring, renderer hardening and additional performance work. V12.1 adds the current audio/pop-up polish.

## Windows graphics crash protection

Some Windows systems can hit a native Ruffle/wgpu Vulkan panic. The launcher therefore does **not** use Vulkan by default.

- Default: DirectX 12 (`dx12`)
- If DX12 exits unsuccessfully: automatically retry OpenGL
- Force OpenGL: `desktop\run-native.bat --gl`
- Explicit Vulkan test only: `desktop\run-native.bat --vulkan`
- Force DX12: `desktop\run-native.bat --dx12`

These renderer options work with every `--game` selection. If a cached Ruffle build itself appears broken, add `--refresh`.

## Ruffle channel

The default is a recent Ruffle nightly because Flash compatibility/performance fixes land there first. To use the newest stable release instead, add `--stable`, for example:

```text
desktop\run-native.bat --game stickwar --stable
sh desktop/run-native.sh --game epicwar5 --stable
```

## Kingdom Rush Frontiers sandbox features

The KRF in-level sandbox is organized into Heroes, Enemies, Waves/Time Attack, Towers/Clipboard, Cheats/Cleanup and Performance pages. Opening the sandbox pauses the level.

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

All three released mod lines keep combat simulation full-rate. Optimization is concentrated on allocations, targeting/search work, UI redraws, cosmetic cadence/effect budgets, swarm back-pressure and adaptive render quality rather than skipping core attacks/movement.

For best laptop performance:

- plug into power and disable battery saver;
- close the browser copy while using native Ruffle;
- on dual-GPU Windows laptops, assign `.native\ruffle\ruffle.exe` to the high-performance GPU;
- use each game's diagnostics/performance controls when available;
- compare nightly vs `--stable` if one Ruffle build regresses on your hardware.

## Saves and records

Native Ruffle stores Flash local data separately from browser Ruffle. KRF Time Attack/loop records and other Flash local saves may therefore be separate from the browser versions unless their local data is migrated.

## Build verification

Release SWFs are built from verified binaries/sources, imported with FFDec where applicable, re-exported, and checked for required gameplay/mod markers before they are published. SHA-256/build records in `assets/` identify the verified binaries.
