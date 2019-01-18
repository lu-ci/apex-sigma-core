# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def lovecalculator(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.mentions:
        if len(pld.msg.mentions) in [1, 2]:
            first_tar = None
            second_tar = None
            if len(pld.msg.mentions) == 1:
                first_tar = pld.msg.author
                second_tar = pld.msg.mentions[0]
            elif len(pld.msg.mentions) == 2:
                first_tar = pld.msg.mentions[0]
                second_tar = pld.msg.mentions[1]
            first_item = first_tar.display_name
            second_item = second_tar.display_name
            value_one_one = int(str(first_tar.id)[6])
            value_one_two = int(str(first_tar.id)[9])
            value_two_one = int(str(second_tar.id)[6])
            value_two_two = int(str(second_tar.id)[9])
            mod_one = (10 - abs(value_one_one - value_two_one)) * 10
            mod_two = (10 - abs(value_one_two - value_two_two)) * 10
            value = (mod_one + mod_two) // 2
            bar_len = (value * 2) // 10
            empty_len = 20 - bar_len
            bar_text = f'[{"▣"*bar_len}{"▢"*empty_len}] {value}%'
            response = discord.Embed(color=0xff6666, title='💝 Love Calculator')
            response.add_field(name='First Item', value=f'```haskell\n{first_item}\n```')
            response.add_field(name='Second Item', value=f'```haskell\n{second_item}\n```')
            response.add_field(name='Value', value=f'```css\n{bar_text}\n```', inline=False)
        else:
            response = error('No targets given.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
