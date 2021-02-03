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

from sigma.core.utilities.generic_responses import GenericResponse

log_keys = [
    'log_antispam_channel', 'log_bans_channel', 'log_deletions_channel', 'log_edits_channel', 'log_filters_channel',
    'log_kicks_channel', 'log_modules_channel', 'log_movement_channel', 'log_mutes_channel', 'log_purges_channel',
    'log_warnings_channel', 'log_incidents_channel'
]
accepted_logs = [lk.lower()[4:-8] for lk in log_keys]


async def set_log_channels(log_ords, gld_id, chn, db):
    """

    :param log_ords:
    :type log_ords: list[str]
    :param gld_id:
    :type gld_id: int
    :param chn:
    :type chn: discord.Channel
    :param db:
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: list[str]
    """
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


async def loggingchannel(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
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
                if all_keys:
                    response = GenericResponse('Logging channel disabled.').ok()
                else:
                    response = GenericResponse('Logging channels disabled.').ok()
                    response.description = '\n'.join(results)
            elif pld.msg.channel_mentions:
                target_chn = pld.msg.channel_mentions[0]
                if pld.msg.guild.me.permissions_in(target_chn).send_messages:
                    results = await set_log_channels(keys, pld.msg.guild.id, target_chn.id, cmd.db)
                    if all_keys:
                        response = GenericResponse(f'Logging channel set to #{target_chn.name}.').ok()
                    else:
                        response = GenericResponse('Logging channels edited').ok()
                        response.description = '\n'.join(results)
                else:
                    response = GenericResponse('I can\'t write in that channel.').error()
            else:
                response = GenericResponse('No channel targeted.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
