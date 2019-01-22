import errno
import os
import shutil

import arrow
import discord
from discord.raw_models import RawReactionActionEvent
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from sigma.core.mechanics.caching import get_cache
from sigma.core.mechanics.config import Configuration
from sigma.core.mechanics.cooldown import CooldownControl
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.executor import ExecutionClockwork
from sigma.core.mechanics.information import Information
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.music import MusicCore
from sigma.core.mechanics.payload import GuildPayload, GuildUpdatePayload, ReactionPayload, VoiceStateUpdatePayload
from sigma.core.mechanics.payload import MemberPayload, MemberUpdatePayload, MessageEditPayload, MessagePayload
from sigma.core.mechanics.payload import RawReactionPayload, ShardReadyPayload
from sigma.core.mechanics.plugman import PluginManager
from sigma.core.utilities.data_processing import set_color_cache_coll

# I love spaghetti!
# Valebu pls, no take my spaghetti... :'(

# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

ci_token = os.getenv('CI')
if not ci_token:
    init_cfg = Configuration()
    if init_cfg.dsc.bot:
        client_class = discord.AutoShardedClient
    else:
        client_class = discord.Client
else:
    client_class = discord.AutoShardedClient


class ApexSigma(client_class):
    def __init__(self):
        super().__init__()
        self.ready = False
        # State attributes before initialization.
        self.log = None
        self.cfg = init_cfg
        self.shard_count = self.cfg.dsc.shard_count
        self.shard_ids = [self.cfg.dsc.shard] if self.cfg.dsc.shard is not None else None
        self.db = None
        self.cool_down = None
        self.music = None
        self.modules = None
        self.queue = ExecutionClockwork(self)
        self.cache = None
        # Initialize startup methods and attributes.
        self.create_cache()
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.loop.run_until_complete(self.init_cacher())
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
        self.gateway_start = 0
        self.gateway_finish = 0

    @staticmethod
    def create_cache():
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.makedirs('cache')

    async def init_cacher(self):
        try:
            self.cache = await get_cache(self.cfg.db.cache_type)
        except OSError:
            self.log.error('Cacher failed to initialize, if you are using Redis, make sure the server is running!')
            exit(errno.ETIMEDOUT)

    def init_logger(self):
        self.log = create_logger('Sigma', shard=init_cfg.dsc.shard)
        self.log.info('Logger Created')

    def init_config(self):
        self.log.info('Loading Configuration...')
        self.log.info(f'Running as a Bot: {self.cfg.dsc.bot}')
        self.log.info(f'Default Bot Prefix: {self.cfg.pref.prefix}')
        self.log.info('Core Configuration Data Loaded')

    async def init_database(self):
        self.log.info('Connecting to Database...')
        self.db = Database(self, self.cfg.db)
        try:
            await self.db[self.db.db_nam].collection.find_one({})
            await self.db.precache_settings()
            await self.db.precache_profiles()
            await self.db.precache_resources()
            set_color_cache_coll(self.db[self.db.db_nam].ColorCache)
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
        self.loop.run_until_complete(self.cool_down.clean_cooldowns())
        self.log.info('Cool-down Controls Successfully Enabled')

    def init_music(self):
        self.log.info('Loading Music Controller...')
        self.music = MusicCore(self)
        self.log.info('Music Controller Initialized and Ready')

    def init_modules(self, init: bool = False):
        if init:
            self.log.info('Loading Sigma Modules')
        self.modules = PluginManager(self, init)

    def is_ready(self):
        try:
            ready = super().is_ready()
        except Exception:
            ready = False
        return ready

    async def get_user(self, uid, cached: bool = False):
        if cached:
            cache_key = f'get_usr_{uid}'
            out = await self.cache.get_cache(cache_key)
            if not out:
                out = super().get_user(uid)
                await self.cache.set_cache(cache_key, out)
        else:
            out = super().get_user(uid)
        return out

    async def get_channel(self, cid: int, cached: bool = False):
        if cached:
            cache_key = f'get_chn_{cid}'
            out = await self.cache.get_cache(cache_key)
            if not out:
                out = super().get_channel(cid)
                await self.cache.set_cache(cache_key, out)
        else:
            out = super().get_channel(cid)
        return out

    def run(self):
        try:
            self.log.info('Connecting to Discord Gateway...')
            self.gateway_start = arrow.utcnow().float_timestamp
            super().run(self.cfg.dsc.token, bot=self.cfg.dsc.bot)
        except discord.LoginFailure:
            self.log.error('Invalid Token!')
            exit(errno.EPERM)

    async def on_connect(self):
        self.loop.create_task(self.queue.event_runner('connect'))

    async def on_shard_ready(self, shard_id: int):
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        self.loop.create_task(self.queue.event_runner('shard_ready', ShardReadyPayload(self, shard_id)))

    async def on_ready(self):
        self.gateway_finish = arrow.utcnow().float_timestamp
        self.log.info(f'Gateway connection established in {round(self.gateway_finish - self.gateway_start, 3)}s')
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info('Apex Sigma Fully Loaded and Ready')
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        self.log.info('Launching On-Ready Modules...')
        self.loop.create_task(self.queue.event_runner('ready'))
        self.log.info('Launching DB-Init Modules...')
        self.loop.create_task(self.queue.event_runner('dbinit'))
        self.log.info('All On-Ready Module Loops Created')
        self.log.info('---------------------------------')

    async def on_message(self, message: discord.Message):
        self.message_count += 1
        if not message.author.bot:
            payload = MessagePayload(self, message)
            self.loop.create_task(self.queue.event_runner('message', payload))
            if self.user.mentioned_in(payload.msg):
                self.loop.create_task(self.queue.event_runner('mention', payload))
            await self.queue.command_runner(payload)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not after.author.bot:
            self.loop.create_task(self.queue.event_runner('message_edit', MessageEditPayload(self, before, after)))

    async def on_message_delete(self, message: discord.Message):
        if not message.author.bot:
            self.loop.create_task(self.queue.event_runner('message_delete', MessagePayload(self, message)))

    async def on_member_join(self, member: discord.Member):
        if not member.bot:
            self.loop.create_task(self.queue.event_runner('member_join', MemberPayload(self, member)))

    async def on_member_remove(self, member: discord.Member):
        if not member.bot:
            self.loop.create_task(self.queue.event_runner('member_remove', MemberPayload(self, member)))

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not before.bot:
            self.loop.create_task(self.queue.event_runner('member_update', MemberUpdatePayload(self, before, after)))

    async def on_guild_join(self, guild: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_join', GuildPayload(self, guild)))

    async def on_guild_remove(self, guild: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_remove', GuildPayload(self, guild)))

    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        self.loop.create_task(self.queue.event_runner('guild_update', GuildUpdatePayload(self, before, after)))

    async def on_voice_state_update(self, member: discord.Member, b: discord.VoiceState, a: discord.VoiceState):
        if not member.bot:
            payload = VoiceStateUpdatePayload(self, member, b, a)
            self.loop.create_task(self.queue.event_runner('voice_state_update', payload))

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if not user.bot:
            payload = ReactionPayload(self, reaction, user)
            self.loop.create_task(self.queue.event_runner('reaction_add', payload))
            if str(reaction.emoji) in ['⬅', '➡']:
                self.loop.create_task(self.queue.event_runner('paginate', payload))

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if not user.bot:
            payload = ReactionPayload(self, reaction, user)
            self.loop.create_task(self.queue.event_runner('reaction_remove', payload))

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != payload.channel_id:
            payload = RawReactionPayload(self, payload)
            self.loop.create_task(self.queue.event_runner('raw_reaction_add', payload))
            if str(payload.raw.emoji) in ['⬅', '➡']:
                self.loop.create_task(self.queue.event_runner('raw_paginate', payload))

    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if payload.user_id != payload.channel_id:
            self.loop.create_task(self.queue.event_runner('raw_reaction_remove', RawReactionPayload(self, payload)))
