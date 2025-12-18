import threading
from src.interfaces.data_source import DataSource
from src.messages.batching import TimeBatch
from src.interfaces.worker import WorkerPool

class MessageStreamProcessor:
    def __init__(self, data_source: DataSource, worker_pool: WorkerPool,
                 window_seconds: float = 300.0):
        self.data_source = data_source
        self.worker_pool = worker_pool
        self.window_seconds = window_seconds
        self.running = False
        self.thread = None
        self.batch_counter = 0

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._process, daemon=True)
        self.thread.start()
        print("Message processor started")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        print("Message processor stopped")

    def _process(self):
        current_batch = TimeBatch(self.window_seconds)
        self.batch_counter += 1
        batch_id = f"msg_batch_{self.batch_counter}"

        try:
            for message in self.data_source.get_data():
                if not self.running:
                    break

                if current_batch.is_ready():
                    self.worker_pool.submit(current_batch, batch_id)
                    current_batch = TimeBatch(self.window_seconds)
                    self.batch_counter += 1
                    batch_id = f"msg_batch_{self.batch_counter}"

                current_batch.add(message)

        except Exception as e:
            print(f"Error processing messages: {e}")
        finally:
            if len(current_batch) > 0:
                self.worker_pool.submit(current_batch, batch_id)