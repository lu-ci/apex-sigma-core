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

import json

import aiohttp
import discord

from sigma.core.utilities.generic_responses import error

imgur_icon = 'https://i.imgur.com/SfU0dnX.png'
imgur_url = "https://api.imgur.com/3/image"


async def upload_image(image_url: str, client_id: str):
    """

    :param image_url:
    :type image_url:
    :param client_id:
    :type client_id:
    :return:
    :rtype:
    """
    link = None
    data = {'type': 'URL', 'image': image_url}
    headers = {'Authorization': f'Client-ID {client_id}'}
    async with aiohttp.ClientSession() as session:
        resp = await session.post(imgur_url, data=data, headers=headers)
    img = await resp.read()
    image_data = json.loads(img)
    if image_data.get('status') == 200:
        link = image_data['data']['link']
    return link


async def imgur(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.client_id:
        if pld.args or pld.msg.attachments:
            image_url = pld.msg.attachments[0].url if pld.msg.attachments else pld.args[0]
            link = await upload_image(image_url, cmd.cfg.client_id)
            if link:
                response = discord.Embed(color=0x85BF25)
                response.set_author(name=link, icon_url=imgur_icon, url=link)
            else:
                response = error('Bad image.')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('The API Key is missing.')
    await pld.msg.channel.send(embed=response)
