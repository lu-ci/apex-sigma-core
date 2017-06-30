from sigma.core.mechanics.logger import create_logger


class SigmaEvent(object):
    def __init__(self, bot, event, plugin_info, event_info):
        self.bot = bot
        self.db = self.bot.db
        self.event = event
        self.event_type = event_info['type']
        self.plugin_info = plugin_info
        self.event_info = event_info
        self.name = self.event_info['name']
        self.log = create_logger(self.name.title())
        self.rating = 0
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = None
        self.insert_command_info()

    def insert_command_info(self):
        if 'alts' in self.event_info:
            self.alts = self.event_info['alts']
        if 'usage' in self.event_info:
            self.usage = self.event_info['usage']
            self.usage = self.usage.replace('{pfx}', self.bot.cfg.pref.prefix)
            self.usage = self.usage.replace('{cmd}', self.name)
        if 'desc' in self.event_info:
            self.desc = self.event_info['desc']
        if 'requirements' in self.event_info:
            self.requirements = self.event_info['requirements']
        if 'permissions' in self.event_info:
            permissions = self.event_info['permissions']
            if 'rating' in permissions:
                self.rating = permissions['rating']
            if 'owner' in permissions:
                self.owner = permissions['owner']
            if 'partner' in permissions:
                self.partner = permissions['partner']
            if 'dmable' in permissions:
                self.dmable = permissions['dmable']

    async def execute(self, *args):
        if self.bot.ready:
            await getattr(self.event, self.name)(self, *args)
