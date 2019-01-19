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
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found, denied


async def viewlist(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        lookup_data = {'server_id': pld.msg.guild.id, 'list_id': pld.args[0].lower()}
        list_coll = cmd.db[cmd.db.db_nam].CustomLists
        list_file = await list_coll.find_one(lookup_data)
        if list_file:
            author_id = list_file.get('user_id')
            list_name = list_file.get('name')
            if list_file.get('private'):
                if author_id == pld.msg.author.id:
                    auth = True
                else:
                    auth = False
            else:
                auth = True
            if auth:
                list_lines = []
                for i, line in enumerate(list_file.get('contents')):
                    list_lines.append(f'**{i + 1}** {line}')
                page = pld.args[1] if len(pld.args) > 1 else 1
                list_lines, page = PaginatorCore.paginate(list_lines, page, 20)
                list_out = '\n'.join(list_lines)
                mode, icon = list_file.get('mode'), ''
                if mode in ['private', 'locked']:
                    icon = ' ⛔' if mode == 'private' else ' 🔏'
                empty = f'No contents. Add lines with `{cmd.bot.cfg.pref.prefix}addline`.'
                response = discord.Embed(color=0xF9F9F9, title=f':bookmark_tabs: {list_name}')
                response.description = empty if list_out == '' else list_out
                response.set_footer(text=f'[{list_file.get("list_id")}]{icon} Page {page}')
            else:
                response = denied('This list is private.')
        else:
            response = not_found('List not found.')
    else:
        response = error('Missing list ID.')
    await pld.msg.channel.send(embed=response)
