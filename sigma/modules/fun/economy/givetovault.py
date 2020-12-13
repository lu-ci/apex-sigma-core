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


async def givetovault(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            amount = int(abs(int(pld.args[0])))
        except ValueError:
            amount = None
        if amount:
            if not await cmd.db.is_sabotaged(pld.msg.author.id):
                currency = cmd.bot.cfg.pref.currency
                current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
                current_kud = current_kud.current
                if current_kud >= amount:
                    current_vault = pld.settings.get('currency_vault')
                    if current_vault is None:
                        current_vault = 0
                    await cmd.db.del_resource(pld.msg.author.id, 'currency', amount, cmd.name, pld.msg)
                    current_vault += amount
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'currency_vault', current_vault)
                    response = ok(f'You added {amount} {currency} to the Vault.')
                else:
                    response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
            else:
                response = error('Transaction declined by Chamomile.')
        else:
            response = error('Invalid amount.')
    else:
        response = error('Amount missing.')
    await pld.msg.channel.send(embed=response)
