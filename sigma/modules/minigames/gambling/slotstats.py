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

from sigma.modules.minigames.gambling.slots import THREE_MOD, TWO_MOD, rarity_rewards, symbols


def get_payout(symbol, bet, triple):
    if triple:
        return int(bet * rarity_rewards[symbol] * THREE_MOD * 0.95)
    else:
        return int(bet * rarity_rewards[symbol] * TWO_MOD * 0.9)


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
    payouts_one = ''
    for symbol in reversed(symbols[:10]):
        thr_comb = get_payout(symbol, bet, True)
        two_comb = get_payout(symbol, bet, False)
        payouts_one += f'{symbol} - {two_comb}/**{thr_comb}**\n'
    payouts_two = ''
    for symbol in reversed(symbols[10:]):
        thr_comb = get_payout(symbol, bet, True)
        two_comb = get_payout(symbol, bet, False)
        payouts_two += f'{symbol} - {two_comb}/**{thr_comb}**\n'
    response.add_field(name='Matches (double/triple)', value=payouts_one)
    response.add_field(name='Cont.', value=payouts_two)
    response.set_footer(text=f'Payouts for a bet of {bet} {currency}.')
    await pld.msg.channel.send(embed=response)
