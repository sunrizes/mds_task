from typing import List
from interfaces.data_source import File

class FileBucket:
    def __init__(self, target_size_mb: float = 10.0):
        self.target_bytes = int(target_size_mb * 1024 * 1024)
        self.items: List[File] = []
        self.current_size = 0
        self.ready = False

    def add(self, file: File) -> bool:
        if self.ready:
            return False

        if self.current_size > 0 and (self.current_size + file.size) > self.target_bytes:
            self.ready = True
            return False

        self.items.append(file)
        self.current_size += file.size

        if self.current_size >= self.target_bytes:
            self.ready = True

        return True

    def is_ready(self) -> bool:
        return self.ready

    def __len__(self):
        return len(self.items)
