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

from sigma.modules.minigames.gambling.slots import TWO_PROFIT, THREE_PROFIT


def get_payout(bet, triple):
    if triple:
        return int(bet * THREE_PROFIT * 0.995)
    else:
        return int(bet * TWO_PROFIT * 0.995)


async def slotstats(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            bet = abs(int(pld.args[0]))
        except ValueError:
            bet = 10
    else:
        bet = 10
    currency_icon = cmd.bot.cfg.pref.currency_icon
    currency = cmd.bot.cfg.pref.currency
    response = discord.Embed(color=0x5dadec, title=f'{currency_icon} Slot Machine Payout')
    response.description = f'**2** Matching - **{get_payout(bet, False)}** {currency}'
    response.description += f'\n**3** Matching - **{get_payout(bet, True)}** {currency}'
    response.set_footer(text=f'Payouts for a bet of {bet} {currency}.')
    await pld.msg.channel.send(embed=response)
