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

from sigma.core.utilities.generic_responses import error


async def destroyresource(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.mentions:
        if len(pld.args) >= 3:
            target = pld.msg.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(pld.args[-1]))
                    currency = cmd.bot.cfg.pref.currency.lower()
                    res_nam = 'currency' if pld.args[0].lower() == currency else pld.args[0].lower()
                    target_amount = await cmd.db.get_resource(target.id, res_nam)
                    target_amount = target_amount.current
                    if amount <= target_amount:
                        await cmd.db.del_resource(target.id, res_nam, amount, cmd.name, pld.msg)
                        title_text = f'🔥 Ok, {amount} of {target.display_name}\'s {res_nam} '
                        title_text += 'has been destroyed.'
                        response = discord.Embed(color=0xFFCC4D, title=title_text)
                    else:
                        response = error(f'{target.display_name} does\'t have that much {cmd.bot.cfg.pref.currency}.')
                except ValueError:
                    response = error('Invalid amount.')
            else:
                response = error(f'You can\'t take {cmd.bot.cfg.pref.currency} from bots.')
        else:
            response = error(f'{cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = error('No user targeted.')
    await pld.msg.channel.send(embed=response)
