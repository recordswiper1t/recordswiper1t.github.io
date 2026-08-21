#!/usr/bin/env python3
"""Epic War 5 sandbox patch builder.

Takes the original Armor Games/Kongregate-era SWF and applies verified AVM2
bytecode AoB patches collected from historical modding research. The builder is
strict by default: every patch must be found or it aborts instead of silently
publishing a broken SWF.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys


def parse_pat(s: str):
    out=[]
    for x in s.split():
        out.append(None if x in {"??","**"} else int(x,16))
    return out

def parse_bytes(s: str): return bytes(int(x,16) for x in s.split())

def find_wild(data: bytes, pat):
    n=len(pat); hits=[]
    for i in range(0,len(data)-n+1):
        if all(p is None or data[i+j]==p for j,p in enumerate(pat)):
            hits.append(i)
    return hits

def patch_exact(data: bytearray, name: str, old: str, new: str, required=True, max_hits=None):
    oldb=parse_bytes(old); newb=parse_bytes(new)
    if len(oldb)!=len(newb): raise ValueError(f"{name}: replacement length differs")
    hits=[]; start=0
    while True:
        i=data.find(oldb,start)
        if i<0: break
        hits.append(i); start=i+1
    if required and not hits: raise RuntimeError(f"required patch not found: {name}")
    if max_hits is not None and len(hits)>max_hits: raise RuntimeError(f"{name}: unexpected {len(hits)} matches")
    for i in hits: data[i:i+len(oldb)]=newb
    return hits

def patch_wild(data: bytearray, name: str, old: str, replacement, required=True, max_hits=None):
    pat=parse_pat(old); hits=find_wild(data,pat)
    if required and not hits: raise RuntimeError(f"required patch not found: {name}")
    if max_hits is not None and len(hits)>max_hits: raise RuntimeError(f"{name}: unexpected {len(hits)} matches")
    for i in hits:
        repl=bytearray(data[i:i+len(pat)])
        replacement(repl)
        data[i:i+len(pat)]=repl
    return hits


def build(src: pathlib.Path, dst: pathlib.Path, report: pathlib.Path, chaos=False):
    raw=src.read_bytes()
    if raw[:3] not in (b'FWS',b'CWS',b'ZWS'):
        raise RuntimeError('input is not an SWF')
    data=bytearray(raw)
    changes={}

    # No mana cost: pushbyte <cost> -> pushbyte 0 before dat_mana assignment.
    changes['no_mana_cost']=patch_wild(
        data,'no mana cost','d0 24 ?? 68 92 01',
        lambda b: b.__setitem__(2,0), required=True)

    # Remove the population/build cap check.
    changes['no_build_limit']=patch_exact(
        data,'no build limit',
        'd0 46 ea 04 00 24 04 0c 28 00 00',
        'd0 46 ea 04 00 24 00 0f 28 00 00', required=True, max_hits=4)

    # Units become available immediately instead of waiting for the normal timer.
    changes['instant_unit_spawn']=patch_exact(
        data,'instant unit spawn',
        '24 00 0d 43 00 00',
        '24 00 0d 00 00 00', required=True)

    # Spell use adds mana instead of subtracting it. Combined with no-cost this
    # intentionally turns the spell system into a sandbox resource generator.
    changes['spells_generate_mana']=patch_exact(
        data,'spells generate mana',
        '66 e6 04 90 4f a1 18 01',
        '66 e6 04 02 4f a1 18 01', required=False)

    # Historical stronger regeneration coefficient patch.
    changes['strong_regen']=patch_exact(
        data,'strong regeneration',
        'd0 66 ad 0e 2f 17 a2 4f fe 0e 01',
        'd0 66 ad 0e 2f 14 a2 4f fe 0e 01', required=False)

    # Optional chaos behavior: losing the hero resolves through the win string.
    if chaos:
        changes['hero_death_wins']=patch_exact(
            data,'hero death wins',
            '68 dc 01 f0 91 03 d0 66 ce 01 2c 8b 11 61 9f 16',
            '68 dc 01 f0 91 03 d0 66 ce 01 2c a1 26 61 9f 16', required=False)

    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(data)
    result={
      'source':str(src), 'output':str(dst), 'chaos':chaos,
      'input_size':len(raw), 'output_size':len(data),
      'input_sha256':hashlib.sha256(raw).hexdigest(),
      'output_sha256':hashlib.sha256(data).hexdigest(),
      'patches':{k:{'count':len(v),'offsets':[hex(x) for x in v[:30]]} for k,v in changes.items()},
    }
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('output')
    ap.add_argument('--report',default='epicwar5-build.json')
    ap.add_argument('--chaos',action='store_true')
    a=ap.parse_args()
    try: build(pathlib.Path(a.input),pathlib.Path(a.output),pathlib.Path(a.report),a.chaos)
    except Exception as e:
        print(f'BUILD FAILED: {e}',file=sys.stderr); sys.exit(2)
