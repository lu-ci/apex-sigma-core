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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.other.drawcard import make_new_deck


async def newdeck(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    new_deck = make_new_deck()
    cache_key = f'{cmd.name}_deck_{pld.msg.author.id}'
    await cmd.db.cache.set_cache(cache_key, new_deck)
    response = GenericResponse(f'Your deck has been rebuilt, {pld.msg.author.display_name}.').ok()
    await pld.msg.channel.send(embed=response)
