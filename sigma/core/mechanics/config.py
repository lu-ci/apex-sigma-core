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


class DiscordConfig(object):
    def __init__(self, client_cfg_data: dict):
        self.raw = client_cfg_data
        self.token = client_cfg_data.get('token', 'You got no token, son!')
        self.owners = client_cfg_data.get('owners', [137951917644054529])
        self.bot = client_cfg_data.get('bot', True)


class DatabaseConfig(object):
    def __init__(self, db_cfg_data: dict):
        self.raw = db_cfg_data
        self.database = db_cfg_data.get('database', 'sigma')
        self.auth = db_cfg_data.get('auth', False)
        self.host = db_cfg_data.get('host', '127.0.0.1')
        self.port = db_cfg_data.get('port', 27017)
        self.username = db_cfg_data.get('username', 'user')
        self.password = db_cfg_data.get('password', 'pass')


class PreferencesConfig(object):
    def __init__(self, pref_cfg_data: dict):
        self.raw = pref_cfg_data
        self.dev_mode = pref_cfg_data.get('dev_mode', False)
        self.status_rotation = pref_cfg_data.get('status_rotation', True)
        self.prefix = pref_cfg_data.get('prefix', '>>')
        self.currency = pref_cfg_data.get('currency', 'Kud')
        self.currency_icon = pref_cfg_data.get('currency_icon', '⚜')
        self.website = pref_cfg_data.get('website', 'https://lucia.moe/sigma')
        self.text_only = pref_cfg_data.get('text_only', False)
        self.music_only = pref_cfg_data.get('music_only', False)
        self.dscbots_token = pref_cfg_data.get('dscbots_token')
        self.movelog_channel = pref_cfg_data.get('movelog_channel')
        self.errorlog_channel = pref_cfg_data.get('errorlog_channel')


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
            with open(db_cfg_path, encoding='utf-8') as discord_config:
                self.db_cfg_data = yaml.safe_load(discord_config)
        else:
            self.log.warning('No database configuration, using defaults.')
            self.db_cfg_data = {}
        if os.path.exists(pref_cfg_config):
            with open(pref_cfg_config, encoding='utf-8') as discord_config:
                self.pref_cfg_data = yaml.safe_load(discord_config)
        else:
            self.log.warning('No preferences configuration, using defaults.')
            self.pref_cfg_data = {}
        self.dsc = DiscordConfig(self.client_cfg_data)
        self.db = DatabaseConfig(self.db_cfg_data)
        self.pref = PreferencesConfig(self.pref_cfg_data)
