"""
Sigma Configuration
"""

import os
from itertools import zip_longest
import yaml
from sigma.core.mechanics.logger import create_logger

class SigmaConfigurationError(Exception):
    pass

class InvalidConfiguration(SigmaConfigurationError):
    pass

class MissingConfiguration(SigmaConfigurationError):
    def __init__(self, file):
        message = f"Missing configuration file: {file}"
        super().__init__(message)

class Config(object):
    log = create_logger("Config")

    def __init__(self, config, *, defaults={}):
        if not isinstance(config, dict):
            raise InvalidConfiguration

        self._defaults = dict(defaults)
        self._config = dict(defaults)
        self._config.update(config)
        self._config_store = {}

        self.__populate()

    def __getattribute__(self, name):
        try:
            return super(Config, self).__getattribute__(name)
        except AttributeError:
            return self.__set(name, None)

    def __repr__(self):
        return str(self._config_store)

    def __populate(self):
        for key, value in self._config.items():
            if isinstance(value, dict):
                self.__populate_dict(key, value)
            elif isinstance(value, list):
                self.__populate_list(key, value)
            else:
                self.__set(key, value)

    def __populate_dict(self, key, dic):
        default = self._defaults.get(key, {})
        self.__set(key, Config(dic, defaults=default))

    def __populate_list(self, key, lst):
        items = zip_longest(lst, self._defaults.get(key, []), fillvalue=None)
        tmp = []
        for elem, default in items:
            if isinstance(elem, dict):
                tmp.append(Config(elem, defaults=(default or {})))
            else:
                tmp.append(elem)
        self.__set(key, tmp)

    def __set(self, key, value):
        self._config_store[key] = value
        return self.__setattr__(key, value)

    @classmethod
    def new(cls, config, *, defaults={}):
        if isinstance(config, list):
            return [cls(conf, defaults=defaults) for conf in config]

        return cls(config, defaults=defaults)

    @classmethod
    def from_file(cls, filename, *, defaults={}, required=True):
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as config_file:
                config = yaml.safe_load(config_file)
                return cls.new(config, defaults=defaults)
        elif required:
            cls.log.error(f"Missing configuration file: {filename}")
            raise MissingConfiguration(filename)

        return cls.new(defaults)

class Version(Config):
    def __init__(self, config, *, defaults={}):
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
def configuration():
    log = create_logger("Configuration")
    log.info('Loading Configuration...')

    config = Config({
        "dsc": Config.from_file('config/core/discord.yml', defaults={
            "token": None,
            "owners": [],
            "bot": True
        }),
        "db": Config.from_file('config/core/database.yml', required=False, defaults={
            "database": "aurora",
            "auth": False,
            "host": "localhost",
            "port": 27017,
            "username": 'admin',
            "password": 'admin'
        }),
        "pref": Config.from_file('config/core/preferences.yml', required=False, defaults={
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
    })

    log.info('Core Configuration Data Loaded')
    return config

# Info
def information():
    return Config({
        "version": Version.from_file("info/version.yml"),
        "authors": Config.from_file("info/authors.yml"),
        "donors": Config.from_file("info/donors.yml"),
    })
