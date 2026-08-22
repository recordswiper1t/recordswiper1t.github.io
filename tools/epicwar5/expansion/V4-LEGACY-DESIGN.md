# Epic War 5 Expansion V4 — Legacy War

Baseline: the released and sitelock-fixed Expansion V3.3.1. V4 is developed on a separate branch so the V3.3.1 full-playthrough build remains stable.

## Goal

Make a version worth replaying after a complete V3.3.1 run by bringing forward the best systems from Epic War 1–4, improving EW5's existing systems, and adding a deep achievement/mastery layer without turning the default campaign into a sandbox.

## Legacy inspirations

### Epic War 1 / 2
- Castle/turret defense as an active part of battle rather than a passive backdrop.
- In-battle structure upgrades and mana/castle investment.
- Distinct Human / Elf / Orc strategic identities.
- Achievement-unlocked special troops.
- Large late-game bosses and “survive the push, then counterattack” pacing.

### Epic War 3
- Counter/revenge waves.
- Stronger group-command identity: charge, retreat, select-all behavior.
- Hero recovery/respawn concepts.
- New Game+ / Cave of Trial style mastery after campaign completion.
- Achievements that unlock meaningful cards/content.

### Epic War 4
- Hard and Epic difficulty layers.
- Revenge waves on higher difficulty.
- Arrow-tower support as an unlockable battle tool.
- Fast command hotkeys and clearer spell cooldown feedback.
- Challenge achievements such as full-upgrade, boss gimmick, Hard clear and Epic clear goals.

## V4 systems

### 1. Legacy Doctrines
Three persistent doctrines inspired by EW2's races. They do not lock the player out of units; they change how the army plays.

**Human — Bastion**
- stronger castle/support structures
- modest armor/health bonus near the player's side of the battlefield
- cheaper fortification upgrades
- Paladin/knight-style defensive bonuses

**Elf — Wildsong**
- stronger idle regeneration and ranged support
- improved spell recovery / mana efficiency
- mobility/range emphasis
- Dryad/guardian-style support bonuses

**Orc — Warhost**
- faster production and higher pressure
- modest offensive bonus when advancing
- larger disposable-unit presence at the cost of weaker defensive scaling
- beast/totem-style bonuses

Doctrine selection starts neutral. Doctrines unlock through normal achievements and can be changed outside battle.

### 2. Castle Support / Battle Research
Bring back the EW1/EW2/EW4 feeling that the player's castle matters.

Per battle, spend mana to raise a small support tree:
1. **Arrow Tower** — periodic defensive volley in the player's half.
2. **Fortified Gate** — temporary castle damage reduction / emergency buffer.
3. **War Academy** — production benefit for currently equipped units.
4. **Arcane Altar** — spell/mana support.

Upgrades reset each battle. Permanent achievements/doctrine bonuses improve them.

### 3. Difficulty and revenge waves
Every replayable stage gains a V4 difficulty setting:
- **Standard** — current V3.3.1 behavior.
- **Hard** — tougher compositions, +1 revenge wave, increased rewards.
- **Epic** — stronger elites/boss logic, +2 revenge/counter waves, highest rewards.

The base V3.3.1 progression remains completable on Standard. Hard/Epic are mastery content, not gates for basic progression.

### 4. Achievements
Persistent V4 achievement bank, target 36–45 achievements. Achievements must reward something tangible: money/EXP, relics, doctrines, support-tree upgrades, challenge toggles, cosmetic labels, or Legacy Trial access.

Initial achievement categories:
- **Campaign:** first win, 10/20/30/40/50 unique clears, Expansion completion.
- **Army:** unlock 6/9/12 slots, field 12 distinct units, win with 3 or fewer slots.
- **Upgrades:** first advanced node, fully upgrade one unit, fully upgrade a hero, finish all advanced nodes on one character.
- **Equipment:** equip 2/3 slots, assemble themed sets, own all relics.
- **Battle skill:** no hero death, no spell win, no castle damage, fast clear, comeback win.
- **Boss/challenge:** defeat selected bosses under conditions.
- **Legacy mastery:** Hard clears, Epic clears, revenge-wave survival, doctrine-specific wins.
- **Collection:** unlock all three doctrines, earn all Legacy relics, achievement milestones.

Achievement integrity rule: while Sandbox Tools are enabled for a battle, V4 achievement unlocks are disabled. Normal progression may still be used for testing, but achievement completion records remain clean.

### 5. Legacy Trials / postgame mastery
After the normal 50-clear path, unlock a separate Legacy mastery layer. Planned first release: 8–12 curated challenge encounters rather than another 25-stage filler campaign.

Examples:
- Goblin Madness / swarm survival homage.
- Big Bang / artillery pressure encounter.
- Angel Slayer aerial/ranged challenge.
- Lord Baal trick/challenge boss.
- Human Bastion trial.
- Elf Wildsong trial.
- Orc Warhost trial.
- Final “War of Heroes” gauntlet.

These may reuse EW5 art but should have new compositions, restrictions, revenge waves, and reward logic.

### 6. Legacy-inspired units and rewards
Do not import third-party binaries/assets. Build new EW5-native interpretations using existing EW5 art/stat/effect systems.

Candidate legacy archetypes:
- Squire / Knight / Paladin defensive line
- Marksman / Crossbow Cavalier ranged line
- Cleric / Dryad support line
- Totem support caster
- Catapult / Trebuchet / Cannon siege line
- Forest Guardian
- Cerberus
- Arch Angel / legacy Angel capstone

Where an EW5 model already closely matches the archetype, use a new stat/effect identity rather than duplicate art for no reason.

### 7. Sandbox Tools in Settings
Default: **OFF** on new and migrated saves.

Persistent settings:
- Sandbox Tools master enable
- sandbox HUD visibility
- optional free spells
- fast production
- building cap override
- population boost
- selected spawn batch / selected unit / mana increment may remain battle-local

When master enable is OFF:
- no F-key sandbox handlers
- no sandbox HUD
- no sandbox gameplay static toggles
- normal campaign behavior

When master enable is ON, expose the complete Optional Sandbox V2 toolkit:
- F1 add mana
- F2/F3 unit select
- F4 ally spawn
- F5 enemy spawn
- F6 batch 1/5/20/50
- F7 1x/4x/8x
- F8 wipe enemies
- F9 instant win
- F10 heal allies
- F11 free spells
- F12 fast production
- B building cap
- P population boost
- [ / ] mana increment
- backtick HUD

Sandbox-enabled battles do not unlock V4 achievements.

### 8. Quality/performance rules
V4 must retain all V3.3 performance work.
- no regression to full battlefield sort on spawn
- keep broad-phase targeting
- keep throttled UI/population scans
- keep effect culling/weather budgets
- keep adaptive render-quality recovery

New V4 systems must avoid per-frame full-list scans. Achievement evaluation belongs at battle result / event boundaries, not every frame.

## First engineering milestone
1. Decompile exact V3.3.1 release.
2. Audit settings/options/world map/battle result/battle control hook points.
3. Add persistent V4 settings + achievement storage APIs.
4. Gate imported sandbox toolkit behind persistent master setting (OFF by default).
5. Add Standard/Hard/Epic persistent setting and revenge-wave hook scaffold.
6. Build/re-decompile verify before authoring Legacy Trials and new archetypes.
