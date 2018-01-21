from sigma.core.mechanics.command import SigmaCommand
import asyncio
import datetime

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.stats_processing import add_special_stats


def player_listening(voice_client):
    user_count = 0
    for member in voice_client.channel.members:
        if not member.bot:
            if not member.voice.self_deaf:
                if not member.voice.deaf:
                    user_count += 1
    if user_count:
        active = True
    else:
        active = False
    return active


def player_active(voice_client):
    if voice_client:
        listening = player_listening(voice_client)
        if listening:
            playing = voice_client.is_playing()
            paused = voice_client.is_paused()
            if playing or paused:
                active = True
            else:
                active = False
        else:
            active = False
    else:
        active = False
    return active


async def play(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if not message.guild.voice_client:
                await cmd.bot.modules.commands['summon'].execute(message, [])
            if args:
                await cmd.bot.modules.commands['queue'].execute(message, args)
            if not cmd.bot.music.get_queue(message.guild.id).empty():
                while not cmd.bot.music.get_queue(message.guild.id).empty():
                    queue = cmd.bot.music.get_queue(message.guild.id)
                    if not message.guild.voice_client:
                        return
                    if message.guild.voice_client.is_playing():
                        return
                    item = await queue.get()
                    if message.guild.id in cmd.bot.music.repeaters:
                        await queue.put(item)
                    init_song_embed = discord.Embed(color=0x3B88C3, title=f'🔽 Downloading {item.title}...')
                    init_song_msg = await message.channel.send(embed=init_song_embed)
                    if not message.guild.voice_client:
                        no_client = discord.Embed(color=0xBE1931, title='❗ The voice client seems to have broken.')
                        await message.channel.send(embed=no_client)
                        return
                    await item.create_player(message.guild.voice_client)
                    await add_special_stats(cmd.db, 'songs_played')
                    cmd.bot.music.currents.update({message.guild.id: item})
                    duration = str(datetime.timedelta(seconds=item.duration))
                    author = f'{item.requester.name}#{item.requester.discriminator}'
                    song_embed = discord.Embed(color=0x3B88C3)
                    song_embed.add_field(name='🎵 Now Playing', value=item.title)
                    song_embed.set_thumbnail(url=item.thumbnail)
                    song_embed.set_author(name=author, icon_url=user_avatar(item.requester), url=item.url)
                    song_embed.set_footer(text=f'Duration: {duration}')
                    await init_song_msg.edit(embed=song_embed)
                    while player_active(message.guild.voice_client):
                        await asyncio.sleep(2)
                response = discord.Embed(color=0x3B88C3, title='🎵 Queue complete.')
                if message.guild.voice_client:
                    await message.guild.voice_client.disconnect()
                    if message.guild.id in cmd.bot.music.queues:
                        del cmd.bot.music.queues[message.guild.id]
                if 'donate' in cmd.bot.modules.commands:
                    await cmd.bot.modules.commands['donate'].execute(message, [])
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The queue is empty.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Channel miss-match prevented me from playing.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)
