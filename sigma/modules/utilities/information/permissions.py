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


async def permissions(_cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    allowed_list = []
    disallowed_list = []
    if message.mentions:
        user_q = message.mentions[0]
    else:
        user_q = message.author
    response = discord.Embed(color=0x3B88C3, title=f'ℹ {user_q.name}\'s Permissions')
    for permission in user_q.guild_permissions:
        if permission[1]:
            allowed_list.append(permission[0].replace('_', ' ').title())
        else:
            disallowed_list.append(permission[0].replace('_', ' ').title())
    if len(allowed_list) == 0:
        allowed_list = ['None']
    if len(disallowed_list) == 0:
        disallowed_list = ['None']
    response.add_field(name='Allowed', value='```yml\n - ' + '\n - '.join(sorted(allowed_list)) + '\n```')
    response.add_field(name='Disallowed', value='```yml\n - ' + '\n - '.join(sorted(disallowed_list)) + '\n```')
    in_ch = discord.Embed(color=0x66CC66, title='✅ Permission list sent to you.')
    await message.author.send(embed=response)
    await message.channel.send(embed=in_ch)
