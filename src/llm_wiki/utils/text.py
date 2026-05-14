from __future__ import annotations

import re


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.strip().lower()).strip("-")
    return s or "untitled"
