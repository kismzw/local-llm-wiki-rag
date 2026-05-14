from __future__ import annotations

import json
from pathlib import Path
import typer
from llm_wiki.config import load_settings
from llm_wiki.ingestion.registry import register_source
from llm_wiki.extraction.dispatcher import extract
from llm_wiki.chunking.chunker import chunk_extracted
from llm_wiki.utils.io import append_jsonl, read_jsonl, write_jsonl

app = typer.Typer()


@app.command()
def main(path: str, type: str = typer.Option(..., "--type")) -> None:
    s = load_settings()
    root = s.root_path
    src = register_source(Path(path), type, root / "metadata/sources.jsonl")
    ext = extract(Path(path), src.id)
    (root / "extracted/documents").mkdir(parents=True, exist_ok=True)
    (root / "extracted/documents" / f"{src.id}.json").write_text(json.dumps(ext, ensure_ascii=False), encoding="utf-8")
    chunks = chunk_extracted(ext, source_path=src.path, target_tokens=s.chunking.target_tokens, overlap_tokens=s.chunking.overlap_tokens)

    chunk_file = root / "extracted/chunks" / f"{src.id}.jsonl"
    if chunk_file.exists():
        existing_rows = read_jsonl(chunk_file)
        dedup_existing_rows = list({r.get("id"): r for r in existing_rows}.values())
        if len(dedup_existing_rows) != len(existing_rows):
            write_jsonl(chunk_file, dedup_existing_rows)
        existing = {r.get("id") for r in dedup_existing_rows}
        new_chunks = [c for c in chunks if c.id not in existing]
    else:
        new_chunks = chunks

    if new_chunks:
        append_jsonl(chunk_file, [c.model_dump() for c in new_chunks])
    all_meta = read_jsonl(root / "metadata/chunks.jsonl")
    dedup_meta_by_key = {}
    for row in all_meta:
        key = (row.get("document_id"), row.get("id"))
        dedup_meta_by_key[key] = row
    dedup_meta = list(dedup_meta_by_key.values())
    if len(dedup_meta) != len(all_meta):
        write_jsonl(root / "metadata/chunks.jsonl", dedup_meta)
    if new_chunks:
        all_meta = dedup_meta
        existing_meta = {r.get("id") for r in all_meta if r.get("document_id") == src.id}
        append_jsonl(root / "metadata/chunks.jsonl", [c.model_dump() for c in new_chunks if c.id not in existing_meta])
    print(src.id)


if __name__ == "__main__":
    app()
