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
import yaml
from arrow.parser import ParserError

from sigma.core.mechanics.command import SigmaCommand

tz_aliases = None
tz_offsets = None


async def timeconvert(cmd: SigmaCommand, message: discord.Message, args: list):
    global tz_aliases
    global tz_offsets
    if not tz_aliases:
        with open(cmd.resource('tz_aliases.yml')) as tz_a_file:
            tz_aliases = yaml.safe_load(tz_a_file)
    if not tz_offsets:
        with open(cmd.resource('tz_offsets.yml')) as tz_o_file:
            tz_offsets = yaml.safe_load(tz_o_file)
    if args:
        conv_input = ' '.join(args).split('>')
        if len(conv_input) == 2:
            from_pieces = conv_input[0].split()
            if len(from_pieces) == 2:
                from_time = from_pieces[0]
                from_zone = from_pieces[1]
                if from_zone.lower() in tz_aliases:
                    from_zone = tz_aliases.get(from_zone.lower())
                if from_zone.lower() in tz_offsets:
                    from_zone = tz_offsets.get(from_zone.lower())
                to_zone = conv_input[1]
                if to_zone.lower() in tz_aliases:
                    to_zone = tz_aliases.get(to_zone.lower())
                if to_zone.lower() in tz_offsets:
                    to_zone = tz_offsets.get(to_zone.lower())
                try:
                    from_string = f'{arrow.utcnow().format("YYYY-MM-DD")} {from_time}:00'
                    if from_zone != 0:
                        from_arrow = arrow.get(from_string).to(str(from_zone))
                    else:
                        from_arrow = arrow.get(from_string)
                    to_arrow = from_arrow.to(str(to_zone))
                    time_out = to_arrow.format('DD. MMM. YYYY - HH:mm:ss (ZZ)')
                    response = discord.Embed(color=0xf9f9f9, title=f'🕥 {time_out}')
                except ParserError:
                    response = discord.Embed(color=0xBE1931, title='❗ Could not parse that time.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid first argument.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid input arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
