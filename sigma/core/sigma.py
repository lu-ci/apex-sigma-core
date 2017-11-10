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
        """
        Sigma Core:
            Apex Sigma's central core.
            Loads and initializes all core submodules.
            Handles all Discord events and command calls.
        """
        super().__init__()
        self.ready = False
        # State attributes before initialization.
        self.log = None
        self.cfg = None
        self.db = None
        self.cool_down = None
        self.music = None
        self.modules = None
        self.queue = QueueControl()
        self.launched = False
        self.cache = {}
        # Initialize startup methods and attributes.
        self.create_cache()
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.init_database()
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
        """Cleans and creates the cache folder."""
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.makedirs('cache')

    def init_logger(self):
        """Initializes the Logger."""
        self.log = create_logger('Sigma')
        self.log.info('Logger Created')

    def init_config(self):
        """Loads and initializes the configuration."""
        self.log.info('Loading Configuration...')
        self.cfg = init_cfg
        self.log.info(f'Running as a Bot: {self.cfg.dsc.bot}')
        self.log.info(f'Default Bot Prefix: {self.cfg.pref.prefix}')
        self.log.info('Core Configuration Data Loaded')

    def init_database(self):
        """Establishes a database connection."""
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

    def init_cool_down(self):
        """Adds the Cooldown Control class."""
        self.log.info('Loading Cool-down Controls...')
        self.cool_down = CooldownControl(self)
        self.log.info('Cool-down Controls Successfully Enabled')

    def init_music(self):
        """Loads and adds the Music core controls."""
        self.log.info('Loading Music Controller...')
        self.music = MusicCore(self)
        self.log.info('Music Controller Initialized and Ready')

    def init_modules(self, init=False):
        """Loads all modules, events, commands."""
        if init:
            self.log.info('Loading Sigma Modules')
        self.modules = PluginManager(self, init)

    def get_prefix(self, message):
        """Retrieves the prefix based on settings."""
        prefix = self.cfg.pref.prefix
        if message.guild:
            pfx_search = self.db.get_guild_settings(message.guild.id, 'Prefix')
            if pfx_search:
                prefix = pfx_search
        return prefix

    def run(self):
        """Starts the Discord connection process."""
        try:
            self.log.info('Connecting to Discord Gateway...')
            super().run(self.cfg.dsc.token, bot=self.cfg.dsc.bot)
        except discord.LoginFailure:
            self.log.error('Invalid Token!')
            exit(errno.EPERM)

    async def event_runner(self, event_name, *args):
        """Generic handler for all event calls."""
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                # self.loop.create_task(event.execute(*args))
                task = event, *args
                await self.queue.queue.put(task)

    async def on_connect(self):
        """Emits an event when the client connets."""
        event_name = 'connect'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    async def on_shard_ready(self, shard_id):
        """Emits an event when a shard is ready."""
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        event_name = 'shard_ready'
        self.loop.create_task(self.event_runner(event_name, shard_id))

    async def on_ready(self):
        """Emits an event when the entire client is ready."""
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
        if os.getenv('CI_TOKEN'):
            self.log.info('Continuous Integration Environment Detected')
            exit()

    def get_cmd_and_args(self, message, args, mention=False):
        """Gets the command and arguemnts from the message."""
        args = list(filter(lambda a: a != '', args))
        if mention:
            if args:
                cmd = args.pop(0).lower()
            else:
                cmd = None
        else:
            cmd = args.pop(0)[len(self.get_prefix(message)):].lower()
        return cmd, args

    def clean_self_mentions(self, message):
        """Removes self mentions in commands that don't use a prefix."""
        for mention in message.mentions:
            if mention.id == self.user.id:
                message.mentions.remove(mention)
                break

    async def on_message(self, message):
        """
        Emits a message event when any message is sent.
        Sends the message content through get_cmd_and_args()
        and returns the results if the message contains a command.
        If it does, the appropriate command will be called.
        """
        self.message_count += 1
        if not message.author.bot:
            event_name = 'message'
            self.loop.create_task(self.event_runner(event_name, message))
            if self.user.mentioned_in(message):
                event_name = 'mention'
                self.loop.create_task(self.event_runner(event_name, message))
            prefix = self.get_prefix(message)
            if message.content.startswith(prefix):
                args = message.content.split(' ')
                cmd, args = self.get_cmd_and_args(message, args)
            elif message.content.startswith(self.user.mention):
                args = message.content.split(' ')[1:]
                self.clean_self_mentions(message)
                cmd, args = self.get_cmd_and_args(message, args, mention=True)
            elif message.content.startswith(f'<@!{self.user.id}>'):
                args = message.content.split(' ')[1:]
                cmd, args = self.get_cmd_and_args(message, args, mention=True)
            else:
                cmd = None
                args = []
            if cmd:
                if cmd in self.modules.alts:
                    cmd = self.modules.alts[cmd]
                if cmd in self.modules.commands:
                    command = self.modules.commands[cmd]
                    # self.loop.create_task(command.execute(message, args))
                    task = command, message, args
                    await self.queue.queue.put(task)

    async def on_message_edit(self, before, after):
        """Emits an event when a message is edited."""
        if not before.author.bot:
            event_name = 'message_edit'
            self.loop.create_task(self.event_runner(event_name, before, after))

    async def on_message_delete(self, message):
        """Emits an event when a message is deleted."""
        if not message.author.bot:
            event_name = 'message_delete'
            self.loop.create_task(self.event_runner(event_name, message))

    async def on_member_join(self, member):
        """Emits an event when a member joins a guild."""
        if not member.bot:
            event_name = 'member_join'
            self.loop.create_task(self.event_runner(event_name, member))

    async def on_member_remove(self, member):
        """Emits an event when a member leaves a guild."""
        if not member.bot:
            event_name = 'member_remove'
            self.loop.create_task(self.event_runner(event_name, member))

    async def on_member_update(self, before, after):
        """Emits an event when a member updates their profile."""
        if not before.bot:
            event_name = 'member_update'
            self.loop.create_task(self.event_runner(event_name, before, after))

    async def on_guild_join(self, guild):
        """Emits an event when the client joins a guild."""
        event_name = 'guild_join'
        self.loop.create_task(self.event_runner(event_name, guild))

    async def on_guild_remove(self, guild):
        """Emits an event when the client leaves a guild."""
        event_name = 'guild_remove'
        self.loop.create_task(self.event_runner(event_name, guild))

    async def on_voice_state_update(self, member, before, after):
        """Emits an event when a member changes their voice state."""
        event_name = 'voice_state_update'
        self.loop.create_task(self.event_runner(event_name, member, before, after))
