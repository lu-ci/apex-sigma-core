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
from arrow.parser import ParserError

from sigma.core.mechanics.command import SigmaCommand


async def timeconvert(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        conv_input = ' '.join(args).split('>')
        if len(conv_input) == 2:
            from_pieces = conv_input[0].split()
            if len(from_pieces) == 2:
                from_time = from_pieces[0].lower()
                from_zone = from_pieces[1].lower()
                alias_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one({'type': 'tz_alias', 'zone': from_zone})
                from_zone = alias_doc.get('value').lower() if alias_doc else from_zone
                offset_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one(
                    {'type': 'tz_offset', 'zone': from_zone}
                ) or {}
                from_zone = offset_doc.get('value') if offset_doc else from_zone
                to_zone = conv_input[1].lower()
                alias_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one({'type': 'tz_alias', 'zone': to_zone})
                to_zone = alias_doc.get('value').lower() if alias_doc else to_zone
                offset_doc = await cmd.db[cmd.db.db_nam].TimezoneData.find_one(
                    {'type': 'tz_offset', 'zone': to_zone}
                ) or {}
                to_zone = offset_doc.get('value') if offset_doc else to_zone
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
