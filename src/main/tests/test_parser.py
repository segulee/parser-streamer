# -*- coding: UTF-8 -*-
# Python3.7

# *******************************************************
#
#   brief       test_parser.py
#   author      segulee@gmail.com
#
# *******************************************************

import os
import logging
import datetime
import unittest
from emitter.logger import loginit  # noqa
from app.parser import Parser, KakaoTalkParser

log = logging.getLogger("app.tests.test_parser")


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        return super().setUp()

    def tearDown(self) -> None:
        self.parser = None
        return super().tearDown()

    def test_run(self) -> bool:
        self.assertIsNone(self.parser.run("", ""))


class KakaoTalkParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_txt_path = os.path.join("tests", "resources.txt")
        self.test_valid_txt_path = os.path.join("tests", "resources2.txt")
        self.out_path = os.path.join("tests", "parsed")
        self.parser = KakaoTalkParser()

        return super().setUp()

    def tearDown(self) -> None:
        self.parser = None
        return super().tearDown()

    def test_read_line(self):
        log.info("test_read_line")
        cnt = 0
        for line in self.parser.read_line(self.test_txt_path):
            cnt += 1
        return self.assertEqual(cnt, 45)

    def _to_date(self, strdate, formatter="%H:%M") -> datetime.datetime:
        return datetime.datetime.strptime(strdate, formatter)

    def test_parse_timestamp(self):
        log.info("test_parse_timestamp")
        self.assertEqual(self.parser.parse_timestamp("2021년 3월 4일"), ("2021", "3", "4"))
        self.assertEqual(self.parser.parse_timestamp("2021년3월4일"), ())
        self.assertEqual(self.parser.parse_timestamp("2021년 3월"), ())
        self.assertEqual(self.parser.parse_timestamp(None), ())

    def test_parse_message(self):
        log.info("test_parse_message")
        self.assertEqual(
            self.parser.parse_message("[me] [오후 7:01] 하하하하"),
            ("me", "오후", "7", "01", "하하하하"),
        )
        self.assertEqual(self.parser.parse_message("[me] [오전 7:01] "), ())
        self.assertEqual(self.parser.parse_message(""), ())
        self.assertEqual(self.parser.parse_message(None), ())

    def test_make_timestamp(self):
        log.info("test_make_timestamp")
        self.assertEqual(self.parser.make_timestamp(("2021", "3", "4")), "2021.03.04")
        self.assertEqual(self.parser.make_timestamp(("2021", "13", "4")), "2021.13.04")
        self.assertEqual(self.parser.make_timestamp(("2021", "3", "14")), "2021.03.14")
        self.assertEqual(self.parser.make_timestamp(None), "")

    def test_make_message(self):
        log.info("test_make_message")
        self.assertEqual(
            self.parser.make_message("2021.03.04", ("me", "오후", "7", "01", "하하하하")),
            "me 2021.03.04 19:01 하하하하",
        )
        self.assertEqual(
            self.parser.make_message("2021.03.04", None),
            "",
        )
        self.assertEqual(
            self.parser.make_message(None, ("me", "오후", "7", "01", "하하하하")),
            "",
        )

    def get_line(self):
        lines = [
            "--------------- 2019년 10월 2일 수요일 ---------------",
            "[you] [오후 5:30] 이게 무슨 일이람",
            "[me] [오후 7:01] 하하하하",
            "--------------- 2019년 10월 3일 목요일 ---------------",
            "[you] [오전 6:31] 테스트 코드",
            "[me] [오후 10:31] 하하하하",
        ]
        for line in lines:
            yield line

    def test_make_file(self):
        log.info("test_make_file")

        self.assertEqual(
            self.parser.make_file(self.get_line(), self.out_path),
            ["tests/parsed/2019.10.02", "tests/parsed/2019.10.03"],
        )

        self.assertEqual(
            self.parser.make_file(None, self.out_path),
            [],
        )

    def test_make_line(self):
        lines = self.get_line()
        parsed = self.parser.make_line(lines)

        self.assertEqual(
            [line for line in parsed],
            [
                "you 2019.10.02 17:30 이게 무슨 일이람",
                "me 2019.10.02 19:01 하하하하",
                "you 2019.10.03 06:31 테스트 코드",
                "me 2019.10.03 22:31 하하하하",
            ],
        )
        res = self.parser.make_line(None)
        self.assertRaises(StopIteration, next, res)

    def test_run_as_file(self):
        log.info("test_run_as_file")
        self.assertEqual(self.parser.run_as_file("", ""), [])
        self.assertEqual(self.parser.run_as_file(self.test_txt_path, ""), [])

    def test_run_as_line(self):
        log.info("test_run_as_line")
        res = self.parser.run_as_line("")
        self.assertRaises(StopIteration, next, res)
        res = self.parser.run_as_line(self.test_valid_txt_path)
        self.assertEqual(next(res), "you 2019.10.02 17:30 이게 무슨 일이람")


if __name__ == "__main__":
    log.info("parser unittest")
    unittest.main()
