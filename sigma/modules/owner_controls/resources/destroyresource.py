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


async def destroyresource(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.mentions:
        if len(args) >= 3:
            target = message.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(args[-1]))
                    res_nam = 'currency' if args[0].lower() == cmd.bot.cfg.pref.currency.lower() else args[0].lower()
                    target_amount = await cmd.db.get_resource(target.id, res_nam)
                    target_amount = target_amount.current
                    if amount <= target_amount:
                        await cmd.db.del_resource(target.id, res_nam, amount, cmd.name, message)
                        title_text = f'🔥 Ok, {amount} of {target.display_name}\'s {res_nam} '
                        title_text += 'has been destroyed.'
                        response = discord.Embed(color=0xFFCC4D, title=title_text)
                    else:
                        err_title = f'❗ {target.display_name} does\'t have that much {cmd.bot.cfg.pref.currency}.'
                        response = discord.Embed(color=0xBE1931, title=err_title)
                except ValueError:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                err_title = f'❗ You can\'t take {cmd.bot.cfg.pref.currency} from bots.'
                response = discord.Embed(color=0xBE1931, title=err_title)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
