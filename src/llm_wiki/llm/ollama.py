from __future__ import annotations

import json
import httpx
from llm_wiki.llm.base import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, model: str, base_url: str = "http://localhost:11434") -> None:
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, system: str | None = None, **kwargs) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        resp = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def generate_json(self, prompt: str, schema: dict | None = None, **kwargs) -> dict:
        txt = self.generate(prompt, **kwargs)
        try:
            return json.loads(txt)
        except json.JSONDecodeError:
            return {"raw": txt}
