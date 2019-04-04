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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.utilities.mathematics.combinechains import combine_names


async def combinenames(_cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.msg.mentions) >= 2:
        combined_name = combine_names(pld.msg.mentions)
        response = discord.Embed(color=0x3B88C3, title=f'🔤 I dub thee... {combined_name}!')
    else:
        response = error('Invalid number of targets.')
    await pld.msg.channel.send(embed=response)
