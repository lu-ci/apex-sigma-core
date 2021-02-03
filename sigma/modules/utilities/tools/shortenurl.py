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

from sigma.core.utilities.generic_responses import GenericResponse


async def shortenurl(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    text_cont = None
    if cmd.cfg.access_token:
        if pld.args:
            if pld.args[-1].lower() == 'text':
                text_mode = True
                long_url = '%20'.join(pld.args[:-1])
            else:
                text_mode = False
                long_url = '%20'.join(pld.args)
            api_url = 'https://api-ssl.bitly.com/v3/shorten'
            api_url += f'?longUrl={long_url}&domain=bit.ly&format=json'
            api_url += f'&access_token={cmd.cfg.access_token}'
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as data:
                    data = await data.read()
                    data = json.loads(data)
            status_code = data['status_code']
            if status_code == 200:
                short_url = data['data']['url']
                if text_mode:
                    response = None
                    text_cont = f'Your URL: <{short_url}>'
                else:
                    response = discord.Embed(color=0x66CC66)
                    response.add_field(name='✅ URL Shortened', value=short_url)
            elif status_code == 500:
                response = GenericResponse('Bad URL.').error()
            else:
                response = GenericResponse(f'Error {status_code} - {data["status_txt"]}.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('No Bit.ly Access Token.').error()
    await pld.msg.channel.send(text_cont, embed=response)
