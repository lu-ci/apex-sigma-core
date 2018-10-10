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


async def listsettings(cmd: SigmaCommand, message: discord.Message, args):
    if args:
        if len(args) > 1:
            if args[1].lower() == 'private':
                mode = 'private'
            elif args[1].lower() == 'locked':
                mode = 'locked'
            else:
                mode = None
            if mode:
                lookup_data = {'server_id': message.guild.id, 'list_id': args[0].lower()}
                list_coll = cmd.db[cmd.db.db_nam].CustomLists
                list_file = await list_coll.find_one(lookup_data)
                if list_file:
                    list_id = list_file.get('list_id')
                    if list_file.get('user_id') == message.author.id:
                        if list_file.get(mode):
                            list_file.update({mode: False})
                            await list_coll.update_one(lookup_data, {'$set': list_file})
                            response = discord.Embed(color=0xFFAC33, title=f'🔓 List `{list_id}` unmarked as {mode}.')
                        else:
                            list_file.update({mode: True})
                            await list_coll.update_one(lookup_data, {'$set': list_file})
                            response = discord.Embed(color=0xFFAC33, title=f'🔏  List `{list_id}` marked as {mode}.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this list.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid list ID.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid mode.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
