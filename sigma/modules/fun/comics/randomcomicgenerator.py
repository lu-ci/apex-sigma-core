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
from io import BytesIO

import aiohttp
import discord
from PIL import Image

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.tools.color import store_image

comic_api = 'https://explosm.net/api/get-random-panels'
cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'


async def open_images(urls):
    """
    Opens image URLs as BytesIO objects.
    :type urls: list[str]
    :rtype: list[io.BytesIO]
    """
    images = []
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as img_session:
                img_data = await img_session.read()
                images.append(BytesIO(img_data))
    return images


async def join_images(urls):
    """
    Joins three images in a vertical manner.
    :type urls:  list[str]
    :rtype: io.BytesIO
    """
    images = list(map(Image.open, await open_images(urls)))
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    base_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        base_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return store_image(base_im)


async def randomcomicgenerator(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    # noinspection PyTypeChecker
    async with aiohttp.ClientSession(cookies={'explosm': 'nui4hbhpq55tr4ouqknb060jr4'}) as session:
        async with session.get(comic_api) as data:
            try:
                data = json.loads(await data.text())
            except json.JSONDecodeError:
                response = GenericResponse('Failed to grab a comic, try again.').error()
                await pld.msg.channel.send(embed=response)
                return
    slug = ''
    urls = []
    for panel in data.get('panels'):
        slug += panel.get('slug')
        filename = panel.get('filename')
        urls.append(f'https://rcg-cdn.explosm.net/panels/{filename}')
    comic_url = f'https://explosm.net/rcg/{slug}'
    comic = await join_images(urls)
    file = discord.File(comic, f'{pld.msg.id}.png')
    response = discord.Embed(color=0xFF6600)
    response.set_image(url=f'attachment://{pld.msg.id}.png')
    response.set_author(name='Cyanide and Happiness Random Comic Generator', icon_url=cnh_image, url=comic_url)
    await pld.msg.channel.send(file=file, embed=response)
