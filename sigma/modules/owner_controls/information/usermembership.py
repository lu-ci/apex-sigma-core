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


async def usermembership(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = ' '.join(args)
        all_members = cmd.bot.get_all_members()
        if '#' in lookup:
            uname = lookup.split('#')[0].lower()
            udisc = lookup.split('#')[1]
            target = discord.utils.find(lambda u: u.name.lower() == uname and u.discriminator == udisc, all_members)
        else:
            try:
                target = discord.utils.find(lambda u: u.id == int(lookup), all_members)
            except ValueError:
                target = None
        if target:
            response = discord.Embed(color=target.color)
            response.set_author(name=f'{target.display_name}\'s Server Presence', icon_url=user_avatar(target))
            presence = [g for g in cmd.bot.guilds if discord.utils.find(lambda g: g.id == target.id, g.members)]
            if presence:
                line_list = []
                for guild in presence:
                    try:
                        invs = await guild.invites()
                        inv = invs[0] if invs else None
                    except discord.Forbidden:
                        inv = None
                    list_line = f'[{guild.name}]({inv.url})' if inv else guild.name
                    line_list.append(list_line)
                response.description = '\n'.join(line_list)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No guild data found.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 User not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
