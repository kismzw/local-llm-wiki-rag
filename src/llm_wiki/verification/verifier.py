from __future__ import annotations


def verify_answer(answer: str, source_texts: list[str]) -> dict:
    claims = [c.strip() for c in answer.split(".") if c.strip()]
    out = []
    for c in claims:
        status = "unsupported"
        for s in source_texts:
            overlap = len(set(c.lower().split()).intersection(set(s.lower().split())))
            if overlap >= 4:
                status = "supported"
                break
            if overlap >= 2:
                status = "partially_supported"
        out.append({"text": c, "status": status, "supporting_sources": [], "notes": "lexical heuristic"})
    overall = "pass" if all(c["status"] != "unsupported" for c in out) else "fail"
    return {"claims": out, "overall_status": overall}
