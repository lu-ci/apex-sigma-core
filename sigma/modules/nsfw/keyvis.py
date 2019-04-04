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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import not_found
from sigma.modules.nsfw.mech.visual_novels import key_vn_list


async def keyvis(_cmd: SigmaCommand, pld: CommandPayload):
    keys = [key for key in key_vn_list]
    choice = pld.args[0].lower() if pld.args else secrets.choice(keys)
    item = key_vn_list.get(choice)
    if item:
        image_number = secrets.randbelow(item[2]) + item[1]
        url_base = 'https://vncg.org'
        image_url = f'{url_base}/f{image_number}.jpg'
        response = discord.Embed(color=0x744EAA)
        response.set_image(url=image_url)
    else:
        response = not_found('No results.')
    await pld.msg.channel.send(embed=response)
