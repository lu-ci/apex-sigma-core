# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
from PIL import Image


async def color(cmd, message, args):
    if args:
        if len(args) == 1:
            color_input = args[0]
            while color_input.startswith('#'):
                color_input = color_input[1:]
            if len(color_input) == 6:
                try:
                    color_tupple = (int(color_input[:2], 16), int(color_input[2:-2], 16), int(color_input[4:], 16))
                    response = None
                    image = Image.new('RGB', (128, 128), color_tupple)
                    image.save(f'cache/{message.id}.png')
                except ValueError:
                    response = discord.Embed(color=0xBE1931, title='❗ Something here is not a number.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid HEX color code.')
        elif len(args) == 3:
            try:
                color_tupple = (int(args[0]), int(args[1]), int(args[2]))
                response = None
                image = Image.new('RGB', (128, 128), color_tupple)
                image.save(f'cache/{message.id}.png')
            except ValueError:
                response = discord.Embed(color=0xBE1931, title='❗ Something here is not a number.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid input, HEX or RGB sequence, please.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    if response:
        await message.channel.send(embed=response)
    else:
        img_file = discord.File(f'cache/{message.id}.png')
        await message.channel.send(file=img_file)
        os.remove(f'cache/{message.id}.png')
