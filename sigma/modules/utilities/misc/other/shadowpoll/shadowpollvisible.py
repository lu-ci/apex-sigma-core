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


async def shadowpollvisible(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        poll_id = args[0].lower()
        poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                visible = poll_file['settings']['visible']
                if not visible:
                    poll_file['settings'].update({'visible': True})
                    await cmd.db[cmd.db.db_nam].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                    response = discord.Embed(color=0xF9F9F9, title=f'👁 Poll {poll_file["id"]} is now visible.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Poll {poll_file["id"]} is already visible.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 Poll not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
