from __future__ import annotations

from llm_wiki.schemas import RetrievalResult


def rerank(query: str, results: list[RetrievalResult], top_k: int) -> list[RetrievalResult]:
    q = set(query.lower().split())
    rescored = []
    for r in results:
        bonus = len(q.intersection(set(r.text.lower().split()))) / 10.0
        rescored.append((r.score + bonus, r))
    rescored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in rescored[:top_k]]
