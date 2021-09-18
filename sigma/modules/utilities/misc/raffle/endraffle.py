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


async def endraffle(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        rafid = pld.args[0].lower()
        raffle = await cmd.db[cmd.db.db_nam].Raffles.find_one({'id': rafid, 'active': True})
        if raffle:
            aid = raffle.get('author')
            if aid == pld.msg.author.id:
                await cmd.db[cmd.db.db_nam].Raffles.update_one(raffle, {'$set': {'end': 0}})
                reaction = '✅'
            else:
                reaction = '⛔'
        else:
            reaction = '🔍'
    else:
        reaction = '❗'
    await pld.msg.add_reaction(reaction)
