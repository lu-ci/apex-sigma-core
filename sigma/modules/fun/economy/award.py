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

from sigma.core.utilities.generic_responses import GenericResponse


async def award(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if len(pld.args) == 2:
            try:
                amount = int(abs(int(pld.args[0])))
            except ValueError:
                amount = None
            if pld.msg.mentions:
                target = pld.msg.mentions[0]
            else:
                target = None
            if amount:
                if target:
                    currency = cmd.bot.cfg.pref.currency
                    current_vault = pld.settings.get('currency_vault')
                    if current_vault is None:
                        current_vault = 0
                    if current_vault >= amount:
                        await cmd.db.add_resource(target.id, 'currency', amount, cmd.name, pld.msg, False)
                        current_vault -= amount
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'currency_vault', current_vault)
                        response = GenericResponse(f'{amount} {currency} given to {target.display_name} from the Vault.').ok()
                    else:
                        response = discord.Embed(color=0xa7d28b, title=f'💸 Not enough {currency} in the Vault.')
                else:
                    response = GenericResponse('No user targeted.').error()
            else:
                response = GenericResponse('Invalid amount.').error()
        else:
            response = GenericResponse('Invalid number of arguments.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
