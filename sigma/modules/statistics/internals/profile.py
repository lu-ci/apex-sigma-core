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

import discord

from sigma.core.utilities.data_processing import user_avatar


async def profile(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    mem_count = len([mem for mem in cmd.bot.get_all_members() if mem.id == message.author.id])
    avatar = user_avatar(target)
    exp = await cmd.db.get_experience(target, message.guild)
    cur = await cmd.db.get_currency(target, message.guild)
    global_level = int(exp['global'] / 13266.85)
    global_currency = int(cur['global'])
    cmd_stats = f'Level: {global_level}'
    cmd_stats += f'\nGuilds: {mem_count}'
    cmd_stats += f'\nMoney: {global_currency} {cmd.bot.cfg.pref.currency}'
    response = discord.Embed(color=target.color)
    response.set_thumbnail(url=avatar)
    response.add_field(name=f'{target.display_name}\'s Profile', value=cmd_stats)
    await message.channel.send(embed=response)
