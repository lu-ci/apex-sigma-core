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
from sigma.core.utilities.generic_responses import GenericResponse


async def get_url_body(url):
    """
    :type url: str
    :rtype: bytes
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
    return data


def parse_parts(lyr, fallback=False):
    """
    :type lyr: str
    :type fallback: bool
    :rtype: list[str]
    """
    pieces = []
    lines = lyr.split('.' if fallback else '\n')
    chunk = []
    for line in lines:
        if sum(len(c) for c in chunk) + len(line) + (1 + len(chunk)) >= 1024:
            pieces.append("\n".join(chunk))
            chunk = [line]
        else:
            chunk.append(line)
    if chunk:
        pieces.append("\n".join(chunk))
    if any([len(piece) > 1024 for piece in pieces]) and not fallback:
        output = parse_parts('\n'.join(pieces), True)
    else:
        output = pieces
    return output


async def get_lyrics_from_html(lyrics_url):
    """
    :type lyrics_url: str
    :rtype: str, str, str, str
    """
    lyrics_text = None
    artist = None
    song = None
    thumbnail = None
    if lyrics_url:
        lyric_page_html = await get_url_body(lyrics_url)
        if lyric_page_html:
            try:
                lyrics_page = lx.fromstring(lyric_page_html)
                lyric_section = lyrics_page.cssselect('[class*=Lyrics__Root]')
                if not lyric_section:
                    lyric_section = lyrics_page.cssselect('[class=lyrics]')
                if lyric_section:
                    lyric_section = lyric_section[0]
                    for br in lyric_section.xpath('*//br'):
                        br.tail = '\n' + br.tail if br.tail else '\n'
                    lyric_footer = lyric_section.cssselect('[class^=Lyrics__Footer]')[0]
                    lyric_section.remove(lyric_footer)
                    lyrics_text = lyric_section.text_content()
                    thumbnail = lyrics_page.cssselect('[class^=PrimaryAlbum__CoverArt]')[0][0][0][0].attrib.get('src')
                    artist = lyrics_page.cssselect('[class*=SongHeader__Artist]')[0].text
                    song = lyrics_page.cssselect('[class^=SongHeader__Title]')[0].text
            except (AttributeError, IndexError):
                pass
    return lyrics_text, artist, song, thumbnail


def find_result(resp):
    """
    :type resp: dict
    :rtype: str
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
    text_only = cmd.bot.cfg.pref.text_only
    if pld.args:
        query = ' '.join(pld.args)
    elif not text_only and cmd.bot.music.currents.get(pld.msg.guild.id):
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
            if len(chunks) > 5:
                end_title = 'Lyrics too long to display in their entirety.'
                end_desc = f'View the full list of lyrics [here]({lyrics_url}).'
                response = discord.Embed(color=await get_image_colors(image), title=end_title, description=end_desc)
                await pld.msg.channel.send(embed=response)
            else:
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
            return
        else:
            response = GenericResponse(f'Nothing found for {query}.').error()
    else:
        if not text_only:
            response = GenericResponse('No song information given, and nothing currently playing.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
