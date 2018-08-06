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

log_keys = [
    'log_antispam', 'log_bans', 'log_deletions', 'log_edits', 'log_filters',
    'log_kicks', 'log_movement', 'log_mutes', 'log_purges', 'log_warnings'
]
accepted_logs = [lk.lower()[4:] for lk in log_keys]


async def log(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            order = ' '.join(args).lower()
            if order == 'all':
                for log_key in log_keys:
                    await cmd.db.set_guild_settings(message.guild.id, log_key, True)
                response = discord.Embed(color=0x77B255, title=f'✅ All logging enabled.')
            elif order == 'none':
                for log_key in log_keys:
                    await cmd.db.set_guild_settings(message.guild.id, log_key, False)
                response = discord.Embed(color=0x77B255, title=f'✅ All logging disabled.')
            else:
                log_ords = order.split('; ')
                results = []
                for log_ord in log_ords:
                    if log_ord in accepted_logs:
                        log_key = f'Log{log_ord.title()}'
                        curr = bool(await cmd.db.get_guild_settings(message.guild.id, log_key))
                        new = not curr
                        await cmd.db.set_guild_settings(message.guild.id, log_key, new)
                        res = 'Enabled' if new else 'Disabled'
                    else:
                        res = 'Invalid'
                    res_line = f'{log_ord.title()}: {res}'
                    results.append(res_line)
                response = discord.Embed(color=0x77B255, title=f'✅ Multiple logging edited.')
                response.description = '\n'.join(results)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
