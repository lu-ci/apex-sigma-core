# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import secrets
from asyncio.queues import Queue

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error


async def shuffle(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.voice:
        same_bound = True
        if pld.msg.guild.voice_client:
            if pld.msg.guild.voice_client.channel.id != pld.msg.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if pld.msg.guild.voice_client:
                queue = cmd.bot.music.get_queue(pld.msg.guild.id)
                if queue:
                    queue_list = await cmd.bot.music.listify_queue(queue)
                    queue_count = len(queue_list)
                    new_queue = Queue()
                    while queue_list:
                        await new_queue.put(queue_list.pop(secrets.randbelow(len(queue_list))))
                    cmd.bot.music.queues.update({pld.msg.guild.id: new_queue})
                    response = discord.Embed(color=0x3B88C3, title=f'🔀 Shuffled {queue_count} songs.')
                    requester = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                    response.set_author(name=requester, icon_url=user_avatar(pld.msg.author))
                else:
                    response = error('The queue is empty.')
            else:
                response = error('I am not connected to any channel.')
        else:
            response = error('You are not in my voice channel.')
    else:
        response = error('You are not in a voice channel.')
    await pld.msg.channel.send(embed=response)
