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

import aiohttp
import discord
from lxml import html

from sigma.core.utilities.generic_responses import GenericResponse


async def leetspeak(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        levels = ['basic', 'advanced', 'ultimate']
        if pld.args[-1].startswith('level:'):
            level = pld.args[-1].split(':')[1].lower()
            text = ' '.join(pld.args[:-1])
            if level not in levels:
                level = None
        else:
            text = ' '.join(pld.args)
            level = 'basic'
        if level:
            leet_url = 'http://www.robertecker.com/hp/research/leet-converter.php?lang=en'
            data = {
                'textbox_input': text,
                'language': 'en',
                'encode': 'encode',
                'modus': level
            }
            async with aiohttp.ClientSession() as session:
                api_data = await session.post(leet_url, data=data)
                page = await api_data.text()
                page = html.fromstring(page)
                table = page.cssselect('.mytable')
                text = table[0][0][1][2].text_content()
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name=f'🔣 {level.title()} L33t Converter', value=text)
        else:
            response = GenericResponse('Invalid l33t level.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
