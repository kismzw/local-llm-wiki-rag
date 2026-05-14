from __future__ import annotations

import typer
from llm_wiki.verification.verifier import verify_answer

app = typer.Typer()


@app.command()
def main(answer: str, source: str) -> None:
    print(verify_answer(answer, [source]))


if __name__ == "__main__":
    app()
