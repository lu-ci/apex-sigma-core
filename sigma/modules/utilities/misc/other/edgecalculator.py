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

import string

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import get_image_colors, user_avatar


def hexify_int(value: int):
    hexpiece = hex(value)[2:]
    while len(hexpiece) < 6:
        hexpiece = f'0{hexpiece}'
    return hexpiece


def hex_to_rgb(hexval: str):
    return [int(hexval[:2], 16), int(hexval[2:-2], 16), int(hexval[-2:], 16)]


async def edgecalculator(_cmd: SigmaCommand, pld: CommandPayload):
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    avatar = user_avatar(target)
    name = target.name
    username_edge = ((len(name) - len([c for c in name if c not in string.ascii_letters])) / len(name)) * 30
    image_edge = ((765 - sum(hex_to_rgb(hexify_int(await get_image_colors(avatar))))) / 765) * 60
    color_edge = ((765 - sum(hex_to_rgb(hexify_int(target.color.value)))) / 765) * 10
    total_edge = round(image_edge + color_edge + username_edge, 2)
    bar_len = int(20 * (total_edge / 100))
    empty_len = 20 - bar_len
    edge_bar = f'[{"▣" * bar_len}{"▢" * empty_len}] {total_edge}%'
    response = discord.Embed(color=target.color)
    response.description = f'```py\n{edge_bar}\n```'
    response.set_author(name=f'{name}\'s Edge Results', icon_url=avatar)
    await pld.msg.channel.send(embed=response)
