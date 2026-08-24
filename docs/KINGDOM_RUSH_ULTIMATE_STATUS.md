# Kingdom Rush Ultimate V14 — release status

V14 is the combined Flash runtime. The central launcher opens it directly with `?campaign=ultimate`, while standalone Kingdom Rush and offline-ready Frontiers V12.2 remain available as recovery choices.

## Released artifact

- file: `assets/kingdom-rush-ultimate-v14.swf`
- size: **91,082,091 bytes**
- SHA-256: **938D42E985F96875C9AAE7C90CA8C0FCC63F3BFB2939750E5C39082208907FCC**
- campaign maps: both native maps — all 19 stages present in the verified Kingdom Rush Flash source plus all 15 Frontiers campaign stages
- in-game map switching: persistent **KR MAP** and **KRF MAP** controls
- shared systems: synchronized stars plus native hero, upgrade, achievement and encyclopedia entry points
- battle tools: clickable KR and KRF sandbox controls with adaptive 1×/2×/4×/8×/12× speed
- Instant Win: direct result-screen path, including the custom final Frontiers stage

The launcher intentionally describes the exact content present in the verified Flash inputs. Later mobile-only post-campaign and endless maps are not advertised as part of this build.

## Gameplay certification completed

The exact V14 SWF was exercised through the same Ruffle browser path used by the site:

- combined title, save selection and Frontiers difficulty/map startup completed without browser errors;
- the persistent KR MAP, KRF MAP and SHARED HUB controls rendered over the native Frontiers map;
- KRF → KR switching produced the real KR map, hid the inactive KRF map completely and centered the narrower KR canvas;
- the shared hub rendered both campaigns' hero, star-upgrade, achievement and encyclopedia entry points plus the complete speed/Instant Win contract;
- fresh post-build decompilation confirmed both direct victory-menu jumps and the custom final-stage bypass in the released bytes;
- the prior V13 battle certification remains the gameplay regression baseline: Southport completed all seven waves and returned from victory, while Emberspike Depths and Hammerhold both started live advancing waves.

The remaining MP3 end-of-stream diagnostic is inherited unchanged from the original Frontiers audio and is non-blocking; it also occurs in the untouched standalone runtime.

## Structural and regression gates

- collision-safe KR class namespacing and Frontiers-parent compatibility bridge;
- 19 KR stage classes, eight KR tier-4 tower classes, and nine source-ready KR hero classes;
- native map routing plus shared star, hero, upgrade, achievement and encyclopedia surfaces;
- fresh compiler/serialization verification and twelve automated release/Ultimate tests;
- preservation of Frontiers sandbox, The Last Rift, audio/pop-up polish, and performance markers;
- standalone Frontiers V12.2 smoke-tested from title through Hammerhold enemy movement.

## Access paths

- central hub: `/`
- combined release: `/ultimate/play.html?campaign=ultimate`
- three-game mobile hub: `/games/`
- standalone recovery choices: `/ultimate/play.html?campaign=kr` and `/ultimate/play.html?campaign=krf`

These routes are release gates: the games are not considered shipped unless the public central page reaches the real title/map/battle runtime rather than only a wrapper page.
