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

import arrow
import discord

from sigma.core.utilities.data_processing import get_image_colors


async def serverinformation(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    gld = pld.msg.guild
    own = gld.owner
    guild_icon = str(gld.icon_url) if gld.icon_url else discord.Embed.Empty
    response = discord.Embed(color=await get_image_colors(guild_icon))
    response.set_author(name=gld.name, icon_url=guild_icon)
    creation_time = arrow.get(gld.created_at).format('DD. MMMM YYYY')
    bot_count = 0
    user_count = 0
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    guild_text = f'Name: **{gld.name}**'
    guild_text += f'\nID: **{gld.id}**'
    guild_text += f'\nMembers: **{user_count}**'
    guild_text += f'\nBots: **{bot_count}**'
    guild_text += f'\nChannels: **{len(gld.channels)}**'
    guild_text += f'\nRoles: **{len(gld.roles)}**'
    guild_text += f'\nCreated: **{creation_time}**'
    response.add_field(name='Guild Info', value=guild_text)
    own_creation_time = arrow.get(own.created_at).format('DD. MMMM YYYY')
    own_text = f'Username: **{own.name}**#{own.discriminator}'
    own_text += f'\nNickname: **{own.display_name}**'
    own_text += f'\nID: **{own.id}**'
    own_text += f'\nStatus: **{str(own.status).replace("dnd", "busy").title()}**'
    own_text += f'\nColor: **{str(own.color).upper()}**'
    own_text += f'\nTop Role: **{own.top_role.name}**'
    own_text += f'\nCreated: **{own_creation_time}**'
    response.add_field(name='Owner Info', value=own_text)
    if gld.afk_channel:
        detail_text = f'AFK Channel: **{gld.afk_channel.name}**'
        detail_text += f'\nAFK Timeout: **{gld.afk_timeout}**'
    else:
        detail_text = 'AFK Channel: **None**'
        detail_text += '\nAFK Timeout: **None**'
    detail_text += f'\nEmojis: **{len(gld.emojis)}**'
    detail_text += f'\nLarge: **{gld.large}**'
    detail_text += f'\nShard: **{gld.shard_id}**'
    detail_text += f'\nVerification: **{gld.verification_level.name.upper()}**'
    response.add_field(name='Details', value=detail_text)
    await pld.msg.channel.send(embed=response)
