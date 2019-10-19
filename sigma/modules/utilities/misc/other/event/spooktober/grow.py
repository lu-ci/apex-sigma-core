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

from sigma.core.utilities.dialogue_controls import bool_dialogue
from sigma.modules.utilities.misc.other.event.spooktober.enchant import EVENT_ONGOING
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import VigorController
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_curse_controller


async def grow(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.id in EVENT_ONGOING:
        return
    EVENT_ONGOING.append(pld.msg.author.id)
    if pld.args:
        try:
            price = abs(int(pld.args[0]))
        except ValueError:
            price = 10
    else:
        price = 10
    if not price:
        price = 1
    candy = await cmd.db.get_resource(pld.msg.author.id, 'sweets')
    if candy.current >= price:
        multiplier = 16.1616
        curse_ctrl = get_curse_controller(cmd.db)
        cursed = await curse_ctrl.is_cursed(pld.msg.author.id)
        if price > 10:
            gain = int(VigorController.basic_exponential(price, price, 0.00775, True, True) * multiplier)
        else:
            gain = int(price * multiplier)
        if cursed:
            gain = gain // 2
        if not gain:
            gain = 1
        question_text = f'❔ Use **{price} sweets** to grow your pumpkin **{gain} grams**?'
        question_embed = discord.Embed(color=0xf9f9f9, title=question_text)
        accepted, timeout = await bool_dialogue(cmd.bot, pld.msg, question_embed)
        if accepted:
            await cmd.db.del_resource(pld.msg.author.id, 'sweets', price, cmd.name, pld.msg)
            await cmd.db.add_resource(pld.msg.author.id, 'weight', gain, cmd.name, pld.msg)
            response_text = f'🎃 Your pumpkin grew and gained **{gain} grams**'
            response = discord.Embed(color=0xf18f26, title=response_text)
        else:
            if timeout:
                response_text = f'🕙 You thought about it for too long.'
                response = discord.Embed(color=0x696969, title=response_text)

            else:
                response_text = f'❌ Ok, maybe you want to grow the pumpkin some other time.'
                response = discord.Embed(color=0xBE1931, title=response_text)
    else:
        response = discord.Embed(color=0x66757f, title=f'🕸 You don\'t have {price} sweets, you have {candy.current}.')
        response.set_footer(text='The default amount is 10, but you can input how many you want to spend.')
    if pld.msg.author.id in EVENT_ONGOING:
        EVENT_ONGOING.remove(pld.msg.author.id)
    await pld.msg.channel.send(embed=response)
