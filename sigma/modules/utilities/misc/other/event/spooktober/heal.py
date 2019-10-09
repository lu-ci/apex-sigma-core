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
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller


def int_in_args(args):
    """
    Iterates the arguments to find at least one number.
    :param args: The arguments.
    :type args: list
    :return:
    :rtype: NoneType or int
    """
    number = None
    for arg in args:
        try:
            number = abs(int(arg))
            break
        except ValueError:
            number = None
    return number


async def heal(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    vc = get_vigor_controller(cmd.db)
    vigor = await vc.get_vigor(target.id)
    missing = 100 - vigor.current
    if missing:
        regen = int_in_args(pld.args)
        if regen is None:
            regen = 100
        regen = regen if missing >= regen else missing
        price = int(regen * 1.666777666)
        question_text = f'❔ Use **{price} sweets** to heal **{regen} vigor**?'
        question_embed = discord.Embed(color=0xf9f9f9, title=question_text)
        accepted, timeout = await bool_dialogue(cmd.bot, pld.msg, question_embed)
        if accepted:
            candy = await cmd.db.get_resource(pld.msg.author.id, 'sweets')
            if candy.current >= price:
                await cmd.db.del_resource(pld.msg.author.id, 'sweets', price, cmd.name, pld.msg)
                await cmd.db.add_resource(target.id, 'vigor', regen, cmd.name, pld.msg)
                if pld.msg.author.id == target.id:
                    response_text = f'💉 You healed for **{regen} vigor**, stay safe out there, it\'s spooky.'
                else:
                    response_text = f'💉 You healed {target.display_name} for **{regen} vigor**, don\'t spoil them.'
                response = discord.Embed(color=0xdd2e44, title=response_text)
            else:
                response = discord.Embed(color=0x66757f, title=f'🕸 You don\'t have {price} sweets.')
        else:
            if timeout:
                response_text = f'🕙 You thought about it for too long.'
                response = discord.Embed(color=0x696969, title=response_text)

            else:
                response_text = f'❌ I get it, I\'m also scared of needles.'
                response = discord.Embed(color=0xBE1931, title=response_text)
    else:
        if pld.msg.author.id == target.id:
            response_text = '🚑 You\'re in perfect health, my services aren\'t needed.'
        else:
            response_text = f'🚑 {target.display_name} is in perfect health, they\'ve went home.'
        response = discord.Embed(color=0xf9f9f9, title=response_text)
    await pld.msg.channel.send(embed=response)
