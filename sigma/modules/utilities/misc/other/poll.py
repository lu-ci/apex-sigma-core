# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def poll(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Missing Arguments.')
        await message.channel.send(None, embed=out_content)
        return
    all_qry = ' '.join(args)
    if all_qry.endswith(';'):
        all_qry = all_qry[:-1]
    poll_name = all_qry.split('; ')[0]
    choice_qry = '; '.join(all_qry.split('; ')[1:])
    if choice_qry.endswith(';'):
        choice_qry = choice_qry[:-1]
    poll_choices = choice_qry.split('; ')
    if len(poll_choices) < 2:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Not enough arguments present.')
        await message.channel.send(None, embed=out_content)
        return
    if len(poll_choices) > 9:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Maximum is 9 choices.')
        await message.channel.send(None, embed=out_content)
        return
    icon_list_base = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🍍 🍅 🍆 🌶 🌽 🍠 🍞 🍗 🍟 🍕 🍺 🍷 🍬 🍙'.split()
    choice_text = ''
    op_num = 0
    emoji_list = []
    for option in poll_choices:
        emoji = icon_list_base.pop(secrets.randbelow(len(icon_list_base)))
        emoji_list.append(emoji)
        choice_text += '\n' + emoji + ' - **' + option + '**'
        op_num += 1
    out_content = discord.Embed(color=0x1ABC9C)
    out_content.add_field(name=poll_name, value=choice_text)
    poll_message = await message.channel.send(None, embed=out_content)
    ic_num = 0
    for emoji in emoji_list:
        await poll_message.add_reaction(emoji=emoji)
        ic_num += 1
