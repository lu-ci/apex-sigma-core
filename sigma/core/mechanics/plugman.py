import os
import yaml
import importlib
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.event import SigmaEvent


class PluginManager(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Plugin Manager')
        self.alts = {}
        self.commands = {}
        self.events = {}
        self.categories = []
        self.log.info('Loading Commands')
        self.load_all_modules()
        self.log.info(f'Loaded {len(self.commands)} Commands')
        self.log.info('---------------------------------')

    def load_all_modules(self):
        self.alts = {}
        self.commands = {}
        self.events = {}
        directory = 'sigma/plugins'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'module.yml':
                    file_path = (os.path.join(root, file))
                    with open(file_path) as plugin_file:
                        plugin_data = yaml.safe_load(plugin_file)
                        if plugin_data['enabled']:
                            self.log.info(f'Loading the {plugin_data["name"]} Module')
                            if 'commands' in plugin_data:
                                if plugin_data['category'] not in self.categories:
                                    self.categories.append(plugin_data['category'])
                                for command_data in plugin_data['commands']:
                                    if self.bot.cfg.pref.music_only:
                                        if plugin_data['category'] == 'music':
                                            add_cmd = True
                                        else:
                                            add_cmd = False
                                    elif self.bot.cfg.pref.text_only:
                                        if plugin_data['category'] != 'music':
                                            add_cmd = True
                                        else:
                                            add_cmd = False
                                    else:
                                        add_cmd = True
                                    if add_cmd:
                                        if command_data['enabled']:
                                            module_root_location = os.path.join(root)
                                            command_module_location = os.path.join(root, command_data["name"])
                                            command_module_location = command_module_location.replace('/', '.')
                                            command_module_location = command_module_location.replace('\\', '.')
                                            command_function = importlib.import_module(command_module_location)
                                            importlib.reload(command_function)
                                            command_data.update({'path': module_root_location})
                                            command = SigmaCommand(self.bot, command_function, plugin_data, command_data)
                                            if command.alts:
                                                for alt in command.alts:
                                                    self.alts.update({alt: command.name})
                                            self.commands.update({command_data['name']: command})
                            if self.bot.cfg.dsc.bot:
                                if not self.bot.cfg.pref.music_only:
                                    if 'events' in plugin_data:
                                        for event_data in plugin_data['events']:
                                            if event_data['enabled']:
                                                command_module_location = os.path.join(root, event_data["name"])
                                                command_module_location = command_module_location.replace('/', '.')
                                                command_module_location = command_module_location.replace('\\', '.')
                                                event_function = importlib.import_module(command_module_location)
                                                importlib.reload(event_function)
                                                event = SigmaEvent(self.bot, event_function, plugin_data, event_data)
                                                if event.event_type in self.events:
                                                    event_list = self.events[event.event_type]
                                                else:
                                                    event_list = []
                                                event_list.append(event)
                                                self.events.update({event.event_type: event_list})
