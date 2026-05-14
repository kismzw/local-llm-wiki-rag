from __future__ import annotations

from pathlib import Path
import ast


def _symbols(py_text: str) -> list[str]:
    try:
        t = ast.parse(py_text)
    except SyntaxError:
        return []
    out = []
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append(n.name)
    return sorted(set(out))


def extract_repo(path: Path, document_id: str) -> dict:
    files = []
    tree_lines = []
    for p in sorted(path.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(path)
        tree_lines.append(str(rel))
        if p.suffix.lower() == ".py":
            txt = p.read_text(encoding="utf-8", errors="ignore")
            files.append({"path": str(rel), "language": "python", "symbols": _symbols(txt), "text": txt})
    return {"document_id": document_id, "repo_name": path.name, "file_tree": "\n".join(tree_lines), "files": files}
