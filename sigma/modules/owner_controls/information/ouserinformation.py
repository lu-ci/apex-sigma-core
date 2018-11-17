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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar, get_image_colors


async def ouserinformation(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        lookup = pld.args[0].lower()
        if '#' in lookup:
            uname = lookup.split('#')[0].lower()
            udisc = lookup.split('#')[1]
            target = discord.utils.find(lambda u: u.name.lower() == uname and u.discriminator == udisc, cmd.bot.users)
        else:
            try:
                target = await cmd.bot.get_user(int(lookup))
            except ValueError:
                target = None
        if target:
            user_color = await get_image_colors(user_avatar(target))
            response = discord.Embed(color=user_color)
            response.set_author(name=f'{target.display_name}\'s Information', icon_url=user_avatar(target))
            creation_time = arrow.get(target.created_at).format('DD. MMMM YYYY')
            user_text = f'Username: **{target.name}**#{target.discriminator}'
            user_text += f'\nID: **{target.id}**'
            user_text += f'\nBot User: **{target.bot}**'
            user_text += f'\nCreated: **{creation_time}**'
            presence = [g for g in cmd.bot.guilds if g.get_member(target.id)]
            response.add_field(name='User Info', value=user_text)
            response.set_footer(text=f'This user is in {len(presence)} guilds.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 User not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
