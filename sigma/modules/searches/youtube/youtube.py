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

from sigma.core.utilities.generic_responses import GenericResponse


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
        lookup = ' '.join(pld.args)
        if pld.args[-1].lower() == ' --text':
            lookup = lookup.rpartition(' ')[0]
            text_mode = True
        extracted_info = await cmd.bot.music.extract_info(lookup)
        if lookup.startswith('http') and '/playlist?' in lookup:
            playlist_url = True
        else:
            playlist_url = False
        if extracted_info:
            song_item = extracted_info
            if '_type' in extracted_info:
                if extracted_info['_type'] == 'playlist':
                    song_item = None
                    if not playlist_url:
                        try:
                            song_item = extracted_info['entries'][0]
                        except IndexError:
                            pass
            if song_item:
                video_url = f'https://www.youtube.com/watch?v={song_item["id"]}'
                if text_mode:
                    response = video_url
                else:
                    info_text = f'Video URL: [Link]({video_url})'
                    info_text += f'\nUploader: [{song_item["uploader"]}]({song_item["uploader_url"]})'
                    stat_text = f'Views: {song_item["view_count"]}'
                    stat_text += f'\nLikes: {song_item["like_count"]}'
                    duration = str(datetime.timedelta(seconds=int(song_item['duration'])))
                    response = discord.Embed(color=yt_color)
                    response.set_author(name=song_item['title'], icon_url=yt_icon, url=video_url)
                    response.set_thumbnail(url=song_item['thumbnail'])
                    response.set_footer(text=f'Video duration: {duration}')
                    response.add_field(name='Info', value=info_text)
                    response.add_field(name='Stats', value=stat_text)
            else:
                response = GenericResponse('Invalid data retrieved. Try a different search.').not_found()
        else:
            response = GenericResponse('No results.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    if text_mode:
        await pld.msg.channel.send(response)
    else:
        await pld.msg.channel.send(embed=response)
