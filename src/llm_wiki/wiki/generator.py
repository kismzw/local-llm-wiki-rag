from __future__ import annotations

from pathlib import Path
from llm_wiki.schemas import SourceDocument, SourceChunk
from llm_wiki.utils.text import slugify
from llm_wiki.wiki.frontmatter import build_frontmatter
from llm_wiki.wiki.templates import TEMPLATES


def _snippets(chunks: list[SourceChunk], n: int = 3, max_chars: int = 280) -> list[str]:
    out: list[str] = []
    seen = set()
    for c in chunks:
        t = " ".join(c.text.split())
        if not t:
            continue
        s = t[:max_chars]
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= n:
            break
    return out


def _source_lines(chunks: list[SourceChunk], max_items: int = 10) -> list[str]:
    seen = set()
    lines: list[str] = []
    for c in chunks:
        if c.id in seen:
            continue
        seen.add(c.id)
        page_part = f", page {c.page}" if c.page is not None else ""
        section_part = f", section {c.section}" if c.section else ""
        lines.append(f"- {c.id}: `{c.source_path}`{page_part}{section_part}, chunk {c.chunk_index}")
        if len(lines) >= max_items:
            break
    return lines


def _chunk_context(chunks: list[SourceChunk], max_chunks: int = 12, max_chars: int = 900) -> str:
    lines: list[str] = []
    for c in chunks[:max_chunks]:
        text = " ".join(c.text.split())[:max_chars]
        lines.append(f"[{c.id}] {text}")
    return "\n".join(lines)


def _fill_section_with_llm(section: str, title: str, context: str, llm_client: object | None) -> str:
    if llm_client is None:
        return ""
    prompt = (
        f"You are writing section '{section}' for wiki page of paper '{title}'.\n"
        "Use only the provided source chunks.\n"
        "Return 2-5 concise bullet points.\n"
        "Each bullet must end with one or more chunk citations like [src_xxx_0001].\n"
        "If evidence is insufficient, return a bullet: '- Needs review: insufficient evidence [src_...]'.\n\n"
        f"Source chunks:\n{context}\n"
    )
    try:
        out = llm_client.generate(prompt)
        return out.strip()
    except Exception:
        return ""


def _ensure_non_empty_sections(body: str, sections: list[str], fallback_citation: str) -> str:
    for section in sections:
        marker = f"## {section}\n\n"
        if marker in body:
            body = body.replace(
                marker,
                f"## {section}\n\n- Needs review: section not confidently extracted yet [{fallback_citation}].\n\n",
            )
    return body


def generate_page(
    doc: SourceDocument,
    chunks: list[SourceChunk],
    wiki_root: Path,
    llm_client: object | None = None,
    log_fn: object | None = None,
) -> Path:
    ptype = "paper" if doc.source_type == "paper" else "meeting" if doc.source_type == "meeting" else "repo"
    sub = "papers" if ptype == "paper" else "projects" if ptype == "repo" else "experiments"
    title = doc.title or doc.id
    body = TEMPLATES[ptype].format(title=title)
    uniq_chunks = list(dict.fromkeys([c.id for c in chunks]))
    cited = "\n".join(_source_lines(chunks, max_items=10))
    if ptype == "paper":
        context = _chunk_context(chunks)
        sections = [
            "One-line Summary",
            "Problem",
            "Method",
            "Architecture",
            "Loss / Objective",
            "Experiments",
            "Key Results",
            "Relevance to My Work",
            "Limitations",
            "Implementation Notes",
            "Key Claims",
        ]
        for section in sections:
            if log_fn:
                log_fn(f"[build_wiki] generating section: {section}")
            filled = _fill_section_with_llm(section, title, context, llm_client)
            if filled:
                body = body.replace(f"## {section}\n", f"## {section}\n\n{filled}\n")
                if log_fn:
                    log_fn(f"[build_wiki] done section: {section}")
            elif log_fn:
                log_fn(f"[build_wiki] fallback section: {section}")
        # Safe local fallback for when model is unavailable.
        samples = _snippets(chunks, n=4)
        if samples:
            body = body.replace("## One-line Summary\n\n", f"## One-line Summary\n\n- {samples[0]} [{uniq_chunks[0]}]\n\n")
        if len(samples) > 1:
            body = body.replace("## Method\n\n", f"## Method\n\n- {samples[1]} [{uniq_chunks[min(1, len(uniq_chunks)-1)]}]\n\n")
        if len(samples) > 2:
            body = body.replace("## Key Results\n\n", f"## Key Results\n\n- {samples[2]} [{uniq_chunks[min(2, len(uniq_chunks)-1)]}]\n\n")
        if len(samples) > 3:
            body = body.replace("## Limitations\n\n", f"## Limitations\n\n- Needs review: {samples[3]} [{uniq_chunks[min(3, len(uniq_chunks)-1)]}]\n\n")
        body = _ensure_non_empty_sections(body, sections, uniq_chunks[0] if uniq_chunks else "src_unknown_0000")
    body = body.replace("## Sources\n", f"## Sources\n\n- `{doc.path}`\n{cited}\n")
    fm = build_frontmatter(title=title, page_type=ptype, source_id=doc.id, source_chunks=uniq_chunks)
    out = wiki_root / sub / f"{slugify(title)}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"{fm}\n\n{body}", encoding="utf-8")
    return out
