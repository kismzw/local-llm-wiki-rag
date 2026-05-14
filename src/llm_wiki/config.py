from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field
import yaml


class ProjectCfg(BaseModel):
    root: str = "."


class LLMCfg(BaseModel):
    backend: str = "ollama"
    model: str = "qwen3:14b"
    temperature: float = 0.1
    max_tokens: int = 4096
    context_window: int = 32768


class EmbeddingCfg(BaseModel):
    backend: str = "sentence_transformers"
    model: str = "BAAI/bge-m3"
    batch_size: int = 16


class RerankerCfg(BaseModel):
    backend: str = "sentence_transformers"
    model: str = "BAAI/bge-reranker-v2-m3"
    enabled: bool = True


class ChunkingCfg(BaseModel):
    target_tokens: int = 800
    overlap_tokens: int = 120
    preserve_sections: bool = True


class RetrievalCfg(BaseModel):
    wiki_top_k: int = 10
    source_top_k: int = 20
    bm25_top_k: int = 20
    rerank_top_k: int = 12
    graph_hops: int = 2


class VerificationCfg(BaseModel):
    enabled: bool = True
    min_support_score: float = 0.65


class StorageCfg(BaseModel):
    sqlite_path: str = "metadata/llm_wiki.sqlite"
    vector_backend: str = "faiss"
    graph_backend: str = "sqlite"


class Settings(BaseModel):
    project: ProjectCfg = Field(default_factory=ProjectCfg)
    llm: LLMCfg = Field(default_factory=LLMCfg)
    embedding: EmbeddingCfg = Field(default_factory=EmbeddingCfg)
    reranker: RerankerCfg = Field(default_factory=RerankerCfg)
    chunking: ChunkingCfg = Field(default_factory=ChunkingCfg)
    retrieval: RetrievalCfg = Field(default_factory=RetrievalCfg)
    verification: VerificationCfg = Field(default_factory=VerificationCfg)
    storage: StorageCfg = Field(default_factory=StorageCfg)
    root_path: Path = Path(".")


def load_settings(config_path: str | Path = "config.yaml") -> Settings:
    p = Path(config_path)
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}
    settings = Settings(**(data or {}))
    settings.root_path = p.resolve().parent
    return settings
