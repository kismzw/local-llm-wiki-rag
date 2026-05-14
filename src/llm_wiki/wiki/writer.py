from pathlib import Path


def write_page(path: Path, content: str, force: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise FileExistsError(f"Refusing overwrite without force: {path}")
    path.write_text(content, encoding="utf-8")
