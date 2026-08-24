# Kingdom Rush Ultimate V13 — verified release status

V13 is the released combined Flash runtime. The central launcher opens it directly with `?campaign=ultimate`, while standalone Kingdom Rush and offline-ready Frontiers V12.2 remain available as recovery choices.

## Released artifact

- file: `assets/kingdom-rush-ultimate-v13.swf`
- size: **91,075,163 bytes**
- SHA-256: **E03AFA8D8DA8E1855FAC2C1E099820F09326F93A830B84BC05EA7A5574D83626**
- campaign selector: **34 stages** — all 19 stages present in the verified Kingdom Rush Flash source plus all 15 Frontiers campaign stages
- shared save/map flow: victory continuation returns to the combined selector

The launcher intentionally describes the exact content present in the verified Flash inputs. Later mobile-only post-campaign and endless maps are not falsely advertised as part of this 34-stage build.

## Gameplay certification completed

The exact released SWF was exercised through the same Ruffle browser path used by the site:

- all five selector pages were opened and counted: 19 KR stages and 15 KRF stages;
- Southport loaded, allowed tower construction, ran all seven waves with enemies and powers active, reached victory, and returned to the shared selector through Continue;
- Emberspike Depths loaded and started a live wave;
- Hammerhold loaded, started a live wave, and showed enemies advancing along the route;
- combined save creation, difficulty selection, campaign switching, stage selection, and map return were exercised;
- retired CPMStar/Mochi startup dependencies and the obsolete Ruffle `preloader` option are absent.

The remaining MP3 end-of-stream diagnostic is inherited unchanged from the original Frontiers audio and is non-blocking; it also occurs in the untouched standalone runtime.

## Structural and regression gates

- collision-safe KR class namespacing and Frontiers-parent compatibility bridge;
- 19 KR stage classes, eight KR tier-4 tower classes, and nine source-ready KR hero classes;
- combined routing, selector, tower, and hero surfaces;
- fresh compiler/serialization verification and six automated Ultimate tests;
- preservation of Frontiers sandbox, The Last Rift, audio/pop-up polish, and performance markers;
- standalone Frontiers V12.2 smoke-tested from title through Hammerhold enemy movement.

## Access paths

- central hub: `/`
- combined release: `/ultimate/play.html?campaign=ultimate`
- three-game mobile hub: `/games/`
- standalone recovery choices: `/ultimate/play.html?campaign=kr` and `/ultimate/play.html?campaign=krf`

These routes are release gates: the games are not considered shipped unless the public central page reaches the real title/map/battle runtime rather than only a wrapper page.
