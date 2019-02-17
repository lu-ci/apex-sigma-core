# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
from sigma.core.utilities.generic_responses import error


def user_auth(message: discord.Message, list_file: dict):
    author_id = list_file.get('user_id')
    if list_file.get('mode') in ['private', 'locked']:
        if author_id == message.author.id:
            auth = True
        else:
            auth = False
    else:
        auth = True
    return auth


async def addline(cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.args) >= 2:
        add_line = ' '.join(pld.args[1:])
        list_coll = cmd.db[cmd.db.db_nam].CustomLists
        lookup_data = {'server_id': pld.msg.guild.id, 'list_id': pld.args[0].lower()}
        list_file = await list_coll.find_one(lookup_data)
        if list_file:
            auth = user_auth(pld.msg, list_file)
            if auth:
                list_file.get('contents').append(add_line)
                await list_coll.update_one(lookup_data, {'$set': list_file})
                response = discord.Embed(color=0xF9F9F9)
                response.title = '📝 Your line was written to the list.'
            else:
                mode = 'private' if list_file.get('mode') == 'private' else 'locked'
                response = discord.Embed(color=0xFFAC33, title=f'🔏 This list is {mode}.')
        else:
            response = error('Missing or invalid list ID.')
    else:
        response = error('Not enough arguments.')
    await pld.msg.channel.send(embed=response)
