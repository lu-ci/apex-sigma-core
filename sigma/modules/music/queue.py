import datetime

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.music import QueueItem
from sigma.core.utilities.data_processing import user_avatar


async def queue(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if message.author.voice:
            same_bound = True
            if message.guild.voice_client:
                if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                    same_bound = False
            if same_bound:
                lookup = ' '.join(args)
                if '/watch?' in lookup:
                    lookup = lookup.split('&')[0]
                    playlist_url = False
                    init_response = discord.Embed(color=0xFFCC66, title='💽 Processing URL...')
                elif '/playlist?' in lookup:
                    playlist_url = True
                    init_response = discord.Embed(color=0xFFCC66,
                                                  title='💽 Processing playlist. This might take a long time...')
                else:
                    if lookup.startswith('http'):
                        playlist_url = True
                    else:
                        playlist_url = False
                    init_response = discord.Embed(color=0xFFCC66, title='💽 Searching...')
                init_res_msg = await message.channel.send(embed=init_response)
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
                                queue_item = QueueItem(message.author, song_entry)
                                queue_container = cmd.bot.music.get_queue(message.guild.id)
                                await queue_container.put(queue_item)
                        final_resp = discord.Embed(color=0xFFCC66,
                                                   title=f'💽 Added {len(entries)} songs from {pl_title}.')
                    else:
                        if song_item:
                            queue_item = QueueItem(message.author, song_item)
                            queue_container = cmd.bot.music.get_queue(message.guild.id)
                            await queue_container.put(queue_item)
                            duration = str(datetime.timedelta(seconds=int(song_item['duration'])))
                            requester = f'{message.author.name}#{message.author.discriminator}'
                            final_resp = discord.Embed(color=0x66CC66)
                            final_resp.add_field(name='✅ Added To Queue', value=song_item['title'])
                            if 'thumbnail' in song_item:
                                final_resp.set_thumbnail(url=song_item['thumbnail'])
                            final_resp.set_author(name=requester, icon_url=user_avatar(message.author))
                            final_resp.set_footer(text=f'Duration: {duration}')
                        else:
                            final_resp = discord.Embed(color=0x696969, title='🔍 Addition returned a null item.')
                    await init_res_msg.edit(embed=final_resp)
                else:
                    final_resp = discord.Embed(color=0x696969, title='🔍 No results.')
                    await init_res_msg.edit(embed=final_resp)
            else:
                if not args:
                    response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
                    await message.channel.send(embed=response)
        else:
            if not args:
                response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
                await message.channel.send(embed=response)
    else:
        music_queue = cmd.bot.music.get_queue(message.guild.id)
        if not music_queue.empty():
            music_queue = await cmd.bot.music.listify_queue(music_queue)
            stats_desc = f'There are **{len(music_queue)}** songs in the queue.'
            if message.guild.id in cmd.bot.music.currents:
                curr = cmd.bot.music.currents[message.guild.id]
                stats_desc += f'\nCurrently playing: [{curr.title}]({curr.url})'
            list_desc_list = []
            boop_headers = ['#', 'Title', 'Requester', 'Duration']
            order_num = 0
            for item in music_queue[:5]:
                order_num += 1
                duration = str(datetime.timedelta(seconds=item.duration))
                title = item.title
                if ' - ' in title:
                    title = ' - '.join(title.split('-')[1:])
                    while title.startswith(' '):
                        title = title[1:]
                if len(title) > 20:
                    title = title[:20] + '...'
                req = item.requester.name
                if len(req) > 9:
                    req = req[:6] + '...'
                list_desc_list.append([order_num, title, req, duration])
            list_desc = boop(list_desc_list, boop_headers)
            list_title = f'List of {len(music_queue[:5])} Upcoming Queued Items'
            response = discord.Embed(color=0x3B88C3)
            response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
            response.add_field(name='Current Music Queue', value=stats_desc)
            response.add_field(name=list_title, value=f'```bat\n{list_desc}\n```')
        else:
            response = discord.Embed(color=0x3B88C3, title='🎵 The queue is empty.')
        await message.channel.send(embed=response)
