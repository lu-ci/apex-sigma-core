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
from sigma.core.utilities.data_processing import user_avatar, get_image_colors


def count_chevrons(chevron_list):
    gg = 0
    bg = 0
    gc = 0
    bc = 0
    for chev in chevron_list:
        good = chev.get('good')
        act = chev.get('act')
        if good:
            if act == 'crush':
                gc += 1
            elif act == 'grab':
                gg += 1
        else:
            if act == 'crush':
                bc += 1
            elif act == 'grab':
                bg += 1
    return gg, gc, bg, bc


async def chevrons(cmd: SigmaCommand, message: discord.Message, args: list):
    target = message.mentions[0] if message.mentions else message.author
    profile = await cmd.db[cmd.db.db_nam].Profiles.find_one({'user_id': target.id}) or {}
    chevron_data = profile.get('chevrons', {})
    chevron_list = chevron_data.get('items', [])
    chevron_tally = chevron_data.get('total', 0)
    starter = 'You have' if message.author.id == target.id else f'{target.name} has'
    ender = '' if chevron_tally == 1 else 's'
    grabbed_good, crushed_good, grabbed_bad, crushed_bad = count_chevrons(chevron_list)
    response_title = f'{starter} a total tally of {chevron_tally} chevron{ender}.'
    response_text = f'Grabbed **{grabbed_good}** good and **{grabbed_bad}** bad chevrons.'
    response_text += f'\nCrushed **{crushed_good}** good and **{crushed_bad}** bad chevrons.'
    response = discord.Embed(color=await get_image_colors(user_avatar(target)))
    response.set_author(name=response_title, icon_url=user_avatar(target))
    response.description = response_text
    await message.channel.send(embed=response)

