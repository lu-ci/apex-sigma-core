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

from io import BytesIO

import discord
from PIL import Image

from sigma.core.utilities.data_processing import rgb_to_hex
from sigma.core.utilities.generic_responses import GenericResponse


def store_image(im):
    """
    :type im: Image
    :rtype: io.BytesIO
    """
    io = BytesIO()
    im.save(io, "PNG")
    io.seek(0)
    return io


def get_color_tuple(args):
    """
    :type args: list
    :rtype: tuple or None
    """
    color_tuple = None
    if len(args) == 1:
        color_input = args[0]
        while color_input.startswith('#'):
            color_input = color_input[1:]
        if len(color_input) == 6:
            try:
                color_tuple = (int(color_input[:2], 16), int(color_input[2:-2], 16), int(color_input[4:], 16))
            except ValueError:
                color_tuple = None
    elif len(args) == 3:
        try:
            color_tuple = (int(args[0]), int(args[1]), int(args[2]))
        except ValueError:
            color_tuple = None
    else:
        color_tuple = None
    return color_tuple


async def color(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    file = None
    if pld.args:
        color_tuple = get_color_tuple(pld.args)
        if color_tuple:
            image = Image.new('RGB', (128, 128), color_tuple)
            image = store_image(image)
            file = discord.File(image, f'{pld.msg.id}.png')
            response = discord.Embed(color=rgb_to_hex(color_tuple))
            response.set_image(url=f'attachment://{pld.msg.id}.png')
        else:
            response = GenericResponse('Invalid input, HEX or RGB sequence, please.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(file=file, embed=response)
