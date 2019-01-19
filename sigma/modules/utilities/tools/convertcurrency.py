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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def convertcurrency(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        if len(pld.args) == 4:
            amount = pld.args[0]
            from_curr = pld.args[1].upper()
            to_curr = pld.args[3].upper()
            try:
                amount = float(amount)
            except ValueError:
                amount = None
            if amount:
                response = None
                start_response = discord.Embed(color=0x3B88C3, title='🏧 Contacting our banks...')
                start_message = await pld.msg.channel.send(embed=start_response)
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
                    end_response = error('Invalid currency.')
                await start_message.edit(embed=end_response)
            else:
                response = error('Invalid amount.')
        else:
            response = error('Bad number of arguments.')
    else:
        response = error('Nothing inputted.')
    if response:
        await pld.msg.channel.send(embed=response)
