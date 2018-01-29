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


async def send(cmd, message, args):
    if args:
        mode, identifier = args[0].split(':')
        identifier = int(identifier)
        mode = mode.lower()
        text = ' '.join(args[1:])
        if mode == 'u':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_members())
            title_end = f'{target.name}#{target.discriminator}'
        elif mode == 'c':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_channels())
            title_end = f'#{target.name} on {target.guild.name}'
        else:
            embed = discord.Embed(color=0xBE1931, title='❗ Invalid Arguments Given.')
            await message.channel.send(embed=embed)
            return
        await target.send(text)
        embed = discord.Embed(color=0x77B255, title=f'✅ Message sent to {title_end}.')
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(color=0xBE1931, title='❗ No Arguments Given.')
        await message.channel.send(embed=embed)
