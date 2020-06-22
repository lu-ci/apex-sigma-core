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

import discord

from sigma.core.utilities.data_processing import user_avatar


async def experience(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    avatar = user_avatar(target)
    exp = await cmd.db.get_resource(target.id, 'experience')
    response = discord.Embed(color=0x47ded4)
    response.set_author(name=f'{target.display_name}\'s Experience Data', icon_url=avatar)
    guild_title = '🎪 Local'
    global_title = '📆 This Month'
    total_title = '📟 Total'
    guild_exp = exp.origins.guilds.get(pld.msg.guild.id)
    local_level = int(guild_exp / 13266.85)
    ranked_level = int(exp.ranked / 13266.85)
    total_level = int(exp.total / 13266.85)
    response.add_field(name=guild_title, value=f"```py\nXP: {guild_exp}\nLevel: {local_level}\n```")
    response.add_field(name=global_title, value=f"```py\nXP: {exp.ranked}\nLevel: {ranked_level}\n```")
    response.add_field(name=total_title, value=f"```py\nXP: {exp.total}\nLevel: {total_level}\n```")
    response.set_footer(text='🔰 Experience is earned by being an active guild member.')
    await pld.msg.channel.send(embed=response)
