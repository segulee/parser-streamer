# -*- coding: UTF-8 -*-
# Python3.7

import re
import os
import logging
from emitter.logger import loginit  # noqa

log = logging.getLogger("app.parser")


class Parser:
    def __init__(self) -> None:
        pass

    def run(self, file_path, out_path) -> list:
        pass


class KakaoTalkParser(Parser):

    MSGPAT = re.compile(r"\[(.+)\] \[(.+) (\d+)\:(\d+)\] (.+)")
    TIMEPAT = re.compile(r"(\d+)년 (\d+)월 (\d+)일")

    def __init__(self) -> None:
        super().__init__()

    def read_line(self, file_path) -> str:
        try:
            with open(file_path, "r") as f:
                for line in f:
                    yield line
        except FileNotFoundError as e:
            log.error("invalid file_path passed. {}".format(e))
            return []

    def run_as_file(self, file_path, out_path) -> list:

        lines = self.read_line(file_path)
        return self.make_file(lines, out_path)

    def run_as_line(self, file_path):
        lines = self.read_line(file_path)
        return self.make_line(lines)

    def make_line(self, lines):
        """
        # TODO:: make_file과 코드 중복 제거, 함수 쪼개기 필요.
        """
        try:
            line = next(lines, None)
        except TypeError as e:
            log.error("not iterable or invalid file".format(e))
            return []

        while True:
            if not line:
                line = next(lines, None)
            time_data = self.parse_timestamp(line)
            timestamp = self.make_timestamp(time_data)
            if not timestamp:
                break

            while True:
                line = next(lines, None)
                if not line or line.startswith("---------------"):
                    break
                msg_data = self.parse_message(line.strip())
                message = self.make_message(timestamp, msg_data)

                if not message:
                    continue
                yield message

            if not line:
                break

    def make_file(self, lines, out_path) -> list:
        """
        # TODO:: make_line과 코드 중복 제거, 함수 쪼개기 필요.
        """
        try:
            line = next(lines, None)
        except TypeError as e:
            log.error("not iterable or invalid file".format(e))
            return []

        paths = []

        while True:
            if not line:
                line = next(lines, None)
            time_data = self.parse_timestamp(line)
            timestamp = self.make_timestamp(time_data)

            path = os.path.join(out_path, timestamp)
            if not path or os.path.isdir(path):
                break

            with open(path, "w") as f:
                while True:
                    line = next(lines, None)
                    if not line or line.startswith("---------------"):
                        break
                    msg_data = self.parse_message(line.strip())
                    message = self.make_message(timestamp, msg_data)

                    if not message:
                        continue
                    f.write(message + "\n")
            paths.append(path)
            if not line:
                break
        return paths

    def get_parsed(self, regex, line) -> tuple:
        try:
            return re.findall(regex, line)[0]
        except Exception:
            return ()

    def parse_timestamp(self, line) -> tuple:
        return self.get_parsed(self.TIMEPAT, line)

    def parse_message(self, line) -> tuple:
        return self.get_parsed(self.MSGPAT, line)

    def make_timestamp(self, time_data) -> str:
        if not time_data:
            return ""
        return "{}.{:02d}.{:02d}".format(*[int(data) for data in time_data])

    def make_message(self, timestamp, msg_data) -> str:
        """make message suitable to send

        Args:
            timestamp: string - line to make dict
            msg_data: list - parsed message data

        Returns:
            string parsed message
        """
        if not msg_data or not timestamp:
            return ""
        time = int(msg_data[2])
        if msg_data[1] == "오후":
            if int(msg_data[2]) != 12:
                time = 12 + int(msg_data[2])
        return "{} {} {:02d}:{:02d} {}".format(
            msg_data[0], timestamp, time, int(msg_data[3]), msg_data[4]
        )
