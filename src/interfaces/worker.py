from abc import ABC, abstractmethod
from concurrent.futures import Future
from typing import Any

class WorkerPool(ABC):
    @abstractmethod
    def submit(self, batch: Any, batch_id: str) -> Future:
        pass

    @abstractmethod
    def shutdown(self, wait: bool = True) -> None:
        pass

    @abstractmethod
    def get_stats(self) -> dict:
        pass