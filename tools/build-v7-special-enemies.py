#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build-v7-special-enemies.py <exported-scripts-dir>")

scripts = Path(sys.argv[1])


def read(name: str) -> str:
    p = scripts / name
    if not p.exists():
        raise SystemExit(f"missing exported script: {p}")
    return p.read_text(encoding="utf-8-sig")


def write(name: str, text: str) -> None:
    (scripts / name).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    return text.replace(old, new, 1)


# Cannibal Beast has a scripted volcano/sacrifice endpoint and never calls the
# base Enemy path-end routine. In recycle mode, loop it before that endpoint.
beast = read("EnemyCanibalBeast.as")
beast = replace_once(
    beast,
    '''         if(this.§package for var§ == this.§with const static§.length - 3)
         {
            this.§return for if§();
            return false;
         }
''',
    '''         if(this.§package for var§ == this.§with const static§.length - 3)
         {
            if(Level.qolRecycleEnemies)
            {
               this.isActive = false;
               this.isBlocked = false;
               this.isFighting = false;
               this.isCharging = false;
               this.soldier = null;
               this.§_-1v§ = "";
               this.§package for var§ = 0;
               this.x = this.§with const static§[0].x;
               this.y = this.§with const static§[0].y;
               this.xSpeed = 0;
               this.ySpeed = 0;
               this.visible = false;
               return true;
            }
            this.§return for if§();
            return false;
         }
''',
    "Cannibal Beast recycle endpoint",
)
write("EnemyCanibalBeast.as", beast)


# Tremor copies the base exit routine instead of delegating to it, so patch its
# copied life-loss branch and its custom death method directly.
tremor = read("EnemyTremor.as")
tremor = replace_once(
    tremor,
    '''         if(this.§package for var§ + 7 < this.§with const static§.length)
         {
            return false;
         }
         this.isActive = false;
         this.§_-uc§ = false;
         this.cRoot.§with for super§(this);
         this.cRoot.§function for const§(this.cost);
         this.cRoot.updateCash(this.gold);
         this.destroyThis();
         return true;
''',
    '''         if(this.§package for var§ + 7 < this.§with const static§.length)
         {
            return false;
         }
         if(Level.qolRecycleEnemies)
         {
            this.isActive = false;
            this.§_-uc§ = false;
            this.isBlocked = false;
            this.isFighting = false;
            this.isCharging = false;
            this.soldier = null;
            this.§_-1v§ = "";
            this.§package for var§ = 0;
            this.x = this.§with const static§[0].x;
            this.y = this.§with const static§[0].y;
            this.xSpeed = 0;
            this.ySpeed = 0;
            this.visible = false;
            return true;
         }
         this.isActive = false;
         this.§_-uc§ = false;
         this.cRoot.§with for super§(this);
         this.cRoot.§function for const§(this.cost);
         this.cRoot.updateCash(this.gold);
         this.destroyThis();
         return true;
''',
    "Tremor recycle endpoint",
)
tremor = replace_once(
    tremor,
    "         this.isDead = true;\n         this.lifeBar.hide();",
    "         this.isDead = true;\n         if(this.cRoot != null)\n         {\n            this.cRoot.qolTimeAttackEnemyKilled();\n         }\n         this.lifeBar.hide();",
    "Tremor timer kill notification",
)
write("EnemyTremor.as", tremor)


for name, needles in {
    "EnemyCanibalBeast.as": ["if(Level.qolRecycleEnemies)", "this.§package for var§ = 0;"],
    "EnemyTremor.as": ["if(Level.qolRecycleEnemies)", "this.cRoot.qolTimeAttackEnemyKilled();"],
}.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r} missing from {name}")

print("V7 special-enemy recycling patches applied successfully")
