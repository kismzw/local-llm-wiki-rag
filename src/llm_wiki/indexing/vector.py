from __future__ import annotations

import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_index(items: list[dict], text_key: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    texts = [i.get(text_key, "") for i in items]
    vec = TfidfVectorizer()
    X = vec.fit_transform(texts) if texts else None
    meta = {"ids": [i.get("id") for i in items], "texts": texts, "vocab": vec.vocabulary_}
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    if X is not None:
        (out_dir / "matrix_shape.txt").write_text(str(X.shape), encoding="utf-8")
