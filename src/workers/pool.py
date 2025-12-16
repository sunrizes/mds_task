import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future
from interfaces.worker import WorkerPool

class ThreadWorkerPool(WorkerPool):
    def __init__(self, num_threads: int = 10):
        self.num_threads = num_threads
        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        self.submitted = 0
        self.completed = 0
        self._lock = threading.Lock()
        print(f"Worker pool initialized with {num_threads} threads")

    def submit(self, batch, batch_id: str) -> Future:
        with self._lock:
            self.submitted += 1

        future = self.executor.submit(self._process_batch, batch, batch_id)
        future.add_done_callback(lambda f: self._on_complete(batch_id, f))
        return future

    def shutdown(self, wait: bool = True):
        print(f"Shutting down worker pool (wait={wait})")
        self.executor.shutdown(wait=wait)
        print(f"Worker pool shutdown. Processed {self.completed}/{self.submitted} batches")

    def get_stats(self) -> dict:
        with self._lock:
            return {
                "submitted": self.submitted,
                "completed": self.completed,
                "pending": self.submitted - self.completed
            }

    def _process_batch(self, batch, batch_id: str):
        print(f"Processing {batch_id} with {len(batch)} items")

        time.sleep(0.1)

        result = {
            "batch_id": batch_id,
            "item_count": len(batch),
            "status": "processed"
        }

        if hasattr(batch, "current_size"):
            result["total_bytes"] = batch.current_size
            result["total_mb"] = round(batch.current_size / (1024 * 1024), 2)
        elif hasattr(batch.items[0] if batch.items else None, "timestamp"):
            if batch.items:
                time_span = batch.items[-1].timestamp - batch.items[0].timestamp
                result["time_span_seconds"] = round(time_span, 2)

        print(f"Completed {batch_id}: {result}")
        return result

    def _on_complete(self, batch_id: str, future: Future):
        with self._lock:
            self.completed += 1

        try:
            exception = future.exception()
            if exception:
                print(f"Batch {batch_id} failed: {exception}")
        except Exception as e:
            print(f"Error in completion callback: {e}")