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

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import error, not_found

filter_names = ['arguments', 'extensions', 'words', 'invites']


def get_overrides(message: discord.Message, overrides: list, target_type: str):
    """

    :param message:
    :type message:
    :param overrides:
    :type overrides:
    :param target_type:
    :type target_type:
    :return:
    :rtype:
    """
    overridden_items = []
    guild_dict = {'channels': message.guild.channels, 'users': message.guild.members, 'roles': message.guild.roles}
    guild_items = guild_dict.get(target_type)
    for ovr_chn_id in overrides:
        pnd = '#' if target_type == 'channels' else ''
        exc_item = discord.utils.find(lambda c: c.id == ovr_chn_id, guild_items)
        exc_item_name = f'{pnd}{exc_item.name}' if exc_item else str(ovr_chn_id)
        overridden_items.append(exc_item_name)
    return overridden_items


async def filteroverrides(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        filter_name = pld.args[0].lower()
        if filter_name in filter_names:
            overrides = pld.settings.get('filter_overrides') or {}
            if overrides:
                override = overrides.get(filter_name, {})
                channels = override.get('channels')
                roles = override.get('roles')
                users = override.get('users')
                if any([channels, roles, users]):
                    guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
                    override_data = [(channels, 'channels'), (roles, 'roles'), (users, 'users')]
                    response = discord.Embed(color=await get_image_colors(guild_icon))
                    name = f'{filter_name[:-1].title()} Filter Overrides'
                    response.set_author(name=name, icon_url=guild_icon)
                    for data in override_data:
                        if data[0]:
                            ovr_lines = get_overrides(pld.msg, data[0], data[1])
                            response.add_field(name=data[1].title(), value=', '.join(ovr_lines), inline=False)
                else:
                    response = not_found(f'No overrides for `blocked{filter_name}` found.')
            else:
                response = not_found('No overrides found.')
        else:
            response = error('Invalid filter.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
