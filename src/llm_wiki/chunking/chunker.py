from __future__ import annotations

from llm_wiki.schemas import SourceChunk
from llm_wiki.utils.hashing import sha256_bytes
from llm_wiki.utils.text import estimate_tokens


def _split_words(text: str, size: int, overlap: int) -> list[tuple[str, int, int]]:
    words = text.split()
    if not words:
        return []
    out = []
    start = 0
    while start < len(words):
        end = min(len(words), start + size)
        chunk_words = words[start:end]
        out.append((" ".join(chunk_words), start, end))
        if end == len(words):
            break
        start = max(start + 1, end - overlap)
    return out


def chunk_extracted(extracted: dict, source_path: str, target_tokens: int, overlap_tokens: int) -> list[SourceChunk]:
    doc_id = extracted["document_id"]
    doc_hash = doc_id.replace("doc_", "")
    chunks: list[SourceChunk] = []
    idx = 0
    if "pages" in extracted:
        units = [{"text": p.get("text", ""), "page": p.get("page"), "section": None} for p in extracted["pages"]]
    elif "files" in extracted:
        units = [{"text": f.get("text", ""), "page": None, "section": f.get("path")} for f in extracted["files"]]
    else:
        units = [{"text": s.get("text", ""), "page": None, "section": s.get("section")} for s in extracted.get("sections", [])]

    for unit in units:
        for text, s, e in _split_words(unit["text"], target_tokens, overlap_tokens):
            cid = f"src_{doc_hash}_{idx:04d}"
            chunks.append(SourceChunk(
                id=cid,
                document_id=doc_id,
                chunk_index=idx,
                text=text,
                source_path=source_path,
                page=unit["page"],
                section=unit["section"],
                start_char=s,
                end_char=e,
                token_count=estimate_tokens(text),
                content_hash=sha256_bytes(text.encode("utf-8")),
                metadata={},
            ))
            idx += 1
    return chunks
