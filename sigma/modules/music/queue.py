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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.music import QueueItem
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


def shorten(text, max_len, appendage):
    """
    :type text: str
    :type max_len: int
    :type appendage: str
    """
    if len(text) > max_len:
        text = text[:max_len] + appendage
    return text


async def queue(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    page_num = False
    if len(pld.args) == 1:
        if pld.args[0].isdigit():
            page_num = int(pld.args[0])
    if pld.args and not page_num:
        if pld.msg.author.voice:
            same_bound = True
            if pld.msg.guild.voice_client:
                if pld.msg.guild.voice_client.channel.id != pld.msg.author.voice.channel.id:
                    same_bound = False
            if same_bound:
                lookup = ' '.join(pld.args)
                if '/watch?' in lookup:
                    lookup = lookup.split('&')[0]
                    playlist_url = False
                    init_response = discord.Embed(color=0xFFCC66, title='💽 Processing URL...')
                elif '/playlist?' in lookup:
                    playlist_url = True
                    init_response = discord.Embed(
                        color=0xFFCC66,
                        title='💽 Processing playlist. This might take a long time...'
                    )
                else:
                    if lookup.startswith('http'):
                        playlist_url = True
                    else:
                        playlist_url = False
                    init_response = discord.Embed(color=0xFFCC66, title='💽 Searching...')
                init_res_msg = await pld.msg.channel.send(embed=init_response)
                extracted_info = await cmd.bot.music.extract_info(lookup)
                if extracted_info:
                    if '_type' in extracted_info:
                        if extracted_info['_type'] == 'playlist':
                            if not playlist_url:
                                song_item = extracted_info['entries'][0]
                                playlist = False
                            else:
                                song_item = None
                                playlist = True
                        else:
                            song_item = extracted_info
                            playlist = False
                    else:
                        song_item = extracted_info
                        playlist = False
                    if playlist:
                        pl_title = extracted_info['title']
                        entries = extracted_info['entries']
                        for song_entry in entries:
                            if song_entry:
                                queue_item = QueueItem(pld.bot, pld.msg.author, song_entry)
                                queue_container = cmd.bot.music.get_queue(pld.msg.guild.id)
                                await queue_container.put(queue_item)
                        final_resp = discord.Embed(
                            color=0xFFCC66,
                            title=f'💽 Added {len(entries)} songs from {pl_title}.'
                        )
                    else:
                        if song_item:
                            queue_item = QueueItem(pld.bot, pld.msg.author, song_item)
                            queue_container = cmd.bot.music.get_queue(pld.msg.guild.id)
                            await queue_container.put(queue_item)
                            duration = str(datetime.timedelta(seconds=int(song_item.get('duration', 0))))
                            requester = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                            final_resp = discord.Embed(color=0x66CC66)
                            final_resp.add_field(name='✅ Added To Queue', value=song_item.get('title', "No Title"))
                            if 'thumbnail' in song_item:
                                final_resp.set_thumbnail(url=song_item.get('thumbnail'))
                            final_resp.set_author(name=requester, icon_url=user_avatar(pld.msg.author))
                            final_resp.set_footer(text=f'Duration: {duration}')
                        else:
                            final_resp = GenericResponse('Addition returned a null item.').not_found()
                    try:
                        await init_res_msg.edit(embed=final_resp)
                    except discord.NotFound:
                        pass
                else:
                    final_resp = GenericResponse('No results.').not_found()
                    try:
                        await init_res_msg.edit(embed=final_resp)
                    except discord.NotFound:
                        pass
            else:
                if not pld.args:
                    response = GenericResponse('You are not in my voice channel.').error()
                    await pld.msg.channel.send(embed=response)
        else:
            if not pld.args:
                response = GenericResponse('You are not in a voice channel.').error()
                await pld.msg.channel.send(embed=response)
    else:
        music_queue = cmd.bot.music.get_queue(pld.msg.guild.id)
        if not music_queue.empty():
            music_list_all = await cmd.bot.music.listify_queue(music_queue)
            stats_desc = f'There are **{len(music_list_all)}** songs in the queue.'
            if pld.msg.guild.id in cmd.bot.music.currents:
                curr = cmd.bot.music.currents[pld.msg.guild.id]
                stats_desc += f'\nCurrently playing: [{curr.title}]({curr.url})'
            list_desc_list = []
            boop_headers = ['#', 'Title', 'Requester', 'Duration']
            order_num = 0
            page = page_num if page_num else 1
            music_list, page = PaginatorCore.paginate(music_list_all, page, 5)
            for item in music_list:
                order_num += 1
                duration = str(datetime.timedelta(seconds=item.duration))
                title = item.title
                if ' - ' in title:
                    title = ' - '.join(title.split('-')[1:]).strip()
                title = shorten(title, 20, '...')
                req = shorten(item.requester.name, 9, '...')
                list_desc_list.append([order_num, title, req, duration])
            list_desc = boop(list_desc_list, boop_headers)
            list_title = f'Queued Items on Page {page}'
            response = discord.Embed(color=0x3B88C3)
            guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon.url else None
            response.set_author(name=pld.msg.guild.name, icon_url=guild_icon)
            response.add_field(name='Current Music Queue', value=stats_desc, inline=False)
            response.add_field(name=list_title, value=f'```bat\n{list_desc}\n```', inline=False)
        else:
            response = discord.Embed(color=0x3B88C3, title='🎵 The queue is empty.')
        await pld.msg.channel.send(embed=response)
