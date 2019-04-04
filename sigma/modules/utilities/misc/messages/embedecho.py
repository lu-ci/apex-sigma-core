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
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error


async def embedecho(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        response = discord.Embed(color=pld.msg.author.color, timestamp=pld.msg.created_at)
        response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
        response.description = f'{" ".join(pld.args)[:800]}'
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
