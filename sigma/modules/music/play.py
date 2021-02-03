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

import asyncio
import datetime

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.core.utilities.stats_processing import add_special_stats


def player_listening(voice_client):
    """

    :param voice_client:
    :type voice_client: discord.VoiceClient
    :return:
    :rtype: bool
    """
    user_count = 0
    for member in voice_client.channel.members:
        if not member.bot:
            if not member.voice.self_deaf:
                if not member.voice.deaf:
                    user_count += 1
    return bool(user_count)


def player_active(voice_client):
    """

    :param voice_client:
    :type voice_client: discord.VoiceClient
    :return:
    :rtype: bool
    """
    active = False
    if voice_client:
        listening = player_listening(voice_client)
        if listening:
            playing = voice_client.is_playing()
            paused = voice_client.is_paused()
            if playing or paused:
                active = True
    return active


async def play(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.voice:
        same_bound = True
        if pld.msg.guild.voice_client:
            if pld.msg.guild.voice_client.channel.id != pld.msg.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if not pld.msg.guild.voice_client:
                cmn_cmd = cmd.bot.modules.commands['summon']
                await getattr(cmn_cmd.command, cmn_cmd.name)(cmn_cmd, pld)
            if pld.args:
                queue_cmd = cmd.bot.modules.commands['queue']
                await getattr(queue_cmd.command, queue_cmd.name)(queue_cmd, pld)
            if not cmd.bot.music.get_queue(pld.msg.guild.id).empty():
                while not cmd.bot.music.get_queue(pld.msg.guild.id).empty():
                    queue = cmd.bot.music.get_queue(pld.msg.guild.id)
                    if not pld.msg.guild.voice_client:
                        return
                    if pld.msg.guild.voice_client.is_playing():
                        return
                    item = await queue.get()
                    if pld.msg.guild.id in cmd.bot.music.repeaters:
                        await queue.put(item)
                    init_song_embed = discord.Embed(color=0x3B88C3, title=f'🔽 Downloading {item.title}...')
                    init_song_msg = await pld.msg.channel.send(embed=init_song_embed)
                    if not pld.msg.guild.voice_client:
                        no_client = error('The voice client seems to have broken.')
                        await pld.msg.channel.send(embed=no_client)
                        return
                    player_made = False
                    player_attempts = 0
                    while not player_made and player_attempts < 3:
                        try:
                            await item.create_player(pld.msg.guild.voice_client)
                            player_made = True
                        except discord.ClientException:
                            player_attempts += 1
                            # noinspection PyBroadException
                            try:
                                if pld.msg.guild.voice_client:
                                    await pld.msg.guild.voice_client.disconnect()
                                cmn_cmd = cmd.bot.modules.commands['summon']
                                await getattr(cmn_cmd.command, cmn_cmd.name)(cmn_cmd, pld)
                            except Exception:
                                pass
                    if not player_made:
                        no_client = error('The voice client seems to be unable to connect.')
                        await pld.msg.channel.send(embed=no_client)
                        return
                    else:
                        await add_special_stats(cmd.db, 'songs_played')
                        cmd.bot.music.currents.update({pld.msg.guild.id: item})
                        duration = str(datetime.timedelta(seconds=item.duration))
                        author = f'{item.requester.name}#{item.requester.discriminator}'
                        song_embed = discord.Embed(color=0x3B88C3)
                        song_embed.add_field(name='🎵 Now Playing', value=item.title)
                        song_embed.set_thumbnail(url=item.thumbnail)
                        song_embed.set_author(name=author, icon_url=user_avatar(item.requester), url=item.url)
                        song_embed.set_footer(text=f'Duration: {duration}')
                        try:
                            await init_song_msg.edit(embed=song_embed)
                        except discord.NotFound:
                            await pld.msg.channel.send(embed=song_embed)
                        while player_active(pld.msg.guild.voice_client):
                            await asyncio.sleep(2)
                response = discord.Embed(color=0x3B88C3, title='🎵 Queue complete.')
                if pld.msg.guild.voice_client:
                    await pld.msg.guild.voice_client.disconnect()
                    if pld.msg.guild.id in cmd.bot.music.queues:
                        del cmd.bot.music.queues[pld.msg.guild.id]
                if 'donate' in cmd.bot.modules.commands:
                    await cmd.bot.modules.commands['donate'].execute(pld)
            else:
                response = error('The queue is empty.')
        else:
            response = error('Channel miss-match prevented me from playing.')
    else:
        response = error('You are not in a voice channel.')
    await pld.msg.channel.send(embed=response)
