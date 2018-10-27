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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied


async def ratelimit(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author.permissions_in(message.channel).manage_guild:
        try:
            split = args[0].split('/')
            amount, timespan = abs(int(split[0])), abs(int(split[1]))
        except (IndexError, ValueError):
            amount = timespan = None
        if amount and timespan:
            await cmd.db.set_guild_settings(message.guild.id, 'rate_limit_amount', amount)
            await cmd.db.set_guild_settings(message.guild.id, 'rate_limit_timespan', timespan)
            response = discord.Embed(color=0x77B255, title=f'✅ Message rate limit set to {amount} per {timespan}s.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No limit and span or ivalid input.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
