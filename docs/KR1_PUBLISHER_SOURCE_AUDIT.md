# KR1 publisher-source structural audit

Source-audit workflow: `.github/workflows/audit-kr1-official-source.yml`.

The workflow retrieves the historical Armor Games publisher web build only for structural analysis, then discards the SWF/decompiled scripts. It uploads hashes and class-name inventories only.

## Verified source

- historical publisher file: `kingdom-rush-12141.swf`
- SHA-256: `7b5467a3eccc17f6dd001ff2d41bdf1b03d79fd515a2a9586c42bfd982bb1e23`
- FFDec used for the audit: 26.2.1

## Structural result

| Metric | KR1 publisher build | Frontiers V11/V12 base |
| --- | ---: | ---: |
| exported AS files | 994 | 1302 |
| detected classes | 995 | 1103 |
| level-class candidates | 35 | 23 |
| enemy-class candidates | 124 | 58 |
| tower-class candidates | 78 | 59 |
| hero-class candidates | 63 | 93 |
| direct class-name collisions | **203** | **203** |

The key practical finding is that the KR1 source contains concrete `Level1` through `Level19` classes. The combined build therefore has real source material for the 12 main KR1 maps plus seven additional map classes in this historical Flash release. The later KR1 post-campaign maps that are absent from this build remain reconstruction/source-input work.

## Tower coverage in the source

All eight KR1 tier-4 gameplay classes needed for the four-choice combined tower tree are present structurally:

- `TowerArcherRanger`
- `TowerArcherMusketeer`
- `TowerSoldierPaladin`
- `TowerSoldierBarbarian`
- `TowerMageArcane`
- `TowerMageSorcerer`
- `TowerEngineerTesla`
- `TowerEngineerBfg`

This means the KR1 tower half should be imported from real game logic rather than reimplemented from memory.

## Hero coverage in the source

The build contains gameplay classes for the early/core KR1 hero set, including Gerald, Alleria, Malik, Bolin, Magnus, Ignus, King Denas, Elora/Frost and Ingvar/Viking. It does **not** structurally expose the entire 13-hero target roster in this audited web build, so the final 29-hero combined roster still needs compatible source/reconstruction for the missing later KR1 heroes and missing later Frontiers heroes.

## Merge implication

A raw append is not viable: 203 class names collide, including `Level`, `Level1`-`Level15`, `Enemy`, standard tower graphic/linkage classes, menus and shared utility classes. The importer must therefore:

1. namespace imported KR1 ABC/class/linkage names;
2. remap imported SWF character IDs and every dependent reference;
3. exclude the KR1 document-class/root timeline from becoming the active application;
4. retain Frontiers as the authoritative engine and existing V11/V12 enhancement layer;
5. import only validated KR1 definitions/assets/scripts needed by the combined content.

The merge probe workflow now tests FFDec XML round-tripping and records the XML tag/reference schema needed to implement that remapper.
