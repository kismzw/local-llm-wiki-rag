from __future__ import annotations

from pathlib import Path
from llm_wiki.extraction.code import extract_repo
from llm_wiki.extraction.markdown import extract_markdown
from llm_wiki.extraction.pdf import extract_pdf
from llm_wiki.extraction.text import extract_text


def extract(path: Path, document_id: str) -> dict:
    if path.is_dir():
        return extract_repo(path, document_id)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path, document_id)
    if suffix == ".md":
        return extract_markdown(path, document_id)
    return extract_text(path, document_id)
