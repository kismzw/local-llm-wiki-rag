from __future__ import annotations

from pathlib import Path
from llm_wiki.schemas import GraphEdge
from llm_wiki.utils.io import append_jsonl


def build_simple_graph(claims: list[dict], out_nodes: Path, out_edges: Path) -> None:
    nodes = {}
    edges = []
    eidx = 1
    for c in claims:
        page_ids = c.get("wiki_page_ids", [])
        for pid in page_ids:
            nodes[pid] = {"id": pid, "type": "Page"}
            cid = c["id"]
            nodes[cid] = {"id": cid, "type": "Claim"}
            edges.append(GraphEdge(
                id=f"edge_{eidx:06d}",
                source_id=pid,
                target_id=cid,
                relation="supports",
                confidence="medium",
                source_chunk_ids=c.get("source_chunk_ids", []),
                metadata={},
            ).model_dump())
            eidx += 1
    append_jsonl(out_nodes, list(nodes.values()))
    append_jsonl(out_edges, edges)
