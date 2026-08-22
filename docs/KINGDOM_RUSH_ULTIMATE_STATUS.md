# Kingdom Rush Ultimate V13 — release gate status

V13 is deliberately fail-closed. The current authoritative Frontiers runtime is **V12.1** (`kingdom-rush-frontiers-v12-1.swf`), with V12 and V11 retained only as fallbacks for tooling. Ultimate must preserve the V12 Last Rift content, the V12.1 audio/pop-up polish, and the existing sandbox/performance systems while importing KR1 content.

## Automated gates

The branch contains reproducible CI for the release-critical structural and compile layers:

- KR1 + Frontiers collision-safe binary coexistence and FFDec round-trip verification.
- Southport / `KR1__Level1` recompilation against the Frontiers shared core.
- One compatibility adapter plus all publisher-source KR1 `Level1`–`Level19` stage classes.
- All eight publisher-source KR1 tier-4 tower classes.
- All nine publisher-source selectable KR1 hero classes.
- Combined campaign/save routing, world-map selector, tower menu and hero selector surfaces.
- Preservation checks for Frontiers sandbox markers, The Last Rift, and—when V12.1 is selected—the V12.1 `qolPopupsEnabled` marker.

A green compile or serialized SWF is necessary but is **not** sufficient for release.

## Runtime gates that still require gameplay certification

The following cannot be truthfully completed by static CI alone:

- Southport paths, waves, exits/lives, build spots, powers, win/loss, Heroic and Iron behavior.
- KR1 tower ability-rank behavior and exact clipboard/copy-paste semantics in live play.
- KR1 hero movement, combat, cooldown, skill, death and respawn lifecycle behavior.
- Stage-by-stage gameplay testing for the source-ready KR1 campaign/post-campaign maps.
- Combined save/UI behavior across real campaign progression and a full regression pass.

## Content-source blockers

The publisher KR1 Flash build provides `Level1`–`Level19`, not the complete later KR1 content target. The existing Frontiers Flash source also lacks the later Frontiers post-campaign/endless set. Those remaining maps require either a compatible source the user is entitled to use or a legal reconstruction inside the Flash runtime.

Until those dependencies and runtime gates are satisfied, PR #42 remains a draft and no launcher should promote an Ultimate SWF as the completed V13 release.
