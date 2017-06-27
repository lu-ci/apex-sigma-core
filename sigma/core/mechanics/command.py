import os
import yaml
import importlib
from sigma.core.mechanics.logger import create_logger


class Command(object):
    def __init__(self, bot, command, plugin_info, command_info):
        self.bot = bot
        self.command = command
        self.plugin_info = plugin_info
        self.command_info = command_info
        self.log = create_logger(self.plugin_info['name'])
        self.name = self.command_info['name']
        self.rating = 0
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = None
        self.alts = None
        self.usage = f'{bot.cfg.pref.prefix}{self.name}'
        self.desc = 'No description provided.'
        self.insert_command_info()

    def insert_command_info(self):
        if 'alts' in self.command_info:
            self.alts = self.command_info['alts']
        if 'usage' in self.command_info:
            self.usage = self.command_info['usage']
            self.usage = self.usage.replace('{pfx}', self.bot.cfg.pref.prefix)
            self.usage = self.usage.replace('{cmd}', self.name)
        if 'desc' in self.command_info:
            self.desc = self.command_info['desc']
        if 'requirements' in self.command_info:
            self.requirements = self.command_info['requirements']
        if 'permissions' in self.command_info:
            permissions = self.command_info['permissions']
            if 'rating' in permissions:
                self.rating = permissions['rating']
            if 'owner' in permissions:
                self.owner = permissions['owner']
            if 'partner' in permissions:
                self.partner = permissions['partner']
            if 'dmable' in permissions:
                self.dmable = permissions['dmable']

    async def execute(self, message, args):
        task = getattr(self.command, self.name)(self, message, args)
        self.bot.loop.create_task(task)


class PluginManager(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Plugin Manager')
        self.alts = {}
        self.commands = {}
        self.events = {}
        self.log.info('Loading Commands')
        self.load_commands()
        self.log.info(f'Loaded All {len(self.commands)} Commands')

    def load_commands(self):
        directory = 'sigma/plugins'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'module.yml':
                    file_path = (os.path.join(root, file))
                    with open(file_path) as plugin_file:
                        plugin_data = yaml.safe_load(plugin_file)
                        if plugin_data['enabled']:
                            if 'commands' in plugin_data:
                                for command_data in plugin_data['commands']:
                                    if command_data['enabled']:
                                        self.log.info(f'Loading the [ {command_data["name"].upper()} ] Command')
                                        command_module_location = os.path.join(root, command_data["name"])
                                        command_module_location = command_module_location.replace('/', '.')
                                        command_module_location = command_module_location.replace('\\', '.')
                                        command_function = importlib.import_module(
                                            f'{command_module_location}'
                                        )
                                        command = Command(self.bot, command_function, plugin_data, command_data)
                                        if command.alts:
                                            for alt in command.alts:
                                                self.alts.update({alt: command.name})
                                        self.commands.update({command_data['name']: command})
