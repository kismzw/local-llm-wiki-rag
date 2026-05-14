class LLMClient:
    def generate(self, prompt: str, system: str | None = None, **kwargs) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, schema: dict | None = None, **kwargs) -> dict:
        raise NotImplementedError
