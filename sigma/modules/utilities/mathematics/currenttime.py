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

import arrow
import discord
from arrow.parser import ParserError

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def currenttime(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    shift = None
    if pld.args:
        shift = ' '.join(pld.args).lower()
        alias_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one({'type': 'tz_alias', 'zone': shift})
        shift = alias_doc.get('value').lower() if alias_doc else shift.lower()
        offset_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one({'type': 'tz_offset', 'zone': shift}) or {}
        shift = offset_doc.get('value') if offset_doc else shift
    try:
        now = arrow.utcnow()
        if shift:
            now = now.to(shift)
    except ParserError:
        now = None
    if now:
        time_out = now.format('DD. MMM. YYYY - HH:mm:ss')
        response = discord.Embed(color=0xf9f9f9, title=f'🕥 {time_out}')
    else:
        response = error('Could not parse that time.')
    await pld.msg.channel.send(embed=response)
