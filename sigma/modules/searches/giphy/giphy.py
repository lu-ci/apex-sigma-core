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
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found

giphy_icon = 'https://i.imgur.com/tmDySRu.gif'


async def giphy(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.api_key:
        if pld.args:
            qry = ' '.join(pld.args)
            url = f'https://api.giphy.com/v1/gifs/search?q={qry}&api_key={cmd.cfg.api_key}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data_response:
                    search_data = await data_response.read()
                    search_data = json.loads(search_data)
            data = search_data.get('data')
            if data:
                data = secrets.choice(data)
                gif_id = data.get('id')
                gif_url = f'https://media.giphy.com/media/{gif_id}/giphy.gif'
                response = discord.Embed(color=0x262626)
                response.set_image(url=gif_url)
                response.set_footer(icon_url=giphy_icon, text='Powered By GIPHY.')
            else:
                response = not_found('No results')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('The API Key is missing.')
    await pld.msg.channel.send(embed=response)
