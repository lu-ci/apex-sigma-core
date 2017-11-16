"""
Sigma Plugin Manager

Structure:
    PluginManager
      [SigmaModule]
        [SigmaCommand]
        [SigmaEvent]
"""

import os

from sigma.core.mechanics.module import SigmaModule
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.module_component import Disabled

class PluginManager(object):
    def __init__(self, bot, init):
        self.log = create_logger("Plugin Manager")
        if init:
            self.log.info('Loading Sigma Modules')
        self.bot = bot
        self.prefix = bot.cfg.pref.prefix
        self.path = None
        self.init = init
        self.modules = {}
        self._alts = {}

        self.load_all_modules()

        if self.init:
            self.log.info(f'Loaded {len(self.commands)} Commands and '
                          f'{len(self.events)} Events')
            self.log.info('---------------------------------')

    @property
    def events(self):
        tmp = {}
        for module in self.modules.values():
            for name, evlist in module.events.items():
                tmp[name] = evlist

        return tmp

    @property
    def commands(self):
        tmp = {}
        for module in self.modules.values():
            for name, cmd in module.commands.items():
                tmp[name] = cmd

        return tmp

    @property
    def alts(self):
        tmp = {}
        for module in self.modules.values():
            tmp.update(module.alts)

        return tmp

    def load_module(self, file):
        try:
            mod_name, mod = SigmaModule.from_file(self, file)
            self.modules[mod_name] = mod
            return (mod_name, mod)
        except Disabled:
            pass

    def unload_module(self, name):
        pass

    def reload_module(self, name):
        pass

    def load_all_modules(self):
        self.plugin_files('sigma/modules', self.load_module)

    def plugin_files(self, directory, callback):
        for root, _dir, files in os.walk(directory):
            if 'module.yml' in files:
                callback(os.path.join(root, 'module.yml'))
