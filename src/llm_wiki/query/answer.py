from __future__ import annotations

from llm_wiki.schemas import RetrievalResult


def generate_answer(query: str, results: list[RetrievalResult]) -> str:
    if not results:
        return "Insufficient evidence found in local wiki and source chunks."
    lines = [f"Question: {query}", "", "Answer:"]
    top = results[:3]
    for r in top:
        cid = r.source_chunk_ids[0] if r.source_chunk_ids else r.id
        lines.append(f"- {r.text[:220]} [{cid}]")
    return "\n".join(lines)


def generate_answer_ja_with_citations(query: str, results: list[RetrievalResult], llm_client: object | None = None) -> str:
    if not results:
        return "十分な根拠が見つかりませんでした。"
    if llm_client is None:
        return generate_answer(query, results)

    top = results[:8]
    context_lines = []
    for r in top:
        cid = r.source_chunk_ids[0] if r.source_chunk_ids else r.id
        context_lines.append(f"[{cid}] {r.text[:900]}")
    context = "\n".join(context_lines)

    prompt = (
        "以下の根拠チャンクだけを使って、日本語で簡潔に回答してください。\n"
        "ルール:\n"
        "- 断定は根拠がある場合のみ。\n"
        "- 箇条書き2-5行。\n"
        "- 各行の末尾に必ずチャンクID引用を付ける（例: [src_xxx_0001]）。\n"
        "- 根拠不十分ならその旨を明記。\n\n"
        f"質問: {query}\n\n"
        f"根拠チャンク:\n{context}\n"
    )
    try:
        out = llm_client.generate(prompt).strip()
        if out:
            return f"Question: {query}\n\nAnswer:\n{out}"
    except Exception:
        pass
    return generate_answer(query, results)
