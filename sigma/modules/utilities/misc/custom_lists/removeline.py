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


async def removeline(cmd: SigmaCommand, message: discord.Message, args):
    if args:
        if len(args) > 1:
            list_coll = cmd.db[cmd.db.db_nam].CustomLists
            lookup_data = {'server_id': message.guild.id, 'list_id': args[0].lower()}
            list_file = await list_coll.find_one(lookup_data)
            if list_file:
                author_id = list_file.get('user_id')
                if author_id == message.author.id or message.author.id == 213695612351283200:
                    line = args[1]
                    if line.isdigit():
                        try:
                            list_file.get('contents', []).pop(int(line) - 1)
                            await list_coll.update_one(lookup_data, {'$set': list_file})
                            response = discord.Embed(color=0xFFCC4D, title=f'🔥 Line {line} was deleted.')
                        except IndexError:
                            response = discord.Embed(color=0x696969, title='🔍 Line not found.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Invalid line number.')
                else:
                    response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this list.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Missing or invalid list ID.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
