# Kingdom Rush Ultimate V13 — release gate status

V13 is deliberately fail-closed. The current authoritative Frontiers runtime is **V12.1** (`kingdom-rush-frontiers-v12-1.swf`), with V12 and V11 retained only as fallbacks for tooling. Ultimate must preserve the V12 Last Rift content, the V12.1 audio/pop-up polish, and the existing sandbox/performance systems while importing KR1 content.

## Automated gates

The branch contains reproducible CI for the release-critical structural and compile layers:

- KR1 + Frontiers collision-safe binary coexistence and FFDec round-trip verification.
- Southport / `KR1__Level1` recompilation against the Frontiers shared core.
- **The real 37-member KR1 `Level` semantic bridge compiles with all publisher-source KR1 `Level1`–`Level19` stage classes and survives a fresh FFDec re-export verification.**
- All eight publisher-source KR1 tier-4 tower classes.
- All nine publisher-source selectable KR1 hero classes.
- Combined campaign/save routing, world-map selector, tower menu and hero selector surfaces.
- Preservation checks for Frontiers sandbox markers, The Last Rift, and—when V12.1 is selected—the V12.1 `qolPopupsEnabled` marker.
- A strengthened composition workflow combines the semantic bridge, all source-ready stages/towers/heroes, and shared campaign/roster UI into one candidate and retains the candidate SWF as an Actions artifact when the gate succeeds.
- The V13 branch is merged with the current `main` laptop/iPhone release shell, including the three-game native Ruffle launcher and current V12.1 browser labels.

The semantic bridge is generated from the namespaced KR1 `Level` export while keeping Frontiers `Level` as the parent runtime. Required ActionScript imports are preserved, and the build fails if any expected compatibility member is absent.

A green compile or serialized SWF is necessary but is **not** sufficient for release.

## Runtime gates that still require gameplay certification

The following cannot be truthfully completed by static CI alone:

- Southport paths, waves, exits/lives, build spots, powers, win/loss, Heroic and Iron behavior.
- KR1 tower ability-rank behavior and exact clipboard/copy-paste semantics in live play.
- KR1 hero movement, combat, cooldown, skill, death and respawn lifecycle behavior.
- Stage-by-stage gameplay testing for the source-ready KR1 campaign/post-campaign maps.
- Combined save/UI behavior across real campaign progression and a full regression pass.

## Content-source blockers

The publisher KR1 Flash build provides `Level1`–`Level19`, not the complete later KR1 content target. The existing Frontiers Flash source also lacks the later Frontiers post-campaign/endless set. In total, 17 locked-scope original stage/endless pieces are absent from the verified Flash inputs. Those remaining maps require either compatible legitimate source material or reconstruction inside the Flash runtime.

A reference-only CI probe searches the verified builds for loader, URL, external/premium asset and missing-stage references without committing publisher source bodies.

## Native iPhone distinction

The Safari/Ruffle iPhone players are already part of the public hub. A modified native full-content iOS app is a separate port and remains source-dependent: its inventory tooling requires a legitimately owned user-supplied IPA/app bundle and does not bypass FairPlay or redistribute paid game assets.

Until the missing content dependencies and runtime gameplay gates are satisfied, PR #42 remains a draft and no launcher should promote an Ultimate SWF as the completed V13 release.
