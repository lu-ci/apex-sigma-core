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

from sigma.core.utilities.generic_responses import GenericResponse


async def get_category(cmd, guild):
    """
    Gets the temporary voice channel category for the server.
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param guild: The guild that triggered the event.
    :type guild: discord.Guild
    :return:
    :rtype: discord.CategoryChannel
    """
    custom_cat_id = await cmd.db.get_guild_settings(guild.id, 'temp_channel_category')
    custom_cat = guild.get_channel(custom_cat_id)
    if custom_cat:
        return custom_cat
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
    if pld.msg.guild.me.permissions_in(temp_vc_cat).manage_channels:
        perms = {'manage_channels': True, 'manage_roles': True, 'read_messages': True, 'connect': True, 'speak': True}
        overwrites = {pld.msg.author: discord.PermissionOverwrite(**perms)}
        await pld.msg.guild.create_voice_channel(room_name, reason=reason, overwrites=overwrites, category=temp_vc_cat)
        response = GenericResponse(f'{room_name} created.').ok()
    else:
        response = GenericResponse('I can\'t create channels in that category.').error()
    await pld.msg.channel.send(embed=response)
