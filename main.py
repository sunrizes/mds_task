import logging
import time
from messages.message import MessageSource
from messages.processor import MessageStreamProcessor
from files.file import ExponentialFileSource
from files.processor import FileProcessor
from workers.pool import ThreadWorkerPool

class DataProcessingSystem:
    def __init__(self, num_threads=10, message_rate=10.0, window_seconds=300.0,
                 num_files=100, mean_file_mb=5.0, bucket_mb=10.0):
        print("INIT START")

        self.pool = ThreadWorkerPool(num_threads)

        msg_source = MessageSource(message_rate)
        self.msg_processor = MessageStreamProcessor(msg_source, self.pool, window_seconds)

        file_source = ExponentialFileSource(num_files, mean_file_mb)
        self.file_processor = FileProcessor(file_source, self.pool, bucket_mb)

        print("INIT END")

    def start(self):
        print("SYS START")
        
        self.msg_processor.start()
        
        self.file_processor.process()

    def stop(self):
        print("SYS STOP")
        
        self.msg_processor.stop()
        time.sleep(2)
        self.pool.shutdown(wait=True)
        
        stats = self.pool.get_stats()
        print(f"Final stats: {stats}")

    def get_stats(self):
        return self.pool.get_stats()


def run_demo():
    print("DEMO START")

    system = DataProcessingSystem(
        num_threads=10,
        message_rate=60.0,
        window_seconds=5.0,
        num_files=20,
        mean_file_mb=3.0,
        bucket_mb=10.0
    )

    try:
        system.start()
        time.sleep(15)
        stats = system.get_stats()
        print(f"Stats: {stats}")

    finally:
        system.stop()

    print("DEMO END")

if __name__ == "__main__":
    run_demo()