#!/usr/bin/env python3
"""Build the user-story-mapping.skill bundle (a zip with SKILL.md at the root).

Run from anywhere; output lands at the repo root.

The .skill format is a plain zip with the skill's directory contents at the
zip's root level (SKILL.md, references/, scripts/, ...). This works in:
- Claude Code (via plugin install or direct skill load)
- Cursor / Codex CLI / Goose / Letta / Roo / Kiro / OpenCode / ~30 other
  Agent Skills v1 compliant hosts that don't speak Claude-Code's plugin format
"""
from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "user-story-mapping"
OUT_PATH = REPO_ROOT / "user-story-mapping.skill"

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".mypy_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".tmp"}


def build() -> int:
    if not SKILL_DIR.is_dir():
        print(f"error: {SKILL_DIR} not found", file=sys.stderr)
        return 1

    if not (SKILL_DIR / "SKILL.md").is_file():
        print(f"error: {SKILL_DIR / 'SKILL.md'} not found", file=sys.stderr)
        return 1

    if OUT_PATH.exists():
        OUT_PATH.unlink()

    file_count = 0
    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(SKILL_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if any(f.endswith(s) for s in EXCLUDE_SUFFIXES):
                    continue
                src = Path(root) / f
                arcname = src.relative_to(SKILL_DIR).as_posix()
                z.write(src, arcname)
                file_count += 1

    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"built {OUT_PATH.relative_to(REPO_ROOT)} ({file_count} files, {size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(build())
