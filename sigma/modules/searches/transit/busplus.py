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
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand

bp_logo = "https://i.imgur.com/bNxFe09.png"


def find_hr(times: list, hr: int):
    data = None
    for elem in times:
        if elem.get('hour') == hr:
            data = elem
    return data


def make_time(hour: int, minutes: int):
    hour = str(hour) if len(str(hour)) == 2 else f'0{hour}'
    minutes = str(minutes) if len(str(minutes)) == 2 else f'0{minutes}'
    return f'{hour}:{minutes}'


def make_time_list(terminus_times: list, current_time: arrow.Arrow, data_pool: str):
    time_list = []
    previous_hour = int(current_time.shift(hours=-1).format('HH'))
    current_hour = int(current_time.format('HH'))
    next_hour = int(current_time.shift(hours=1).format('HH'))
    prev_hr = find_hr(terminus_times, previous_hour)
    curr_hr = find_hr(terminus_times, current_hour)
    next_hr = find_hr(terminus_times, next_hour)
    for hour_set in [prev_hr, curr_hr, next_hr]:
        if hour_set:
            hour = hour_set.get('hour')
            minute_set = hour_set.get(data_pool)
            for minutes in minute_set:
                time_list.append(make_time(hour, minutes))
    return time_list


async def busplus(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        line_number = "%20".join(args)
        api_url = f'https://api.lucia.moe/rest/bus/times/{line_number}'
        current_time = arrow.utcnow().to('Europe/Belgrade')
        current_day = current_time.format('d')
        data_pool = 'sun' if current_day == '7' else 'sat' if current_day == '6' else 'reg'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data:
                data = await data.read()
                data = json.loads(data)
        if isinstance(data, list):
            response = discord.Embed(color=0x003050)
            response.set_author(name=f'BusPlus: Line {" ".join(args)} Departures', icon_url=bp_logo)
            for terminus in data:
                terminus_name = terminus.get('terminus').title()
                terminus_times = terminus.get('times')
                time_list = make_time_list(terminus_times, current_time, data_pool)
                response.add_field(name=terminus_name, value=" | ".join(time_list), inline=False)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Line not found or bad data.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing line number.')
    await message.channel.send(embed=response)
