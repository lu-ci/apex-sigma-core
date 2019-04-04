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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import ok


async def get_category(cmd: SigmaCommand, guild: discord.Guild):
    """

    :param cmd:
    :type cmd:
    :param guild:
    :type guild:
    :return:
    :rtype:
    """
    temp_cat = None
    cat_count = len(guild.categories)
    for category in guild.categories:
        if category.name.startswith('[Σ]'):
            temp_cat = category
            break
    if not temp_cat:
        cat_name = f'[Σ] {cmd.bot.user.name} Temp Channels'
        temp_cat = await guild.create_category_channel(name=cat_name, reason='Temp Channel Category')
        await temp_cat.edit(position=cat_count)
    return temp_cat


async def temproom(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    room_name = ' '.join(pld.args) or f'{pld.msg.author.display_name}\'s Room'
    room_name = f'[Σ] {room_name}'
    reason = f'Temporary voice channel by {pld.msg.author.name}#{pld.msg.author.discriminator}.'
    temp_vc_cat = await get_category(cmd, pld.msg.guild)
    tmp_vc = await pld.msg.guild.create_voice_channel(room_name, reason=reason, category=temp_vc_cat)
    await tmp_vc.set_permissions(pld.msg.author, manage_channels=True)
    response = ok(f'{room_name} created.')
    await pld.msg.channel.send(embed=response)
