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

import datetime
import json
import secrets

import aiohttp
import discord

from sigma.core.utilities.generic_responses import error, not_found


async def deezer(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        search = '%20'.join(pld.args)
        qry_url = f'http://api.deezer.com/search/track?q={search}'
        async with aiohttp.ClientSession() as session:
            async with session.get(qry_url) as data:
                data = await data.read()
                data = json.loads(data)
                data = data['data']
        if data:
            data = data[0]
            track_url = data['link']
            track_title = data['title_short']
            track_duration = data['duration']
            preview_url = data['preview']
            artist_name = data['artist']['name']
            artist_image = data['artist']['picture_medium']
            album_title = data['album']['title']
            album_image = data['album']['cover_medium']
            deezer_icon = 'http://e-cdn-files.deezer.com/images/common/favicon/favicon-96x96-v00400045.png'
            deezer_colors = [0xff0000, 0xffed00, 0xff0092, 0xbed62f, 0x00c7f2]
            deezer_color = secrets.choice(deezer_colors)
            song_desc = f'Preview: [Here]({preview_url})'
            song_desc += f'\nDuration: {datetime.timedelta(seconds=track_duration)}'
            response = discord.Embed(color=deezer_color)
            response.set_author(name=artist_name, icon_url=artist_image, url=track_url)
            response.add_field(name=f'{track_title}', value=song_desc)
            response.set_thumbnail(url=album_image)
            response.set_footer(icon_url=deezer_icon, text=f'Album: {album_title}')
        else:
            response = not_found('No results.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
