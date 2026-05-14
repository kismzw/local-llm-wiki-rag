from llm_wiki.chunking.chunker import chunk_extracted


def test_deterministic_ids():
    e = {"document_id": "doc_abcd1234", "sections": [{"section": "s", "text": "a b c d e f g h i j"}]}
    c1 = chunk_extracted(e, "raw/x.md", 3, 1)
    c2 = chunk_extracted(e, "raw/x.md", 3, 1)
    assert [x.id for x in c1] == [x.id for x in c2]
    assert all(x.source_path == "raw/x.md" for x in c1)
