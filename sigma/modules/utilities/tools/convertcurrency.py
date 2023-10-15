"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
from typing import Optional

import aiohttp
import arrow
import discord

from sigma.core.utilities.generic_responses import GenericResponse

API_BASE = 'https://openexchangerates.org/api'

CURRENCIES_BASE = f'{API_BASE}/currencies.json' \
                  f'?prettyprint=false' \
                  f'&show_alternative=true' \
                  f'&show_inactive=false'
LATEST_BASE = f'{API_BASE}/latest.json' \
              f'?prettyprint=false' \
              f'&show_alternative=true'

CURRENCIES_EXPIRATION = 7 * 24 * 60 * 60
LATEST_EXPIRATION = 24 * 60 * 60


async def get_timed_document(db, name, expiration) -> Optional[dict]:
    data = None
    now = arrow.utcnow().float_timestamp
    doc = await db[db.db_nam].Currencies.find_one({'name': name})
    if doc:
        ts = doc.get('timestamp')
        expired = now - ts > expiration
        if not expired:
            data = doc.get('data')
    return data


async def get_currencies_from_db(db) -> Optional[dict]:
    return await get_timed_document(db, 'currencies', CURRENCIES_EXPIRATION)


async def get_latest_from_db(db):
    return await get_timed_document(db, 'latest', LATEST_EXPIRATION)


async def fetch_response(uri: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as data:
            data = await data.read()
            data = json.loads(data)
    return data


async def update_currencies(db, app_id: str) -> dict:
    now = arrow.utcnow().float_timestamp
    uri = f'{CURRENCIES_BASE}&app_id={app_id}'
    data = await fetch_response(uri)
    await db[db.db_nam].Currencies.update_one(
        {'name': 'currencies'},
        {'$set': {'data': data, 'timestamp': now}},
        upsert=True
    )
    return data


async def update_latest(db, app_id: str) -> dict:
    now = arrow.utcnow().float_timestamp
    uri = f'{LATEST_BASE}&app_id={app_id}'
    data = await fetch_response(uri)
    await db[db.db_nam].Currencies.update_one(
        {'name': 'latest'},
        {'$set': {'data': data.get('rates'), 'timestamp': now}},
        upsert=True
    )
    return data.get('rates')


def convert(amount: float, from_curr: str, to_curr: str, rates: dict) -> float:
    if from_curr == to_curr:
        converted = amount
    else:
        to_usd = amount / rates.get(from_curr)
        converted = to_usd * rates.get(to_curr)
    return converted


async def convertcurrency(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.app_id:
        if pld.args:
            if len(pld.args) == 4:
                currencies = await get_currencies_from_db(cmd.db)
                if not currencies:
                    currencies = await update_currencies(cmd.db, cmd.cfg.app_id)
                from_curr = pld.args[1].upper()
                to_curr = pld.args[3].upper()
                if from_curr in currencies:
                    if to_curr in currencies:
                        amount = pld.args[0]
                        try:
                            amount = float(amount)
                        except ValueError:
                            amount = None
                        if amount:
                            rates = await get_latest_from_db(cmd.db)
                            if not rates:
                                rates = await update_latest(cmd.db, cmd.cfg.app_id)
                            converted = convert(amount, from_curr, to_curr, rates)
                            title = f'🏧 Currency Exchange: {from_curr} -> {to_curr}'
                            response = discord.Embed(color=0x3B88C3, title=title)
                            response.add_field(name=currencies.get(from_curr), value=round(amount, 4))
                            response.add_field(name=currencies.get(to_curr), value=round(converted, 4))
                        else:
                            response = GenericResponse('Invalid amount.').error()
                    else:
                        response = GenericResponse('Unrecognized target currency.').error()
                else:
                    response = GenericResponse('Unrecognized source currency.').error()
            else:
                response = GenericResponse('Bad number of arguments.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    if response:
        await pld.msg.channel.send(embed=response)
