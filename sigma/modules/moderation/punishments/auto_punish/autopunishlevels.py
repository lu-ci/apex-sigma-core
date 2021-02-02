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

import datetime

import discord

from sigma.core.utilities.data_processing import convert_to_seconds
from sigma.core.utilities.generic_responses import denied, error, ok

actions = ['textmute', 'hardmute', 'kick', 'softban', 'ban', 'remove']


def parse_time(seconds):
    humanized = str(datetime.timedelta(seconds=seconds))
    pieces = humanized.split(', ')
    out = ''
    if len(pieces) > 1:
        piece = pieces[0].split()
        out += piece[0] + piece[-1][0]
    parts = pieces[-1].split(':')
    initials = {0: 'h', 1: 'm', 2: 's'}
    for i, part in enumerate(parts):
        num = int(part)
        if num > 0:
            out += str(num) + initials[i]
    return out


async def autopunishlevels(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_guild:
        if not pld.args:
            settings = pld.settings.get('auto_punish_levels') or {}
            if settings:
                level_info = []
                for level, details in settings.items():
                    action = details.get('action')
                    duration = details.get('duration')
                    lvl_word = 'Warning' if int(level) == 1 else 'Warnings'
                    info = f'**{level} {lvl_word}:** {action.title()}'
                    if duration:
                        info += f' ({parse_time(duration)})'
                    level_info.append(info)
                response = discord.Embed(color=0x3B88C3, title='🔄 Auto-Punishment Levels')
                response.description = '\n'.join(level_info)
            else:
                response = error('No Auto-Punishments set.')
        else:
            if ':' in pld.args[0]:
                duration = None
                if len(pld.args) > 1 and pld.args[-1].startswith('--time='):
                    try:
                        duration = convert_to_seconds(pld.args[-1].split('=')[-1])
                    except (LookupError, ValueError):
                        err_response = error('Please use the format HH:MM:SS.')
                        await pld.msg.channel.send(embed=err_response)
                        return
                level, _, action = pld.args[0].partition(':')
                if level.isdigit() and action.lower() in actions:
                    settings = pld.settings.get('auto_punish_levels') or {}
                    if action.lower() == 'remove':
                        if str(level) in settings:
                            settings.pop(str(level))
                        response = ok(f'Level {level} punishment removed.')
                    else:
                        if duration and action.lower() in ['softban', 'kick']:
                            err_response = error(f'{action.title()} cannot be timed.')
                            await pld.msg.channel.send(embed=err_response)
                            return
                        settings.update({str(level): {'action': action.lower(), 'duration': duration}})
                        ok_text = f'Level {level} set to {action.lower()}'
                        if duration:
                            ok_text += f' ({parse_time(duration)})'
                        response = ok(ok_text)
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'auto_punish_levels', settings)
                else:
                    ender = 'level' if not level.isdigit() else 'punishment'
                    response = error(f'Invalid {ender}.')
            else:
                response = error('Separate level and punishment with a colon.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
