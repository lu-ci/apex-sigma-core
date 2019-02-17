# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import abc

import discord


class SigmaPayload(abc.ABC):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}

    async def init(self):
        pass


class UpdatePayload(SigmaPayload):
    def __init__(self, bot, before, after):
        super().__init__(bot)
        self.before = before
        self.after = after


class ShardReadyPayload(SigmaPayload):
    def __init__(self, bot, shard: int):
        super().__init__(bot)
        self.shard = shard


class MessagePayload(SigmaPayload):
    def __init__(self, bot, msg: discord.Message):
        super().__init__(bot)
        self.msg = msg

    async def init(self):
        if self.msg.guild:
            self.settings = await self.bot.db.get_guild_settings(self.msg.guild.id)


class MessageEditPayload(UpdatePayload):
    async def init(self):
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class CommandPayload(MessagePayload):
    def __init__(self, bot, msg: discord.Message, args: list):
        super().__init__(bot, msg)
        self.args = args


class CommandEventPayload(CommandPayload):
    def __init__(self, bot, cmd, pld: CommandPayload):
        super().__init__(bot, pld.msg, pld.args)
        self.cmd = cmd


class MemberPayload(SigmaPayload):
    def __init__(self, bot, member: discord.Member):
        super().__init__(bot)
        self.member = member

    async def init(self):
        if self.member.guild:
            self.settings = await self.bot.db.get_guild_settings(self.member.guild.id)


class MemberUpdatePayload(UpdatePayload):
    async def init(self):
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class GuildPayload(SigmaPayload):
    def __init__(self, bot, guild: discord.Guild):
        super().__init__(bot)
        self.guild = guild

    async def init(self):
        self.settings = await self.bot.db.get_guild_settings(self.guild.id)


class GuildUpdatePayload(UpdatePayload):
    async def init(self):
        self.settings = await self.bot.db.get_guild_settings(self.after.id)


class VoiceStateUpdatePayload(UpdatePayload):
    def __init__(self, bot, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        super().__init__(bot, before, after)
        self.member = member

    async def init(self):
        if self.member.guild:
            self.settings = await self.bot.db.get_guild_settings(self.member.guild.id)


class BanPayload(GuildPayload):
    def __init__(self, bot, guild: discord.Guild, user: discord.Member or discord.User):
        super().__init__(bot, guild)
        self.user = user


class UnbanPayload(GuildPayload):
    def __init__(self, bot, guild: discord.Guild, user: discord.User):
        super().__init__(bot, guild)
        self.user = user


class ReactionPayload(SigmaPayload):
    def __init__(self, bot, reaction: discord.Reaction, user: discord.User):
        super().__init__(bot)
        self.reaction = reaction
        self.user = user

    async def init(self):
        if self.reaction.message.guild:
            self.settings = await self.bot.db.get_guild_settings(self.reaction.message.guild.id)


class RawReactionPayload(SigmaPayload):
    def __init__(self, bot, raw: discord.RawReactionActionEvent):
        super().__init__(bot)
        self.raw = raw

    async def init(self):
        self.settings = await self.bot.db.get_guild_settings(self.raw.guild_id)
