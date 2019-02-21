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

import os
import socket
import sys

import arrow
import discord
import humanfriendly
import psutil

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


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


def get_shard_latency(latencies: list, shard_id: int):
    shard_latency = None
    for lat_sd, lat_ms in latencies:
        if lat_sd == shard_id:
            shard_latency = lat_ms
            break
    return int(shard_latency * 1000)


async def status(cmd: SigmaCommand, pld: CommandPayload):
    uptime_set = arrow.utcnow().float_timestamp - cmd.bot.start_time.float_timestamp
    processed = round(cmd.bot.queue.processed / uptime_set, 3)
    os_icon, os_color = get_os_icon()
    general_text = f'Latency: **{int(cmd.bot.latency * 1000)}ms**'
    general_text += f'\nPlatform: **{sys.platform.upper()}**'
    general_text += f'\nStarted: **{arrow.get(psutil.boot_time()).humanize()}**'
    cpu_clock = psutil.cpu_freq()
    cpu_clock = round(cpu_clock.current, 2) if cpu_clock else '???'
    cpu_text = f'Count: **{psutil.cpu_count()} ({psutil.cpu_count(logical=False)})**'
    cpu_text += f'\nUsage: **{psutil.cpu_percent()}%**'
    cpu_text += f'\nClock: **{cpu_clock} MHz**'
    avail_mem = psutil.virtual_memory().available
    total_mem = psutil.virtual_memory().total
    used_mem = humanfriendly.format_size(total_mem - avail_mem, binary=True)
    total_mem = humanfriendly.format_size(total_mem, binary=True)
    sigma_mem = humanfriendly.format_size(psutil.Process(os.getpid()).memory_info().rss, binary=True)
    mem_text = f'Me: **{sigma_mem}**'
    mem_text += f'\nUsed: **{used_mem}**'
    mem_text += f'\nTotal: **{total_mem}**'
    response = discord.Embed(color=os_color)
    response.set_author(name=socket.gethostname(), icon_url=os_icon)
    response.add_field(name='General', value=general_text)
    response.add_field(name='CPU', value=cpu_text)
    response.add_field(name='Memory', value=mem_text)
    if cmd.bot.cfg.dsc.bot:
        shard_latency = get_shard_latency(cmd.bot.latencies, pld.msg.guild.shard_id)
        verbose_description = f'Shard: #{pld.msg.guild.shard_id} | '
        verbose_description += f'Latency: {shard_latency}ms | '
        verbose_description += f'Activity: {processed} ev/s'
        response.description = verbose_description
    await pld.msg.channel.send(embed=response)
