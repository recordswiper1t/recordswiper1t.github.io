#!/usr/bin/env python3
from pathlib import Path
import sys

source_path = Path(__file__).with_name('build-v12.py')
src = source_path.read_text(encoding='utf-8')

old1 = "level=rep(level,\n'''         this.qolTimerLabel.text = \"TIME  \""
new1 = "level=rep(level,\nr'''         this.qolTimerLabel.text = \"TIME  \""
old2 = "this.qolBestTimeText();''',\n'''         this.qolTimerLabel.text = \"TIME \""
new2 = "this.qolBestTimeText();''',\nr'''         this.qolTimerLabel.text = \"TIME \""

if old1 not in src or old2 not in src:
    raise SystemExit('V12 runner could not locate timer escape normalization anchors')
src = src.replace(old1, new1, 1).replace(old2, new2, 1)

namespace = {
    '__name__': '__main__',
    '__file__': str(source_path),
}
exec(compile(src, str(source_path), 'exec'), namespace, namespace)
