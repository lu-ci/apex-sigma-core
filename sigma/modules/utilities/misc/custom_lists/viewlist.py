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
from sigma.core.utilities.data_processing import paginate


async def viewlist(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup_data = {'server_id': message.guild.id, 'list_id': args[0].lower()}
        list_coll = cmd.db[cmd.db.db_nam].CustomLists
        list_file = await list_coll.find_one(lookup_data)
        if list_file:
            author_id = list_file.get('user_id')
            author = cmd.bot.get_user(author_id)
            creator = author.name if author else author_id
            if list_file.get('private'):
                if author_id == message.author.id:
                    auth = True
                else:
                    auth = False
            else:
                auth = True
            if auth:
                list_lines = []
                for i, line in enumerate(list_file.get('contents')):
                    list_lines.append(f'**{i + 1}** {line}')
                page = args[1] if len(args) > 1 else 1
                list_lines, page = paginate(list_lines, page, 20)
                list_out = '\n'.join(list_lines)
                pv = '⛔' if list_file.get('private') else ''
                lk = '🔏' if list_file.get('locked') else ''
                spacer = ' ' if pv or lk else ''
                empty = f'No contents. Add lines with `{cmd.bot.cfg.pref.prefix}al`.'
                response = discord.Embed(color=0xF9F9F9, title=f':bookmark_tabs: {creator}\'s List')
                response.description = empty if list_out == '' else list_out
                response.set_footer(text=f'[{list_file.get("list_id")}]{spacer}{pv}{lk} Page {page}')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ This list is private.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 List not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing list ID.')
    await message.channel.send(embed=response)
