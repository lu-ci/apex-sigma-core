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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import get_image_colors


async def topexperience(cmd: SigmaCommand, message: discord.Message, args: list):
    value_name = 'Experience'
    sort_key = 'global'
    lb_icon = cmd.bot.user.avatar_url
    lb_category = 'Global'
    if args:
        if args[0].lower() == 'local':
            sort_key = f'guilds.{message.guild.id}'
            lb_icon = message.guild.icon_url or lb_icon
            lb_category = message.guild.name
        elif args[0].lower() == 'total':
            sort_key = 'total'
            lb_category = 'Total'
    all_docs = await cmd.db[cmd.db.db_cfg.database].ExperienceSystem.find({}).sort(sort_key, -1).limit(50).to_list(None)
    leader_docs = []
    for data_doc in all_docs:
        if sort_key == 'global' or sort_key == 'total':
            user_value = data_doc.get(sort_key) or 0
        else:
            user_value = data_doc.get('guilds').get(str(message.guild.id)) or 0
        user_level = int(user_value / 13266.85)
        user_object = discord.utils.find(lambda usr: usr.id == data_doc.get('UserID'), cmd.bot.get_all_members())
        if user_object:
            leader_docs.append([user_object, user_level, user_value])
            if len(leader_docs) >= 20:
                break
    table_data = [[doc[0].name[:12], str(doc[1]), str(doc[2])] for doc in leader_docs]
    table_body = boop(table_data, ['User Name', 'Level', value_name])
    response = discord.Embed(color=await get_image_colors(lb_icon))
    response.set_author(name=f'{lb_category} {value_name} Leaderboard', icon_url=lb_icon)
    response.description = f'```hs\n{table_body}\n```'
    await message.channel.send(embed=response)
