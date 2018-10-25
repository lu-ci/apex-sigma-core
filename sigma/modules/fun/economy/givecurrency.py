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


async def givecurrency(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        if len(args) >= 2:
            if message.mentions:
                target = message.mentions[0]
                try:
                    amount = abs(int(args[0]))
                except ValueError:
                    amount = None
                if amount:
                    if not await cmd.db.is_sabotaged(target.id) and not await cmd.db.is_sabotaged(message.author.id):
                        current_kud = await cmd.db.get_resource(message.author.id, 'currency')
                        current_kud = current_kud.current
                        if current_kud >= amount:
                            await cmd.db.del_resource(message.author.id, 'currency', amount, cmd.name, message)
                            await cmd.db.add_resource(target.id, 'currency', amount, cmd.name, message, False)
                            title = f'✅ Transferred {amount} to {target.display_name}.'
                            response = discord.Embed(color=0x77B255, title=title)
                        else:
                            response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have that much.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Transaction declined by Lucia\'s Guard.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
