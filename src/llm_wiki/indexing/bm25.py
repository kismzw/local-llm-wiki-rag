from __future__ import annotations

from rank_bm25 import BM25Okapi


def build_bm25(corpus: list[str]) -> BM25Okapi:
    tokenized = [doc.split() for doc in corpus]
    return BM25Okapi(tokenized)


def search_bm25(index: BM25Okapi, corpus: list[dict], query: str, top_k: int = 10) -> list[dict]:
    scores = index.get_scores(query.split())
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [{**corpus[i], "score": float(s)} for i, s in ranked]
