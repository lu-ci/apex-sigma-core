import os
import yaml
import errno
import requests
from .logger import create_logger


class DiscordConfig(object):
    def __init__(self, client_cfg_data):
        self.raw = client_cfg_data
        self.token = client_cfg_data['token']
        self.owners = client_cfg_data['owners']
        self.bot = client_cfg_data['bot']


class DatabaseConfig(object):
    def __init__(self, db_cfg_data):
        self.raw = db_cfg_data
        self.database = db_cfg_data['database']
        self.auth = db_cfg_data['auth']
        self.host = db_cfg_data['host']
        self.port = db_cfg_data['port']
        self.username = db_cfg_data['username']
        self.password = db_cfg_data['password']


class PreferencesConfig(object):
    def __init__(self, pref_cfg_data):
        self.raw = pref_cfg_data
        self.dev_mode = pref_cfg_data['dev_mode']
        self.status_rotation = pref_cfg_data['status_rotation']
        self.prefix = pref_cfg_data['prefix']
        self.currency = pref_cfg_data['currency']
        self.currency_icon = pref_cfg_data['currency_icon']
        self.website = pref_cfg_data['website']
        self.text_only = pref_cfg_data['text_only']
        self.music_only = pref_cfg_data['music_only']
        if 'dscbots_token' in pref_cfg_data:
            self.dscbots_token = pref_cfg_data['dscbots_token']
        else:
            self.dscbots_token = None
        if 'movelog_channel' in pref_cfg_data:
            self.movelog_channel = pref_cfg_data['movelog_channel']
        else:
            self.movelog_channel = None


class Configuration(object):
    def __init__(self):
        self.log = create_logger('Config')
        ci_token = os.getenv('CI_TOKEN')
        if ci_token:
            ci_config_url = f'https://api.lucia.moe/secret/ci/{ci_token}'
            ci_config = requests.get(ci_config_url).json()
            self.client_cfg_data = ci_config['discord']
            self.db_cfg_data = ci_config['database']
            self.pref_cfg_data = ci_config['preferences']
        else:
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
