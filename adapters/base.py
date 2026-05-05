from abc import ABC, abstractmethod
from typing import List, Dict, Generator

class ModelAdapter(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Human-readable model name."""
        ...

    @abstractmethod
    def call(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Call the model and yield response text chunks. Raise on error."""
        ...

    @abstractmethod
    def is_rate_limit_error(self, error: Exception) -> bool:
        """True if the exception was caused by a rate limit."""
        ...
