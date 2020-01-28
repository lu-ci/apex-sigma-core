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

from sigma.core.utilities.generic_responses import error, ok


async def givecurrency(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) >= 2:
            if pld.msg.mentions:
                target = pld.msg.mentions[0]
                try:
                    amount = abs(int(pld.args[-1]))
                except ValueError:
                    amount = None
                if amount:
                    if not await cmd.db.is_sabotaged(target.id) and not await cmd.db.is_sabotaged(pld.msg.author.id):
                        current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
                        current_kud = current_kud.current
                        if current_kud >= amount:
                            await cmd.db.del_resource(pld.msg.author.id, 'currency', amount, cmd.name, pld.msg)
                            await cmd.db.add_resource(target.id, 'currency', amount, cmd.name, pld.msg, False)
                            response = ok(f'Transferred {amount} to {target.display_name}.')
                        else:
                            response = discord.Embed(color=0xa7d28b, title='💸 You don\'t have that much.')
                    else:
                        response = error('Transaction declined by Lucia\'s Guard.')
                else:
                    response = error('Invalid amount.')
            else:
                response = error('No user targeted.')
        else:
            response = error('Missing arguments.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
