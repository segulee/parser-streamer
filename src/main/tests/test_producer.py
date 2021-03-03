# -*- coding: UTF-8 -*-
# Python3.7

# *******************************************************
#
#   brief       test_parser.py
#   author      segulee@gmail.com
#
# *******************************************************

import logging
import unittest
from emitter.logger import loginit  # noqa
from app.producer import Producer, MessageProducer

log = logging.getLogger("app.tests.test_parser")


class MockKafkaProducer:
    def __init__(self):
        pass

    def flush(self):
        pass

    def send(self, *args, **kwargs):
        pass

    def close(self):
        pass


class ProducerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = Producer(MockKafkaProducer())

    def tearDown(self) -> None:
        self.producer = None
        return super().tearDown()

    def test_produce(self) -> bool:
        return True


class MessageProducerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MessageProducer(MockKafkaProducer())

    def tearDown(self) -> None:
        self.producer = None
        return super().tearDown()

    def test_line_to_dict(self) -> bool:
        log.info("test_line_to_dict")
        tup_res = self.producer._line_to_dict("me 2021.03.04 19:01 테스트 라인 abcd")
        self.assertTrue(
            tup_res[0] == "me"
            and tup_res[1]["message"] == "테스트 라인 abcd"  # noqa
            # and tup_res[1]["timestamp"] == "2021.03.04 19:01"  # noqa
        )
        self.assertRaises(AttributeError, self.producer._line_to_dict, None)
        self.assertRaises(IndexError, self.producer._line_to_dict, "")
        self.assertRaises(ValueError, self.producer._line_to_dict, "me 2021:123 hi")

    def test_produce(self) -> bool:
        log.info("test_produce")
        self.assertIsNone(self.producer.produce([]))
        self.assertIsNone(self.producer.produce(None))


if __name__ == "__main__":
    log.info("producer unittest")
    unittest.main()
