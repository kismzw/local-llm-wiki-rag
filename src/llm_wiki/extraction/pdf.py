from __future__ import annotations

from pathlib import Path
from pypdf import PdfReader


def extract_pdf(path: Path, document_id: str) -> dict:
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        pages.append({"page": i, "text": page.extract_text() or "", "tables": [], "metadata": {}})
    return {"document_id": document_id, "pages": pages}
