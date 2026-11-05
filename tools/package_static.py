#!/usr/bin/env python3
"""Copy only the published static surface into dist (no notes, Git, or QA files)."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parent.parent
dest=root/'dist';dest.mkdir(exist_ok=True)
for p in root.glob('*.html'):shutil.copy2(p,dest/p.name)
for name in ['assets','topics','lessons']:shutil.copytree(root/name,dest/name,dirs_exist_ok=True)
print('Static publication surface ready in dist/.')
