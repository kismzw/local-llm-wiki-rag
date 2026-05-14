from __future__ import annotations

import typer
from llm_wiki.config import load_settings
from llm_wiki.graph.builder import build_simple_graph
from llm_wiki.utils.io import read_jsonl

app = typer.Typer()


@app.command()
def main() -> None:
    s = load_settings()
    root = s.root_path
    claims = read_jsonl(root / "metadata/claims.jsonl")
    build_simple_graph(claims, root / "graph/nodes.jsonl", root / "graph/edges.jsonl")
    print("graph built")


if __name__ == "__main__":
    app()
