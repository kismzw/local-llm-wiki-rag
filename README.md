# local-llm-wiki-rag

Local-first source-grounded Markdown Wiki + RAG system.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python scripts/ingest.py raw/meetings/sample.md --type meeting
python scripts/build_wiki.py --source <doc_id>
python scripts/build_graph.py
python scripts/build_indexes.py
python scripts/query.py "What is this project about?"
```
