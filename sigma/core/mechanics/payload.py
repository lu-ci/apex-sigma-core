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

import abc

import discord


class SigmaPayload(abc.ABC):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}
        self.profile = {}

    async def init(self):
        pass


class MessagePayload(SigmaPayload):
    def __init__(self, bot, msg: discord.Message):
        super().__init__(bot)
        self.msg = msg

    async def init(self):
        self.profile = await self.bot.db.get_profile(self.msg.author.id)
        if self.msg.guild:
            self.settings = await self.bot.db.get_guild_settings(self.msg.guild.id)


class CommandPayload(MessagePayload):
    def __init__(self, bot, msg: discord.Message, args: list):
        super().__init__(bot, msg)
        self.args = args


