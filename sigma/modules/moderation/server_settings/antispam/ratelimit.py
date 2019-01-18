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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, ok, error


async def ratelimit(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        try:
            split = pld.args[0].split('/')
            amount, timespan = abs(int(split[0])), abs(int(split[1]))
        except (IndexError, ValueError):
            amount = timespan = None
        if amount and timespan:
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'rate_limit_amount', amount)
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'rate_limit_timespan', timespan)
            response = ok(f'Message rate limit set to {amount} per {timespan}s.')
        else:
            response = error('No limit and span or ivalid input.')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)
