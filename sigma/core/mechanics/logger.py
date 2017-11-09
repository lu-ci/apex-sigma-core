"""
Sigma Logger:
  This log module will log to a file at "{project_root}/log" which will be rotated daily.
  Logs will also be written to the Systemd Journal if it's available.
  Otherwise logs will be written to stdout.
"""

import os
import sys

import logging
from logging.handlers import TimedRotatingFileHandler

systemd_journal_available = False

try:
    from systemd import journal
    systemd_journal_available = True
except ModuleNotFoundError:
    sys.stderr.write("Systemd journal not available, using stdout\n")

def create_logger(name):
    "Add a new logger"
    return Logger.create(name)

def with_logger(name=None, level=None):
    "Decorator to make a logger available in the decorated class."

    def decorator(cls):
        cls.log = Logger.create(name or cls.__name__, level=level)
        return cls

    return decorator

class Logger(object):
    "The logger core"

    loggers = {}

    def __init__(self, name, *, level=None):
        self.default_fmt = '%(levelname)-8s %(asctime)s %(name)-20s %(message)s'
        self.default_date_fmt = '%Y.%m.%d %H:%M:%S'
        self.name = name
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(level or logging.INFO)
        self.created = False

    @classmethod
    def get(cls, name, *, level=None):
        "Get a logger with :name: or create a new one."

        if name in cls.loggers.keys():
            return cls.loggers.get(name)
        else:
            cls.loggers[name] = cls(name, level=level)
            return cls.loggers[name]

    def info(self, message):
        return self._logger.info(message)

    def debug(self, message):
        return self._logger.debug(message)

    def error(self, message):
        return self._logger.error(message)

    def warn(self, message):
        return self._logger.warn(message)

    def warning(self, message):
        return self._logger.warn(message)

    def exception(self, message):
        return self._logger.exception(message)

    @classmethod
    def create(cls, name, *, level=None):
        "Create a logger with :name: if it has not been created before."

        logger = cls.get(name, level=level)
        if logger.created:
            return

        if systemd_journal_available:
            cls.add_journal_handler(logger)
        else:
            cls.add_stdout_handler(logger)

        cls.add_file_handler(logger)
        logger.created = True
        return logger

    def add_handler(self, handler, fmt=None, date_fmt=None):
        "Add a new log handler with format handlers."

        fmt = fmt or self.default_fmt
        date_fmt = date_fmt or self.default_date_fmt
        handler.setFormatter(logging.Formatter(fmt, date_fmt))
        self._logger.addHandler(handler)

    @staticmethod
    def add_journal_handler(logger):
        "Add a log handler that logs to the Systemd journal."

        handler = journal.JournaldLogHandler(identifier='sigma')
        log_fmt = '[%(name)-10s]: %(message)s'
        logger.add_handler(handler, log_fmt)

    @staticmethod
    def add_stdout_handler(logger):
        "Add a log hander that logs to the standard output."
        handler = logging.StreamHandler()
        logger.add_handler(handler)

    @staticmethod
    def add_file_handler(logger):
        """
        Add a log handler that writes logs to a auto rotated file.
        The file will be rotated every day.
        """
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        filename = os.path.join(log_dir, 'sigma.log')
        handler = TimedRotatingFileHandler(filename,
                                           when='d', interval=1,
                                           encoding='utf-8', utc=True)
        logger.add_handler(handler)
