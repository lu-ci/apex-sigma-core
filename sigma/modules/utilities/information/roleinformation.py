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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found


async def roleinformation(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        lookup = ' '.join(pld.args)
        role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), pld.msg.guild.roles)
        if role:
            creation_time = arrow.get(role.created_at).format('DD. MMMM YYYY')
            desc_text = f'Name: **{role.name}**'
            desc_text += f'\nID: **{role.id}**'
            desc_text += f'\nColor: **{str(role.color).upper()}**'
            desc_text += f'\nHoisted: **{role.hoist}**'
            desc_text += f'\nMembers: **{len(role.members)}**'
            desc_text += f'\nCreated: **{creation_time}**'
            response = discord.Embed(color=role.color)
            response.add_field(name=f'{role.name} Information', value=desc_text)
        else:
            response = not_found(f'{lookup} not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
