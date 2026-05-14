from pathlib import Path
from llm_wiki.extraction.markdown import extract_markdown
from llm_wiki.extraction.code import extract_repo


def test_markdown_preserves_heading(tmp_path: Path):
    p = tmp_path / "m.md"
    p.write_text("# Title\n\nBody", encoding="utf-8")
    out = extract_markdown(p, "doc_x")
    assert "# Title" in out["sections"][0]["text"]


def test_code_extraction_paths(tmp_path: Path):
    r = tmp_path / "repo"
    r.mkdir()
    f = r / "a.py"
    f.write_text("def main():\n    return 1\n", encoding="utf-8")
    out = extract_repo(r, "doc_r")
    assert out["files"][0]["path"] == "a.py"
