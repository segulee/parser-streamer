# -*- coding: UTF-8 -*-
# Python3.7

# *******************************************************
#
#   brief       main.py
#   author      segulee@gmail.com
#
# *******************************************************

import os
import sys
import json
import logging
import argparse

from kafka import KafkaProducer
from app.parser import KakaoTalkParser
from app.producer import MessageProducer

log = logging.getLogger("app.main")


def run_parser(file_path, out_path):
    log.info("run parser")
    KakaoTalkParser().run_as_file(file_path, out_path)


def run_producer(file_path):
    log.info("run producer")

    # TODO:: write conf file to serve server, encoding
    server = "localhost:9092"
    encoding = "utf-8"

    lines = KakaoTalkParser().run_as_line(file_path)
    kafka_producer = KafkaProducer(
        bootstrap_servers=[server],
        key_serializer=lambda k: k.encode(encoding),
        value_serializer=lambda k: json.dumps(k).encode(encoding),
    )
    producer = MessageProducer(kafka_producer)
    producer.produce(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--producer",
        action="store_true",
        default=False,
        help="produce message to kafka cluster",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="debug mode",
        required=False,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="file path to parse.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out",
        default=os.path.join("app", "parsed"),
        help="output path for parsed messages.",
    )
    args = parser.parse_args()
    if args.debug:
        log.setLevel(logging.DEBUG)

    if args.file:
        if args.producer:
            run_producer(args.file)
        else:
            run_parser(args.file, args.out)

    log.info("run main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
