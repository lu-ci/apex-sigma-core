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

import secrets
from typing import Optional

import discord
import lxml.html as lx

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget
from sigma.modules.searches.vndb.models.visual_novel import VisualNovel

vndb_icon = 'https://i.imgur.com/YrK5tQF.png'


async def get_vn(lookup: str) -> Optional[VisualNovel]:
    vn = None
    result = await get_vn_result(lookup)
    if result is not None:
        vnid = int(result[0][0].attrib.get('href')[2:])
        uri = f'https://vndb.org/v{vnid}'
        page = await aioget(uri)
        page_root = lx.fromstring(page)
        vn = VisualNovel(page_root)
    return vn


async def get_vn_result(lookup: str):
    uri = f'https://vndb.org/v/all?f=&p=1&q={lookup}&s=p0p'
    search_page = await aioget(uri)
    search_root = lx.fromstring(search_page)
    search_results = search_root.cssselect('.imghover')
    highest_elem = None
    highest_score = 0
    for result in search_results:
        parent = result.getparent().getparent()
        ratings = int(parent[-1][-1][-1][-1][-1].text.strip()[1:-1])
        if ratings > highest_score:
            highest_score = ratings
            highest_elem = result
    return highest_elem


async def visualnoveldatabase(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join(pld.args) if pld.args else None
    if lookup:
        vn = await get_vn(lookup)
        if vn is not None:
            nsfw_pass = not vn.nsfw or (vn.nsfw and pld.msg.channel.is_nsfw())
            if nsfw_pass:
                tag_block = ', '.join(vn.tags[:10])
                if len(tag_block) >= 1024:
                    tag_block = f'{tag_block[:1021]}...'
                if len(vn.tags) >= 10:
                    tag_block += '...'
                response = discord.Embed(color=await get_image_colors(vn.image))
                response.set_author(name=vn.title, url=vn.url, icon_url=vndb_icon)
                response.set_thumbnail(url=vn.image)
                response.add_field(name='Tags', value=tag_block, inline=False)
                response.add_field(name='Description', value=vn.description, inline=False)
                if vn.aliases:
                    response.set_footer(text=f'Aliases: {", ".join(vn.aliases)}')
                screen_pool = vn.screenshots
                if vn.nsfw:
                    if len(vn.nsfw_screenshots):
                        screen_pool = vn.nsfw_screenshots
                if len(screen_pool):
                    random_screen = screen_pool.pop(secrets.randbelow(len(screen_pool)))
                    response.set_image(url=random_screen)
            else:
                response = GenericResponse(f'{vn.title} is NSFW but #{pld.msg.channel.name} is not.').error()
        else:
            response = GenericResponse('Couldn\'t find a visual novel by that name.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
