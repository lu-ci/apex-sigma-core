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
from sigma.core.utilities.data_processing import user_avatar


async def wallet(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    currency = await cmd.db.get_currency(target, message.guild)
    currency_name = cmd.bot.cfg.pref.currency
    currency_icon = cmd.bot.cfg.pref.currency_icon
    response = discord.Embed(color=0xaa8dd8)
    response.set_author(name=f'{target.display_name}\'s Currency Data', icon_url=avatar)
    current_title = f'{currency_icon} Current Amount'
    guild_title = '🎪 Earned Here'
    global_title = '🌍 Earned Globally'
    response.add_field(name=current_title, value=f"```py\n{currency['current']} {currency_name}\n```", inline=True)
    response.add_field(name=guild_title, value=f"```py\n{currency['guild']} {currency_name}\n```", inline=True)
    response.add_field(name=global_title, value=f"```py\n{currency['global']} {currency_name}\n```", inline=True)
    response.set_footer(text=f'{currency_icon} {currency_name} is earned by participating in minigames.')
    await message.channel.send(embed=response)
