# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
from geopy.geocoders import Nominatim

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.searches.meteorology.weather.visual_storage import icons


def get_unit_and_search(args):
    if args[-1].startswith('unit'):
        allowed_units = ['auto', 'ca', 'uk2', 'us', 'si']
        unit_trans = {'c': 'si', 'metric': 'si', 'f': 'us', 'imperial': 'us'}
        if len(args[-1].split(':')) == 2:
            unit = args[-1].split(':')[1].lower()
            if unit in unit_trans:
                unit = unit_trans[unit]
            if unit not in allowed_units:
                unit = 'auto'
        else:
            unit = 'auto'
        search = ' '.join(args[:-1])
    else:
        search = ' '.join(args)
        unit = 'auto'
    return search, unit


def get_dis_and_deg(unit, forecast):
    if unit in ['si', 'ca', 'uk2']:
        if unit == 'uk2':
            deg = '°C'
            dis = 'M'
        else:
            deg = '°C'
            dis = 'KM'
    elif unit == 'auto':
        if '°C' in forecast:
            deg = '°C'
            dis = 'KM'
        else:
            deg = '°F'
            dis = 'M'
    else:
        deg = '°F'
        dis = 'M'
    return dis, deg


async def weather(cmd: SigmaCommand, pld: CommandPayload):
    if cmd.cfg.secret_key:
        if pld.args:
            search, unit = get_unit_and_search(pld.args)
            if search:
                geo_parser = Nominatim()
                try:
                    location = geo_parser.geocode(search)
                except Exception as e:
                    response = discord.Embed(color=0xBE1931, title=f'Geocoder {str(e).lower()}.')
                else:
                    if location:
                        lat = location.latitude
                        lon = location.longitude
                        req_url = f'https://api.darksky.net/forecast/{cmd.cfg.secret_key}/{lat},{lon}?units={unit}'
                        async with aiohttp.ClientSession() as session:
                            async with session.get(req_url) as data:
                                search_data = await data.read()
                                data = json.loads(search_data)
                        curr = data['currently']
                        icon = curr['icon']
                        forecast = data['daily']['summary']
                        dis, deg = get_dis_and_deg(unit, forecast)
                        forecast_title = f'{icons[icon]["icon"]} {curr["summary"]}'
                        response = discord.Embed(color=icons[icon]['color'], title=forecast_title)
                        response.description = f'Location: {location}'
                        response.add_field(name='📄 Forecast', value=forecast, inline=False)
                        info_title = '🌡 Temperature'
                        info_text = f'Current: {round(curr["temperature"], 2)}{deg}'
                        info_text += f'\nFeels Like: {round(curr["apparentTemperature"], 2)}{deg}'
                        info_text += f'\nDew Point: {round(curr["dewPoint"], 2)}{deg}'
                        response.add_field(name=info_title, value=info_text)
                        wind_title = '💨 Wind'
                        wind_text = f'Speed: {round(curr["windSpeed"], 2)} {dis}/H'
                        wind_text += f'\nGust: {round(curr["windGust"], 2)} {dis}/H'
                        wind_text += f'\nBearing: {curr["windBearing"]}°'
                        response.add_field(name=wind_title, value=wind_text)
                        other_title = '📉 Other'
                        other_text = f'Humidity: {round(curr["humidity"] * 100, 2)}%'
                        other_text += f'\nPressure: {round(curr["pressure"], 2)}mbar'
                        if 'visibility' in curr:
                            other_text += f'\nVisibility: {round(curr["visibility"], 2)} {dis}'
                        else:
                            other_text += '\nVisibility: Unknown'
                        response.add_field(name=other_title, value=other_text)
                    else:
                        response = not_found('Location not found.')
            else:
                response = error('Missing location.')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('The API Key is missing.')
    await pld.msg.channel.send(embed=response)
