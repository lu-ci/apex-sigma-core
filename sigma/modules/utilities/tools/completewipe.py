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

from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse

IGNORE_COLLS = [
    'Interactions', 'BlacklistedUsers', 'BanClockworkDocs', 'HardmuteClockworkDocs'
]


async def completewipe(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    quesbed = discord.Embed(color=0xf9f9f9, title='❔ Are you sure you want to wipe your data?')
    quesbed.description = cmd.desc
    dialogue = DialogueCore(cmd.bot, pld.msg, quesbed)
    dresp = await dialogue.bool_dialogue()
    if dresp.ok:
        total = 0
        collections = await cmd.db[cmd.db.db_nam].list_collection_names()
        for collection in collections:
            if collection not in IGNORE_COLLS:
                results = await cmd.db[cmd.db.db_nam][collection].delete_many({'user_id': pld.msg.author.id})
                total += results.deleted_count
        response = GenericResponse(f'All your data has been wiped. Deleted {total} documents.').ok()
    else:
        response = dresp.generic('data wipe')
    await pld.msg.channel.send(embed=response)
