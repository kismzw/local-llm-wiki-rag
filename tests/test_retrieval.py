from llm_wiki.indexing.bm25 import build_bm25, search_bm25
from llm_wiki.retrieval.pipeline import merge_results
from llm_wiki.schemas import RetrievalResult


def test_bm25_exact_term():
    corpus = [{"id": "1", "text": "integrated gradients method"}, {"id": "2", "text": "random text"}]
    idx = build_bm25([x["text"] for x in corpus])
    out = search_bm25(idx, corpus, "integrated")
    assert out and out[0]["id"] == "1"


def test_merge_dedup():
    r1 = RetrievalResult(id="a", text="x", source_type="s", score=1.0)
    r2 = RetrievalResult(id="a", text="x", source_type="s", score=0.9)
    assert len(merge_results([r1], [r2])) == 1
