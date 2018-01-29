# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import socket
import sys

import arrow
import discord
import humanfriendly
import psutil


def get_os_icon():
    if sys.platform == 'win32':
        icon = 'https://i.imgur.com/wTMT4yG.png'
        color = 0x11b7ee
    elif sys.platform == 'linux':
        icon = 'https://i.imgur.com/pKxZYK7.png'
        color = 0xefba20
    else:
        icon = 'https://i.imgur.com/QxlJJgA.png'
        color = 0x696969
    return icon, color


async def status(cmd, message, args):
    uptime_set = arrow.utcnow().float_timestamp - cmd.bot.start_time.float_timestamp
    processed = round(cmd.bot.queue.processed / uptime_set, 3)
    os_icon, os_color = get_os_icon()
    general_text = f'Latency: **{int(cmd.bot.latency * 1000)}ms**'
    general_text += f'\nPlatform: **{sys.platform.upper()}**'
    general_text += f'\nStarted: **{arrow.get(psutil.boot_time()).humanize()}**'
    cpu_clock = psutil.cpu_freq()
    if cpu_clock:
        cpu_clock = round(cpu_clock.current, 2)
    else:
        cpu_clock = 'X'
    cpu_text = f'Count: **{psutil.cpu_count()} ({psutil.cpu_count(logical=False)})**'
    cpu_text += f'\nUsage: **{psutil.cpu_percent()}%**'
    cpu_text += f'\nClock: **{cpu_clock} MHz**'
    avail_mem = psutil.virtual_memory().available
    total_mem = psutil.virtual_memory().total
    used_mem = humanfriendly.format_size(total_mem - avail_mem, binary=True)
    total_mem = humanfriendly.format_size(total_mem, binary=True)
    mem_text = f'Used: **{used_mem}**'
    mem_text += f'\nTotal: **{total_mem}**'
    mem_text += f'\nPercent: **{int(psutil.virtual_memory().percent)}%**'
    response = discord.Embed(color=os_color)
    response.set_author(name=socket.gethostname(), icon_url=os_icon)
    response.add_field(name='General', value=general_text)
    response.add_field(name='CPU', value=cpu_text)
    response.add_field(name='Memory', value=mem_text)
    if cmd.bot.cfg.dsc.bot:
        current_shard = message.guild.shard_id
        shard_latency = int(cmd.bot.latencies[current_shard][1] * 1000)
        verbose_description = f'Shard: #{current_shard} | '
        verbose_description += f'Latency: {shard_latency}ms | '
        verbose_description += f'Activity: {processed} ev/s'
        response.description = verbose_description
    await message.channel.send(embed=response)
