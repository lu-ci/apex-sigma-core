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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload

fortune_files = []


async def fortune(cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    if not fortune_files:
        fortune_docs = await cmd.db[cmd.db.db_nam].FortuneData.find().to_list(None)
        [fortune_files.append(fd) for fd in fortune_docs if 0 < len(fd) < 800]
    fort = secrets.choice(fortune_files).get('content')
    response = discord.Embed(color=0x8CCAF7)
    response.add_field(name='🔮 Fortune', value=fort)
    await message.channel.send(embed=response)
