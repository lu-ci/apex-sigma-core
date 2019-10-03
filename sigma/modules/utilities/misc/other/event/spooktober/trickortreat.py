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
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller

TOT_RESPONSES = {
    0: [
        'The local dentist gave you a mean look as he shut the door in your face.',
        'Karen dropped something heavy in your bag! Oh no, it\'s an essential oil.',
        'Stoners open the door but are interrupted as police raid their home.',
        'The kind old man gives you a creepy feeling, it\'s best if you left.',
        'Nobody is answering the door even though you can hear footsteps.'
    ],
    1: [
        'The sweet old lady dropped a piece of candy in your bag, nice!'
    ]
}

TOT_COLORS = {}

TOT_ICONS = {}


async def trickortreat(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    vc = get_vigor_controller(cmd.db)
    chance = await vc.get_chances(pld.msg.author.id, 95)
    success = vc.roll_chance(chance)
    bonus = 2 if vc.roll_chance(2.75) else 1 if vc.roll_chance(12.5) else 0
    sweets = 1 + bonus if success else 0
    tot_text = secrets.choice(TOT_RESPONSES.get(sweets))
    tot_icon = TOT_ICONS.get(sweets)
    tot_color = TOT_COLORS.get(sweets)
    tot_status = 'No sweets this time...' if sweets == 0 else f'**(+{sweets} Sweets)**'
    response = discord.Embed(color=tot_color, title=f'{tot_icon} {tot_text} {tot_status}')
    await pld.msg.channel.send(embed=response)
