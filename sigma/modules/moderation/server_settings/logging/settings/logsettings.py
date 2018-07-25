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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied
from humanfriendly.tables import format_pretty_table as boop

log_keys = [
    'LogAntispam', 'LogBans', 'LogDeletions', 'LogEdits', 'LogFilters',
    'LogKicks', 'LogModules', 'LogMovement', 'LogMutes', 'LogPurges', 'LogWarnings'
]


async def logsettings(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        settings = []
        for log_key in log_keys:
            if log_key == 'LogModules':
                enabled = await cmd.db.get_guild_settings(message.guild.id, 'LoggedModules')
            else:
                enabled = await cmd.db.get_guild_settings(message.guild.id, log_key)
            channel_id = await cmd.db.get_guild_settings(message.guild.id, log_key + 'Channel')
            channel = discord.utils.find(lambda x: x.id == channel_id, message.guild.channels)
            chn = channel.name if channel else 'Not Set'
            state = 'Enabled' if enabled else 'Disabled'
            log_line = [log_key[3:], chn, state]
            settings.append(log_line)
        headers = ['Type', 'Channel', 'State']
        output = boop(settings, column_names=headers)
        response = discord.Embed(color=0xC1694F)
        enabled_count = len([l for l in settings if l[2] == 'Enabled'])
        details = f'```py\n{enabled_count} out of {len(log_keys)} logs enabled.\n```'
        response.add_field(name=f'📋 Log settings', value=details, inline=False)
        response.add_field(name=f'📄 Details', value=f'```\n{output}\n```', inline=False)
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
