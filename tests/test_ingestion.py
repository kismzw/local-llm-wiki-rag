from pathlib import Path
from llm_wiki.ingestion.registry import register_source


def test_duplicate_detected(tmp_path: Path):
    p = tmp_path / "a.md"
    p.write_text("hello", encoding="utf-8")
    meta = tmp_path / "sources.jsonl"
    a = register_source(p, "meeting", meta)
    b = register_source(p, "meeting", meta)
    assert a.id == b.id


def test_unsupported_type(tmp_path: Path):
    p = tmp_path / "a.exe"
    p.write_text("x", encoding="utf-8")
    meta = tmp_path / "sources.jsonl"
    try:
        register_source(p, "misc", meta)
        assert False
    except ValueError:
        assert True
