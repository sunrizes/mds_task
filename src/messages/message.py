import time
import random
from typing import Iterator
from data_source import DataSource, Message

class MessageSource(DataSource):
    def __init__(self, rate_per_minute: float = 10.0, duration_minutes: float = None):
        self.rate_per_minute = rate_per_minute
        self.duration_minutes = duration_minutes
        self.lambda_per_second = rate_per_minute / 60.0

    def get_data(self) -> Iterator[Message]:
        start_time = time.time()
        count = 0

        while True:
            if self.duration_minutes:
                elapsed = (time.time() - start_time) / 60.0
                if elapsed >= self.duration_minutes:
                    break

            time.sleep(random.expovariate(self.lambda_per_second))

            count += 1
            yield Message(content=f"Message #{count}", timestamp=time.time())
