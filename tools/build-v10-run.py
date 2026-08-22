#!/usr/bin/env python3
from pathlib import Path

# Compatibility runner for build-v10.py. Legion Archer uses an if-based sell
# handler rather than the switch/case pattern used by the other specials.
path = Path(__file__).with_name('build-v10.py')
source = path.read_text(encoding='utf-8')
source = source.replace("'§_-Xb§.as': ['case \"sell\"']", "'§_-Xb§.as': ['if(param1 == \"sell\")']")
exec(compile(source, str(path), 'exec'))
