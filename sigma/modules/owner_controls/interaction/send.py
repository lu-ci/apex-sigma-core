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


async def send(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        error_response = discord.Embed(color=0xBE1931, title='❗ Bad input.')
        try:
            mode, identifier = pld.args[0].split(':')
            identifier = int(identifier)
        except ValueError:
            await pld.msg.channel.send(embed=error_response)
            return
        mode = mode.lower()
        text = ' '.join(pld.args[1:])
        if mode == 'u':
            target = await cmd.bot.get_user(identifier)
            title_end = f'{target.name}#{target.discriminator}'
        elif mode == 'c':
            target = await cmd.bot.get_channel(identifier)
            title_end = f'#{target.name} on {target.guild.name}'
        else:
            await pld.msg.channel.send(embed=error_response)
            return
        if text:
            try:
                await target.send(text)
                response = discord.Embed(color=0x77B255, title=f'✅ Message sent to {title_end}.')
            except discord.Forbidden:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t message that user.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing message to send.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
