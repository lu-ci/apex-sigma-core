import errno
import os

import yaml

from .logger import create_logger


class DiscordConfig(object):
    def __init__(self, client_cfg_data):
        self.raw = client_cfg_data
        self.token = client_cfg_data.get('token')
        self.owners = client_cfg_data.get('owners')
        self.bot = client_cfg_data.get('bot')


class DatabaseConfig(object):
    def __init__(self, db_cfg_data):
        self.raw = db_cfg_data
        self.database = db_cfg_data.get('database')
        self.auth = db_cfg_data.get('auth')
        self.host = db_cfg_data.get('host')
        self.port = db_cfg_data.get('port')
        self.username = db_cfg_data.get('username')
        self.password = db_cfg_data.get('password')


class PreferencesConfig(object):
    def __init__(self, pref_cfg_data):
        self.raw = pref_cfg_data
        self.dev_mode = pref_cfg_data.get('dev_mode')
        self.status_rotation = pref_cfg_data.get('status_rotation')
        self.prefix = pref_cfg_data.get('prefix')
        self.currency = pref_cfg_data.get('currency')
        self.currency_icon = pref_cfg_data.get('currency_icon')
        self.website = pref_cfg_data.get('website')
        self.text_only = pref_cfg_data.get('text_only')
        self.music_only = pref_cfg_data.get('music_only')
        self.dscbots_token = pref_cfg_data.get('dscbots_token')
        self.movelog_channel = pref_cfg_data.get('movelog_channel')


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
            self.log.error('Missing Discord Configuration File!')
            exit(errno.ENOENT)
        if os.path.exists(db_cfg_path):
            with open(db_cfg_path, encoding='utf-8') as discord_config:
                self.db_cfg_data = yaml.safe_load(discord_config)
        else:
            self.log.error('Missing Database Configuration File!')
            exit(errno.ENOENT)
        if os.path.exists(pref_cfg_config):
            with open(pref_cfg_config, encoding='utf-8') as discord_config:
                self.pref_cfg_data = yaml.safe_load(discord_config)
        else:
            self.log.error('Missing Preferences Configuration File!')
            exit(errno.ENOENT)
        self.dsc = DiscordConfig(self.client_cfg_data)
        self.db = DatabaseConfig(self.db_cfg_data)
        self.pref = PreferencesConfig(self.pref_cfg_data)
