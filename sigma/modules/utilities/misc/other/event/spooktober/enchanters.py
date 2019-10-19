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
import datetime

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_enchantment_controller


async def enchanters(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    encore = get_enchantment_controller(cmd.db)
    encs = await encore.get_enchanters(target.id)
    if encs:
        response = discord.Embed(color=0x55acee)
        response.set_author(name=f'{target.name}\'s Enchanters', icon_url=user_avatar(target))
        enchanter_block_lines = []
        for enc in encs:
            enc_usr = await cmd.bot.get_user(int(enc))
            enc_nam = enc_usr.name if enc_usr else enc
            time_diff = encs.get(enc) + encore.time_limit - arrow.utcnow().timestamp
            time_text = datetime.timedelta(seconds=time_diff)
            enchanter_block_lines.append(f'**{time_text}** from {enc_nam}')
        enchanter_block_lines = list(sorted(enchanter_block_lines))
        response.description = '\n'.join(enchanter_block_lines)
    else:
        starter = 'You are' if target.id == pld.msg.author.id else f'{target.name} is'
        response = error(f'{starter} not enchanted.')
    await pld.msg.channel.send(embed=response)
