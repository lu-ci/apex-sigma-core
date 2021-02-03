"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os
import sys

import arrow

systemd_journal_available = False

try:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from systemd import journal

    systemd_journal_available = True
except ModuleNotFoundError:
    sys.stderr.write("Systemd journal not available, using stdout\n")


def create_logger(name, *, to_title=False, level=None, shards=None):
    """
    Adds a new logger instance.
    :param name: The logger name.
    :type name: str
    :param to_title: Should the logger name be titleized.
    :type to_title: bool
    :param level: The logging level.
    :type level: int
    :param shards: The logging shard identifier.
    :type shards: list
    :return:
    :rtype: sigma.core.mechanics.logger.Logger
    """
    if to_title:
        logname = titleize(name)
    else:
        logname = name
    return Logger.create(logname, level=level, shards=shards)


def titleize(string):
    """
    Convert a string from :ModuleName: to :Module Name:.
    :param string: The string to titleize.
    :type string: str
    :return:
    :rtype: str
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
    """

    __slots__ = (
        "default_fmt", "default_date_fmt", "name",
        "created", "_logger"
    )

    loggers = {}

    def __init__(self, name, *, level=None):
        """
        :param name: The logger name and indentifier.
        :type name: str
        :param level: The logging level.
        :type level: int
        """
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
        :param name: The name of the logger.
        :type name: str
        :param level: The logging level.
        :type level: int
        :return:
        :rtype: sigma.core.mechanics.logger.Logger
        """
        if name not in cls.loggers.keys():
            cls.loggers.update({name: cls(name, level=level)})
        return cls.loggers.get(name)

    def info(self, message):
        """
        Generates an INFO level logging line.
        :param message: The logged text contents.
        :type message: str
        """
        self._logger.info(message)

    def debug(self, message):
        """
        Generates an DEBUG level logging line.
        :param message: The logged text contents.
        :type message: str
        """
        self._logger.debug(message)

    def error(self, message):
        """
        Generates an ERROR level logging line.
        :param message: The logged text contents.
        :type message: str
        """
        self._logger.error(message)

    def warn(self, message):
        """
        This just calls the warning method
        due to the parent method being deprecated.
        :param message: The logged text contents.
        :type message: str
        """
        self.warning(message)

    def warning(self, message):
        """
        Generates an WARNING level logging line.
        :param message: The logged text contents.
        :type message: str
        """
        self._logger.warning(message)

    def exception(self, message):
        """
        Generates an EXCEPTION level logging line.
        :param message: The logged text contents.
        :type message: str
        """
        self._logger.exception(message)

    @classmethod
    def create(cls, name, *, level=None, shards=None):
        """
        Creates a new logger class instance.
        :param name: The name of the logger.
        :type name: str
        :param level: The logger level.
        :type level: int
        :param shards: The logging shard identifier.
        :type shards: list
        :return:
        :rtype: sigma.core.mechanics.logger.Logger
        """
        logger = cls.get(name, level=level)
        if logger.created:
            return logger

        if systemd_journal_available:
            cls.add_journal_handler(logger)
        else:
            cls.add_stdout_handler(logger)

        cls.add_file_handler(logger, shards)
        logger.created = True
        return logger

    def add_handler(self, handler, fmt=None, date_fmt=None):
        """
        Add a new log handler with format handlers.
        :param handler:
        :type handler: logging.Handler
        :param fmt:
        :type fmt: str
        :param date_fmt:
        :type date_fmt: str
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
        :type logger: sigma.core.mechanics.logger.Logger
        """
        handler = journal.JournaldLogHandler(identifier='sigma')
        log_fmt = '[ {levelname:.1s} | {name:<25.25s} ]: {message:s}'
        logger.add_handler(handler, log_fmt)

    @staticmethod
    def add_stdout_handler(logger):
        """
        Add a log handler that logs to the standard output.
        :param logger:
        :type logger: sigma.core.mechanics.logger.Logger
        """
        handler = logging.StreamHandler()
        logger.add_handler(handler)

    @staticmethod
    def add_file_handler(logger, shards=None):
        """
        Adds a regular file handler for the logging.
        :param shards:
        :type shards: list[int] or None
        :param logger:
        :type logger: sigma.core.mechanics.logger.Logger
        """
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        now = arrow.utcnow()
        if shards is not None:
            format_name = f'sigma.{"-".join([str(shard) for shard in shards])}.{now.format("YYYY-MM-DD")}.log'
        else:
            format_name = f'sigma.{now.format("YYYY-MM-DD")}.log'
        filename = os.path.join(log_dir, format_name)
        handler = logging.FileHandler(filename, encoding='utf-8')
        logger.add_handler(handler)
