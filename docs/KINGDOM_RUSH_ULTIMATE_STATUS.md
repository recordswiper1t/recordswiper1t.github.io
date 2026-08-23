# Kingdom Rush Ultimate V13 — release gate status

> Historical V13 integration record. This single-SWF approach was not promoted: gameplay tests exposed unresolved cross-engine class-initialization faults. The shipping Ultimate launcher instead provides both campaigns through isolated, tested runtimes, with Frontiers V12.2 removing obsolete online startup dependencies.

V13 is deliberately fail-closed. The current authoritative Frontiers runtime is **V12.1** (`kingdom-rush-frontiers-v12-1.swf`), with V12 and V11 retained only as fallbacks for tooling. Ultimate must preserve the V12 Last Rift content, the V12.1 audio/pop-up polish, and the existing sandbox/performance systems while importing KR1 content.

## Automated gates

The branch contains reproducible CI for the release-critical structural and compile layers:

- KR1 + Frontiers collision-safe binary coexistence and FFDec round-trip verification.
- Southport / `KR1__Level1` recompilation against the Frontiers shared core.
- **The real 37-member KR1 `Level` semantic bridge compiles with all publisher-source KR1 `Level1`–`Level19` stage classes and survives a fresh FFDec re-export verification with zero null stubs.**
- All eight publisher-source KR1 tier-4 tower classes.
- All nine publisher-source selectable KR1 hero classes.
- Combined campaign/save routing, world-map selector, tower menu and hero selector surfaces.
- Preservation checks for Frontiers sandbox markers, The Last Rift, and—when V12.1 is selected—the V12.1 `qolPopupsEnabled` marker.
- **The strengthened single composed candidate passes compilation and fresh FFDec re-export verification with the semantic bridge, 19 KR1 stages, 8 KR1 tier-4 towers, 9 source-ready KR1 heroes, and the combined campaign/tower/hero UI all present together.**
- The V13 branch is merged with the current `main` laptop/iPhone release shell, including the three-game native Ruffle launcher and current V12.1 browser labels.

The retained Actions artifact `ultimate-v12-1-composed-source-ready` contains `ultimate-source-ready.swf` with:

- size: **91,083,570 bytes**
- SHA-256: **647b9f9af5393ef72d2bebb8d02346ce58c99dfd5952fe68491ca864e2e480f0**
- 19 source-ready KR1 stage classes
- 8 KR1 tier-4 tower classes
- 9 source-ready KR1 hero classes
- 37 semantic `Level` compatibility members, 0 missing
- combined router/selector/menu surfaces

The semantic bridge is generated from the namespaced KR1 `Level` export while keeping Frontiers `Level` as the parent runtime. Required ActionScript imports are preserved, and the build fails if any expected compatibility member is absent.

A green compile or serialized SWF is necessary but is **not** sufficient for release. The candidate remains an Actions artifact rather than a public V13 release until runtime/content gates are real.

## Runtime gates that still require gameplay certification

The following cannot be truthfully completed by static CI alone:

- Southport paths, waves, exits/lives, build spots, powers, win/loss, Heroic and Iron behavior.
- KR1 tower ability-rank behavior and exact clipboard/copy-paste semantics in live play.
- KR1 hero movement, combat, cooldown, skill, death and respawn lifecycle behavior.
- Stage-by-stage gameplay testing for the source-ready KR1 campaign/post-campaign maps.
- Combined save/UI behavior across real campaign progression and a full regression pass.

## Content-source blockers

The publisher KR1 Flash build provides `Level1`–`Level19`, not the complete later KR1 content target. The existing Frontiers Flash source also lacks the later Frontiers post-campaign/endless set. In total, **17 locked-scope original stage/endless pieces are absent from the verified Flash inputs**. Those remaining maps require either compatible legitimate source material or reconstruction inside the Flash runtime.

A reference-only CI probe searches the verified builds for loader, URL, external/premium asset and missing-stage references without committing publisher source bodies.

## Native iPhone distinction

The Safari/Ruffle iPhone players are already part of the public hub. A modified native full-content iOS app is a separate port and remains source-dependent: its inventory tooling requires a legitimately owned user-supplied IPA/app bundle and does not bypass FairPlay or redistribute paid game assets.

Until the missing content dependencies and runtime gameplay gates are satisfied, PR #42 remains a draft and no launcher should promote an Ultimate SWF as the completed V13 release.
