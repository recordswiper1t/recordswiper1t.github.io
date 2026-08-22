#!/usr/bin/env python3
"""Rank Frontiers Level members as semantic candidates for KR1 adapter members.

The input source stays local/CI-only. Output contains member signatures and
structural similarity scores, never method bodies. This helps replace compile
stubs in KR1__Level with real Frontiers-backed behavior after the compiler layer
is proven.
"""
from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from level_api_diff import FUNC_RE, members, read, serial_member_list  # noqa: E402

IDENT_RE = re.compile(r"§[^§]+§|[A-Za-z_$][A-Za-z0-9_$]*")
TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|§[^§]+§|[A-Za-z_$][A-Za-z0-9_$]*|'
    r'\d+(?:\.\d+)?|===|!==|>>>|>>|<<|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|%=|'
    r'[{}()\[\].,;:+\-*/%<>=!?&|^~]'
)
KEYWORDS = {
    "if", "else", "for", "each", "while", "do", "switch", "case", "default",
    "break", "continue", "return", "throw", "try", "catch", "finally", "new",
    "this", "super", "null", "true", "false", "in", "is", "as", "typeof",
    "delete", "void", "var", "const", "function",
}


def arg_count(args: str | None) -> int:
    if not args or not args.strip():
        return 0
    depth = 0
    count = 1
    in_string = None
    escaped = False
    for ch in args:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in "\"'":
            in_string = ch
        elif ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            count += 1
    return count


def find_matching_brace(text: str, open_pos: int) -> int | None:
    depth = 0
    quote = None
    escaped = False
    line_comment = False
    block_comment = False
    i = open_pos
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if line_comment:
            if ch == "\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
                continue
            i += 1
            continue
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue
        if ch == "/" and nxt == "/":
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def extract_functions(text: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for m in FUNC_RE.finditer(text):
        name = m.group(2)
        brace = text.find("{", m.end())
        if brace < 0:
            continue
        end = find_matching_brace(text, brace)
        if end is None:
            continue
        body = text[brace + 1:end]
        row = {
            "name": name,
            "visibility": (m.group(1) or "internal").strip(),
            "args": m.group(3).strip(),
            "return_type": (m.group(4) or "").strip() or None,
            "arg_count": arg_count(m.group(3)),
            "body": body,
        }
        out.setdefault(name, []).append(row)
    return out


def normalize_tokens(body: str) -> list[str]:
    tokens = []
    for tok in TOKEN_RE.findall(body):
        if tok.startswith(('"', "'")):
            tokens.append("STR")
        elif tok[0].isdigit():
            tokens.append("NUM")
        elif IDENT_RE.fullmatch(tok):
            tokens.append(tok if tok in KEYWORDS else "ID")
        else:
            tokens.append(tok)
    return tokens


def score_tokens(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    seq = SequenceMatcher(None, a, b, autojunk=False).ratio()
    len_ratio = min(len(a), len(b)) / max(len(a), len(b))
    # Sequence shape is primary; length agreement prevents tiny generic hooks
    # from ranking too highly against large functions.
    return 0.82 * seq + 0.18 * len_ratio


def public_function_row(row: dict, score: float) -> dict:
    return {
        "name": row["name"],
        "visibility": row["visibility"],
        "args": row["args"],
        "return_type": row["return_type"],
        "arg_count": row["arg_count"],
        "normalized_token_count": len(row["tokens"]),
        "structural_similarity": round(score, 5),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kr1-level", type=Path, required=True)
    ap.add_argument("--krf-level", type=Path, required=True)
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    kr1_text = read(args.kr1_level)
    krf_text = read(args.krf_level)
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    candidates = contract.get("adapter_candidates", {})
    if not isinstance(candidates, dict):
        raise SystemExit("contract missing adapter_candidates")

    kr1_funcs = extract_functions(kr1_text)
    krf_funcs = extract_functions(krf_text)
    kr1_members = members(kr1_text)
    krf_members = members(krf_text)

    for rows in kr1_funcs.values():
        for row in rows:
            row["tokens"] = normalize_tokens(row["body"])
    for rows in krf_funcs.values():
        for row in rows:
            row["tokens"] = normalize_tokens(row["body"])

    out = {}
    for name in sorted(candidates):
        source_sigs = kr1_members.get(name, [])
        kinds = {x.kind for x in source_sigs}
        if "function" in kinds and name in kr1_funcs:
            source = kr1_funcs[name][0]
            ranked = []
            for rows in krf_funcs.values():
                for row in rows:
                    # Prefer matching arity. Return type is a soft filter because
                    # obfuscated/decompiled types can differ across the two games.
                    if row["arg_count"] != source["arg_count"]:
                        continue
                    score = score_tokens(source["tokens"], row["tokens"])
                    if source["return_type"] and row["return_type"] == source["return_type"]:
                        score = min(1.0, score + 0.035)
                    ranked.append((score, row))
            ranked.sort(key=lambda x: (-x[0], x[1]["name"]))
            out[name] = {
                "kind": "function",
                "kr1_signatures": serial_member_list(source_sigs),
                "kr1_normalized_token_count": len(source["tokens"]),
                "frontiers_candidates": [public_function_row(r, s) for s, r in ranked[:args.top]],
            }
        else:
            source_type = source_sigs[0].type if source_sigs else None
            same_type = []
            same_kind = []
            for other_name, rows in krf_members.items():
                for row in rows:
                    if row.kind not in {"var", "const"}:
                        continue
                    public = {
                        "name": other_name,
                        "kind": row.kind,
                        "visibility": row.visibility,
                        "type": row.type,
                    }
                    same_kind.append(public)
                    if source_type and row.type == source_type:
                        same_type.append(public)
            out[name] = {
                "kind": "field",
                "kr1_signatures": serial_member_list(source_sigs),
                "frontiers_same_type_candidates": same_type[:60],
                "frontiers_field_candidate_count": len(same_kind),
            }

    payload = {
        "adapter_member_count": len(out),
        "members": out,
        "policy": {
            "method_bodies_emitted": False,
            "normalized_body_tokens_emitted": False,
            "structural_scores_only": True,
            "candidate_ranking_requires_manual_semantic_confirmation": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        name: (row.get("frontiers_candidates") or row.get("frontiers_same_type_candidates") or [])[:3]
        for name, row in out.items()
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
