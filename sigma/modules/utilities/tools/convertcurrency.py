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
import json

import aiohttp
import discord


async def convertcurrency(cmd, message, args):
    if args:
        if len(args) == 4:
            amount = args[0]
            from_curr = args[1].upper()
            to_curr = args[3].upper()
            try:
                amount = float(amount)
            except ValueError:
                amount = None
            if amount:
                response = None
                start_response = discord.Embed(color=0x3B88C3, title='🏧 Contacting our banks...')
                start_message = await message.channel.send(embed=start_response)
                api_url = f'http://free.currencyconverterapi.com/api/v3/convert?q={from_curr}_{to_curr}&compact=ultra'
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url) as data:
                        data = await data.read()
                        data = json.loads(data)
                if data:
                    curr_key = list(data.keys())[0]
                    multi = data[curr_key]
                    out_amount = round(amount * multi, 5)
                    title = f'🏧 {amount} {from_curr} = {out_amount} {to_curr}'
                    end_response = discord.Embed(color=0x3B88C3, title=title)
                else:
                    end_response = discord.Embed(color=0xBE1931, title='❗ Invalid currency.')
                await start_message.edit(embed=end_response)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Bad number of arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    if response:
        await message.channel.send(embed=response)
