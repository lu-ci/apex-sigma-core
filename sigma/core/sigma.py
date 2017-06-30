import errno
import discord
import pymongo

from sigma.core.mechanics.database import Database
from sigma.core.mechanics.config import load_config
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.plugman import PluginManager


class ApexSigma(discord.AutoShardedClient):
    def __init__(self):
        super().__init__()
        self.ready = False
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.init_database()
        self.log.info('---------------------------------')
        self.init_modules()

    def init_logger(self):
        self.log = create_logger('Sigma')
        self.log.info('Logger Created')

    def init_config(self):
        self.log.info('Loading Configuration...')
        self.cfg = load_config()
        self.log.info('Configuration Loaded')

    def init_database(self):
        self.log.info('Connecting to Database...')
        self.db = Database(self, self.cfg.db)
        try:
            self.db.test.collection.find_one({})
        except pymongo.errors.ServerSelectionTimeoutError:
            self.log.error('A Connection To The Database Host Failed!')
            exit(errno.ETIMEDOUT)
        except pymongo.errors.OperationFailure:
            self.log.error('Database Access Operation Failed!')
            exit(errno.EACCES)
        self.log.info('Successfully Connected to Database')

    def init_modules(self):
        self.log.info('Loading Sigma Modules')
        self.modules = PluginManager(self)

    def get_prefix(self, message):
        prefix = self.cfg.pref.prefix
        if message.guild:
            pfx_search = self.db.get_guild_settings(message.guild.id, 'Prefix')
            if pfx_search:
                prefix = pfx_search
        return prefix

    def run(self):
        try:
            self.log.info('Connecting to Discord Gateway...')
            super().run(self.cfg.dsc.token, bot=self.cfg.dsc.bot)
        except discord.LoginFailure:
            self.log.error('Invalid Token!')
            exit(errno.EPERM)

    async def on_connect(self):
        self.log.info('Connection to Discord Established')
        event_name = 'connect'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    async def on_ready(self):
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        event_name = 'ready'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    async def on_message(self, message):
        if not message.author.bot:
            event_name = 'message'
            prefix = self.get_prefix(message)
            if message.content.startswith(prefix):
                args = message.content.split(' ')
                cmd = args.pop(0)[len(self.cfg.pref.prefix):].lower()
                if cmd in self.modules.alts:
                    cmd = self.modules.alts[cmd]
                if cmd in self.modules.commands:
                    self.loop.create_task(self.modules.commands[cmd].execute(message, args))
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(message))
            if self.user.mentioned_in(message):
                event_name = 'mention'
                if event_name in self.modules.events:
                    for event in self.modules.events[event_name]:
                        self.loop.create_task(event.execute(message))

    async def on_message_edit(self, before, after):
        if not before.author.bot:
            event_name = 'message_edit'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(before, after))

    async def on_member_join(self, member):
        if not member.bot:
            event_name = 'member_join'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(member))

    async def on_member_remove(self, member):
        if not member.bot:
            event_name = 'member_remove'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(member))

    async def on_member_update(self, before, after):
        if not before.bot:
            event_name = 'member_update'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(before, after))

    async def on_guild_join(self, guild):
        event_name = 'guild_join'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(guild))

    async def on_guild_remove(self, guild):
        event_name = 'guild_remove'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(guild))
