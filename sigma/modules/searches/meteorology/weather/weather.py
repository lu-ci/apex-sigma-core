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

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget

api_base = 'https://api.openweathermap.org/data/2.5/weather'
dis_deg_map = {'imperial': ('m', '°F'), 'metric': ('m', '°C')}
condition_map = {
    '01d': ('☀', 0xffac33),
    '02d': ('⛅', 0xffac33),
    '03d': ('🌥', 0xffac33),
    '04d': ('☁', 0xccd6dd),
    '09d': ('🌧', 0x5dadec),
    '10d': ('🌦', 0xffac33),
    '11d': ('⛈', 0xf4900c),
    '13d': ('🌨', 0x5dadec),
    '50d': ('🌫', 0xccd6dd),
    '01n': ('🌕', 0xffd983),
    '02n': ('☁', 0xccd6dd),
    '03n': ('☁', 0xccd6dd),
    '04n': ('☁', 0xccd6dd),
    '09n': ('🌧', 0x5dadec),
    '10n': ('🌧', 0x5dadec),
    '11n': ('⛈', 0xf4900c),
    '13n': ('🌨', 0x5dadec),
    '50n': ('🌫', 0xccd6dd),
}


def parse_query(args):
    """
    :type args: list[str]
    :rtype: str, str
    """
    if args[-1].startswith('unit'):
        units = ['c', 'f', 'metric', 'imperial']
        unit_map = {'c': 'metric', 'f': 'imperial'}
        if len(args[-1].split(':')) == 2:
            unit = args[-1].split(':')[1].lower()
            unit = unit_map.get(unit, unit)
            if unit not in units:
                unit = 'metric'
        else:
            unit = 'metric'
        search = ' '.join(args[:-1])
    else:
        search = ' '.join(args)
        unit = 'metric'
    return search, unit


def get_bearing(deg):
    """
    :type deg: int
    :rtype: str
    """
    directions = [
        ['E', [0, 22.5]],
        ['NE', [22.5, 67.5]],
        ['N', [67.5, 112.5]],
        ['NW', [112.5, 157.5]],
        ['W', [157.5, 202.5]],
        ['SW', [202.5, 247.5]],
        ['S', [247.5, 292.5]],
        ['SE', [292.5, 337.5]],
        ['E', [337.5, 360]]
    ]
    bearing = 'E'
    for direction in directions:
        bearing = direction[0]
        if direction[1][0] <= deg < direction[1][1]:
            break
    return bearing


async def weather(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.api_key:
        if pld.args:
            search, unit = parse_query(pld.args)
            if search:
                api_url = f'{api_base}?appid={cmd.cfg.api_key}&q={search}&units={unit}'
                data: dict = await aioget(api_url, as_json=True)
                if data['cod'] == 200:
                    dis, deg = dis_deg_map[unit]
                    location = f'{data["name"]}, {data["sys"]["country"]}'
                    description = data["weather"][0]["description"].title()
                    icon, color = condition_map[data['weather'][0]['icon']]
                    response = discord.Embed(color=color, title=f'{icon} {location} - {description}')

                    temp_title = '🌡 Temperature'
                    temp_text = f'Actual: **{round(data["main"]["temp"], 2)}{deg}**'
                    temp_text += f'\nFeels Like: **{round(data["main"]["feels_like"], 2)}{deg}**'
                    response.add_field(name=temp_title, value=temp_text)

                    wind_title = '💨 Wind'
                    wind_text = f'Speed: **{round(data["wind"]["speed"], 2)}{dis}/s**'
                    wind_text += f'\nBearing: **{data["wind"]["deg"]}° ({get_bearing(data["wind"]["deg"])})**'
                    response.add_field(name=wind_title, value=wind_text)

                    other_title = '🌎 Atmosphere'
                    other_text = f'Humidity: **{round(data["main"]["humidity"], 2)}%**'
                    other_text += f'\nPressure: **{round(data["main"]["pressure"], 2)}mbar**'
                    response.add_field(name=other_title, value=other_text)
                else:
                    response = GenericResponse('Location not found.').not_found()
            else:
                response = GenericResponse('Missing location.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await pld.msg.channel.send(embed=response)
