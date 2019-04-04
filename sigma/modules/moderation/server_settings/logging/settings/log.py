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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, ok

log_keys = [
    'log_antispam', 'log_bans', 'log_deletions', 'log_edits', 'log_filters',
    'log_kicks', 'log_movement', 'log_mutes', 'log_purges', 'log_warnings', 'log_incidents'
]
accepted_logs = [lk.lower()[4:] for lk in log_keys]


async def log(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            order = ' '.join(pld.args).lower()
            if order == 'all':
                for log_key in log_keys:
                    await cmd.db.set_guild_settings(pld.msg.guild.id, log_key, True)
                response = ok('All logging enabled.')
            elif order == 'none':
                for log_key in log_keys:
                    await cmd.db.set_guild_settings(pld.msg.guild.id, log_key, False)
                response = ok('All logging disabled.')
            else:
                log_ords = order.split('; ')
                results = []
                for log_ord in log_ords:
                    if log_ord in accepted_logs:
                        log_key = f'log_{log_ord}'
                        curr = bool(pld.settings.get(log_key))
                        new = not curr
                        await cmd.db.set_guild_settings(pld.msg.guild.id, log_key, new)
                        res = 'Enabled' if new else 'Disabled'
                    else:
                        res = 'Invalid'
                    res_line = f'{log_ord.title()}: {res}'
                    results.append(res_line)
                response = ok('Log types edited.')
                response.description = '\n'.join(results)
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
