# -*- coding: UTF-8 -*-
# Python3.7

import logging
import datetime
from emitter.logger import loginit  # noqa

log = logging.getLogger("app.producer")


class Producer:
    def __init__(self, producer):
        self.producer = producer

    def produce(self, lines):
        pass


class MessageProducer(Producer):
    def __init__(self, producer):
        super().__init__(producer)

    def produce(self, lines):
        while True:
            try:
                line = next(lines)
            except StopIteration:
                log.info("End of lines.")
                break
            except TypeError as e:
                log.error("Invalid lines produced. {}".format(e))
                break

            try:
                key, value = self.line_to_dict(line)
                log.debug("key: {}, value: {}".format(key, value))

                self.producer.send("testmessage", key=key, value=value)
                self.producer.flush()
            except (IndexError, AttributeError) as e:
                log.error("Invalid line saved. {}".format(e))
                continue
            except ValueError as e:
                log.error("Invalid timestamp saved. {}".format(e))
            except Exception as e:
                log.warning("Unhandled Exception. {}".format(e))
                continue

        self.producer.close()

    def _line_to_dict(self, line):
        """make kafka message like dict from input string

        Args:
            string: line to make dict

        Returns:
            key: string kafka key
            value: dict kafka value with timestamp, message

        Raises:
            ValueError: timestamp parsing error
            IndexError: invalid line input
            AttributeError: invalid line input
        """
        part = line.split(" ")
        key = part[0]
        timestamp = datetime.datetime.strptime(
            part[1] + " " + part[2], "%Y.%m.%d %H:%M"
        )

        value = {"timestamp": str(timestamp), "message": " ".join(part[3:])}

        return key, value
