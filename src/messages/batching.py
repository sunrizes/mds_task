import time
import threading
from typing import List
from interfaces.data_source import Message

class TimeBatch:
    def __init__(self, window_seconds: float = 300.0):
        self.window_seconds = window_seconds
        self.items: List[Message] = []
        self.start_time = None
        self.ready = False
        self._lock = threading.Lock()

    def add(self, message: Message) -> bool:
        with self._lock:
            if self.ready:
                return False

            if not self.start_time:
                self.start_time = time.time()

            self.items.append(message)

            if time.time() - self.start_time >= self.window_seconds:
                self.ready = True

            return True

    def is_ready(self) -> bool:
        with self._lock:
            if self.ready:
                return True

            if not self.start_time:
                return False

            if time.time() - self.start_time >= self.window_seconds:
                self.ready = True

            return self.ready

    def __len__(self):
        return len(self.items)