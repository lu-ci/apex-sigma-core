﻿"""
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
from sigma.core.utilities.generic_responses import GenericResponse


async def poll(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not pld.args:
        out_content = GenericResponse('Nothing inputted.').error()
        await pld.msg.channel.send(embed=out_content)
        return
    all_qry = ' '.join(pld.args)
    if all_qry.endswith(';'):
        all_qry = all_qry[:-1]
    poll_name = all_qry.split('; ')[0]
    choice_qry = '; '.join(all_qry.split('; ')[1:])
    if choice_qry.endswith(';'):
        choice_qry = choice_qry[:-1]
    poll_choices = choice_qry.split('; ')
    if len(poll_choices) < 2:
        out_content = GenericResponse('Not enough arguments.').error()
        await pld.msg.channel.send(embed=out_content)
        return
    if len(poll_choices) > 9:
        out_content = GenericResponse('Maximum is 9 choices.').error()
        await pld.msg.channel.send(embed=out_content)
        return
    icon_list_base = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🍍 🍅 🍆 🌶 🌽 🍠 🍞 🍗 🍟 🍕 🍺 🍷 🍬 🍙'.split()
    choice_text = ''
    emoji_list = []
    for option in poll_choices:
        emoji = icon_list_base.pop(secrets.randbelow(len(icon_list_base)))
        emoji_list.append(emoji)
        choice_text += f'\n{emoji} - {option}'
    out_content = discord.Embed(color=pld.msg.author.color)
    out_content.set_author(name=f'{pld.msg.author.name}\'s Poll', icon_url=user_avatar(pld.msg.author))
    out_content.description = poll_name
    out_content.add_field(name='Choices', value=choice_text)
    out_content.set_footer(text=f'[{secrets.token_hex(3)}] React with your vote below!')
    poll_message = await pld.msg.channel.send(embed=out_content)
    for emoji in emoji_list:
        await poll_message.add_reaction(emoji)
