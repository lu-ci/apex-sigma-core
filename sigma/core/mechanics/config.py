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

import os

import yaml

from sigma.core.mechanics.logger import create_logger


class ModuleConfig(dict):
    """
    This class contains module configuration data
    that is stored in an object with pseudo-attributes.
    It's just a dict with an overwritten __getattr__ method.
    """

    def __init__(self, cmd):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        """
        self.cmd = cmd
        try:
            self.data = getattr(self.cmd.command, 'defaults')
        except AttributeError:
            self.data = {}
        super().__init__(self.data)

    def __getattr__(self, item):
        return self.get(item)

    def load(self, data):
        """
        Loads or overwrites the current module config settings.
        :type data: dict
        """
        self.data = data if data is not None else {}
        self.update(self.data)


class DiscordConfig(object):
    """
    Holds the Discord client configuration data.
    """

    __slots__ = (
        "raw", "token", "owners", "bot", "shards", "shard_count", "max_messages"
    )

    def __init__(self, client_cfg_data):
        """
        :type client_cfg_data: dict
        """
        self.raw = client_cfg_data
        self.token = self.raw.get('token')
        self.owners = self.raw.get('owners', [137951917644054529])
        self.bot = self.raw.get('bot', True)
        self.max_messages = self.raw.get('max_messages')
        try:
            self.shards = [int(shard) for shard in os.environ['SIGMA_SHARDS'].split(',')]
            self.shard_count = int(os.environ['SIGMA_SHARD_COUNT'])
        except (ValueError, KeyError):
            self.shards = None
            self.shard_count = None


class DatabaseConfig(object):
    """
    Holds the MongoDB connection configuration data.
    """

    __slots__ = (
        "raw", "database", "auth", "host", "port",
        "username", "password"
    )

    def __init__(self, db_cfg_data):
        """
        :type db_cfg_data: dict
        """
        self.raw = db_cfg_data
        self.database = self.raw.get('database', 'sigma')
        self.auth = self.raw.get('auth', False)
        self.host = self.raw.get('host', '127.0.0.1')
        self.port = self.raw.get('port', 27017)
        self.username = self.raw.get('username', 'user')
        self.password = self.raw.get('password', 'pass')


class PreferencesConfig(object):
    """
    Holds personalization preferences and settings data.
    """

    __slots__ = (
        "raw", "dev_mode", "status_rotation", "prefix",
        "currency", "currency_icon", "website", "text_only",
        "music_only", "movelog_channel", "errorlog_channel"
    )

    def __init__(self, pref_cfg_data):
        """
        :type pref_cfg_data: dict
        """
        self.raw = pref_cfg_data
        self.dev_mode = self.raw.get('dev_mode', False)
        self.status_rotation = self.raw.get('status_rotation', True)
        self.prefix = self.raw.get('prefix', '>>')
        self.currency = self.raw.get('currency', 'Kud')
        self.currency_icon = self.raw.get('currency_icon', '⚜')
        self.website = self.raw.get('website', 'https://luciascipher.com/sigma')
        self.text_only = self.raw.get('text_only', False)
        self.music_only = self.raw.get('music_only', False)
        self.movelog_channel = self.raw.get('movelog_channel')
        self.errorlog_channel = self.raw.get('errorlog_channel')


class CacheConfig(object):
    """
    Holds configuration parameters for all cache types.
    """

    __slots__ = (
        "raw", "type",
        "time", "size",
        "host", "port",
        "db"
    )

    def __init__(self, cache_cfg_data):
        """
        :type cache_cfg_data: dict
        """
        self.raw = cache_cfg_data
        self.type = self.raw.get('type')
        self.time = self.raw.get('time', 300)
        self.size = self.raw.get('size', 1000000)
        self.host = self.raw.get('host', '127.0.0.1')
        self.port = self.raw.get('port', 6379)
        self.db = self.raw.get('db', 3)


class Configuration(object):
    """
    Main configuration container.
    Holds all other configuration classes.
    """

    __slots__ = (
        "log", "client_cfg_data", "db_cfg_data", "pref_cfg_data",
        "cache_cfg_data", "dsc", "db", "pref", "cache"
    )

    def __init__(self):
        self.log = create_logger('Config')
        cli_cfg_path = 'config/core/discord.yml'
        db_cfg_path = 'config/core/database.yml'
        pref_cfg_path = 'config/core/preferences.yml'
        cache_cfg_path = 'config/core/cache.yml'
        if os.path.exists(cli_cfg_path):
            with open(cli_cfg_path, encoding='utf-8') as discord_config:
                self.client_cfg_data = yaml.safe_load(discord_config)
        else:
            self.log.warning('No discord configuration, using defaults.')
            self.client_cfg_data = {}
        if os.path.exists(db_cfg_path):
            with open(db_cfg_path, encoding='utf-8') as database_config:
                self.db_cfg_data = yaml.safe_load(database_config)
        else:
            self.log.warning('No database configuration, using defaults.')
            self.db_cfg_data = {}
        if os.path.exists(pref_cfg_path):
            with open(pref_cfg_path, encoding='utf-8') as preferences_config:
                self.pref_cfg_data = yaml.safe_load(preferences_config)
        else:
            self.log.warning('No preferences configuration, using defaults.')
            self.pref_cfg_data = {}
        if os.path.exists(cache_cfg_path):
            with open(cache_cfg_path, encoding='utf-8') as cache_config:
                self.cache_cfg_data = yaml.safe_load(cache_config)
        else:
            self.log.warning('No cache configuration, using defaults.')
            self.cache_cfg_data = {}
        self.dsc = DiscordConfig(self.client_cfg_data)
        self.db = DatabaseConfig(self.db_cfg_data)
        self.pref = PreferencesConfig(self.pref_cfg_data)
        self.cache = CacheConfig(self.cache_cfg_data)
