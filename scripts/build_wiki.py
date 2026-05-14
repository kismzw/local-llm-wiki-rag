from __future__ import annotations

from pathlib import Path
import typer
from llm_wiki.config import load_settings
from llm_wiki.schemas import SourceDocument, SourceChunk
from llm_wiki.utils.io import read_jsonl, append_jsonl
from llm_wiki.wiki.generator import generate_page
from llm_wiki.claims.extractor import extract_claims_from_chunks
from llm_wiki.llm.ollama import OllamaClient

app = typer.Typer()


@app.command()
def main(
    source: str = typer.Option(..., "--source"),
    no_llm: bool = typer.Option(False, "--no-llm", help="Disable LLM section generation and use local fallback."),
) -> None:
    s = load_settings()
    root = s.root_path
    docs = [SourceDocument(**d) for d in read_jsonl(root / "metadata/sources.jsonl")]
    doc = next((d for d in docs if d.id == source), None)
    if not doc:
        raise typer.BadParameter(f"source not found: {source}")
    chunks = [SourceChunk(**c) for c in read_jsonl(root / "extracted/chunks" / f"{source}.jsonl")]
    llm_client = None if no_llm else (OllamaClient(model=s.llm.model) if s.llm.backend == "ollama" else None)
    out = generate_page(doc, chunks, root / "wiki", llm_client=llm_client, log_fn=typer.echo)
    claims = extract_claims_from_chunks(chunks, wiki_page_id=out.stem)
    existing_claims = read_jsonl(root / "metadata/claims.jsonl")
    existing_keys = {
        (c.get("text"), tuple(c.get("source_chunk_ids", [])), tuple(c.get("wiki_page_ids", [])))
        for c in existing_claims
    }
    new_claims = []
    for c in claims:
        key = (c.text, tuple(c.source_chunk_ids), tuple(c.wiki_page_ids))
        if key not in existing_keys:
            new_claims.append(c.model_dump())
    if new_claims:
        append_jsonl(root / "metadata/claims.jsonl", new_claims)
    print(str(out))


if __name__ == "__main__":
    app()
