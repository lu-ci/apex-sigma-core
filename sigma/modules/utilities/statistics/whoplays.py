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


async def whoplays(cmd, message, args):
    if not args:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        game_title = ' '.join(args)
        gamer_list = ''
        x = 0
        y = 0
        for member in message.guild.members:
            if member.game:
                x += 1
                if str(member.game).lower() == game_title.lower():
                    y += 1
                    gamer_list += member.name + ', '
        gamer_list = gamer_list[:-2]
        if gamer_list == '':
            gamer_list = 'None'
        title = f'{y}/{x} people are playing {game_title}'
        gamers = '```\n' + gamer_list + '\n```'
        response = discord.Embed(color=0x1ABC9C)
        response.add_field(name=title, value=gamers)
    await message.channel.send(None, embed=response)
