import errno
import os
import yaml

from .logger import create_logger

class Config(object):
    log = create_logger("Config")

    def __init__(self, config, *, defaults={}):
        self.config = defaults
        self.config.update(config)

        for key, value in self.config.items():
            self.__setattr__(key, value)

    @classmethod
    def from_file(cls, filename, *, defaults={}, required=True):
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as config_file:
                config = yaml.safe_load(config_file)
                return cls(config, defaults=defaults)
        elif required:
            cls.log.error('Missing Discord Configuration File!')
            exit(errno.ENOENT)
        else:
            return cls(defaults)

class Version(Config):
    def __init__(self, config):
        super().__init__(config, defaults={
            "major": config.get("version", {}).get("major", 0),
            "minor": config.get("version", {}).get("minor", 0),
            "patch": config.get("version", {}).get("patch", 0)
        })

    def __str__(self):
        ver = f"{self.major}.{self.minor}.{self.patch}"
        ver += " Beta" if self.beta else ""
        return ver

# General config
def load_discord_config():
    return Config.from_file('config/core/discord.yml', defaults={
        "token": None,
        "owners": [],
        "bot": True
    })

def load_database_config():
    return Config.from_file('config/core/database.yml', required=False, defaults={
        "database": "aurora",
        "auth": False,
        "host": "localhost",
        "port": 27017,
        "username": 'admin',
        "password": 'admin'
    })

def load_preferences():
    return Config.from_file('config/core/preferences.yml', defaults={
        "dev_mode": False,
        "status_rotation": True,
        "text_only": False,
        "music_only": False,
        "prefix": ">>",
        "currency": "Kud",
        "currency_icon": "⚜",
        "website": "https://lucia.moe/#/sigma",
        "dscbots_token": None,
        "movelog_channel": None,
        "key_to_my_heart": "redacted"
    })

def configuration():
    log = create_logger("Configuration")
    log.info('Loading Configuration...')
    config = Config({
        "dsc": load_discord_config(),
        "db": load_database_config(),
        "pref": load_preferences()
    })
    log.info('Core Configuration Data Loaded')
    return config

# Info
def information():
    return Config({
        "version": version(),
        "authors": authors(),
        "donors": donors()
    })

def authors():
    with open('info/authors.yml', encoding='utf-8') as authors_file:
        authors_data = yaml.safe_load(authors_file)
        return [Config(author) for author in authors_data]

def donors():
    with open('info/donors.yml', encoding='utf-8') as donors_file:
        donors_data = yaml.safe_load(donors_file)
        return [Config(donor) for donor in donors_data.get("donors", [])]

def version():
    with open('info/version.yml', encoding='utf-8') as version_file:
        version_data = yaml.safe_load(version_file)
        return Version(version_data)
