from pathlib import Path
from llm_wiki.schemas import SourceDocument, SourceChunk
from llm_wiki.wiki.generator import generate_page


def test_page_has_required_sections(tmp_path: Path):
    d = SourceDocument(id="doc_a", path="raw/a.md", source_type="paper", content_hash="x")
    c = [SourceChunk(id="src_a_0001", document_id="doc_a", chunk_index=0, text="some text", source_path="raw/a.md", token_count=2, content_hash="h")]
    out = generate_page(d, c, tmp_path)
    t = out.read_text(encoding="utf-8")
    assert "---" in t
    assert "## Sources" in t
    assert "## Needs Review" in t
    assert "# Paper:" in t
