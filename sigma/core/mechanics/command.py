from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.permissions import CommandPermissions


class SigmaCommand(object):
    def __init__(self, bot, command, plugin_info, command_info):
        self.bot = bot
        self.db = self.bot.db
        self.command = command
        self.plugin_info = plugin_info
        self.command_info = command_info
        self.name = self.command_info['name']
        self.log = create_logger(self.name.title())
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
        if self.bot.ready:
            perms = CommandPermissions(self, message)
            if perms.permitted:
                task = getattr(self.command, self.name)(self, message, args)
                self.bot.loop.create_task(task)
            else:
                try:
                    await message.author.send(embed=perms.response)
                except:
                    pass
