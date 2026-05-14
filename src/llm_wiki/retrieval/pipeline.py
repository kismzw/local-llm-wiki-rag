from __future__ import annotations

from llm_wiki.schemas import RetrievalResult


def classify_query(query: str) -> str:
    q = query.lower()
    if "compare" in q:
        return "experiment_comparison"
    if "how" in q or "relation" in q:
        return "multi_hop_reasoning"
    if "summary" in q:
        return "broad_summary"
    return "exact_lookup"


def merge_results(*groups: list[RetrievalResult]) -> list[RetrievalResult]:
    seen = set()
    out = []
    for g in groups:
        for r in g:
            key = (r.id, r.source_type)
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
    return out
