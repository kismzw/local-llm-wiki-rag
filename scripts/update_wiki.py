from __future__ import annotations

import typer
from pathlib import Path
from llm_wiki.config import load_settings
from llm_wiki.wiki.updater import patch_update

app = typer.Typer()


@app.command()
def main(source: str = typer.Option(..., "--source"), target: str = typer.Option(..., "--target")) -> None:
    _ = source
    s = load_settings()
    patch_update(s.root_path / target, f"Potential updates from {source}; review required.")
    print(target)


if __name__ == "__main__":
    app()
