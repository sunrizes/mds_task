import unittest
import time
from src.interfaces.data_source import Message
from src.messages.message import MessageSource
from src.messages.batching import TimeBatch


class TestMessageProcessing(unittest.TestCase):
    def test_message_creation(self):
        msg = Message("test", 12345.0)
        self.assertEqual(msg.content, "test")
        self.assertEqual(msg.timestamp, 12345.0)

    def test_time_batch(self):
        batch = TimeBatch(window_seconds=1.0)
        
        msg1 = Message("msg1")
        msg2 = Message("msg2")
        
        self.assertTrue(batch.add(msg1))
        self.assertTrue(batch.add(msg2))
        self.assertEqual(len(batch), 2)
        
        time.sleep(1.1)
        self.assertTrue(batch.is_ready())

    def test_time_batch_ready_after_window(self):
        batch = TimeBatch(window_seconds=0.5)
        batch.add(Message("test"))
        
        self.assertFalse(batch.is_ready())
        time.sleep(0.6)
        self.assertTrue(batch.is_ready())

    def test_time_batch_cannot_add_when_ready(self):
        batch = TimeBatch(window_seconds=0.1)
        batch.add(Message("test"))
        time.sleep(0.2)
        
        self.assertTrue(batch.is_ready())
        self.assertFalse(batch.add(Message("test2")))

    def test_source(self):
        source = MessageSource(rate_per_minute=600.0, duration_minutes=0.1)
        messages = list(source.get_data())
        
        self.assertGreater(len(messages), 0)
        self.assertIsInstance(messages[0], Message)

if __name__ == "__main__":
    unittest.main()