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
import secrets

import discord

from sigma.core.utilities.dialogue_controls import bool_dialogue
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.sweets import SweetsController
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller


async def steal(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else None
    if target:
        currency = cmd.bot.cfg.pref.currency
        vc = get_vigor_controller(cmd.db)
        vigor = await vc.get_vigor(pld.msg.author.id)
        chance = round(await vc.get_chances(pld.msg.author.id, 75), 2)
        question_text = f'❔ You have a {chance}% chance of success, continue?'
        question_embed = discord.Embed(color=0xf9f9f9, title=question_text)
        question_embed.set_footer(text=f'If you fail, you\'ll lose some vigor and {currency}.')
        accepted, timeout = await bool_dialogue(cmd.bot, pld.msg, question_embed)
        if accepted:
            success = vc.roll_chance(chance)
            if success:
                target_candy = await cmd.db.get_resource(target.id, 'sweets')
                stolen_amount = secrets.randbelow(20) + 5
                stolen_amount = target_candy.current if stolen_amount > target_candy.current else stolen_amount
                stolen_amount = await SweetsController.add_sweets(cmd.db, pld.msg, stolen_amount, cmd.name, False)
                await cmd.db.del_resource(target.id, 'sweets', stolen_amount, cmd.name, pld.msg)
                vigor_loss = secrets.randbelow(3) + 3
                vigor_loss = vigor_loss if vigor.current >= vigor_loss else vigor.current
                await cmd.db.del_resource(pld.msg.author.id, 'vigor', vigor_loss, cmd.name, pld.msg)
                response_text = f'🗡 You pull a knife on {target.display_name}!'
                response = discord.Embed(color=0x67757f, title=response_text)
                response.description = f'They shakingly give you **{stolen_amount} sweets**.'
                response.description += f' You lose **{vigor_loss} vigor** for being a horrible person.'
            else:
                vigor_loss = secrets.randbelow(10) + 5
                vigor_loss = vigor_loss if vigor.current >= vigor_loss else vigor.current
                await cmd.db.del_resource(pld.msg.author.id, 'vigor', vigor_loss, cmd.name, pld.msg)
                curr = await cmd.db.get_resource(pld.msg.author.id, 'currency')
                curr_loss = secrets.randbelow(8000) + 2000
                curr_loss = curr_loss if curr.current >= curr_loss else curr.current
                response_text = '🚔 You screwed up and got detained!'
                response = discord.Embed(color=0xdd2e44, title=response_text)
                response.description = 'Some nearby officers pinned you to the cold, hard ground.'
                response.description += f' You lost **{vigor_loss} vigor** and had to pay'
                response.description += f' **{curr_loss} {currency}** for assault charges and fines.'
        else:
            if timeout:
                response_text = f'🕙 You thought about it too much.'
                response = discord.Embed(color=0x696969, title=response_text)

            else:
                response_text = f'❌ You chickened out.'
                response = discord.Embed(color=0xBE1931, title=response_text)
    await pld.msg.channel.send(embed=response)
