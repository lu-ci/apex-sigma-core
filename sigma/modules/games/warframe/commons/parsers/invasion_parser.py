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

aura_list = [
    'brief respite', 'corrosive projection', 'dead eye',
    'emp aura', 'empowered blades', 'enemy radar', 'energy siphon',
    'growing power', 'infested impedance', 'loot detector',
    'physique', 'pistol amp', 'pistol scavenger', 'rejuvenation',
    'rifle amp', 'rifle scavenger', 'shield disruption',
    'shotgun amp', 'shotgun scavenger', 'sniper scavenger',
    'speed holster', 'sprint boost', 'stand united', 'steel charge'
]


def item_name_fixer(item_name):
    if ' ' not in item_name:
        item_name_new = ''
        for char in item_name:
            if char == char.upper():
                if char != item_name[0]:
                    item_name_new += f' {char}'
                else:
                    item_name_new += char
            else:
                item_name_new += char
    else:
        item_name_new = item_name
    return item_name_new


def parse_invasion_data(invasion_data):
    lines = invasion_data.split('\n')
    out_list = []
    for line in lines[1:-1]:
        spliced = line.split('|')
        data = {
            'id': spliced[0],
            'title': spliced[-1],
            'node': spliced[1],
            'planet': spliced[2],
            'factions': {
                'one': spliced[3],
                'two': spliced[8]
            },
            'stamps': {
                'start': int(lines[0]),
                'end': int(spliced[13])
            },
            'rewards': {
                'one': item_name_fixer(spliced[5]),
                'two': item_name_fixer(spliced[10])
            }
        }
        out_list.append(data)
    return out_list


async def get_invasion_data(db):
    invasion_url = 'https://deathsnacks.com/wf/data/invasion_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(invasion_url) as data:
            invasion_data = await data.text()
            invasion_data = parse_invasion_data(invasion_data)
    invasion_out = None
    for invasion in invasion_data:
        event_id = invasion['id']
        db_check = await db[db.db_cfg.database].WarframeCache.find_one({'EventID': event_id})
        if not db_check:
            now = arrow.utcnow().timestamp
            await db[db.db_cfg.database].WarframeCache.insert_one({'EventID': event_id, 'Created': now})
            invasion_out = invasion
            break
    triggers = ['invasion']
    if invasion_out:
        item_rewards = [invasion_out['rewards']['one'], invasion_out['rewards']['two']]
        for item_reward in item_rewards:
            triggers += item_reward.lower().split(' ')
            if item_reward.lower() in aura_list:
                triggers.append('aura')
    return invasion_out, triggers


async def generate_invasion_embed(data):
    timestamp_end = data['stamps']['end']
    event_datetime = arrow.get().utcfromtimestamp(timestamp_end).datetime
    title = data['title']
    if title.lower().startswith('grin'):
        color = 0xff5050
    elif title.lower().startswith('corp'):
        color = 0x6699ff
    elif title.lower().startswith('inf'):
        color = 0x339966
    elif title.lower().startswith('phor'):
        color = 0x339966
    else:
        color = 0xF9F9F9
    response = discord.Embed(color=color, timestamp=event_datetime)
    invasion_desc = f'Factions: {data["factions"]["one"]} vs {data["factions"]["two"]}'
    invasion_desc += f'\nLocation: {data["node"]} ({data["planet"]})'
    if data['factions']['one'].lower().startswith('infes'):
        invasion_desc += f'\nReward: {data["rewards"]["two"]}'
    elif data['factions']['two'].lower().startswith('infes'):
        invasion_desc += f'\nReward: {data["rewards"]["one"]}'
    else:
        invasion_desc += f'\nRewards: {data["rewards"]["one"]} vs {data["rewards"]["two"]}'
    response.add_field(name=data['title'], value=f'{invasion_desc}')
    response.set_thumbnail(url='https://i.imgur.com/QUPS0ql.png')
    return response
