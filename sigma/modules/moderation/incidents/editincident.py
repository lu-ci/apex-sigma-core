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
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied


async def editincident(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        icore = get_incident_core(cmd.db)
        if len(pld.args) >= 2:
            lookup = pld.args[0]
            reason = ' '.join(pld.args[1:])
            incident = await icore.get_by_token(pld.msg.guild.id, lookup)
            if incident:
                if not len(reason) > 1000:
                    incident.edit(pld.msg.author, reason)
                    await icore.save(incident)
                    response = discord.Embed(color=0x66CC66, title=f'✅ Incident {incident.id} updated.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Reasons have a limit of 1000 characters.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ No incident with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = permission_denied('Manage Messages')
    await pld.msg.channel.send(embed=response)
