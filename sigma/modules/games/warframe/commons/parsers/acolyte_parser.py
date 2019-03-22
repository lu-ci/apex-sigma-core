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

import hashlib

import arrow
import discord

from sigma.modules.games.warframe.commons.worldstate import WorldState

ac_imgs = {
    'angst': 'https://vignette.wikia.nocookie.net/warframe/images/e/ec/StrikerAcolyte.png',
    'malice': 'https://vignette.wikia.nocookie.net/warframe/images/1/1b/HeavyAcolyte.png',
    'mania': 'https://vignette.wikia.nocookie.net/warframe/images/a/a9/RogueAcolyte.png',
    'misery': 'https://vignette.wikia.nocookie.net/warframe/images/1/19/AreaCasterAcolyte.png',
    'torment': 'https://vignette.wikia.nocookie.net/warframe/images/3/38/ControlAcolyte.png',
    'violence': 'https://vignette.wikia.nocookie.net/warframe/images/5/56/DuellistAcolyte.png'
}


def make_acolyte_id(ac_name, ac_location):
    time_sect = arrow.utcnow().format('YYYY-MM-DD-HH')
    hash_string = f'acolyte_{ac_name}_{ac_location}_ {time_sect}'
    cryp = hashlib.new('md5')
    cryp.update(hash_string.encode('utf-8'))
    return cryp.hexdigest()


async def get_acolyte_data(db):
    acolytes = await WorldState().acolytes
    acolytes_out = None
    triggers = ['acolyte']
    if acolytes:
        for acolyte in acolytes:
            if acolyte.get('discovered'):
                ac_id = make_acolyte_id(acolyte.get('name'), acolyte.get('location'))
                db_check = await db[db.db_nam].WarframeCache.find_one({'event_id': ac_id})
                if not db_check:
                    now = arrow.utcnow().timestamp
                    await db[db.db_nam].WarframeCache.insert_one({'event_id': ac_id, 'created': now})
                    acolytes_out = acolyte
                    triggers.append((acolytes_out.get('name').lower()))
                    break
    return acolytes_out, triggers


def generate_acolyte_embed(acd):
    details = f'Health: **{round(acd.get("health") * 100, 2)}%**'
    details += f'\nLocation: **{acd.get("location")}**'
    response = discord.Embed(color=0xcc0000, title=f'{acd.get("name")} has been found!')
    response.set_thumbnail(url=ac_imgs.get(acd.get("name").lower()))
    response.description = details
    return response
