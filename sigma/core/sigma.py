import os
import errno
import arrow
import discord
import pymongo

from sigma.core.mechanics.database import Database
from sigma.core.mechanics.config import load_config
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.plugman import PluginManager
from sigma.core.mechanics.cooldown import CooldownControl
from sigma.core.mechanics.music import MusicCore

# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Aurora Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# I love spaghetti!
# Valebu pls, no take my spaghetti... :'(

init_cfg = load_config()

if init_cfg.dsc.bot:
    client_class = discord.AutoShardedClient
else:
    client_class = discord.Client


class ApexSigma(client_class):
    def __init__(self):
        super().__init__()
        self.ready = False
        self.create_cache()
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.init_database()
        self.log.info('---------------------------------')
        self.init_cooldown()
        self.log.info('---------------------------------')
        self.init_music()
        self.log.info('---------------------------------')
        self.init_modules()
        self.start_time = arrow.utcnow()
        self.message_count = 0
        self.command_count = 0

    @staticmethod
    def create_cache():
        if not os.path.exists('cache'):
            os.makedirs('cache')

    def init_logger(self):
        self.log = create_logger('Sigma')
        self.log.info('Logger Created')

    def init_config(self):
        self.log.info('Loading Configuration...')
        self.cfg = load_config()
        self.log.info(f'Running as a Bot: {self.cfg.dsc.bot}')
        self.log.info(f'Default Bot Prefix: {self.cfg.pref.prefix}')
        self.log.info('Core Configuration Data Loaded')

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

    def init_cooldown(self):
        self.log.info('Loading Cooldown Controls...')
        self.cooldown = CooldownControl(self)
        self.log.info('Cooldown Controls Successfully Enabled')

    def init_music(self):
        self.log.info('Loading Music Controller...')
        self.music = MusicCore(self)
        self.log.info('Music Controller Initialized and Ready')

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
        event_name = 'connect'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    async def on_shard_ready(self, shard_id):
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        event_name = 'shard_ready'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(shard_id))

    async def on_ready(self):
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info('Apex Sigma Fully Loaded and Ready')
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        self.log.info('Launching On-Ready Modules...')
        event_name = 'ready'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())
        self.log.info('All On-Ready Module Loops Created')
        self.log.info('---------------------------------')
        if os.getenv('CI_TOKEN'):
            self.log.info('Continuous Integration Environment Detected')
            exit()

    async def on_message(self, message):
        self.message_count += 1
        if not message.author.bot:
            event_name = 'message'
            prefix = self.get_prefix(message)
            if message.content.startswith(prefix):
                args = message.content.split(' ')
                cmd = args.pop(0)[len(self.get_prefix(message)):].lower()
                if cmd in self.modules.alts:
                    cmd = self.modules.alts[cmd]
                if cmd in self.modules.commands:
                    self.loop.create_task(self.modules.commands[cmd].execute(message, args))
                    # await self.modules.commands[cmd].execute(message, args)
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(message))
                    # await event.execute(message)
            if self.user.mentioned_in(message):
                event_name = 'mention'
                if event_name in self.modules.events:
                    for event in self.modules.events[event_name]:
                        self.loop.create_task(event.execute(message))
                        # await event.execute(message)

    async def on_message_edit(self, before, after):
        if not before.author.bot:
            event_name = 'message_edit'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(before, after))
                    # await event.execute(before, after)

    async def on_member_join(self, member):
        if not member.bot:
            event_name = 'member_join'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(member))
                    # await event.execute(member)

    async def on_member_remove(self, member):
        if not member.bot:
            event_name = 'member_remove'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(member))
                    # await event.execute(member)

    async def on_member_update(self, before, after):
        if not before.bot:
            event_name = 'member_update'
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    self.loop.create_task(event.execute(before, after))
                    # await event.execute(before, after)

    async def on_guild_join(self, guild):
        event_name = 'guild_join'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(guild))
                # await event.execute(guild)

    async def on_guild_remove(self, guild):
        event_name = 'guild_remove'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(guild))
                # await event.execute(guild)

    async def on_voice_state_update(self, member, before, after):
        event_name = 'voice_state_update'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(member, before, after))
                # await event.execute(member, before, after)
