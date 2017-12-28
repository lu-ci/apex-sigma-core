import errno
import os
import shutil

import arrow
import discord
import pymongo

from sigma.core.mechanics.config import Configuration
from sigma.core.mechanics.cooldown import CooldownControl
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.information import Information
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.music import MusicCore
from sigma.core.mechanics.plugman import PluginManager
from sigma.core.mechanics.threading import QueueControl

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
        self.queue = QueueControl(self)
        self.launched = False
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
        except pymongo.errors.ServerSelectionTimeoutError:
            self.log.error('A Connection To The Database Host Failed!')
            exit(errno.ETIMEDOUT)
        except pymongo.errors.OperationFailure:
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

    async def get_prefix(self, message):
        prefix = self.cfg.pref.prefix
        if message.guild:
            pfx_search = await self.db.get_guild_settings(message.guild.id, 'Prefix')
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

    async def event_runner(self, event_name, *args):
        if self.ready:
            if event_name in self.modules.events:
                for event in self.modules.events[event_name]:
                    task = event, *args
                    await self.queue.queue.put(task)

    async def on_connect(self):
        event_name = 'connect'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    async def on_shard_ready(self, shard_id):
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        event_name = 'shard_ready'
        self.loop.create_task(self.event_runner(event_name, shard_id))

    async def on_ready(self):
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info('Apex Sigma Fully Loaded and Ready')
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        self.log.info('Launching On-Ready Modules...')
        self.loop.create_task(self.event_runner('ready'))
        if not self.launched:
            self.loop.create_task(self.event_runner('launch'))
            self.launched = True
        self.log.info('All On-Ready Module Loops Created')
        self.log.info('---------------------------------')

    async def get_cmd_and_args(self, message, args, mention=False):
        args = list(filter(lambda a: a != '', args))
        if mention:
            if args:
                cmd = args.pop(0).lower()
            else:
                cmd = None
        else:
            pfx = await self.get_prefix(message)
            cmd = args.pop(0)[len(pfx):].lower()
        return cmd, args

    def clean_self_mentions(self, message):
        for mention in message.mentions:
            if mention.id == self.user.id:
                message.mentions.remove(mention)
                break

    async def on_message(self, message):
        self.message_count += 1
        if not message.author.bot:
            self.loop.create_task(self.event_runner('message', message))
            if self.user.mentioned_in(message):
                self.loop.create_task(self.event_runner('mention', message))
            prefix = await self.get_prefix(message)
            if message.content.startswith(prefix):
                args = message.content.split(' ')
                cmd, args = await self.get_cmd_and_args(message, args)
            elif message.content.startswith(self.user.mention):
                args = message.content.split(' ')[1:]
                self.clean_self_mentions(message)
                cmd, args = await self.get_cmd_and_args(message, args, mention=True)
            elif message.content.startswith(f'<@!{self.user.id}>'):
                args = message.content.split(' ')[1:]
                cmd, args = await self.get_cmd_and_args(message, args, mention=True)
            else:
                cmd = None
                args = []
            if cmd:
                if cmd in self.modules.alts:
                    cmd = self.modules.alts[cmd]
                if cmd in self.modules.commands:
                    command = self.modules.commands[cmd]
                    task = command, message, args
                    await self.queue.queue.put(task)

    async def on_message_edit(self, before, after):
        if not before.author.bot:
            self.loop.create_task(self.event_runner('message_edit', before, after))

    async def on_message_delete(self, message):
        if not message.author.bot:
            self.loop.create_task(self.event_runner('message_delete', message))

    async def on_member_join(self, member):
        if not member.bot:
            self.loop.create_task(self.event_runner('member_join', member))

    async def on_member_remove(self, member):
        if not member.bot:
            self.loop.create_task(self.event_runner('member_remove', member))

    async def on_member_update(self, before, after):
        if not before.bot:
            self.loop.create_task(self.event_runner('member_update', before, after))

    async def on_guild_join(self, guild):
        self.loop.create_task(self.event_runner('guild_join', guild))

    async def on_guild_remove(self, guild):
        self.loop.create_task(self.event_runner('guild_remove', guild))

    async def on_guild_update(self, before, after):
        self.loop.create_task(self.event_runner('guild_update', before, after))

    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            self.loop.create_task(self.event_runner('voice_state_update', member, before, after))
