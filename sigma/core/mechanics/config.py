import os
import yaml
import requests


def load_config():
    ci_token = os.getenv('CI_TOKEN')
    if ci_token:
        ci_config_url = f'https://data.auroraproject.xyz/secret/ci/{ci_token}'
        ci_config = requests.get(ci_config_url).json()
        client_cfg_data = ci_config['discord']
        db_cfg_data = ci_config['database']
        pref_cfg_data = ci_config['preferences']
    else:
        with open('config/core/discord.yml', encoding='utf-8') as discord_config:
            client_cfg_data = yaml.safe_load(discord_config)
        with open('config/core/database.yml', encoding='utf-8') as discord_config:
            db_cfg_data = yaml.safe_load(discord_config)
        with open('config/core/preferences.yml', encoding='utf-8') as discord_config:
            pref_cfg_data = yaml.safe_load(discord_config)

    class DiscordConfig(object):
        raw = client_cfg_data
        token = client_cfg_data['token']
        owners = client_cfg_data['owners']
        bot = client_cfg_data['bot']

    class DatabaseConfig(object):
        raw = db_cfg_data
        database = db_cfg_data['database']
        auth = db_cfg_data['auth']
        host = db_cfg_data['host']
        port = db_cfg_data['port']
        username = db_cfg_data['username']
        password = db_cfg_data['password']

    class PreferencesConfig(object):
        raw = pref_cfg_data
        dev_mode = pref_cfg_data['dev_mode']
        status_rotation = pref_cfg_data['status_rotation']
        prefix = pref_cfg_data['prefix']
        currency = pref_cfg_data['currency']
        currency_icon = pref_cfg_data['currency_icon']
        website = pref_cfg_data['website']
        text_only = pref_cfg_data['text_only']
        music_only = pref_cfg_data['music_only']
        if 'dscbots_token' in pref_cfg_data:
            dscbots_token = pref_cfg_data['dscbots_token']
        else:
            dscbots_token = None

    class Configuration(object):
        dsc = DiscordConfig
        db = DatabaseConfig
        pref = PreferencesConfig

    return Configuration
