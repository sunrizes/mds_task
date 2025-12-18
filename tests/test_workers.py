import unittest
import time
from src.interfaces.data_source import Message
from src.messages.batching import TimeBatch
from src.files.bucketing import FileBucket
from src.interfaces.data_source import File
from src.workers.pool import ThreadWorkerPool


class TestWorkerPool(unittest.TestCase):
    def test_worker_pool_creation(self):
        pool = ThreadWorkerPool(num_threads=5)
        self.assertEqual(pool.num_threads, 5)
        pool.shutdown()

    def test_submit_message_batch(self):
        pool = ThreadWorkerPool(num_threads=2)
        
        batch = TimeBatch(window_seconds=1.0)
        batch.add(Message("test"))
        batch.ready = True
        
        future = pool.submit(batch, "test_batch")
        result = future.result(timeout=5.0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["batch_id"], "test_batch")
        self.assertEqual(result["status"], "processed")
        
        pool.shutdown()

    def test_submit_file_bucket(self):
        pool = ThreadWorkerPool(num_threads=2)
        
        bucket = FileBucket(target_size_mb=10.0)
        bucket.add(File("test.txt", 1024))
        
        future = pool.submit(bucket, "test_bucket")
        result = future.result(timeout=5.0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["batch_id"], "test_bucket")
        self.assertEqual(result["status"], "processed")
        
        pool.shutdown()

    def test_pool_statistics(self):
        pool = ThreadWorkerPool(num_threads=2)

        futures = []
        for i in range(5):
            batch = TimeBatch(window_seconds=1.0)
            batch.add(Message(f"msg {i}"))
            batch.ready = True
            futures.append(pool.submit(batch, f"batch_{i}"))
        
        for future in futures:
            future.result(timeout=5.0)
        
        stats = pool.get_stats()
        self.assertEqual(stats["submitted"], 5)
        self.assertEqual(stats["completed"], 5)
        self.assertEqual(stats["pending"], 0)
        
        pool.shutdown()

    def test_parallel_processing(self):
        pool = ThreadWorkerPool(num_threads=3)
        
        start_time = time.time()
        futures = []

        for i in range(6):
            batch = TimeBatch(window_seconds=1.0)
            batch.add(Message(f"msg {i}"))
            batch.ready = True
            futures.append(pool.submit(batch, f"batch_{i}"))
        
        for future in futures:
            future.result(timeout=5.0)
        
        elapsed = time.time() - start_time
        
        self.assertLess(elapsed, 1.0)
        
        pool.shutdown()


if __name__ == "__main__":
    unittest.main()