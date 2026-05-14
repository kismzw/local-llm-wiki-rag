from __future__ import annotations

from pathlib import Path


def patch_update(target: Path, additions: str) -> None:
    text = target.read_text(encoding="utf-8")
    if "## Conflicts" not in text:
        text += "\n\n## Conflicts\n\n"
    text += f"\n- {additions}\n"
    target.write_text(text, encoding="utf-8")
