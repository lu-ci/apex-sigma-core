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

import discord


class SigmaPayload(abc.ABC):
    """
    The base abstraction class for payload data.
    """

    def __init__(self, bot):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.settings = {}

    async def init(self):
        """
        An asyncronous init method in case the class
        needs to parse something in an asyncronous task loop.
        :return:
        :rtype:
        """
        pass


class UpdatePayload(SigmaPayload):
    """
    Another abstraction base for payloads
    that are generated from update/edit events
    such as user profile, guild settings or message edits.
    """

    def __init__(self, bot, before, after):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.ApexSigma
        :param before: An object as it was before a change.
        :type before: discord.Message or discord.Member or discord.Guild or discord.VoiceState
        :param after: An object as it is after a change.
        :type after: discord.Message or discord.Member or discord.Guild or discord.VoiceState
        """
        super().__init__(bot)
        self.before = before
        self.after = after


class ShardReadyPayload(SigmaPayload):
    """
    Payload generated when a shard is ready.
    """

    def __init__(self, bot, shard):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.ApexSigma
        :param shard: The Shard ID.
        :type shard: int
        """
        super().__init__(bot)
        self.shard = shard


class MessagePayload(SigmaPayload):
    """
    Payload generated when a message is sent.
    """

    def __init__(self, bot, msg):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.ApexSigma
        :param msg: The event message class.
        :type msg: discord.Message
        """
        super().__init__(bot)
        self.msg = msg

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload
        if the message came from a guild and not a DM.
        :return:
        :rtype:
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
        :return:
        :rtype:
        """
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class CommandPayload(MessagePayload):
    """
    Payload generated for command execution.
    """

    def __init__(self, bot, msg, args):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param msg: The message that triggered the command.
        :type msg: discord.Message
        :param args: The arguments passed in the command.
        :type args: list[str]
        """
        super().__init__(bot, msg)
        self.args = args


class CommandEventPayload(CommandPayload):
    """
    Payload generated when a command is executed.
    """

    def __init__(self, bot, cmd, pld):
        """
        :param bot: The core client class.
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

    def __init__(self, bot, member):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param member: The member that triggered the event.
        :type member: discord.Member
        """
        super().__init__(bot)
        self.member = member

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        :return:
        :rtype:
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
        :return:
        :rtype:
        """
        if self.after.guild:
            self.settings = await self.bot.db.get_guild_settings(self.after.guild.id)


class GuildPayload(SigmaPayload):
    """
    Base abstraction class for payloads that use guild data.
    """

    def __init__(self, bot, guild):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param guild: The guild that triggered the event.
        :type guild: discord.Guild
        """
        super().__init__(bot)
        self.guild = guild

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        :return:
        :rtype:
        """
        self.settings = await self.bot.db.get_guild_settings(self.guild.id)


class GuildUpdatePayload(UpdatePayload):
    """
    Payload generated when a guild's settings are changed.
    """

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        :return:
        :rtype:
        """
        self.settings = await self.bot.db.get_guild_settings(self.after.id)


class VoiceStateUpdatePayload(UpdatePayload):
    """
    Payload generated when a member changes their voice state.
    """

    def __init__(self, bot, member, before, after):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param member: The member that had their state changed.
        :type member: discord.Member
        :param before: The member's previous voice state.
        :type before: discord.VoiceState
        :param after: The member's voice state after the change.
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

    def __init__(self, bot, guild, user):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param guild: The guild a user was banned from.
        :type guild: discord.Guild
        :param user: The user that was banned.
        :type user: discord.Member or discord.User
        """
        super().__init__(bot, guild)
        self.user = user


class UnbanPayload(GuildPayload):
    """
    Payload generated when a member is unbanned.
    """

    def __init__(self, bot, guild, user):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param guild: The guild the user was unbanned from.
        :type guild: discord.Guild
        :param user: The user that was unbanned.
        :type user: discord.User
        """
        super().__init__(bot, guild)
        self.user = user


class ReactionPayload(SigmaPayload):
    """
    Payload generated when a reaction event triggers it.
    """

    def __init__(self, bot, reaction, user):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param reaction: The reaction that was added.
        :type reaction: discord.Reaction
        :param user: The user that added the reaction.
        :type user: discord.User
        """
        super().__init__(bot)
        self.reaction = reaction
        self.user = user

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        :return:
        :rtype:
        """
        if self.reaction.message.guild:
            self.settings = await self.bot.db.get_guild_settings(self.reaction.message.guild.id)


class RawReactionPayload(SigmaPayload):
    """
    Payload generated when a reaction is added regardless
    of its message being cached or not.
    """

    def __init__(self, bot, raw):
        """
        :param bot: The core client class.
        :type bot: sigma.core.sigma.Apexsigma
        :param raw: The raw reaction wrapper class.
        :type raw: discord.RawReactionActionEvent
        """
        super().__init__(bot)
        self.raw = raw

    async def init(self):
        """
        Processes the guild's settings and adds them to the payload.
        :return:
        :rtype:
        """
        self.settings = await self.bot.db.get_guild_settings(self.raw.guild_id)
