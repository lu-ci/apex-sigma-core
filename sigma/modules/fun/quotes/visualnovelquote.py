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

import discord
import lxml.html as lx

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget

source_page = 'https://vndb.org/r'
vndb_icon = 'https://i.imgur.com/YrK5tQF.png'


def is_vn_thumbnail_nsfw(vn_page: lx.HtmlElement) -> bool:
    try:
        image = vn_page.cssselect('.vnimg')[0][0][0][0].attrib.get('src')
    except IndexError:
        image = None
    nsfw = image is None
    return nsfw


def is_vn_rating_nsfw(vn_page: lx.HtmlElement) -> bool:
    release_tables = vn_page.cssselect('.releases')
    ratings = {}
    if len(release_tables) != 0:
        for table in release_tables:
            for row in table:
                rating = row[1].text_content().strip()
                rating_num = ''
                if 'all' in rating.lower():
                    rating_num = '0'
                else:
                    for char in rating:
                        if char.isdigit():
                            rating_num += char
                if not rating_num:
                    rating_num = '0'
                coutner = ratings.get(rating_num, 0)
                ratings[rating_num] = coutner + 1
    nsfw_ratings = ratings.get('18', 0)
    other_ratings = 0
    for key in ratings:
        if key != '18':
            other_ratings += ratings[key]
    nsfw = nsfw_ratings > other_ratings
    return nsfw


def is_vn_nsfw(vn_page: lx.HtmlElement) -> bool:
    return is_vn_rating_nsfw(vn_page) or is_vn_thumbnail_nsfw(vn_page)


async def get_vn_page(uri: str) -> lx.HtmlElement:
    return lx.fromstring(await aioget(uri))


async def get_vn_quote() -> tuple[str, str]:
    body = await aioget('https://vndb.org/r')
    page = lx.fromstring(body)
    footer_quote = page.cssselect('footer a')[0]
    quote_text = footer_quote.text_content().strip()
    quote_url = f"https://vndb.org{footer_quote.attrib['href']}"
    return quote_text, quote_url


def get_title(vn_page: lx.HtmlElement) -> str:
    out = None
    details = vn_page.cssselect('.vndetails')[0]
    detail_table = details[1]
    titles = detail_table.cssselect('.title')
    # Try english first.
    for title in titles:
        lang = title[1][0].attrib.get('lang')
        if lang is None:
            out = title[1][0].text.strip()
            break
    if out is None:
        for title in titles:
            lang = title[1][0].attrib.get('lang')
            if lang == 'ja':
                out = title[1][0].text.strip()
                break
    return out


def get_image(vn_page: lx.HtmlElement) -> str:
    try:
        image = vn_page.cssselect('.vnimg')[0][0][0][0].attrib.get('src')
    except IndexError:
        image = vn_page.cssselect('.vnimg')[0][0][1][0].attrib.get('src')
    return image


async def visualnovelquote(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    accept_nsfw = pld.msg.channel.is_nsfw()
    accepted = False
    vn_page = None
    quote_text = None
    quote_url = None
    tries = 0
    while not accepted and tries < 10:
        tries += 1
        quote_text, quote_url = await get_vn_quote()
        vn_page = await get_vn_page(quote_url)
        if is_vn_nsfw(vn_page):
            if accept_nsfw:
                accepted = True
            else:
                accepted = False
        else:
            accepted = True
    if vn_page is not None and accepted:
        vn_title = get_title(vn_page)
        vn_image = get_image(vn_page)
        response = discord.Embed(color=0x225588)
        response.set_author(name=vn_title, url=quote_url, icon_url=vndb_icon)
        response.description = quote_text
        response.set_thumbnail(url=vn_image)
        if is_vn_nsfw(vn_page):
            response.set_footer(text='Warning: This VN is NSFW.')
    else:
        response = GenericResponse(f'Could not find an adequate VN in {tries} tries.').error()
    await pld.msg.channel.send(embed=response)
