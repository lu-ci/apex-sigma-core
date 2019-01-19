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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error

variants = ['ban', 'unban', 'kick', 'warn', 'unwarn', 'textmute', 'textunmute', 'hardmute', 'hardunmute']
identifiers = ['moderator', 'target', 'variant']


def parse_incidents(incidents: list, page):
    incidents = sorted(incidents, key=lambda i: i.order)
    incidents, page = PaginatorCore.paginate(incidents, page, 10)
    outlist = []
    for inc in incidents:
        timestamp = arrow.get(inc.timestamp).format('DD. MMM. YYYY. HH:mm')
        details = f'**#{inc.order}** `{inc.id}` - {inc.variant} incident for **{inc.target.name}** on {timestamp}'
        outlist.append(details)
    return '\n'.join(outlist), page


async def listincidents(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        icore = get_incident_core(cmd.db)
        identifier, incidents = None, None
        page = pld.args[-1] if len(pld.args) in [1, 3] else 1
        if len(pld.args) >= 2:
            identifier = pld.args[0].lower()
            if (pld.msg.mentions or identifier == 'variant') and identifier in identifiers:
                if identifier == 'moderator':
                    mod = pld.msg.mentions[0]
                    incidents = await icore.get_all_by_mod(pld.msg.guild.id, mod.id)
                    response = discord.Embed(color=0x226699)
                    incident_list, page = parse_incidents(incidents, page)
                    response.add_field(name=f'🗃️ Incidents initiated by {mod.name}', value=incident_list)
                elif identifier == 'target':
                    target = pld.msg.mentions[0]
                    incidents = await icore.get_all_by_target(pld.msg.guild.id, target.id)
                    response = discord.Embed(color=0x226699)
                    incident_list, page = parse_incidents(incidents, page)
                    response.add_field(name=f'🗃️ Incidents for {target.name}', value=incident_list)
                else:
                    variant = pld.args[1].lower()
                    if variant in variants:
                        incidents = await icore.get_all_by_variant(pld.msg.guild.id, variant)
                        response = discord.Embed(color=0x226699)
                        response.add_field(name='Details', value=f'```\nPage {page}\n```')
                        incident_list, page = parse_incidents(incidents, page)
                        response.add_field(name=f'🗃️ {identifier.title()} incidents', value=incident_list)
                    else:
                        response = error('Invalid variant.')
            else:
                response = error('Invalid identifier.')
        else:
            incidents = await icore.get_all(pld.msg.guild.id)
            response = discord.Embed(color=0x226699)
            incident_list, page = parse_incidents(incidents, page)
            response.add_field(name='🗃️ All incidents', value=incident_list)
        if not incidents and (identifier in identifiers or not identifier):
            if identifier:
                response = error(f'No incidents found for that {identifier}.')
            else:
                response = error('This server has no incidents.')
    else:
        response = denied('Access Denied. Manage Messages needed.')
    await pld.msg.channel.send(embed=response)
