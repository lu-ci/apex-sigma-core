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
import lxml.html as lx

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import error


async def get_url_body(url: str):
    """

    :param url:
    :type url:
    :return:
    :rtype:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
    return data


def parse_parts(lyr: str):
    """

    :param lyr:
    :type lyr:
    :return:
    :rtype:
    """
    pieces = []
    lines = lyr.split('\n')
    chunk = []
    for line in lines:
        if sum(len(c) for c in chunk) + len(line) >= 1024:
            pieces.append("\n".join(chunk))
            chunk = [line]
        else:
            chunk.append(line)
    if chunk:
        pieces.append("\n".join(chunk))
    return pieces


async def get_lyrics_from_html(lyrics_url: str):
    """

    :param lyrics_url:
    :type lyrics_url:
    :return:
    :rtype:
    """
    lyrics_text = None
    artist = None
    song = None
    thumbnail = None
    if lyrics_url:
        lyric_page_html = await get_url_body(lyrics_url)
        if lyric_page_html:
            lyrics_page = lx.fromstring(lyric_page_html)
            lyric_section = lyrics_page.cssselect('.lyrics')
            if lyric_section:
                lyrics_text = lyric_section[0][1].text_content()
                thumbnail = lyrics_page.cssselect('.cover_art-image')[0].attrib.get('src')
                artist = lyrics_page.cssselect('.header_with_cover_art-primary_info-primary_artist')[0].text
                song = lyrics_page.cssselect('.header_with_cover_art-primary_info-title')[0].text
    return lyrics_text, artist, song, thumbnail


def find_result(resp: dict):
    """

    :param resp:
    :type resp:
    :return:
    :rtype:
    """
    lyr_url = None
    resp = resp or {}
    results = resp.get('response', {}).get('sections', [{}])
    hits = results[0].get('hits')
    for hit in hits:
        if hit.get('type') == 'song':
            lyr_url = hit.get('result', {}).get('url')
            break
    return lyr_url


async def lyrics(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        query = ' '.join(pld.args)
    elif cmd.bot.music.currents.get(pld.msg.guild.id):
        query = cmd.bot.music.currents.get(pld.msg.guild.id).title
    else:
        query = None
    if query:
        api_url = f'https://genius.com/api/search/multi?q={query.lower()}'
        search_data = await get_url_body(api_url)
        search_data = json.loads(search_data)
        lyrics_url = find_result(search_data)
        lyrics_data, artist, song, image = await get_lyrics_from_html(lyrics_url)
        if lyrics_data:
            chunks = parse_parts(lyrics_data)
            chunk_counter = 0
            for chunk in chunks[:5]:
                chunk_counter += 1
                chunk_title = f'🔖 Lyrics for {song} by {artist}'
                response = discord.Embed(color=await get_image_colors(image), title=chunk_title)
                response.description = chunk
                response.set_thumbnail(url=image)
                if len(chunks) != 1:
                    response.set_footer(text=f'Page: {chunk_counter}/{len(chunks)}')
                await pld.msg.channel.send(embed=response)
            if len(chunks) > 5:
                end_title = 'Lyrics too long to display in their entirety.'
                end_desc = f'View the full list of lyrics [here]({lyrics_url}).'
                response = discord.Embed(color=await get_image_colors(image), title=end_title, description=end_desc)
                await pld.msg.channel.send(embed=response)
            return
        else:
            response = error(f'Nothing found for {query}.')
    else:
        response = error('No song information given, and nothing currently playing.')
    await pld.msg.channel.send(embed=response)
