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


async def tempcategory(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_channels:
        if pld.args:
            if pld.args[0].lower() == 'disable':
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'temp_channel_category', None)
                response = GenericResponse('Temp Channel Category disabled.').ok()
                await pld.msg.channel.send(embed=response)
                return
            target = None
            lookup = ' '.join(pld.args).lower()
            if lookup.isdigit():
                try:
                    search = pld.msg.guild.get_channel(int(lookup))
                    if isinstance(search, discord.CategoryChannel):
                        target = search
                except ValueError:
                    target = None
            else:
                target = discord.utils.find(lambda c: c.name.lower() == lookup, pld.msg.guild.categories)
            if target:
                if target.permissions_for(pld.msg.guild.me).manage_channels:
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'temp_channel_category', target.id)
                    response = GenericResponse(f'Temp Channel Category set to {target.name}').ok()
                else:
                    response = GenericResponse('I can\'t create channels in that category.').error()
            else:
                response = GenericResponse('Category not found.').not_found()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Channels needed.').denied()
    await pld.msg.channel.send(embed=response)
