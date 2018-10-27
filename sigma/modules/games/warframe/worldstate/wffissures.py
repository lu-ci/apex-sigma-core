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

import datetime
import json

import aiohttp
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload

tier_names = {
    'VoidT1': 'Lith',
    'VoidT2': 'Meso',
    'VoidT3': 'Neo',
    'VoidT4': 'Axi'
}
fissure_icon = 'https://i.imgur.com/vANGxqe.png'


async def wffissures(_cmd: SigmaCommand, pld: CommandPayload):
    fissure_url = 'https://deathsnacks.com/wf/data/activemissions.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(fissure_url) as data:
            fissure_data = await data.read()
            fissure_list = json.loads(fissure_data)
    response = discord.Embed(color=0x66ccff, title='Currently Ongoing Fissures')
    fissure_list = sorted(fissure_list, key=lambda k: k['Modifier'])
    for fis in fissure_list:
        relic_tier = tier_names[fis['Modifier']]
        fis_desc = f'Location: {fis["Node"]}'
        time_left = fis['Expiry']['sec'] - arrow.utcnow().timestamp
        death_time = str(datetime.timedelta(seconds=time_left))
        fis_desc += f'\nDisappears In: {death_time}'
        response.add_field(name=f'{relic_tier} Void Fissure', value=fis_desc, inline=False)
    response.set_footer(text='Timers are not updated live.')
    response.set_thumbnail(url=fissure_icon)
    await pld.msg.channel.send(embed=response)
