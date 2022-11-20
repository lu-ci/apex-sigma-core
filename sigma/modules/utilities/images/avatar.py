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

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.utilities.misc.other.edgecalculator import hexify_int


async def avatar(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    static = False
    if pld.args:
        if pld.args[-1].lower() == 'static':
            static = True
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
    else:
        target = pld.msg.author
    ava_url = user_avatar(target, static)
    color = await get_image_colors(ava_url)
    response = discord.Embed(color=color)
    response.description = f'Dominant Color: #{hexify_int(color)}'
    response.set_image(url=ava_url)
    await pld.msg.channel.send(embed=response)
