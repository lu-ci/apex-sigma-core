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

import aiohttp
import arrow
import discord

from sigma.modules.games.warframe.commons.parsers.image_parser import FailedIconGrab, grab_image

aura_list = [
    'brief respite', 'corrosive projection', 'dead eye',
    'emp aura', 'empowered blades', 'enemy radar', 'energy siphon',
    'growing power', 'infested impedance', 'loot detector',
    'physique', 'pistol amp', 'pistol scavenger', 'rejuvenation',
    'rifle amp', 'rifle scavenger', 'shield disruption',
    'shotgun amp', 'shotgun scavenger', 'sniper scavenger',
    'speed holster', 'sprint boost', 'stand united', 'steel charge'
]

overridden_icons = {
    'endo': 'https://vignette.wikia.nocookie.net/warframe/images/f/f2/EndoIconRenderLarge.png'
}


def parse_alert_data(alert_data):
    lines = alert_data.split('\n')
    out_list = []
    for line in lines[:-1]:
        spliced = line.split('|')
        rewards = spliced[9]
        reward_spliced = rewards.split(' - ')
        credit_reward = int(reward_spliced[0].replace(',', '').replace('cr', ''))
        if len(reward_spliced) > 1:
            item_reward = reward_spliced[1]
        else:
            item_reward = None
        data = {
            'id': spliced[0],
            'node': spliced[1],
            'planet': spliced[2],
            'type': spliced[3],
            'faction': spliced[4],
            'levels': {
                'low': spliced[5],
                'high': spliced[6]
            },
            'stamps': {
                'start': int(spliced[7]),
                'end': int(spliced[8])
            },
            'rewards': {
                'credits': credit_reward,
                'item': item_reward
            }
        }
        out_list.append(data)
    return out_list


async def get_alert_data(db):
    alert_url = 'https://deathsnacks.com/wf/data/alerts_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(alert_url) as data:
            alert_data = await data.text()
            alert_data = parse_alert_data(alert_data)
    alert_out = None
    for alert in alert_data:
        event_id = alert['id']
        db_check = await db[db.db_cfg.database]['WarframeCache'].find_one({'EventID': event_id})
        if not db_check:
            await db[db.db_cfg.database]['WarframeCache'].insert_one({'EventID': event_id})
            alert_out = alert
            break
    triggers = []
    if alert_out:
        item_reward = alert_out['rewards']['item']
        if item_reward:
            triggers = item_reward.lower().split(' ')
            if item_reward.lower() in aura_list:
                triggers.append('aura')
            else:
                if 'aura' in triggers:
                    triggers.remove('aura')
    return alert_out, triggers


def get_item_name(reward):
    pieces = reward.title().split(' ')
    try:
        int(pieces[0])
        resource = True
    except ValueError:
        resource = False
    if resource:
        rw_name = '_'.join(pieces[1:])
    else:
        rw_name = '_'.join(pieces)
    return rw_name


async def generate_alert_embed(data):
    timestamp_start = data['stamps']['start']
    timestamp_end = data['stamps']['end']
    duration_sec = timestamp_end - timestamp_start
    duration_tag = str(datetime.timedelta(seconds=duration_sec))
    event_datetime = arrow.get().utcfromtimestamp(timestamp_end).datetime
    response = discord.Embed(color=0xffcc66, timestamp=event_datetime)
    alert_desc = f'Type: {data["faction"]} {data["type"]}'
    alert_desc += f'\nLevels: {data["levels"]["low"]} - {data["levels"]["high"]}'
    alert_desc += f'\nLocation: {data["node"]} ({data["planet"]})'
    alert_desc += f'\nReward: {data["rewards"]["credits"]}cr'
    if data['rewards']['item']:
        if 'riven' in data['rewards']['item']:
            reward_icon = 'https://i.imgur.com/RAQvxog.png'
        else:
            try:
                reward_name = get_item_name(data['rewards']['item'])
                if reward_name.lower() in overridden_icons:
                    reward_icon = overridden_icons.get(reward_name.lower())
                else:
                    reward_icon = await grab_image(reward_name)
            except FailedIconGrab:
                reward_icon = 'https://i.imgur.com/99ennZD.png'
        alert_desc += f' + {data["rewards"]["item"]}'
    else:
        reward_icon = 'https://i.imgur.com/WeUJXIx.png'
    response.add_field(name=f'Warframe Alert', value=f'{alert_desc}')
    response.set_thumbnail(url=reward_icon)
    response.set_footer(icon_url='https://i.imgur.com/99ennZD.png', text=f'Duration: {duration_tag}')
    return response
