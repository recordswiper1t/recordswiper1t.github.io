#!/usr/bin/env python3
"""Epic War 5 sandbox patch builder.

Applies verified AVM2 AoB patches to the *uncompressed* SWF body, then restores
CWS compression. Strict required-patch checks prevent publishing a silently
incompatible build.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, struct, sys, zlib


def parse_pat(s: str):
    return [None if x in {"??","**"} else int(x,16) for x in s.split()]

def parse_bytes(s: str): return bytes(int(x,16) for x in s.split())

def find_wild(data: bytes, pat):
    n=len(pat); hits=[]
    for i in range(0,len(data)-n+1):
        if all(p is None or data[i+j]==p for j,p in enumerate(pat)): hits.append(i)
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
        repl=bytearray(data[i:i+len(pat)]); replacement(repl); data[i:i+len(pat)]=repl
    return hits

def unpack_swf(raw: bytes):
    sig=raw[:3]; version=raw[3:4]; declared=raw[4:8]
    if sig==b'FWS': return bytearray(raw), 'FWS'
    if sig==b'CWS':
        body=zlib.decompress(raw[8:])
        data=bytearray(b'FWS'+version+declared+body)
        expected=struct.unpack('<I',declared)[0]
        if len(data)!=expected: raise RuntimeError(f'uncompressed length {len(data)} != declared {expected}')
        return data, 'CWS'
    if sig==b'ZWS': raise RuntimeError('ZWS/LZMA input not supported by this builder yet')
    raise RuntimeError('input is not an SWF')

def repack_swf(data: bytearray, original_sig: str):
    if original_sig=='FWS': return bytes(data)
    if original_sig=='CWS': return b'CWS'+bytes(data[3:8])+zlib.compress(bytes(data[8:]),9)
    raise RuntimeError('unsupported output compression')

def build(src: pathlib.Path, dst: pathlib.Path, report: pathlib.Path, chaos=False):
    raw=src.read_bytes(); data,original_sig=unpack_swf(raw); changes={}

    changes['no_mana_cost']=patch_wild(data,'no mana cost','d0 24 ?? 68 92 01',lambda b:b.__setitem__(2,0),required=True)
    changes['no_build_limit']=patch_exact(data,'no build limit','d0 46 ea 04 00 24 04 0c 28 00 00','d0 46 ea 04 00 24 00 0f 28 00 00',required=True,max_hits=4)
    changes['instant_unit_spawn']=patch_exact(data,'instant unit spawn','24 00 0d 43 00 00','24 00 0d 00 00 00',required=True)
    changes['spells_generate_mana']=patch_exact(data,'spells generate mana','66 e6 04 90 4f a1 18 01','66 e6 04 02 4f a1 18 01',required=False)
    changes['strong_regen']=patch_exact(data,'strong regeneration','d0 66 ad 0e 2f 17 a2 4f fe 0e 01','d0 66 ad 0e 2f 14 a2 4f fe 0e 01',required=False)
    if chaos:
        changes['hero_death_wins']=patch_exact(data,'hero death wins','68 dc 01 f0 91 03 d0 66 ce 01 2c 8b 11 61 9f 16','68 dc 01 f0 91 03 d0 66 ce 01 2c a1 26 61 9f 16',required=False)

    out=repack_swf(data,original_sig)
    dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(out)
    result={'source':str(src),'output':str(dst),'chaos':chaos,'compression':original_sig,'input_size':len(raw),'uncompressed_size':len(data),'output_size':len(out),'input_sha256':hashlib.sha256(raw).hexdigest(),'output_sha256':hashlib.sha256(out).hexdigest(),'patches':{k:{'count':len(v),'offsets':[hex(x) for x in v[:30]]} for k,v in changes.items()}}
    report.parent.mkdir(parents=True,exist_ok=True); report.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--report',default='epicwar5-build.json'); ap.add_argument('--chaos',action='store_true'); a=ap.parse_args()
    try: build(pathlib.Path(a.input),pathlib.Path(a.output),pathlib.Path(a.report),a.chaos)
    except Exception as e: print(f'BUILD FAILED: {e}',file=sys.stderr); sys.exit(2)
