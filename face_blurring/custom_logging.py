import logging
import urllib.parse
from contextvars import ContextVar
from dataclasses import dataclass

import yaml
from slack_sdk import WebClient

from config import settings

ctx_request = ContextVar("request")

LOG_FILE = settings.log.file
LOG_LEVEL = settings.log.level
SLACK_BOT_TOKEN = settings.slack.token
SLACK_CHANNEL_ID = settings.slack.channel_id


@dataclass
class RequestInfo:
    path: str
    query: str
    peer: str


class InjectingFilter(logging.Filter):
    def filter(self, record):
        request: RequestInfo = ctx_request.get()
        record.urlpath = request.path
        record.query = urllib.parse.unquote(request.query)
        record.peer = request.peer
        return True


class SlackHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.client = WebClient(token=SLACK_BOT_TOKEN)

    def emit(self, record: logging.LogRecord) -> None:
        if not (SLACK_BOT_TOKEN and SLACK_CHANNEL_ID):
            return
        try:
            msg = self.format(record)
            self.client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=msg)
        except Exception:
            self.handleError(record)


def setup_logging():
    with open("log_config.yaml", "r") as f:
        config = yaml.safe_load(f.read())

        # set log file
        config["handlers"]["filelogger"]["filename"] = LOG_FILE
        config["handlers"]["augmented_filelogger"]["filename"] = LOG_FILE

        # set log level
        config["root"]["level"] = LOG_LEVEL
        for _, v in config["loggers"].items():
            v["level"] = LOG_LEVEL

        logging.config.dictConfig(config)
