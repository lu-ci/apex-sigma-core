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

import discord


async def bots(cmd, message, args):
    online_bots = []
    offline_bots = []
    total_bots = 0
    for user in message.guild.members:
        if user.bot:
            total_bots += 1
            name = user.name + '#' + user.discriminator
            status = str(user.status)
            if status == 'offline':
                offline_bots.append(name)
            else:
                online_bots.append(name)
    if total_bots == 0:
        embed = discord.Embed(title='❗ No bots were found on this server.', color=0xBE1931)
    else:
        embed = discord.Embed(title='Bot Status on ' + message.guild.name, color=0x1ABC9C)
        embed.add_field(name='Online', value='```\n - ' + '\n - '.join(sorted(online_bots)) + '\n```')
        embed.add_field(name='Offline', value='```\n' + ' - ' + '\n - '.join(sorted(offline_bots)) + '\n```')
    await message.channel.send(None, embed=embed)
