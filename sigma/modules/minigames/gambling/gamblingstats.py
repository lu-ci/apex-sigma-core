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


async def gamblingstats(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    globally = False
    if pld.args:
        if pld.args[-1].lower() == '--global':
            globally = True
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    is_author = target.id == pld.msg.author.id
    if not globally:
        pool = await cmd.db.get_resource(target.id, 'currency')
        slot_gain = int(pool.origins.functions.get('slots'))
        roul_gain = int(pool.origins.functions.get('roulette'))
        bkjk_gain = int(pool.origins.functions.get('blackjack'))
        slot_loss = int(pool.expenses.functions.get('slots'))
        roul_loss = int(pool.expenses.functions.get('roulette'))
        bkjk_loss = int(pool.expenses.functions.get('blackjack'))
    else:
        queries = [
            {'origins.functions.slots': {'$gt': 0}},
            {'origins.functions.roulette': {'$gt': 0}},
            {'origins.functions.blackjack': {'$gt': 0}},
            {'expenses.functions.slots': {'$gt': 0}},
            {'expenses.functions.roulette': {'$gt': 0}},
            {'expenses.functions.blackjack': {'$gt': 0}}
        ]
        pools = await cmd.db[cmd.db.db_name].CurrencyResource.find({'$or': queries}).to_list(None)
        slot_gain = 0
        roul_gain = 0
        bkjk_gain = 0
        slot_loss = 0
        roul_loss = 0
        bkjk_loss = 0
        for pool in pools:
            if 'origins' in pool:
                ori = pool['origins']['functions']
                slot_gain += int(ori.get('slots', 0))
                roul_gain += int(ori.get('roulette', 0))
                bkjk_gain += int(ori.get('blackjack', 0))
            if 'expenses' in pool:
                exp = pool['expenses']['functions']
                slot_loss += int(exp.get('slots', 0))
                roul_loss += int(exp.get('roulette', 0))
                bkjk_loss += int(exp.get('blackjack', 0))
    if any([slot_gain, roul_gain, bkjk_gain, slot_loss, roul_loss, bkjk_loss]):
        title = '🎰 Gambling Statistics' + ('' if globally else f' for {target.display_name}')
        response = discord.Embed(color=0xbe1931, title=title)
        gain_value = None
        if any([slot_gain, roul_gain, bkjk_gain]):
            gain_value = f'Slots: **{slot_gain}**\n'
            gain_value += f'Roulette: **{roul_gain}**\n'
            gain_value += f'Blackjack: **{bkjk_gain}**\n'
            gain_value += f'Total: **{slot_gain + roul_gain}**'
        response.add_field(name='Gains', value=gain_value if gain_value else 'No gains yet...')
        loss_value = None
        if any([slot_loss, roul_loss, bkjk_loss]):
            loss_value = f'Slots: **{slot_loss}**\n'
            loss_value += f'Roulette: **{roul_loss}**\n'
            loss_value += f'Blackjack: **{bkjk_loss}**\n'
            loss_value += f'Total: **{slot_loss + roul_loss}**'
        response.add_field(name='Losses', value=loss_value if loss_value else 'No losses yet...')
        if any([slot_gain, roul_gain, bkjk_gain]) and any([slot_loss, roul_loss, bkjk_loss]):
            net_value = f'Slots: **{slot_gain - slot_loss}**\n'
            net_value += f'Roulette: **{roul_gain - roul_loss}**\n'
            net_value += f'Blackjack: **{bkjk_gain - bkjk_loss}**\n'
            net_value += f'Total: **{(slot_gain + roul_gain + bkjk_gain) - (slot_loss + roul_loss + bkjk_loss)}**'
            response.add_field(name='Net Changes', value=net_value)
    else:
        name = 'You' if is_author else target.display_name
        connector = 'have' if is_author else 'has'
        starter = 'No' if globally else f'{name} {connector} no'
        response = discord.Embed(color=0xc6e4b5, title=f'💸 {starter} gains or losses...')
    await pld.msg.channel.send(embed=response)
