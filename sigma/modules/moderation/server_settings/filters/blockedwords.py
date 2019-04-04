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

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.generic_responses import info


async def blockedwords(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    blocked_words = pld.settings.get('blocked_words')
    if not blocked_words:
        response = info('There are no blocked words.')
    else:
        total_count = len(blocked_words)
        blocked_words, page = PaginatorCore.paginate(blocked_words, pld.args[0] if pld.args else 1, 20)
        showing_count = len(blocked_words)
        response = info(f'Words blocked on {pld.msg.guild.name}')
        response.description = ', '.join(blocked_words)
        response.set_footer(text=f'[Page {page}] Total: {total_count} | Showing: {showing_count}')
    await pld.msg.channel.send(embed=response)
