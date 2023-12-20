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

import secrets

import discord

fortune_files = []


async def fortune(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not fortune_files:
        fortune_docs = await cmd.db[cmd.db.db_name].FortuneData.find().to_list(None)
        [fortune_files.append(fd) for fd in fortune_docs if 0 < len(fd) < 800]
    fort = secrets.choice(fortune_files).get('content')
    response = discord.Embed(color=0x8CCAF7)
    response.add_field(name='🔮 Fortune', value=fort)
    await pld.msg.channel.send(embed=response)
