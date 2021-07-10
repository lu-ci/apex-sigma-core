"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import abc


class SigmaPayload(abc.ABC):
    """
    The base abstraction class for payload data.
    """

    __slots__ = ("bot", "settings")

    def __init__(self, bot):
        """
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.settings = {}

    async def init(self):
        """
        An asyncronous init method in case the class
        needs to parse something in an asyncronous task loop.
        """
        pass


class UpdatePayload(SigmaPayload):
    """
    Another abstraction base for payloads
    that are generated from update/edit events
    such as user profile, guild settings or message edits.
    """

    __slots__ = ("before", "after")

    def __init__(self, bot, before, after):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :type before: discord.Message or discord.Member or discord.Guild or discord.VoiceState
        :type after: discord.Message or discord.Member or discord.Guild or discord.VoiceState
        """
        super().__init__(bot)
        self.before = before
        self.after = after


class ShardReadyPayload(SigmaPayload):
    """
    Payload generated when a shard is ready.
    """

    __slots__ = ("shard",)

    def __init__(self, bot, shard):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :type shard: int
        """
        super().__init__(bot)
        self.shard = shard


class MessagePayload(SigmaPayload):
    """
    Payload generated when a message is sent.
    """

    __slots__ = ("msg",)

    def __init__(self, bot, msg):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :type msg: discord.Message
        """
        super().__init__(bot)
        self.msg = msg

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload
        if the message came from a guild and not a DM.
        """
        if self.msg.guild:
            self.settings = await self.bot.db.get_guild_settings(self.msg.guild.id)


class MessageEditPayload(UpdatePayload):
    """
    Payload generated when a message is edited.
    """

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload
        if the message came from a guild and not a DM.
        """
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class CommandPayload(MessagePayload):
    """
    Payload generated for command execution.
    """

    __slots__ = ("args",)

    def __init__(self, bot, msg, args):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type msg: discord.Message
        :type args: list[str]
        """
        super().__init__(bot, msg)
        self.args = args


class CommandEventPayload(CommandPayload):
    """
    Payload generated when a command is executed.
    """

    __slots__ = ("cmd",)

    def __init__(self, bot, cmd, pld):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :param cmd: The command that was executed.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        :param pld: The command's payload data.
        :type pld: sigma.core.mechanics.payload.CommandPayload
        """
        super().__init__(bot, pld.msg, pld.args)
        self.cmd = cmd


class MemberPayload(SigmaPayload):
    """
    Base abstraction class for payloads containing member data.
    """

    __slots__ = ("member",)

    def __init__(self, bot, member):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type member: discord.Member
        """
        super().__init__(bot)
        self.member = member

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        if self.member.guild:
            self.settings = await self.bot.db.get_guild_settings(self.member.guild.id)


class MemberUpdatePayload(UpdatePayload):
    """
    Payload generated when a member is updated.
    This is a very broad event and can be cause by the member
    changing their online status, name, nickname, avatar, etc.
    """

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class GuildPayload(SigmaPayload):
    """
    Base abstraction class for payloads that use guild data.
    """

    __slots__ = ("guild",)

    def __init__(self, bot, guild):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type guild: discord.Guild
        """
        super().__init__(bot)
        self.guild = guild

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        self.settings = await self.bot.db.get_guild_settings(self.guild.id)


class GuildUpdatePayload(UpdatePayload):
    """
    Payload generated when a guild's settings are changed.
    """

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        self.settings = await self.bot.db.get_guild_settings(self.after.id)


class VoiceStateUpdatePayload(UpdatePayload):
    """
    Payload generated when a member changes their voice state.
    """

    __slots__ = ("member",)

    def __init__(self, bot, member, before, after):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type member: discord.Member
        :type before: discord.VoiceState
        :type after: discord.VoiceState
        """
        super().__init__(bot, before, after)
        self.member = member

    async def init(self):
        if self.member.guild:
            self.settings = await self.bot.db.get_guild_settings(self.member.guild.id)


class BanPayload(GuildPayload):
    """
    Payload generated when a member is banned from a guild.
    """

    __slots__ = ("user",)

    def __init__(self, bot, guild, user):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type guild: discord.Guild
        :type user: discord.Member or discord.User
        """
        super().__init__(bot, guild)
        self.user = user


class UnbanPayload(GuildPayload):
    """
    Payload generated when a member is unbanned.
    """

    __slots__ = ("user",)

    def __init__(self, bot, guild, user):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type guild: discord.Guild
        :type user: discord.User
        """
        super().__init__(bot, guild)
        self.user = user


class ReactionPayload(SigmaPayload):
    """
    Payload generated when a reaction event triggers it.
    """

    __slots__ = ("user", "reaction")

    def __init__(self, bot, reaction, user):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type reaction: discord.Reaction
        :type user: discord.User
        """
        super().__init__(bot)
        self.reaction = reaction
        self.user = user

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        if self.reaction.message.guild:
            self.settings = await self.bot.db.get_guild_settings(self.reaction.message.guild.id)


class RawReactionPayload(SigmaPayload):
    """
    Payload generated when a reaction is added regardless
    of its message being cached or not.
    """

    __slots__ = ("raw",)

    def __init__(self, bot, raw):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type raw: discord.RawReactionActionEvent
        """
        super().__init__(bot)
        self.raw = raw

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        self.settings = await self.bot.db.get_guild_settings(self.raw.guild_id)


class RawMessageDeletePayload(SigmaPayload):
    """
    Payload generated when a message is deleted
    regardless of it being cached or not.
    """

    __slots__ = ("raw",)

    def __init__(self, bot, raw):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type raw: discord.RawMessageDeleteEvent
        """
        super().__init__(bot)
        self.raw = raw

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        self.settings = await self.bot.db.get_guild_settings(self.raw.guild_id)


class RawMessageEditPayload(SigmaPayload):
    """
    Payload generated when a message is edited
    regardless of it being cached or not.
    """
    __slots__ = ("raw",)

    def __init__(self, bot, raw):
        """
        :type bot: sigma.core.sigma.Apexsigma
        :type raw: discord.RawMessageUpdateEvent
        """
        super().__init__(bot)
        self.raw = raw

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        """
        self.settings = await self.bot.db.get_guild_settings(self.raw.guild_id)
