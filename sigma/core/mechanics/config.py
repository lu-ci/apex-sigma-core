# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import os

import yaml

from sigma.core.mechanics.logger import create_logger


class ModuleConfig(object):
    def __init__(self, data: dict):
        self.data = data

    def __getattr__(self, item):
        return self.data.get(item)


class DiscordConfig(object):
    def __init__(self, client_cfg_data: dict):
        self.raw = client_cfg_data
        self.token = self.raw.get('token', 'You got no token, son!')
        self.owners = self.raw.get('owners', [137951917644054529])
        self.bot = self.raw.get('bot', True)
        try:
            self.shard = int(os.environ['SIGMA_SHARD'])
            self.shard_count = int(os.environ['SIGMA_SHARD_COUNT'])
        except (ValueError, KeyError):
            self.shard = None
            self.shard_count = None


class DatabaseConfig(object):
    def __init__(self, db_cfg_data: dict):
        self.raw = db_cfg_data
        self.database = self.raw.get('database', 'sigma')
        self.auth = self.raw.get('auth', False)
        self.host = self.raw.get('host', '127.0.0.1')
        self.port = self.raw.get('port', 27017)
        self.username = self.raw.get('username', 'user')
        self.password = self.raw.get('password', 'pass')
        self.cache_type = self.raw.get('cache_type')


class PreferencesConfig(object):
    def __init__(self, pref_cfg_data: dict):
        self.raw = pref_cfg_data
        self.dev_mode = self.raw.get('dev_mode', False)
        self.status_rotation = self.raw.get('status_rotation', True)
        self.prefix = self.raw.get('prefix', '>>')
        self.currency = self.raw.get('currency', 'Kud')
        self.currency_icon = self.raw.get('currency_icon', '⚜')
        self.website = self.raw.get('website', 'https://lucia.moe/sigma')
        self.text_only = self.raw.get('text_only', False)
        self.music_only = self.raw.get('music_only', False)
        self.movelog_channel = self.raw.get('movelog_channel')
        self.errorlog_channel = self.raw.get('errorlog_channel')


class Configuration(object):
    def __init__(self):
        self.log = create_logger('Config')
        cli_cfg_path = 'config/core/discord.yml'
        db_cfg_path = 'config/core/database.yml'
        pref_cfg_config = 'config/core/preferences.yml'
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
        if os.path.exists(pref_cfg_config):
            with open(pref_cfg_config, encoding='utf-8') as preferences_config:
                self.pref_cfg_data = yaml.safe_load(preferences_config)
        else:
            self.log.warning('No preferences configuration, using defaults.')
            self.pref_cfg_data = {}
        self.dsc = DiscordConfig(self.client_cfg_data)
        self.db = DatabaseConfig(self.db_cfg_data)
        self.pref = PreferencesConfig(self.pref_cfg_data)
