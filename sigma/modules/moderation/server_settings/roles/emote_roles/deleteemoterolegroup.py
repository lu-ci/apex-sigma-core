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

from sigma.core.utilities.generic_responses import denied, error, not_found


async def deleteemoterolegroup(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            group_id = pld.args[0].lower()
            emote_groups = pld.settings.get('emote_role_groups') or {}
            if group_id in emote_groups:
                emote_groups.pop(group_id)
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'emote_role_groups', emote_groups)
                response = discord.Embed(color=0xFFCC4D, title=f'🔥 Emote role group {group_id} has been deleted.')
            else:
                response = not_found(f'Group {group_id} not found.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
