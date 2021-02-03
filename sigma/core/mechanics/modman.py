"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import importlib
import os

import yaml

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.logger import create_logger


class ModuleManager(object):
    """
    The module manager handles all loading of modules
    as well as the commands and events within those modules.
    It also serves as a reference storage of loaded instances.
    """

    __slots__ = (
        "bot", "init", "log", "alts",
        "commands", "events", "categories"
    )

    def __init__(self, bot, init):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.ApexSigma
        :param init: Is this the first module manager initialization.
        :type init: bool
        """
        self.bot = bot
        self.init = init
        self.log = create_logger('Module Manager', shards=self.bot.cfg.dsc.shards)
        self.alts = {}
        self.commands = {}
        self.events = {}
        self.categories = []
        if self.init:
            self.log.info('Loading Commands')
        self.load_all_modules()
        if self.init:
            self.log.info(f'Loaded {len(self.commands)} Commands')
            for evkey in self.events:
                ev_count = len(self.events.get(evkey))
                end = 's' if ev_count != 1 else ''
                self.log.info(f'Loaded {ev_count} {evkey.replace("_", " ").title()} Event{end}')
            self.log.info('---------------------------------')

    @staticmethod
    def clean_path(path):
        """
        Cleans the OS path of a module to a python interpretable one.
        :param path: The path to the module.
        :type path: str
        :return:
        :rtype: str
        """
        out = path.replace('/', '.').replace('\\', '.')
        return out

    def load_module(self, root, module_data):
        """
        Loads a given modules commands, events, and information.
        :param root: The module origin path.
        :type root: str
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        if self.init:
            self.log.info(f'Loading the {module_data.get("name")} Module')
        self.load_category(module_data)
        if 'commands' in module_data:
            self.load_commands(root, module_data)
        if self.bot.cfg.dsc.bot:
            if not self.bot.cfg.pref.music_only:
                if 'events' in module_data:
                    self.load_events(root, module_data)

    def load_function(self, root, data):
        """
        Loads the defining function to execute of the event or command.
        :param root: The module origin path.
        :type root: str
        :param data: Document containing the module's details.
        :type data: dict
        :return:
        :rtype: function
        """
        module_location = self.clean_path(os.path.join(root, data.get("name")))
        module_function = importlib.import_module(module_location)
        importlib.reload(module_function)
        return module_function

    def load_category(self, module_data):
        """
        Loads the category identifier of the module.
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        if module_data.get('category') not in self.categories:
            self.categories.append(module_data.get('category'))

    def load_commands(self, root, module_data):
        """
        Loads the commands within the given module.
        :param root: The module origin path.
        :type root: str
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        for command_data in module_data.get('commands'):
            if command_data.get('enabled'):
                self.load_command_executable(root, command_data, module_data)

    def load_events(self, root, module_data):
        """
        Loads the events within the given module.
        :param root: The module origin path.
        :type root: str
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        for event_data in module_data.get('events'):
            if event_data.get('enabled'):
                self.load_event_executable(root, event_data, module_data)

    def load_command_executable(self, root, command_data, module_data):
        """
        Loads the command's executable and defining function call.
        :param root: The command origin path.
        :type root: str
        :param command_data: Document containing the command's details.
        :type command_data: dict
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        command_data.update({'path': os.path.join(root)})
        command_function = self.load_function(root, command_data)
        cmd = SigmaCommand(self.bot, command_function, module_data, command_data)
        if cmd.alts:
            for alt in cmd.alts:
                self.alts.update({alt: cmd.name})
        self.commands.update({command_data.get('name'): cmd})

    def load_event_executable(self, root, event_data, module_data):
        """
        Loads the event's executable and defining function call.
        :param root: The command origin path.
        :type root: str
        :param event_data: Document containing the event's details.
        :type event_data: dict
        :param module_data: Document containing the module's details.
        :type module_data: dict
        """
        event_function = self.load_function(root, event_data)
        event_data.update({'path': os.path.join(root)})
        event = SigmaEvent(self.bot, event_function, module_data, event_data)
        if event.event_type in self.events:
            event_list = self.events.get(event.event_type)
        else:
            event_list = []
        event_list.append(event)
        self.events.update({event.event_type: event_list})

    def load_all_modules(self):
        """
        Loads all modules by going through every module yaml
        in the modules directory recursively.
        """
        self.alts = {}
        self.commands = {}
        self.events = {}
        directory = 'sigma/modules'
        for root, _dirs, files in os.walk(directory):
            for file in files:
                if file == 'module.yml':
                    file_path = os.path.join(root, file)
                    with open(file_path, encoding='utf-8') as module_file:
                        module_data = yaml.safe_load(module_file)
                        if module_data.get('enabled'):
                            if self.bot.cfg.pref.text_only:
                                if module_data.get('category') == 'music':
                                    continue
                            if self.bot.cfg.pref.music_only:
                                if module_data.get('category') not in ['music', 'help']:
                                    continue
                            self.load_module(root, module_data)
