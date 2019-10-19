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

from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.sweets import SweetsController
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller

TOT_RESPONSES = {
    0: 'Nobody answered the door.',
    1: 'You got a piece of candy!',
    2: 'You got a large lollipop!',
    3: 'You got a king sized candy bar!'
}

TOT_COLORS = {
    0: 0xbdddf4,
    1: 0xdd2e44,
    2: 0xffcc4d,
    3: 0xc1694f
}

TOT_ICONS = {
    0: '💨',
    1: '🍬',
    2: '🍭',
    3: '🍫'
}


async def trickortreat(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        vc = get_vigor_controller(cmd.db)
        vigor = await vc.get_vigor(pld.msg.author.id)
        if vigor.current:
            cooldown = await vc.get_cooldown(pld.msg.author.id, 90)
            await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, cooldown)
            chance = await vc.get_chances(pld.msg.author.id, 95)
            success = vc.roll_chance(chance)
            bonus = 2 if vc.roll_chance(2.75) else 1 if vc.roll_chance(12.5) else 0
            sweets = 1 + bonus if success else 0
            tot_text = TOT_RESPONSES.get(sweets)
            tot_icon = TOT_ICONS.get(sweets)
            tot_color = TOT_COLORS.get(sweets)
            actual_sweets = int(sweets * (1.66 + secrets.randbelow(6)))
            await cmd.db.del_resource(pld.msg.author.id, 'vigor', 1, cmd.name, pld.msg)
            added_sweets = await SweetsController.add_sweets(cmd.db, pld.msg, actual_sweets, cmd.name, False)
            tot_status = 'No sweets this time...' if added_sweets == 0 else f'**(+{added_sweets} Sweets)**'
            response = discord.Embed(color=tot_color, title=f'{tot_icon} {tot_text} {tot_status}')
        else:
            response = discord.Embed(color=0x77b255, title='🤢 You\'re too tired, you need vigor.')
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You can look for candy again in {timeout} seconds.')
    await pld.msg.channel.send(embed=response)
