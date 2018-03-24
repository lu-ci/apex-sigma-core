import errno
import os
import shutil

import arrow
import discord
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

from sigma.core.mechanics.config import Configuration
from sigma.core.mechanics.cooldown import CooldownControl
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.executor import ExecutionClockwork
from sigma.core.mechanics.information import Information
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.music import MusicCore
from sigma.core.mechanics.plugman import PluginManager

# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

init_cfg = Configuration()

if init_cfg.dsc.bot:
    client_class = discord.AutoShardedClient
else:
    client_class = discord.Client


class ApexSigma(client_class):
    def __init__(self):
        super().__init__()
        self.ready = False
        # State attributes before initialization.
        self.log = None
        self.cfg = None
        self.db = None
        self.cool_down = None
        self.music = None
        self.modules = None
        self.queue = ExecutionClockwork(self)
        self.cache = {}
        # Initialize startup methods and attributes.
        self.create_cache()
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.loop.run_until_complete(self.init_database())
        self.log.info('---------------------------------')
        self.init_cool_down()
        self.log.info('---------------------------------')
        self.init_music()
        self.log.info('---------------------------------')
        self.info = Information()
        self.init_modules(init=True)
        self.start_time = arrow.utcnow()
        self.message_count = 0
        self.command_count = 0

    @staticmethod
    def create_cache():
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.makedirs('cache')

    def init_logger(self):
        self.log = create_logger('Sigma')
        self.log.info('Logger Created')

    def init_config(self):
        self.log.info('Loading Configuration...')
        self.cfg = init_cfg
        self.log.info(f'Running as a Bot: {self.cfg.dsc.bot}')
        self.log.info(f'Default Bot Prefix: {self.cfg.pref.prefix}')
        self.log.info('Core Configuration Data Loaded')

    async def init_database(self):
        self.log.info('Connecting to Database...')
        self.db = Database(self, self.cfg.db)
        try:
            await self.db[self.db.db_cfg.database].collection.find_one({})
            await self.db.precache_settings()
        except ServerSelectionTimeoutError:
            self.log.error('A Connection To The Database Host Failed!')
            exit(errno.ETIMEDOUT)
        except OperationFailure:
            self.log.error('Database Access Operation Failed!')
            exit(errno.EACCES)
        self.log.info('Successfully Connected to Database')

    def init_cool_down(self):
        self.log.info('Loading Cool-down Controls...')
        self.cool_down = CooldownControl(self)
        self.log.info('Cool-down Controls Successfully Enabled')

    def init_music(self):
        self.log.info('Loading Music Controller...')
        self.music = MusicCore(self)
        self.log.info('Music Controller Initialized and Ready')

    def init_modules(self, init=False):
        if init:
            self.log.info('Loading Sigma Modules')
        self.modules = PluginManager(self, init)

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

    async def on_shard_ready(self, shard_id: int):
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        event_name = 'shard_ready'
        self.loop.create_task(self.queue.event_runner(event_name, shard_id))

    async def on_ready(self):
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info('Apex Sigma Fully Loaded and Ready')
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        self.log.info('Launching On-Ready Modules...')
        self.loop.create_task(self.queue.event_runner('ready'))
        self.log.info('All On-Ready Module Loops Created')
        self.log.info('---------------------------------')

    async def on_message(self, message: discord.Message):
        self.message_count += 1
        if not message.author.bot:
            self.loop.create_task(self.queue.event_runner('message', message))
            if self.user.mentioned_in(message):
                self.loop.create_task(self.queue.event_runner('mention', message))
            await self.queue.command_runner(message)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not before.author.bot:
            self.loop.create_task(self.queue.event_runner('message_edit', before, after))

    async def on_message_delete(self, message: discord.Message):
        if not message.author.bot:
            self.loop.create_task(self.queue.event_runner('message_delete', message))

    async def on_member_join(self, member: discord.Member):
        if not member.bot:
            self.loop.create_task(self.queue.event_runner('member_join', member))

    async def on_member_remove(self, member: discord.Member):
        if not member.bot:
            self.loop.create_task(self.queue.event_runner('member_remove', member))

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not before.bot:
            self.loop.create_task(self.queue.event_runner('member_update', before, after))

    async def on_guild_join(self, guild: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_join', guild))

    async def on_guild_remove(self, guild: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_remove', guild))

    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_update', before, after))

    async def on_voice_state_update(self, member: discord.Member, b: discord.VoiceState, a: discord.VoiceState):
        if not member.bot:
            self.loop.create_task(self.queue.event_runner('voice_state_update', member, b, a))

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if not user.bot:
            self.loop.create_task(self.queue.event_runner('reaction_add', reaction, user))

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if not user.bot:
            self.loop.create_task(self.queue.event_runner('reaction_remove', reaction, user))
