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

import datetime
import json

import aiohttp
import arrow
import discord

TIMER_URL = 'https://www.xenoveritas.org/static/ffxiv/timer.html'
TIMER_API = 'https://www.xenoveritas.org/static/ffxiv/timers.json?v=99v8'
FFXIV_LOGO = 'https://i.imgur.com/ZCA8EsI.png'
FFXIV_COLOR = 0x9f2637


def add_timer_block(response, timer_data):
    """
    :type response: discord.Embed
    :type timer_data: dict
    """
    name = timer_data.get('name').split('>')[1].split('<')[0]
    now = arrow.utcnow()
    start = arrow.get(timer_data.get('start') / 1000)
    end_stamp = timer_data.get('end')
    if end_stamp:
        end = arrow.get(timer_data.get('end') / 1000)
        diff = to_delta(end) if now > start else to_delta(start)
        end_text = f'{end.format("DD. MMM. YYYY")} (In {diff})'
    else:
        end_text = timer_data.get('endLabel', 'Unspecified')
    descriptive = f'{start.format("DD. MMM. YYYY")} - {end_text}'
    response.add_field(name=f'{name}', value=descriptive, inline=False)


def next_daily():
    """
    Gets the next daily timer.
    :rtype: arrow.Arrow
    """
    now = arrow.utcnow()
    ttd = arrow.get(arrow.utcnow().format('YYYY-MM-DD 15:00:ssZZ'))
    while now > ttd:
        ttd = ttd.shift(days=1)
    return ttd


def next_weekly():
    """
    Gets the next weekly timer.
    :rtype: arrow.Arrow
    """
    starting_point = '2019-05-14 08:00:00+00:00'
    now = arrow.utcnow()
    ttw = arrow.get(starting_point)
    while now > ttw:
        ttw = ttw.shift(weeks=1)
    return ttw


def to_delta(arrow_object):
    """
    :type arrow_object: arrow.Arrow
    :rtype: str
    """
    now = arrow.utcnow().int_timestamp
    aot = arrow_object.int_timestamp
    out = datetime.timedelta(seconds=abs(now - aot))
    return str(out)


async def finalfantasyxivtimers(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(TIMER_API) as timer_api_req:
            timer_api_resp = await timer_api_req.read()
            timer_data = json.loads(timer_api_resp)
    timers = timer_data.get('timers')
    daily_delta, weekly_delta = to_delta(next_daily()), to_delta(next_weekly())
    response = discord.Embed(color=FFXIV_COLOR)
    response.set_author(name='Final Fantasy XIV Event Timers', url=TIMER_URL, icon_url=FFXIV_LOGO)
    response.description = f'Daily Reset: In {daily_delta}\nWeekly Reset: In {weekly_delta}'
    response.set_footer(text='All dates and times are shown in UTC.')
    if timers:
        timers = list(sorted(timers, key=lambda t: t.get('end', 0)))
        for timer in timers:
            add_timer_block(response, timer)
    await pld.msg.channel.send(embed=response)
