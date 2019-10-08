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
        question_embed.set_footer(text=f'If you fail, you\'ll love some vigor, candy and {currency}.')
        accepted, timeout = await bool_dialogue(cmd.bot, pld.msg, question_embed)
        if accepted:
            success = vc.roll_chance(chance)
            if success:
                # Add some candy to author.
                # Del some candy from target.
                # Lose 3-5 vigor.
                pass
            else:
                # Add some candy to target.
                # Del some candy from author.
                # Lose 5-15 vigor.
                pass
        else:
            if timeout:
                response_text = f'🕙 You thought about it too much.'
                response = discord.Embed(color=0x696969, title=response_text)

            else:
                response_text = f'❌ You chickened out.'
                response = discord.Embed(color=0xBE1931, title=response_text)
    await pld.msg.channel.send(embed=response)
