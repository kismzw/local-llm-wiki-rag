from __future__ import annotations


def build_summaries(chunks: list[dict]) -> list[dict]:
    out = []
    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c["document_id"], []).append(c)
    for doc_id, cs in by_doc.items():
        joined = " ".join(c["text"] for c in cs)[:1200]
        out.append({"id": f"summary_{doc_id}_l2", "level": 2, "source_ids": [c["id"] for c in cs], "title": f"{doc_id} summary", "text": joined, "generated_by": "heuristic"})
    return out
