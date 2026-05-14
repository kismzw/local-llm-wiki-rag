from __future__ import annotations

import typer
from llm_wiki.config import load_settings
from llm_wiki.indexing.vector import build_tfidf_index
from llm_wiki.indexing.summaries import build_summaries
from llm_wiki.utils.io import read_jsonl, append_jsonl

app = typer.Typer()


@app.command()
def main() -> None:
    s = load_settings()
    root = s.root_path
    chunks = read_jsonl(root / "metadata/chunks.jsonl")
    build_tfidf_index(chunks, "text", root / "indexes/source_vector")
    summaries = build_summaries(chunks)
    append_jsonl(root / "indexes/summary_index/summaries.jsonl", summaries)
    build_tfidf_index(summaries, "text", root / "indexes/summary_index")
    print("indexes built")


if __name__ == "__main__":
    app()
