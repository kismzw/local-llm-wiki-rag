from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path
from llm_wiki.schemas import SourceDocument
from llm_wiki.utils.hashing import sha256_file
from llm_wiki.utils.io import append_jsonl, read_jsonl

SUPPORTED = {".pdf", ".md", ".txt", ".csv", ".json", ".jsonl", ".py"}


def _source_id(file_hash: str) -> str:
    return f"doc_{file_hash[:8]}"


def register_source(path: Path, source_type: str, metadata_path: Path) -> SourceDocument:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_file() and path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    content_hash = sha256_file(path) if path.is_file() else sha256_file(next(path.rglob("*"))) if any(path.rglob("*")) else "0" * 64
    source_id = _source_id(content_hash)
    existing = read_jsonl(metadata_path)
    for row in existing:
        if row.get("content_hash") == content_hash:
            return SourceDocument(**row)

    stat = path.stat()
    doc = SourceDocument(
        id=source_id,
        path=str(path),
        source_type=source_type,
        title=path.stem,
        created_at=datetime.fromtimestamp(stat.st_ctime, UTC).isoformat(),
        modified_at=datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
        content_hash=content_hash,
        metadata={},
    )
    append_jsonl(metadata_path, [doc.model_dump()])
    return doc
