import anthropic
from typing import List, Dict, Generator
from .base import ModelAdapter
from config import ANTHROPIC_API_KEY

class ClaudeAdapter(ModelAdapter):
    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def get_name(self) -> str:
        return f"Claude ({self.model_name})"

    def call(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        system_msg = ""
        anthropic_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg += m["content"] + "\n"
            else:
                anthropic_messages.append({"role": m["role"], "content": m["content"]})

        system_msg = system_msg.strip() or None

        try:
            with self.client.messages.stream(
                model=self.model_name,
                max_tokens=4096,
                system=system_msg,
                messages=anthropic_messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except anthropic.RateLimitError:
            raise

    def is_rate_limit_error(self, error: Exception) -> bool:
        return isinstance(error, anthropic.RateLimitError)
