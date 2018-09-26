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


async def generatecurrency(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        if len(args) >= 2:
            target = message.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(args[0]))
                    await cmd.db.add_resource(target.id, 'currency', amount, False)
                    title_text = f'✅ Ok, I\'ve given {amount} {cmd.bot.cfg.pref.currency} to {target.display_name}.'
                    response = discord.Embed(color=0x77B255, title=title_text)
                except ValueError:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                err_title = f'❗ You can\'t give {cmd.bot.cfg.pref.currency} to bots.'
                response = discord.Embed(color=0xBE1931, title=err_title)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
