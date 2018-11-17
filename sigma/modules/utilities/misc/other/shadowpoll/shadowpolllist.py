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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def shadowpolllist(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        if pld.args[0].startswith('c'):
            lookup = {'origin.channel': pld.msg.channel.id, 'settings.active': True}
        elif pld.args[0].startswith('s'):
            lookup = {'origin.server': pld.msg.guild.id, 'settings.active': True}
        else:
            lookup = {'origin.author': pld.msg.author.id}
    else:
        lookup = {'origin.author': pld.msg.author.id}
    poll_files = await cmd.db[cmd.db.db_nam].ShadowPolls.find(lookup).to_list(None)
    if poll_files:
        response = discord.Embed(color=0xF9F9F9, title='📊 Shadow Poll List')
        list_lines = []
        for poll_file in poll_files:
            list_line = f'`{poll_file["id"]}` - {poll_file["poll"]["question"]}'
            if not poll_file['settings']['active']:
                list_line += ' [!]'
            list_lines.append(list_line)
        poll_list = '\n'.join(list_lines)
        response.description = poll_list
    else:
        response = discord.Embed(color=0x696969, title='🔍 There are no polls.')
    await pld.msg.channel.send(embed=response)
