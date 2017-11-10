import os
import yaml
import importlib

from sigma.core.mechanics.logger import create_logger

class SigmaModuleComponent(object):
    def __init__(self, parent, config):
        self.config = config
        self.name = config['name']
        self.category = config.get('category', None)

        self.parent = parent
        self.bot = parent.bot
        self.db = parent.bot.db
        self.path = config.get('path', parent.path)

        self.log = create_logger(self.name)

    @classmethod
    def from_config(cls, parent, config):
        if not config['enabled']:
            return

        component = cls(parent, config)
        return (component.name, component)

    @classmethod
    def from_file(cls, parent, file):
        if os.path.exists(file):
            with open(file) as config_file:
                config = yaml.safe_load(config_file)
                config['path'] = os.path.dirname(file)
                return cls.from_config(parent, config)

    @property
    def prefix(self):
        return self.config.get('prefix', self.parent.prefix)

    @property
    def nsfw(self):
        return self.permission('nsfw')

    @property
    def owner(self):
        return self.permission('owner')

    @property
    def partner(self):
        return self.permission('partner')

    @property
    def dmable(self):
        return self.permission('dmable')

    def permission(self, name):
        return self.config.get('permissions', {}).get(name, False)

    def resource(self, res_path):
        return f'{self.path}/res/{res_path}'.replace('\\', '/')

    def load_path(self, path):
        func = importlib.import_module(self.path_to_module(path))
        importlib.reload(func)
        return func

    @staticmethod
    def path_to_module(path):
        return path.replace('/', '.').replace('\\', '.')
