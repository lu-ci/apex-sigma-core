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

import discord
import lxml.html as lx

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import error, not_found
from sigma.core.utilities.url_processing import aioget
from sigma.modules.searches.vndb.models.visual_novel import VisualNovel

vndb_icon = 'https://i.imgur.com/YrK5tQF.png'


def get_name_match(results: list, lookup: str):
    """

    :param results:
    :type results:
    :param lookup:
    :type lookup:
    :return:
    :rtype:
    """
    match = None
    results = results[1:]
    if len(results):
        for result in results:
            try:
                vn_name = result[0].text
                if vn_name.lower() == lookup.lower():
                    match = f"https://vndb.org/{result[0].attrib.get('href')}"
                    break
            except IndexError:
                pass
        if match is None:
            match = f"https://vndb.org/{results[0][0].attrib.get('href')}"
    return match


async def get_details_page(lookup: str):
    """

    :param lookup:
    :type lookup:
    :return:
    :rtype:
    """
    if lookup == '--random':
        lookup = secrets.randbelow(25261) + 1
    try:
        int(lookup)
        page_url = f'https://vndb.org/v{lookup}'
    except ValueError:
        page_url = f'https://vndb.org/v/all?q={lookup};fil=tagspoil-0;rfil=;o=d;s=pop'
    search_page = await aioget(page_url)
    search_page_root = lx.fromstring(search_page)
    if not search_page_root.cssselect('.vnimg'):
        results = search_page_root.cssselect('.tc1')
        search_page_root = None
        if results:
            search_url = get_name_match(results, lookup)
            if search_url:
                search_page = await aioget(search_url)
                search_page_root = lx.fromstring(search_page)
    return search_page_root


async def get_vn(lookup: str):
    """

    :param lookup:
    :type lookup:
    :return:
    :rtype:
    """
    vn_data = None
    page_root = await get_details_page(lookup)
    if page_root is not None:
        vn_data = VisualNovel(page_root)
    return vn_data


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
                response = error(f'{vn.title} is NSFW but #{pld.msg.channel.name} is not.')
        else:
            response = not_found('Couldn\'t find a visual novel by that name.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
