#!/usr/bin/env python3
"""Runtime routing table for Kingdom Rush Ultimate stages.

This turns stable manifest stage IDs into runtime class identities without using
`LevelN` as save/progression identity. Missing/reconstruction stages stay
explicitly unroutable until real content exists.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json

from content_manifest import STAGES, CUSTOM_STAGES, validate as validate_content


@dataclass(frozen=True)
class Route:
    stage_id: str
    game: str
    title: str
    kind: str
    runtime_class: str | None
    runtime_mode: str
    save_key: str
    unlock_after: str | None
    source_ready: bool
    source_requirement: str


def route_for(stage) -> Route:
    runtime_class = None
    runtime_mode = "standard"
    source_ready = False

    if stage.game == "krf" and stage.kind == "main" and stage.source_locator:
        runtime_class = stage.source_locator
        source_ready = True
    elif stage.game == "kr1" and stage.source_locator:
        runtime_class = "KR1__" + stage.source_locator
        source_ready = True
    elif stage.id == "krf-v12-the-last-rift":
        # Last Rift is entered through V12's Level15 post-boss controller rather
        # than a separate native level class.
        runtime_class = "Level15"
        runtime_mode = "v12_last_rift"
        source_ready = True

    return Route(
        stage_id=stage.id,
        game=stage.game,
        title=stage.title,
        kind=stage.kind,
        runtime_class=runtime_class,
        runtime_mode=runtime_mode,
        save_key=f"ultimate.stage.{stage.id}",
        unlock_after=stage.unlock_after,
        source_ready=source_ready,
        source_requirement=stage.source_requirement,
    )


def routes(include_custom: bool = True) -> list[Route]:
    validate_content()
    stages = STAGES + (CUSTOM_STAGES if include_custom else [])
    return [route_for(s) for s in stages]


def validate() -> None:
    rows = routes(True)
    ids = [r.stage_id for r in rows]
    keys = [r.save_key for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate stage IDs in runtime registry")
    if len(keys) != len(set(keys)):
        raise SystemExit("duplicate save keys in runtime registry")

    by_id = {r.stage_id: r for r in rows}
    if by_id["kr1-southport"].runtime_class != "KR1__Level1":
        raise SystemExit("Southport runtime route mismatch")
    if by_id["kr1-the-dark-tower"].runtime_class != "KR1__Level12":
        raise SystemExit("KR1 final main route mismatch")
    if by_id["krf-hammerhold"].runtime_class != "Level1":
        raise SystemExit("Hammerhold runtime route mismatch")
    if by_id["krf-emberspike-depths"].runtime_class != "Level15":
        raise SystemExit("Frontiers final main route mismatch")
    if by_id["krf-v12-the-last-rift"].runtime_mode != "v12_last_rift":
        raise SystemExit("Last Rift runtime mode mismatch")

    for row in rows:
        if row.source_requirement == "non_flash_or_reconstruction" and row.runtime_class is not None:
            raise SystemExit(f"{row.stage_id}: missing-source content must not be routable yet")


def summary(rows: list[Route]) -> dict:
    return {
        "route_count_including_bonus": len(rows),
        "source_ready_routes": sum(r.source_ready for r in rows),
        "blocked_routes": sum(not r.source_ready for r in rows),
        "kr1_ready_routes": sum(r.game == "kr1" and r.source_ready for r in rows),
        "krf_ready_routes": sum(r.game == "krf" and r.source_ready for r in rows),
        "stable_save_namespace": "ultimate.stage.<stage-id>",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--without-custom", action="store_true")
    args = p.parse_args()
    validate()
    rows = routes(not args.without_custom)
    payload = {"summary": summary(rows), "routes": [asdict(r) for r in rows]}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
