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
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import get_image_colors


async def makeemoterolegroup(cmd: SigmaCommand, message: discord.Message, args: list):
    emote_groups = await cmd.db.get_guild_settings(message.guild.id, 'EmoteRoleGroups') or {}
    group_list = list(emote_groups.keys())
    if emote_groups:
        if args:
            page = args[0]
            try:
                page = int(page)
            except ValueError:
                page = 1
        else:
            page = 1
        if page < 1:
            page = 1
        start_range = 10 * (page - 1)
        end_range = 10 * page
        group_count = len(group_list)
        group_list = group_list[start_range:end_range]
        if len(group_list) > 1:
            ender = 's'
        else:
            ender = ''
        summary = f'Showing **{len(group_list)}** group{ender} from Page **#{page}**.'
        summary += f'\n{message.guild.name} has **{group_count}** emote role group{ender}.'
        rl_out = ''
        group_list = sorted(group_list)
        for rl in group_list:
            rl_out += f'\n`{rl}`: {len(list(emote_groups.get(rl).keys()))} Roles'
        response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
        response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        response.add_field(name=f'Emote Role Group Summary', value=summary, inline=False)
        response.add_field(name=f'List of Emote Role Groups', value=f'{rl_out}', inline=False)
        response.set_footer(text=f'You can see all roles in a group using the {cmd.bot.cfg.pref.prefix}verg command.')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 {message.guild.name} has no emote role groups.')
    await message.channel.send(embed=response)
