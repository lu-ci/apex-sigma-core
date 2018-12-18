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
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied

log_keys = [
    'log_antispam_channel', 'log_bans_channel', 'log_deletions_channel', 'log_edits_channel', 'log_filters_channel',
    'log_kicks_channel', 'log_modules_channel', 'log_movement_channel', 'log_mutes_channel', 'log_purges_channel',
    'log_warnings_channel', 'log_incidents_channel'
]
accepted_logs = [lk.lower()[4:-8] for lk in log_keys]


async def set_log_channels(log_ords: list, gld_id: int, chn, db: Database):
    results = []
    for log_ord in log_ords:
        if log_ord in accepted_logs:
            log_key = f'log_{log_ord}_channel'
            await db.set_guild_settings(gld_id, log_key, chn)
            res = 'Set' if chn else 'Disabled'
        else:
            res = 'Invalid'
        res_line = f'{log_ord.title()}: {res}'
        results.append(res_line)
    return results


async def loggingchannel(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            mode, order = pld.args[0].lower(), ' '.join(pld.args[1:]).lower()
            if order:
                keys = [log_ord for log_ord in order.split('; ')]
                all_keys = False
            else:
                keys = [log_key for log_key in accepted_logs]
                all_keys = True
            if mode == 'disable':
                results = await set_log_channels(keys, pld.msg.guild.id, None, cmd.db)
                response = discord.Embed(color=0x77B255)
                if all_keys:
                    response.title = '✅ Logging channel disabled.'
                else:
                    response.title = '✅ Logging channels disabled.'
                    response.description = '\n'.join(results)
            elif pld.msg.channel_mentions:
                target_chn = pld.msg.channel_mentions[0]
                if pld.msg.guild.me.permissions_in(target_chn).send_messages:
                    results = await set_log_channels(keys, pld.msg.guild.id, target_chn.id, cmd.db)
                    response = discord.Embed(color=0x77B255)
                    if all_keys:
                        response.title = f'✅ Logging channel set to #{target_chn.name}.'
                    else:
                        response.title = '✅ Logging channels edited'
                        response.description = '\n'.join(results)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ I can\'t write in that channel.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No channel targeted.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)
