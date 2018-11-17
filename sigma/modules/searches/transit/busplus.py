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

import aiohttp
import arrow
import discord
import lxml.html as lx

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.payload import CommandPayload

bp_logo = "https://i.imgur.com/bNxFe09.png"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


async def get_line_url(line_number: str):
    url_base = 'https://www.busevi.com'
    async with aiohttp.ClientSession() as session:
        async with session.get(url_base) as qs_session:
            home_html = await qs_session.text()
    root = lx.fromstring(home_html)
    line_url = None
    line_buttons = root.cssselect('.vc_btn3')
    for line_button in line_buttons:
        if line_button.text:
            if line_button.text.lower().strip() == line_number.lower():
                line_url = f'{url_base}{line_button.attrib.get("href")}'
                break
    return line_url


def parse_time(element):
    row_list = []
    for row in element:
        text_list = []
        for column in row:
            text_list.append(column.text.strip() if column.text else None)
        row_list.append(text_list)
    return row_list


def parse_title(head):
    line_title_split = head.text_content().strip().split('\n')
    line_title_one = line_title_split[0].strip()
    line_title_two = line_title_split[-1][2:].strip()
    return [line_title_one, line_title_two]


def parse_slices(slices: list):
    slice_list = []
    for slice_piece in slices:
        slice_data = {}
        slice_hour = int(slice_piece[0])
        try:
            regular_minutes = [int(minutes) for minutes in slice_piece[1].split()]
        except (IndexError, AttributeError):
            regular_minutes = []
        try:
            saturday_minutes = [int(minutes) for minutes in slice_piece[2].split()]
        except (IndexError, AttributeError):
            saturday_minutes = []
        try:
            sunday_minutes = [int(minutes) for minutes in slice_piece[3].split()]
        except (IndexError, AttributeError):
            sunday_minutes = []
        slice_data.update(
            {
                'hour': slice_hour,
                'reg': regular_minutes,
                'sat': saturday_minutes,
                'sun': sunday_minutes
            }
        )
        slice_list.append(slice_data)
    return slice_list


async def get_time_table(page_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as qs_session:
            time_html = await qs_session.text()
    root = lx.fromstring(time_html)
    table_elems = root.cssselect('.row-hover')
    table_elem_index_one = int((len(table_elems) / 2)) - 1
    table_elem_index_two = len(table_elems) - 1
    table_elems = [table_elems[table_elem_index_one], table_elems[table_elem_index_two]]
    loop_index = 0
    time_data = []
    line_title_heads = root.cssselect('.wpb_wrapper')[8]
    for element in table_elems:
        line_title = parse_title(line_title_heads)[loop_index]
        time_slices = parse_time(element)
        parsed_slices = parse_slices(time_slices)
        slice_data = {'terminus': line_title, 'times': parsed_slices}
        time_data.append(slice_data)
        loop_index += 1
    return time_data


def parse_lines(html_str: str):
    root = lx.fromstring(html_str)
    line_items = root.cssselect('.asl_res_url')
    line_list = []
    for line_item in line_items:
        line_url = line_item.attrib.get('href')
        line_name = line_item.text.strip()
        line_data = {'name': line_name, 'url': line_url}
        line_list.append(line_data)
    return line_list


def get_correct(lookup: int, itterable: list):
    result = None
    for itter in itterable:
        itter_name = itter.get('name')
        if itter_name.startswith(f'Linija {lookup}'):
            result = itter
            break
    return result


async def get_line_data(db: Database, line_number: str):
    target_cache = await db[db.db_nam].BusPlusCache.find_one({'Line': line_number})
    if target_cache:
        target_cache.pop('_id')
        result = target_cache.get('Timetable')
    else:
        target_line = await get_line_url(line_number)
        if target_line:
            time_table_data = await get_time_table(target_line)
            line_data = {'Line': line_number, 'Timetable': time_table_data}
            if target_cache is None:
                await db[db.db_nam].BusPlusCache.insert_one(line_data)
            else:
                await db[db.db_nam].BusPlusCache.update_one({'Line': line_number}, {'$set': line_data})
            result = time_table_data or {'error': 'Line data not found.'}
        else:
            result = {'error': 'Line data not found.'}
    return result


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


async def busplus(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        line_number = " ".join(pld.args)
        current_time = arrow.utcnow().to('Europe/Belgrade')
        current_day = current_time.format('d')
        data_pool = 'sun' if current_day == '7' else 'sat' if current_day == '6' else 'reg'
        data = await get_line_data(cmd.db, line_number)
        if isinstance(data, list):
            response = discord.Embed(color=0x003050)
            response.set_author(name=f'BusPlus: Line {" ".join(pld.args)} Departures', icon_url=bp_logo)
            for terminus in data:
                terminus_name = terminus.get('terminus').title()
                terminus_times = terminus.get('times')
                time_list = make_time_list(terminus_times, current_time, data_pool)
                response.add_field(name=terminus_name, value=" | ".join(time_list), inline=False)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Line not found or bad data.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing line number.')
    await pld.msg.channel.send(embed=response)
