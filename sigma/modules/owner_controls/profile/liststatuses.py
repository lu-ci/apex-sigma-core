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
from sigma.core.utilities.data_processing import paginate, get_image_colors, user_avatar

from humanfriendly.tables import format_pretty_table as boop


async def liststatuses(cmd: SigmaCommand, message: discord.Message, args: list):
    status_data = await cmd.db[cmd.db.db_cfg.database].StatusFiles.find({}).to_list(None)
    if status_data:
        status_list = [[s['ID'], s['Text']] for s in status_data]
        status_list = sorted(status_list, key=lambda x: x[1])
        total_status = len(status_list)
        page = args[0] if args else 1
        status_list, page = paginate(status_list, page, 10)
        status_block = boop(status_list, ['ID', 'Text'])
        response = discord.Embed(color=await get_image_colors(cmd.bot.user.avatar_url))
        response.set_author(name=f'{cmd.bot.user.name}\'s Status Rotation Items', icon_url=user_avatar(cmd.bot.user))
        response.add_field(name='Info', value=f'Showing {len(status_list)} items out of {total_status} on page {page}.')
        response.add_field(name="List", value=f'```\n{status_block}\n```', inline=False)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No statuses found.')
    await message.channel.send(embed=response)
