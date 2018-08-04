# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import get_image_colors, paginate


async def listrolegroups(cmd: SigmaCommand, message: discord.Message, args: list):
    role_groups = await cmd.db.get_guild_settings(message.guild.id, 'role_groups') or {}
    group_list = list(role_groups.keys())
    if role_groups:
        group_count = len(group_list)
        page = args[0] if args else 1
        group_list, page = paginate(group_list, page)
        ender = 's' if len(group_list) > 1 else ''
        summary = f'Showing **{len(group_list)}** group{ender} from Page **#{page}**.'
        summary += f'\n{message.guild.name} has **{group_count}** role group{ender}.'
        rl_out = ''
        group_list = sorted(group_list)
        for rl in group_list:
            rl_out += f'\n`{rl}`: {len(list(role_groups.get(rl)))} Roles'
        response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
        response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        response.add_field(name=f'Role Group Summary', value=summary, inline=False)
        response.add_field(name=f'List of Role Groups', value=f'{rl_out}', inline=False)
        response.set_footer(text=f'You can see all roles in a group using the {cmd.bot.cfg.pref.prefix}verg command.')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 {message.guild.name} has no role groups.')
    await message.channel.send(embed=response)
