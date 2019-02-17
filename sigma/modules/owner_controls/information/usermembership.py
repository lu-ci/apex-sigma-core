# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, not_found


async def usermembership(cmd: SigmaCommand, pld: CommandPayload):
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
            response = discord.Embed(color=target.color)
            response.set_author(name=f'{target.display_name}\'s Server Presence', icon_url=user_avatar(target))
            presence = [g for g in cmd.bot.guilds if g.get_member(target.id)]
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
                response = error('No guild data found.')
        else:
            response = not_found('User not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
