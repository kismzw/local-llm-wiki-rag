from pathlib import Path
from llm_wiki.graph.builder import build_simple_graph
from llm_wiki.graph.retrieval import get_neighbors


def test_graph_nodes_edges(tmp_path: Path):
    claims = [{"id": "claim_1", "wiki_page_ids": ["page_1"], "source_chunk_ids": ["src_1"]}]
    np = tmp_path / "nodes.jsonl"
    ep = tmp_path / "edges.jsonl"
    build_simple_graph(claims, np, ep)
    n = get_neighbors("page_1", str(ep), hops=1)
    assert n
