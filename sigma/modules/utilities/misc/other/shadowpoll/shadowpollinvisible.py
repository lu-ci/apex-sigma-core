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
from sigma.core.utilities.generic_responses import error, not_found


async def shadowpollinvisible(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        poll_id = pld.args[0].lower()
        poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == pld.msg.author.id:
                visible = poll_file['settings']['visible']
                if visible:
                    poll_file['settings'].update({'visible': False})
                    await cmd.db[cmd.db.db_nam].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                    response = discord.Embed(color=0x161616, title=f'🕶 Poll {poll_file["id"]} is now invisible.')
                else:
                    response = error(f'Poll {poll_file["id"]} is already invisible.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = not_found('Poll not found.')
    else:
        response = error('Missing poll ID.')
    await pld.msg.channel.send(embed=response)
