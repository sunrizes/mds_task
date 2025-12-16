import random
from typing import Iterator
from src.interfaces.data_source import DataSource, File

class ExponentialFileSource(DataSource):
    def __init__(self, num_files: int = 100, mean_size_mb: float = 5.0):
        self.num_files = num_files
        self.mean_size_mb = mean_size_mb
        self.mean_size_bytes = mean_size_mb * 1024 * 1024

    def get_data(self) -> Iterator[File]:
        for i in range(self.num_files):
            size = int(random.expovariate(1.0 / self.mean_size_bytes))
            size = max(1, size)
            yield File(name=f"file_{i+1:04d}.dat", size=size)

class MockFileSource(DataSource):
    def __init__(self, files):
        self.files = files

    def get_data(self) -> Iterator[File]:
        for file in self.files:
            yield file
