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


async def givecurrency(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            if message.mentions:
                target = message.mentions[0]
                try:
                    amount = abs(int(args[0]))
                except ValueError:
                    amount = None
                if amount:
                    current_kud = await cmd.db.get_currency(message.author, message.guild).get('current')
                    current_kud = current_kud.get('current')
                    if current_kud >= amount:
                        await cmd.db.rmv_currency(message.author, amount)
                        await cmd.db.add_currency(target, message.guild, amount, additive=False)
                        title = f'✅ Transferred {amount} to {target.display_name}.'
                        response = discord.Embed(color=0x77B255, title=title)
                    else:
                        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have that much.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    await message.channel.send(embed=response)
