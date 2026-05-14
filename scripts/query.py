from __future__ import annotations

import typer
from llm_wiki.config import load_settings
from llm_wiki.utils.io import read_jsonl
from llm_wiki.schemas import RetrievalResult
from llm_wiki.retrieval.pipeline import classify_query
from llm_wiki.reranking.rerank import rerank
from llm_wiki.query.answer import generate_answer_ja_with_citations
from llm_wiki.verification.verifier import verify_answer
from llm_wiki.indexing.bm25 import build_bm25, search_bm25
from llm_wiki.llm.ollama import OllamaClient

app = typer.Typer()


def _is_this_paper_query(query: str) -> bool:
    q = query.lower()
    return "この論文" in query or "this paper" in q


def _latest_paper_doc_id(sources: list[dict]) -> str | None:
    papers = [s for s in sources if s.get("source_type") == "paper"]
    if not papers:
        return None
    papers.sort(key=lambda x: x.get("modified_at") or "", reverse=True)
    return papers[0].get("id")


@app.command()
def main(query: str) -> None:
    s = load_settings()
    root = s.root_path
    _qt = classify_query(query)
    chunks = read_jsonl(root / "metadata/chunks.jsonl")
    sources = read_jsonl(root / "metadata/sources.jsonl")

    scoped_chunks = chunks
    target_doc_id = None
    if _is_this_paper_query(query):
        target_doc_id = _latest_paper_doc_id(sources)
        if target_doc_id:
            scoped_chunks = [c for c in chunks if c.get("document_id") == target_doc_id]
            print(f"[query] scope: latest paper {target_doc_id} ({len(scoped_chunks)} chunks)")

    if not scoped_chunks:
        scoped_chunks = chunks

    corpus = [{"id": c["id"], "text": c["text"], "source_path": c.get("source_path"), "document_id": c.get("document_id")} for c in scoped_chunks]
    bm25 = build_bm25([x["text"] for x in corpus])
    bm25_hits = search_bm25(bm25, corpus, query, top_k=max(s.retrieval.source_top_k, 20))
    if not bm25_hits and target_doc_id:
        bm25_hits = corpus[: max(s.retrieval.source_top_k, 20)]

    results = [
        RetrievalResult(
            id=c["id"],
            text=c["text"],
            source_type="source_chunk",
            score=float(c.get("score", 0.0)),
            path=c.get("source_path"),
            source_chunk_ids=[c["id"]],
            metadata={"document_id": c.get("document_id")},
        )
        for c in bm25_hits
    ]
    ranked = rerank(query, results, top_k=s.retrieval.rerank_top_k)
    llm_client = OllamaClient(model=s.llm.model) if s.llm.backend == "ollama" else None
    ans = generate_answer_ja_with_citations(query, ranked, llm_client=llm_client)
    v = verify_answer(ans, [r.text for r in ranked])
    print(ans)
    print("\nVerification:", v["overall_status"])


if __name__ == "__main__":
    app()
