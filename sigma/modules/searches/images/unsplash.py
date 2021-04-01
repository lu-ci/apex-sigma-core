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

from sigma.core.utilities.generic_responses import GenericResponse

unsplash_icon = 'https://i.imgur.com/jXH3eQ1.png'
api_url = 'https://api.unsplash.com/photos/random'


async def unsplash(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.client_id:
        if pld.args:
            qry = ' '.join(pld.args)
            url = f'https://api.unsplash.com/search/photos?query={qry}&client_id={cmd.cfg.client_id}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data_response:
                    search_data = await data_response.read()
                    search_data = json.loads(search_data)
            data = search_data.get('results')
            if data:
                data = secrets.choice(data)
                user_name = data.get('user', {}).get('name')
                user_link = data.get('user', {}).get('links', {}).get('html')
                response = discord.Embed(color=0x262626)
                response.set_author(name=f'By {user_name}', url=user_link)
                response.set_image(url=data.get('urls', {}).get('raw'))
                response.set_footer(icon_url=unsplash_icon, text='Powered by Unsplash')
            else:
                response = GenericResponse('No results').not_found()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await pld.msg.channel.send(embed=response)
