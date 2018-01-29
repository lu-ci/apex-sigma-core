# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

systemd_journal_available = False

try:
    from systemd import journal

    systemd_journal_available = True
except ModuleNotFoundError:
    sys.stderr.write("Systemd journal not available, using stdout\n")


def create_logger(name, *, to_title=False, level=None):
    """
    Add a new logger.
    :param name:
    :param to_title:
    :param level:
    :return:
    """
    if to_title:
        logname = titleize(name)
    else:
        logname = name

    return Logger.create(logname, level=level)


def titleize(string):
    """
    Convert a string from :ModuleName: to :Module Name:.
    :param string:
    :return:
    """
    new_string = ""
    for i, char in enumerate(string):
        if char.isupper() and i != 0:
            new_string += " " + char
        else:
            new_string += char
    return new_string


class Logger(object):
    """
    Sigma Logger:
    This log module will log to a file at "{project_root}/log" which will be rotated daily.
    Logs will also be written to the Systemd Journal if it's available.
    Otherwise logs will be written to stdout.
    :param name:
    :param level:
    """
    loggers = {}

    def __init__(self, name, *, level=None):
        self.default_fmt = '[ {levelname:^8s} | {asctime:s} | {name:<25.25s} ] {message:s}'
        self.default_date_fmt = '%Y.%m.%d %H:%M:%S'
        self.name = name
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(level or logging.DEBUG)
        self.created = False

    @classmethod
    def get(cls, name, *, level=None):
        """
        Get a logger with :name: or create a new one.
        :param name:
        :param level:
        :return:
        """
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
        return self.warning(message)

    def warning(self, message):
        return self._logger.warning(message)

    def exception(self, message):
        return self._logger.exception(message)

    @classmethod
    def create(cls, name, *, level=None):
        """
        Create a logger with :name: if it has not been created before.
        :param name:
        :param level:
        :return:
        """
        logger = cls.get(name, level=level)
        if logger.created:
            return logger

        if systemd_journal_available:
            cls.add_journal_handler(logger)
        else:
            cls.add_stdout_handler(logger)

        cls.add_file_handler(logger)
        logger.created = True
        return logger

    def add_handler(self, handler, fmt=None, date_fmt=None):
        """
        Add a new log handler with format handlers.
        :param handler:
        :param fmt:
        :param date_fmt:
        :return:
        """
        fmt = fmt or self.default_fmt
        date_fmt = date_fmt or self.default_date_fmt
        handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=date_fmt, style='{'))
        self._logger.addHandler(handler)

    @staticmethod
    def add_journal_handler(logger):
        """
        Add a log handler that logs to the Systemd journal.
        :param logger:
        :return:
        """
        handler = journal.JournaldLogHandler(identifier='sigma')
        log_fmt = '[ {levelname:.1s} | {name:<25.25s} ]: {message:s}'
        logger.add_handler(handler, log_fmt)

    @staticmethod
    def add_stdout_handler(logger):
        """
        Add a log hander that logs to the standard output.
        :param logger:
        :return:
        """
        handler = logging.StreamHandler()
        logger.add_handler(handler)

    @staticmethod
    def add_file_handler(logger):
        """
        Add a log handler that writes logs to a auto rotated file.
        The file will be rotated every day.
        :param logger:
        :return:
        """
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        filename = os.path.join(log_dir, 'sigma.log')
        handler = TimedRotatingFileHandler(filename, when='d', interval=1, encoding='utf-8', utc=True)
        logger.add_handler(handler)
