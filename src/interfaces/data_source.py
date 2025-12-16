import time
from abc import ABC, abstractmethod
from typing import Any, Iterator

class DataSource(ABC):
    @abstractmethod
    def get_data(self) -> Iterator[Any]:
        pass

class Message:
    def __init__(self, content: Any, timestamp: float = None):
        self.content = content
        self.timestamp = timestamp or time.time()

    def __repr__(self):
        return f"Message({self.content}, {self.timestamp})"

class File:
    def __init__(self, name: str, size: int, content: Any = None):
        self.name = name
        self.size = size
        self.content = content or f"Content of {name}"

    def __repr__(self):
        return f"File({self.name}, {self.size} bytes)"