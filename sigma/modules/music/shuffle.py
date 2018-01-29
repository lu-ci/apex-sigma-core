import secrets
from asyncio.queues import Queue

import discord

from sigma.core.utilities.data_processing import user_avatar


async def shuffle(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                queue = cmd.bot.music.get_queue(message.guild.id)
                if queue:
                    queue_list = await cmd.bot.music.listify_queue(queue)
                    queue_count = len(queue_list)
                    new_queue = Queue()
                    while queue_list:
                        await new_queue.put(queue_list.pop(secrets.randbelow(len(queue_list))))
                    cmd.bot.music.queues.update({message.guild.id: new_queue})
                    response = discord.Embed(color=0x3B88C3, title=f'🔀 Shuffled {queue_count} songs.')
                    requester = f'{message.author.name}#{message.author.discriminator}'
                    response.set_author(name=requester, icon_url=user_avatar(message.author))
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The queue is empty.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)
