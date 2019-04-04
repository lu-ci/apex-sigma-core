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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found


async def urbandictionary(cmd: SigmaCommand, pld: CommandPayload):
    if cmd.cfg.api_key:
        if pld.args:
            ud_input = ' '.join(pld.args).lower()
            url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
            headers = {'X-Mashape-Key': cmd.cfg.api_key, 'Accept': 'text/plain'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as data_response:
                    data = await data_response.read()
                    data = json.loads(data)
            if data.get('list'):
                entry = data.get('list', [{}])[0]
                definition = entry.get('definition', 'Nothing...')
                if len(definition) > 1000:
                    definition = definition[:1000] + '...'
                example = entry.get('example', 'Nothing...')
                if len(example) > 1000:
                    example = example[:1000] + '...'
                definition, example = list(map(lambda i: i.replace('[', '').replace(']', ''), [definition, example]))
                response = discord.Embed(color=0xe27e00, title=f'🥃 Urban Dictionary: {ud_input.upper()}')
                response.set_footer(text=f'Thumbs Up/Down: {entry.get("thumbs_up", 0)}/{entry.get("thumbs_down", 0)}')
                response.add_field(name='Definition', value=definition)
                if example:
                    response.add_field(name='Usage Example', value=example)
            else:
                response = not_found('Unable to find exact results.')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('The API Key is missing.')
    await pld.msg.channel.send(embed=response)
