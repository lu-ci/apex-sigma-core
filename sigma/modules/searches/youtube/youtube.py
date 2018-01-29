import datetime

import discord


async def youtube(cmd, message, args):
    yt_icon = 'https://i.imgur.com/qoH1MUP.png'
    yt_color = 0xcf2227
    text_mode = False
    if args:
        if args[-1].lower() == '-text':
            text_mode = True
        if text_mode:
            lookup = ' '.join(args[:-1])
        else:
            lookup = ' '.join(args)
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
                    rating = round(song_item['average_rating'], 2)
                    response = discord.Embed(color=yt_color)
                    response.set_author(name=song_item['title'], icon_url=yt_icon, url=video_url)
                    response.set_thumbnail(url=song_item['thumbnail'])
                    response.set_footer(text=f'Video duration: {duration} | Rating: {rating}/5')
                    response.add_field(name='Info', value=info_text)
                    response.add_field(name='Stats', value=stat_text)
            else:
                response = discord.Embed(color=0x696969, title='🔍 Invalid data retrieved.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    if text_mode:
        await message.channel.send(response)
    else:
        await message.channel.send(embed=response)
