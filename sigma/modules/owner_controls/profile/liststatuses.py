"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.data_processing import get_image_colors, user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


async def liststatuses(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    status_data = await cmd.db[cmd.db.db_nam].StatusFiles.find().to_list(None)
    if status_data:
        status_list = [[s['id'], s['text']] for s in status_data]
        status_list = sorted(status_list, key=lambda x: x[1])
        total_status = len(status_list)
        page = pld.args[0] if pld.args else 1
        status_list, page = PaginatorCore.paginate(status_list, page)
        status_block = boop(status_list, ['ID', 'Text'])
        response = discord.Embed(color=await get_image_colors(user_avatar(cmd.bot.user)))
        response.set_author(name=f'{cmd.bot.user.name}\'s Status Rotation Items', icon_url=user_avatar(cmd.bot.user))
        info = f'Showing {len(status_list)} items out of {total_status} on page {page}.'
        response.add_field(name='Info', value=f'```py\n{info}\n```')
        response.add_field(name="List", value=f'```\n{status_block}\n```', inline=False)
    else:
        response = GenericResponse('No statuses found.').not_found()
    await pld.msg.channel.send(embed=response)
