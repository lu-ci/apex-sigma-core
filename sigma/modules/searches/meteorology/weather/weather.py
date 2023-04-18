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

import aiohttp
import discord
from geopy.geocoders import Nominatim

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.searches.meteorology.weather.visual_storage import icons


def get_unit_and_search(args):
    """
    :type args: list[str]
    :rtype: str, str
    """
    if args[-1].startswith('unit'):
        allowed_units = ['auto', 'ca', 'uk2', 'us', 'si']
        unit_trans = {'c': 'si', 'metric': 'si', 'f': 'us', 'imperial': 'us'}
        if len(args[-1].split(':')) == 2:
            unit = args[-1].split(':')[1].lower()
            if unit in unit_trans:
                unit = unit_trans[unit]
            if unit not in allowed_units:
                unit = 'metric'
        else:
            unit = 'metric'
        search = ' '.join(args[:-1])
    else:
        search = ' '.join(args)
        unit = 'metric'
    return search, unit


def get_dis_and_deg(unit):
    """
    :type unit: str
    :rtype: str, str
    """
    if unit == 'imperial':
        dis = 'm'
        deg = '°F'
    else:
        dis = 'm'
        deg = '°C'
    return dis, deg


def get_bearing(deg: int) -> str:
    directions = [
        ['E',[0, 22.5]],
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
            search, unit = get_unit_and_search(pld.args)
            if search:
                api_base = 'https://api.openweathermap.org/data/2.5/weather'
                req_url = f'{api_base}?appid={cmd.cfg.api_key}&q={search}&units={unit}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(req_url) as data:
                        search_data = await data.read()
                        data = json.loads(search_data)
                if data['cod'] == 200:
                    location = f'{data["name"]}, {data["sys"]["country"]}'
                    icon = data['weather'][0]['description']
                    unit = 'metric' if unit == 'auto' else unit
                    dis, deg = get_dis_and_deg(unit)
                    forecast_title = f'{icons[icon]["icon"]} {data["weather"][0]["main"]}'
                    response = discord.Embed(color=icons[icon]['color'], title=forecast_title[:256])
                    response.description = f'Location: {location}'
                    info_title = '🌡 Temperature'
                    info_text = f'Current: {round(data["main"]["temp"], 2)}{deg}'
                    info_text += f'\nFeels Like: {round(data["main"]["feels_like"], 2)}{deg}'
                    response.add_field(name=info_title, value=info_text)
                    wind_title = '💨 Wind'
                    wind_text = f'Speed: {round(data["wind"]["speed"], 2)} {dis}/s'
                    wind_text += f'\nBearing: {data["wind"]["deg"]}° ({get_bearing(data["wind"]["deg"])})'
                    response.add_field(name=wind_title, value=wind_text)
                    other_title = '📉 Other'
                    other_text = f'Humidity: {round(data["main"]["humidity"], 2)}%'
                    other_text += f'\nPressure: {round(data["main"]["pressure"], 2)}mbar'
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
