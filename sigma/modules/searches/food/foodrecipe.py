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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found


async def foodrecipe(cmd: SigmaCommand, pld: CommandPayload):
    if cmd.cfg.api_key:
        if pld.args:
            search = ' '.join(pld.args)
            url = f'http://food2fork.com/api/search?key={cmd.cfg.api_key}&q={search}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data:
                    search_data = await data.read()
                    search_data = json.loads(search_data)
            count = search_data['count']
            if count == 0:
                response = not_found('No results.')
            else:
                info = search_data['recipes'][0]
                title = info['title']
                source = info['publisher']
                source_url = info['source_url']
                image_url = info['image_url']
                publisher_url = info['publisher_url']
                response = discord.Embed(color=0xee5b2f)
                response.set_author(name=source, url=publisher_url, icon_url='https://i.imgur.com/RH8LNdQ.png')
                response.add_field(name=title, value='[Recipe Here](' + source_url + ')')
                response.set_thumbnail(url=image_url)
        else:
            response = error('Nothing inputted.')
    else:
        response = error('The API Key is missing.')
    await pld.msg.channel.send(embed=response)
