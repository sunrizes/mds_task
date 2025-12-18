from src.interfaces.data_source import DataSource
from src.files.bucketing import FileBucket
from src.interfaces.worker import WorkerPool

class FileProcessor:
    def __init__(self, data_source: DataSource, worker_pool: WorkerPool, 
                 bucket_size_mb: float = 10.0):
        self.data_source = data_source
        self.worker_pool = worker_pool
        self.bucket_size_mb = bucket_size_mb
        self.bucket_counter = 0

    def process(self):
        current_bucket = FileBucket(self.bucket_size_mb)
        self.bucket_counter += 1
        bucket_id = f"file_bucket_{self.bucket_counter}"

        print("File processor started")

        try:
            for file in self.data_source.get_data():
                if not current_bucket.add(file):
                    self.worker_pool.submit(current_bucket, bucket_id)
                    
                    current_bucket = FileBucket(self.bucket_size_mb)
                    self.bucket_counter += 1
                    bucket_id = f"file_bucket_{self.bucket_counter}"
                    
                    current_bucket.add(file)

        except Exception as e:
            print(f"Error processing files: {e}")
        finally:
            if len(current_bucket) > 0:
                self.worker_pool.submit(current_bucket, bucket_id)

        print("File processor completed")