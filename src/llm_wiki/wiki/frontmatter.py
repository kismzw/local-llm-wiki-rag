from __future__ import annotations

from datetime import date


def build_frontmatter(title: str, page_type: str, source_id: str, source_chunks: list[str]) -> str:
    today = date.today().isoformat()
    lines = [
        "---",
        f"title: {title}",
        f"type: {page_type}",
        "status: draft",
        f"created: {today}",
        f"updated: {today}",
        "sources:",
        f"  - {source_id}",
        "source_chunks:",
    ]
    uniq_chunks = list(dict.fromkeys(source_chunks))
    lines.extend([f"  - {c}" for c in uniq_chunks[:30]])
    lines.extend([
        "entities:",
        "related:",
        "confidence: medium",
        "reviewed: false",
        "---",
    ])
    return "\n".join(lines)
