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

import discord

from sigma.core.utilities.generic_responses import error, not_found


def get_average(dislikes, likes):
    """
    :param dislikes: The amount of dislikes the video has.
    :type dislikes: int
    :param likes: The amount of likes the video has.
    :type likes: int
    :rtype: float
    """
    dislikes = dislikes or 0
    likes = likes or 0
    total = likes + dislikes
    try:
        bad = (dislikes / total) * 5
    except ZeroDivisionError:
        bad = 0
    average = 5 - bad
    return round(average, 2)


async def youtube(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    yt_icon = 'https://i.imgur.com/qoH1MUP.png'
    yt_color = 0xcf2227
    text_mode = False
    if pld.args:
        if pld.args[-1].lower() == '--text':
            text_mode = True
        if text_mode:
            lookup = ' '.join(pld.args[:-1])
        else:
            lookup = ' '.join(pld.args)
        extracted_info = await cmd.bot.music.extract_info(lookup)
        if lookup.startswith('http'):
            playlist_url = True
        else:
            playlist_url = False
        if extracted_info:
            if '_type' in extracted_info:
                if extracted_info['_type'] == 'playlist':
                    if not playlist_url:
                        song_item = extracted_info['entries'][0]
                    else:
                        song_item = None
                else:
                    song_item = extracted_info
            else:
                song_item = extracted_info
            if song_item:
                video_url = f'https://www.youtube.com/watch?v={song_item["id"]}'
                if text_mode:
                    response = video_url
                else:
                    info_text = f'Video URL: [Link]({video_url})'
                    info_text += f'\nUploader: [{song_item["uploader"]}]({song_item["uploader_url"]})'
                    stat_text = f'Views: {song_item["view_count"]}'
                    stat_text += f'\nLikes: {song_item["like_count"]}/{song_item["dislike_count"]}'
                    duration = str(datetime.timedelta(seconds=int(song_item['duration'])))
                    rating = get_average(song_item['dislike_count'], song_item['like_count'])
                    response = discord.Embed(color=yt_color)
                    response.set_author(name=song_item['title'], icon_url=yt_icon, url=video_url)
                    response.set_thumbnail(url=song_item['thumbnail'])
                    response.set_footer(text=f'Video duration: {duration} | Rating: {rating}/5')
                    response.add_field(name='Info', value=info_text)
                    response.add_field(name='Stats', value=stat_text)
            else:
                response = not_found('Invalid data retrieved.')
        else:
            response = not_found('No results.')
    else:
        response = error('Nothing inputted.')
    if text_mode:
        await pld.msg.channel.send(response)
    else:
        await pld.msg.channel.send(embed=response)
