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

from sigma.core.utilities.data_processing import user_avatar


async def userinformation(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
    else:
        target = pld.msg.author
    response = discord.Embed(color=target.color)
    response.set_author(name=f'{target.display_name}\'s Information', icon_url=user_avatar(target))
    creation_time = arrow.get(target.created_at).format('DD. MMMM YYYY')
    user_text = f'Username: **{target.name}**#{target.discriminator}'
    user_text += f'\nID: **{target.id}**'
    user_text += f'\nStatus: **{str(target.status).replace("dnd", "busy").title()}**'
    user_text += f'\nBot User: **{target.bot}**'
    user_text += f'\nCreated: **{creation_time}**'
    response.add_field(name='User Info', value=user_text)
    member_join_time = arrow.get(target.joined_at).format('DD. MMMM YYYY')
    is_moderator = pld.msg.channel.permissions_for(target).manage_guild
    member_text = f'Name: **{target.display_name}**'
    member_text += f'\nColor: **{str(target.color).upper()}**'
    member_text += f'\nTop Role: **{target.top_role.name}**'
    member_text += f'\nModerator: **{is_moderator}**'
    member_text += f'\nJoined: **{member_join_time}**'
    response.add_field(name='Member Info', value=member_text)
    pfx = cmd.db.get_prefix(pld.settings)
    footer = f'To see the user\'s avatar use the {pfx}avatar command.'
    response.set_footer(text=footer)
    await pld.msg.channel.send(embed=response)
