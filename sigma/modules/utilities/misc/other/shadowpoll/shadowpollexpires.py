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
from sigma.modules.utilities.misc.reminders.remindme import convert_to_seconds


async def shadowpollexpires(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        if len(args) == 2:
            poll_id = args[0].lower()
            time_input = args[1]
            try:
                exp_in = convert_to_seconds(time_input)
                poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    if poll_file['origin']['author'] == message.author.id:
                        end_stamp = arrow.utcnow().float_timestamp + exp_in
                        end_human = arrow.get(end_stamp).humanize()
                        end_datet = arrow.get(end_stamp).datetime
                        poll_file['settings'].update({'expires': end_stamp})
                        poll_coll = cmd.db[cmd.db.db_nam].ShadowPolls
                        await poll_coll.update_one({'id': poll_id}, {'$set': poll_file})
                        title = f'⏰ Poll set to expire {end_human}.'
                        response = discord.Embed(color=0xff3333, title=title, timestamp=end_datet)
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 Poll not found.')
            except (LookupError, ValueError):
                response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID and expiration time.')
    await message.channel.send(embed=response)
