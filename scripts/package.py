#!/usr/bin/env python3
"""Build dist/deepen.zip for claude.ai uploads and the Claude Skills API.

The archive root is the skill folder (deepen/SKILL.md), which is what both expect.
Stdlib only. Entries get fixed timestamps, so rebuilding the same SKILL.md gives the
same bytes.

    python3 scripts/package.py
"""
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "deepen"
OUT = ROOT / "dist" / "deepen.zip"
EPOCH = (1980, 1, 1, 0, 0, 0)  # oldest timestamp zip allows

OUT.parent.mkdir(exist_ok=True)
files = sorted(p for p in SKILL_DIR.rglob("*") if p.is_file() and p.name != ".DS_Store")
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in files:
        info = zipfile.ZipInfo(f"deepen/{path.relative_to(SKILL_DIR).as_posix()}", EPOCH)
        info.external_attr = 0o644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, path.read_bytes())

with zipfile.ZipFile(OUT) as zf:
    for name in zf.namelist():
        print(f"  {name}")
print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
