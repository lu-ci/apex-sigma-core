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
from PIL import Image

from sigma.modules.utilities.tools.color import store_image


async def randomcolor(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    piece_r = secrets.randbelow(256)
    piece_g = secrets.randbelow(256)
    piece_b = secrets.randbelow(256)
    color_tupple = (piece_r, piece_g, piece_b)
    hexname = f'Color: `#{str(hex(piece_r))[2:]}{str(hex(piece_g))[2:]}{str(hex(piece_b))[2:]}`'
    image = Image.new('RGB', (128, 128), color_tupple)
    image = store_image(image)
    file = discord.File(image, f'{pld.msg.id}.png')
    await pld.msg.channel.send(hexname, file=file)
