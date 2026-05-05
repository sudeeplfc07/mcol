import openai
from typing import List, Dict, Generator
from .base import ModelAdapter
from config import DEEPSEEK_API_KEY

class DeepSeekAdapter(ModelAdapter):
    def __init__(self, model_name: str = "deepseek-chat"):
        self.model_name = model_name
        self.client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )

    def get_name(self) -> str:
        return f"DeepSeek ({self.model_name})"

    def call(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                max_tokens=4096,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except openai.RateLimitError:
            raise
        except openai.APIStatusError as e:
            if e.status_code == 429:
                raise openai.RateLimitError("Rate limited", response=e.response, body=e.body)
            else:
                raise

    def is_rate_limit_error(self, error: Exception) -> bool:
        return isinstance(error, openai.RateLimitError)
