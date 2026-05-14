from __future__ import annotations

from pathlib import Path


def extract_markdown(path: Path, document_id: str) -> dict:
    return {"document_id": document_id, "sections": [{"section": "document", "text": path.read_text(encoding="utf-8")}]}
