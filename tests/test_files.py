import unittest
from src.interfaces.data_source import File
from src.files.file import ExponentialFileSource, MockFileSource
from src.files.bucketing import FileBucket
from src.files.processor import FileProcessor
from src.workers.pool import ThreadWorkerPool

class TestFileProcessing(unittest.TestCase):
    def test_file_creation(self):
        file = File("test.txt", 1024, "content")
        self.assertEqual(file.name, "test.txt")
        self.assertEqual(file.size, 1024)
        self.assertEqual(file.content, "content")

    def test_file_bucket_basic(self):
        bucket = FileBucket(target_size_mb=10.0)

        file1 = File("file1.txt", 2 * 1024 * 1024)
        file2 = File("file2.txt", 3 * 1024 * 1024)

        self.assertTrue(bucket.add(file1))
        self.assertTrue(bucket.add(file2))
        self.assertEqual(len(bucket), 2)

    def test_file_bucket_reaches_target(self):
        bucket = FileBucket(target_size_mb=10.0)

        bucket.add(File("f1.txt", 5 * 1024 * 1024))
        bucket.add(File("f2.txt", 5 * 1024 * 1024))

        self.assertTrue(bucket.is_ready())

    def test_file_bucket_rejects_when_full(self):
        bucket = FileBucket(target_size_mb=10.0)

        bucket.add(File("f1.txt", 8 * 1024 * 1024))
        bucket.add(File("f2.txt", 2 * 1024 * 1024))
        self.assertTrue(bucket.is_ready())

        self.assertFalse(bucket.add(File("f3.txt", 1 * 1024 * 1024)))

    def test_file_bucket_accepts_first_file_even_if_large(self):
        bucket = FileBucket(target_size_mb=10.0)

        large_file = File("large.txt", 15 * 1024 * 1024)  # 15 MB
        self.assertTrue(bucket.add(large_file))
        self.assertEqual(len(bucket), 1)

    def test_exponential_file_source(self):
        source = ExponentialFileSource(num_files=10, mean_size_mb=5.0)
        files = list(source.get_data())

        self.assertEqual(len(files), 10)
        for file in files:
            self.assertIsInstance(file, File)
            self.assertGreater(file.size, 0)

    def test_mock_file_source(self):
        test_files = [
            File("f1.txt", 100),
            File("f2.txt", 200),
        ]
        source = MockFileSource(test_files)
        files = list(source.get_data())

        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].name, "f1.txt")
        self.assertEqual(files[1].name, "f2.txt")

    def test_file_processor(self):
        test_files = [
            File("f1.txt", 5 * 1024 * 1024),
            File("f2.txt", 6 * 1024 * 1024),
            File("f3.txt", 4 * 1024 * 1024),
        ]

        pool = ThreadWorkerPool(num_threads=2)
        source = MockFileSource(test_files)
        processor = FileProcessor(source, pool, bucket_size_mb=10.0)

        processor.process()

        stats = pool.get_stats()
        self.assertGreater(stats["submitted"], 0)

        pool.shutdown()


if __name__ == "__main__":
    unittest.main()