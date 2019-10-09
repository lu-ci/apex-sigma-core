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

from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_curse_controller


async def vigor(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    self = target.id == pld.msg.author.id
    vc = get_vigor_controller(cmd.db)
    vg = await vc.get_vigor(target.id)
    curse_ctrl = get_curse_controller(cmd.db)
    cursed = await curse_ctrl.is_cursed(target.id)
    if cursed:
        response = discord.Embed(color=0x361683)
        response.set_author(name=f'☠ {target.display_name}\'s Vigor', icon_url=user_avatar(target))
    else:
        response = discord.Embed(color=0xbe1931)
        response.set_author(name=f'❤ {target.display_name}\'s Vigor', icon_url=user_avatar(target))
    starter = 'You have' if self else f'{target.display_name} has'
    referer = 'you' if self else 'them'
    curse_ref = 'You' if self else 'They'
    tt_chance = await vc.get_chances(target.id, 95)
    tt_cd = await vc.get_cooldown(target.id, 300)
    bar_len = (vg.current * 2) // 10
    empty_len = 20 - bar_len
    bar_text = f'[{"▣" * bar_len}{"▢" * empty_len}] {vg.current}%'
    response.description = f'{starter} **{vg.current}** vigor.'
    if cursed:
        curse_timer = await curse_ctrl.get_cursed_time(target.id, True)
        response.description += f'\n{curse_ref} are cursed for **{curse_timer}**.'
    response.description += f'\nThat gives {referer} **{tt_chance}%** trick-or-treating luck.'
    response.description += f'\nAnd a **{tt_cd}s** trick-or-treating cooldown.'
    response.description += f'\n```css\n{bar_text}\n```'
    await pld.msg.channel.send(embed=response)
