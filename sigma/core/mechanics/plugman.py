import importlib
import os

import yaml

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.logger import create_logger


class PluginManager(object):
    def __init__(self, bot, init):
        self.bot = bot
        self.init = init
        self.log = create_logger('Plugin Manager')
        self.alts = {}
        self.commands = {}
        self.events = {}
        self.categories = []
        if self.init:
            self.log.info('Loading Commands')
        self.load_all_modules()
        if self.init:
            self.log.info(f'Loaded {len(self.commands)} Commands')
            self.log.info('---------------------------------')

    @staticmethod
    def clean_path(path):
        out = path.replace('/', '.').replace('\\', '.')
        return out

    def load_module(self, root, module_data):
        if self.init:
            self.log.info(f'Loading the {module_data.get("name")} Module')
        if 'commands' in module_data:
            self.load_commands(root, module_data)
        if self.bot.cfg.dsc.bot:
            if not self.bot.cfg.pref.music_only:
                if 'events' in module_data:
                    self.load_events(root, module_data)

    def load_function(self, root, data):
        module_location = self.clean_path(os.path.join(root, data.get("name")))
        module_function = importlib.import_module(module_location)
        importlib.reload(module_function)
        return module_function

    def load_commands(self, root, module_data):
        if module_data.get('category') not in self.categories:
            self.categories.append(module_data.get('category'))
        for command_data in module_data.get('commands'):
            if self.should_add(module_data):
                if command_data.get('enabled'):
                    self.load_command_executable(root, command_data, module_data)

    def load_events(self, root, module_data):
        for event_data in module_data.get('events'):
            if event_data.get('enabled'):
                self.load_event_execuable(root, event_data, module_data)

    def load_command_executable(self, root, command_data, plugin_data):
        command_data.update({'path': os.path.join(root)})
        command_function = self.load_function(root, command_data)
        cmd = SigmaCommand(self.bot, command_function, plugin_data, command_data)
        if cmd.alts:
            for alt in cmd.alts:
                self.alts.update({alt: cmd.name})
        self.commands.update({command_data.get('name'): cmd})

    def load_event_execuable(self, root, event_data, plugin_data):
        event_function = self.load_function(root, event_data)
        event = SigmaEvent(self.bot, event_function, plugin_data, event_data)
        if event.event_type in self.events:
            event_list = self.events.get(event.event_type)
        else:
            event_list = []
        event_list.append(event)
        self.events.update({event.event_type: event_list})

    def should_add(self, module_data):
        if self.bot.cfg.pref.music_only:
            if module_data.get('category') == 'music':
                add_cmd = True
            else:
                add_cmd = False
        elif self.bot.cfg.pref.text_only:
            if module_data.get('category') != 'music':
                add_cmd = True
            else:
                add_cmd = False
        else:
            add_cmd = True
        return add_cmd

    def load_all_modules(self):
        self.alts = {}
        self.commands = {}
        self.events = {}
        directory = 'sigma/modules'
        module_file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'module.yml':
                    file_path = os.path.join(root, file)
                    with open(file_path, encoding='utf-8') as plugin_file:
                        module_data = yaml.safe_load(plugin_file)
                        if module_data.get('enabled'):
                            self.load_module(root, module_data)
