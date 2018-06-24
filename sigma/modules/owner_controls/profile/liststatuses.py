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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate


async def liststatuses(cmd: SigmaCommand, message: discord.Message, args: list):
    status_data = await cmd.db[cmd.db.db_cfg.database].StatusFiles.find({}).to_list(None)
    if status_data:
        status_list = []
        for status in status_data:
            status_list.append(f"ID: **{status.get('ID')}** Text: **{status.get('Text')}**")
        page = args[0] if args else 1
        status_list, page = paginate(status_list, page, 20)
        response = discord.Embed(color=0x1B6F5F)
        response.add_field(name=f'💭 Statuses on page {page}', value='\n'.join(status_list))
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No statuses found.')
    await message.channel.send(embed=response)
