import os
import yaml
import importlib
from sigma.core.mechanics.logger import create_logger


class Command(object):
    def __init__(self, bot, command, plugin_info, command_info):
        self.bot = bot
        self.command = command
        self.log = create_logger(plugin_info['name'])
        self.name = command_info['name']
        self.rating = 0
        self.alts = []
        self.usage = f'{bot.cfg.pref.prefix}{self.name}'
        self.desc = 'No description provided.'

    async def execute(self, message, args):
        self.bot.loop.create_task(self.command.sigma_command(self, message, args))


class PluginManager(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Plugin Manager')
        self.alts = {}
        self.commands = {}
        self.events = {}
        self.log.info('Loading Commands')
        self.load_commands()
        self.log.info('Loaded All Commands')
        self.log.info(self.commands)

    def load_commands(self):
        directory = 'sigma/plugins'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'module.yml':
                    print(file)
                    file_path = (os.path.join(root, file))
                    with open(file_path) as plugin_file:
                        plugin_data = yaml.safe_load(plugin_file)
                        print(plugin_data)
                        if 'commands' in plugin_data:
                            for command_data in plugin_data['commands']:
                                self.log.info(f'Loading the {command_data["name"].title()} Command')
                                command_function = importlib.import_module(f'{os.path.join(root, command_data[""])}')
                                command = Command(self.bot, command_function, plugin_data, command_data)
                                self.commands.update({command_data['name']: command})
