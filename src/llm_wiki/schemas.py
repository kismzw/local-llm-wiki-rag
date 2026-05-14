from __future__ import annotations

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    id: str
    path: str
    source_type: str
    title: str | None = None
    created_at: str | None = None
    modified_at: str | None = None
    content_hash: str
    metadata: dict = Field(default_factory=dict)


class SourceChunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    text: str
    source_path: str
    page: int | None = None
    section: str | None = None
    start_char: int | None = None
    end_char: int | None = None
    token_count: int
    content_hash: str
    metadata: dict = Field(default_factory=dict)


class WikiPage(BaseModel):
    id: str
    path: str
    title: str
    page_type: str
    status: str
    sources: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    related_pages: list[str] = Field(default_factory=list)
    confidence: str
    reviewed: bool
    content_hash: str


class Claim(BaseModel):
    id: str
    text: str
    claim_type: str
    source_chunk_ids: list[str] = Field(default_factory=list)
    wiki_page_ids: list[str] = Field(default_factory=list)
    confidence: str
    support_status: str
    metadata: dict = Field(default_factory=dict)


class Entity(BaseModel):
    id: str
    name: str
    entity_type: str
    aliases: list[str] = Field(default_factory=list)
    description: str | None = None
    source_chunk_ids: list[str] = Field(default_factory=list)


class GraphEdge(BaseModel):
    id: str
    source_id: str
    target_id: str
    relation: str
    confidence: str
    source_chunk_ids: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class RetrievalResult(BaseModel):
    id: str
    text: str
    source_type: str
    score: float
    path: str | None = None
    source_chunk_ids: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
