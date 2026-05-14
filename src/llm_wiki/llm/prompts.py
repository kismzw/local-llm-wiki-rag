from pathlib import Path


def load_prompt(name: str, root: Path) -> str:
    path = root / "prompts" / f"{name}.md"
    return path.read_text(encoding="utf-8")
