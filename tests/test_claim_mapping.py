from llm_wiki.schemas import SourceChunk
from llm_wiki.claims.extractor import extract_claims_from_chunks


def test_claims_have_source_ids():
    cs = [SourceChunk(id="src_x_0001", document_id="doc_x", chunk_index=0, text="MICA uses co attention between features for prediction outcomes.", source_path="raw/x", token_count=10, content_hash="h")]
    claims = extract_claims_from_chunks(cs, "wiki_x")
    assert claims
    assert claims[0].source_chunk_ids
