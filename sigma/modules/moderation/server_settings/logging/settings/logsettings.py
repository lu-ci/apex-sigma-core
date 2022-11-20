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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.server_settings.logging.settings.log import log_keys


async def logsettings(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        settings = []
        for log_key in log_keys:
            if log_key == 'log_modules':
                enabled = pld.settings.get('logged_modules')
            else:
                enabled = pld.settings.get(log_key)
            channel_id = pld.settings.get(f'{log_key}_channel')
            channel = await cmd.bot.get_channel(channel_id)
            chn = channel.name if channel else 'Not Set'
            state = 'Enabled' if enabled else 'Disabled'
            log_line = [log_key[4:].title(), chn, state]
            settings.append(log_line)
        headers = ['Type', 'Channel', 'State']
        output = boop(settings, column_names=headers)
        response = discord.Embed(color=0xC1694F)
        enabled_count = len([opt for opt in settings if opt[2] == 'Enabled'])
        details = f'```py\n{enabled_count} out of {len(log_keys)} logs enabled.\n```'
        response.add_field(name='📋 Log settings', value=details, inline=False)
        response.add_field(name='📄 Details', value=f'```\n{output}\n```', inline=False)
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
