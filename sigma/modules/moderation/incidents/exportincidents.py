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

import os

import arrow
import discord

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.utilities.generic_responses import denied, error
from sigma.modules.minigames.utils.ongoing.ongoing import is_ongoing, set_ongoing, del_ongoing

variants = ['ban', 'unban', 'kick', 'warn', 'unwarn', 'textmute', 'textunmute', 'hardmute', 'hardunmute']
identifiers = ['moderator', 'target', 'variant']


def make_export_file(guild_name: str, incidents: list, modifier: str):
    """

    :param guild_name:
    :type guild_name:
    :param incidents:
    :type incidents:
    :param modifier:
    :type modifier:
    :return:
    :rtype:
    """
    if not os.path.exists('cache'):
        os.makedirs('cache')
    file_name = f'{guild_name} Incidents.txt'
    with open(f'cache/{file_name}', 'w', encoding='utf-8') as export_file:
        info_lines = f'Server: {guild_name}\n'
        info_lines += f'Incidents: {len(incidents)} [{modifier}]\n'
        info_lines += f'Date: {arrow.utcnow().format("DD. MMMM YYYY HH:mm:ss")} UTC\n'
        info_lines += f'{"=" * 40}\n\n'
        export_file.write(info_lines)
        export_file.write('\n'.join([incident.to_text() for incident in incidents]))
    return file_name


async def exportincidents(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    file = None
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        if not is_ongoing(cmd.name, pld.msg.guild.id):
            set_ongoing(cmd.name, pld.msg.guild.id)
            icore = get_incident_core(cmd.db)
            response, target = None, None
            identifier, incidents = None, None
            title = '🗃️ Gathering all '
            if pld.args:
                if len(pld.args) == 2:
                    identifier = pld.args[0].lower()
                    if (pld.msg.mentions or identifier == 'variant') and identifier in identifiers:
                        if identifier == 'moderator':
                            target = pld.msg.mentions[0]
                            incidents = await icore.get_all_by_mod(pld.msg.guild.id, target.id)
                            title += f'incidents issued by {target.name}.'
                        elif identifier == 'target':
                            target = pld.msg.mentions[0]
                            incidents = await icore.get_all_by_target(pld.msg.guild.id, target.id)
                            title += f'incidents for {target.name}.'
                        else:
                            target = pld.args[1].lower()
                            if target in variants:
                                incidents = await icore.get_all_by_variant(pld.msg.guild.id, target)
                                title += f'{target} incidents.'
                            else:
                                response = error('Invalid variant.')
                    else:
                        response = error('Invalid identifier.')
            else:
                incidents = await icore.get_all(pld.msg.guild.id)
                title += 'incidents.'
            if not response:
                if incidents:
                    response = discord.Embed(color=0x226699, title=title)
                    response.set_footer(text='A text file will be sent to you shortly.')
                    if identifier:
                        modifier = f'{identifier.title()}: {target.title() if identifier == "variant" else target.name}'
                    else:
                        modifier = 'All'
                    file_name = make_export_file(pld.msg.guild.name, incidents, modifier)
                    file = discord.File(f'cache/{file_name}', file_name)
                else:
                    if identifier:
                        response = error(f'No incidents found for that {identifier}.')
                    else:
                        response = error('This server has no incidents.')
        else:
            response = error('There is already one ongoing.')
    else:
        response = denied('Access Denied. Manage Messages needed.')
    if is_ongoing(cmd.name, pld.msg.guild.id):
        del_ongoing(cmd.name, pld.msg.guild.id)
    await pld.msg.channel.send(embed=response)
    if file:
        try:
            await pld.msg.author.send(file=file)
        except (discord.NotFound, discord.Forbidden):
            denied_response = error('I was unable to DM you, please adjust your settings.')
            await pld.msg.channel.send(pld.msg.author.mention, embed=denied_response)
