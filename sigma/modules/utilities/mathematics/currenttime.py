# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import yaml
from arrow.parser import ParserError

tz_aliases = None
tz_offsets = None


async def currenttime(cmd, message, args):
    global tz_aliases
    global tz_offsets
    if not tz_aliases:
        with open(cmd.resource('tz_aliases.yml')) as tz_a_file:
            tz_aliases = yaml.safe_load(tz_a_file)
    if not tz_offsets:
        with open(cmd.resource('tz_offsets.yml')) as tz_o_file:
            tz_offsets = yaml.safe_load(tz_o_file)
    if args:
        shift = ' '.join(args).lower()
        if shift in tz_aliases:
            shift = tz_aliases.get(shift)
        if shift in tz_offsets:
            shift = tz_offsets.get(shift)
    else:
        shift = None
    try:
        if shift:
            now = arrow.utcnow().to(shift)
        else:
            now = arrow.utcnow()
    except ParserError:
        now = None
    if now:
        time_out = now.format('DD. MMM. YYYY - HH:mm:ss')
        response = discord.Embed(color=0xf9f9f9, title=f'🕥 {time_out}')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Could not parse that time.')
    await message.channel.send(embed=response)
