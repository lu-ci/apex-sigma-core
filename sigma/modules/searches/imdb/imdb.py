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

import discord
from lxml import html

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget


async def imdb(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        search = '%20'.join(pld.args)
        api_url = f'http://sg.media-imdb.com/suggests/{search[0].lower()}/{search}.json'
        search_data = await aioget(api_url)
        search_data = search_data.partition('(')[-1][:-1]
        data = json.loads(search_data)
        data = data.get('d')
        if data:
            data = list(filter(lambda x: bool(x.get('qid')), data))
        data = data[0] if data else None

        if data:
            imdb_icon = 'https://ia.media-imdb.com/images/G/01/imdb/images/mobile/'
            imdb_icon += 'apple-touch-icon-web-152x152-1475823641._CB522736557_.png'

            movie_id = data.get('id')
            movie_url = f'http://www.imdb.com/title/{movie_id}/'
            title = data.get('l', 'Unknown')
            staring = data.get('s', 'Unknown')
            staring = ' and'.join(staring.rsplit(',', 1))
            year = data.get('y', 'Unknown')

            response = discord.Embed(color=0xebc12d, title=f'{title} ({year})', url=movie_url)
            response.description = f'\nStaring {staring}'

            page = await aioget(movie_url, headers=cmd.bot.get_agent())
            element = html.fromstring(page).cssselect(".sc-466bb6c-1.dRrIo")
            try:
                response.description = element[0].text
            except (IndexError, AttributeError):
                response.description = 'Unable to get description'

            response.set_footer(text='From the Internet Movie Database', icon_url=imdb_icon)

            image = data.get('i', [None])[0]
            if image:
                response.set_thumbnail(url=image)
        else:
            response = GenericResponse('No results.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
