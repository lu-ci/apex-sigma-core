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

import os

import discord
import secrets
from PIL import Image

from sigma.core.mechanics.command import SigmaCommand


async def randomcolor(cmd: SigmaCommand, message: discord.Message, args: list):
    piece_r = secrets.randbelow(256)
    piece_g = secrets.randbelow(256)
    piece_b = secrets.randbelow(256)
    color_tupple = (piece_r, piece_g, piece_b)
    hexname = f'Color: `#{str(hex(piece_r))[2:]}{str(hex(piece_g))[2:]}{str(hex(piece_b))[2:]}`'
    image = Image.new('RGB', (128, 128), color_tupple)
    image.save(f'cache/{message.id}.png')
    img_file = discord.File(f'cache/{message.id}.png')
    await message.channel.send(hexname, file=img_file)
    os.remove(f'cache/{message.id}.png')
