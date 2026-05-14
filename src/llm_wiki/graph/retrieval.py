from __future__ import annotations

from llm_wiki.utils.io import read_jsonl


def get_neighbors(entity_id: str, edges_path: str, hops: int = 2) -> list[dict]:
    edges = read_jsonl(__import__('pathlib').Path(edges_path))
    seen = {entity_id}
    frontier = {entity_id}
    out = []
    for _ in range(hops):
        nf = set()
        for e in edges:
            if e["source_id"] in frontier and e["target_id"] not in seen:
                out.append(e)
                nf.add(e["target_id"])
            if e["target_id"] in frontier and e["source_id"] not in seen:
                out.append(e)
                nf.add(e["source_id"])
        seen |= nf
        frontier = nf
    return out
