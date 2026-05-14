from __future__ import annotations

from llm_wiki.schemas import Claim, SourceChunk


SUPPORT = {"supported", "partially_supported", "unsupported", "contradicted", "needs_review"}


def extract_claims_from_chunks(chunks: list[SourceChunk], wiki_page_id: str) -> list[Claim]:
    claims = []
    idx = 1
    for c in chunks:
        sentences = [s.strip() for s in c.text.split(".") if len(s.strip().split()) >= 6]
        for s in sentences[:2]:
            claims.append(Claim(
                id=f"claim_{idx:06d}",
                text=s + ".",
                claim_type="fact",
                source_chunk_ids=[c.id],
                wiki_page_ids=[wiki_page_id],
                confidence="medium",
                support_status="supported",
                metadata={},
            ))
            idx += 1
    return claims
