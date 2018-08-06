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


async def quote(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0]
        try:
            lookup = int(lookup)
        except ValueError:
            lookup = None
        if lookup:
            try:
                msg = await message.channel.get_message(lookup)
            except discord.NotFound:
                msg = None
            if not msg:
                for channel in message.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        try:
                            msg = await channel.get_message(lookup)
                            break
                        except discord.Forbidden:
                            msg = None
                        except discord.NotFound:
                            msg = None
            if msg:
                if msg.content:
                    location = f'{msg.guild.name} | #{msg.channel.name}'
                    response = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
                    response.set_author(name=f'{msg.author.display_name}', icon_url=user_avatar(msg.author))
                    response.description = msg.content
                    response.set_footer(text=location)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ That message has no text content.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Message not found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid message ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing message ID.')
    await message.channel.send(embed=response)
