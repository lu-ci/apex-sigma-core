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

import arrow
import discord

from sigma.modules.games.warframe.commons.worldstate import WorldState

invasion_icon = 'https://i.imgur.com/QUPS0ql.png'
faction_colors = {'grineer': 0xff5050, 'corpus': 0x6699ff, 'infestation': 0x339966}
aura_list = [
    'brief respite', 'corrosive projection', 'dead eye',
    'emp aura', 'empowered blades', 'enemy radar', 'energy siphon',
    'growing power', 'infested impedance', 'loot detector',
    'physique', 'pistol amp', 'pistol scavenger', 'rejuvenation',
    'rifle amp', 'rifle scavenger', 'shield disruption',
    'shotgun amp', 'shotgun scavenger', 'sniper scavenger',
    'speed holster', 'sprint boost', 'stand united', 'steel charge'
]


async def get_invasion_data(db):
    """

    :param db:
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: dict, list[str]
    """
    invasions = await WorldState().invasions
    invasion_out = None
    triggers = ['invasion']
    for invasion in invasions:
        event_id = invasion['id']
        db_check = await db[db.db_nam].WarframeCache.find_one({'event_id': event_id})
        if not db_check:
            active = invasion['endScore'] > abs(invasion['score'])
            if active:
                now = arrow.utcnow().int_timestamp
                await db[db.db_nam].WarframeCache.insert_one({'event_id': event_id, 'created': now})
                invasion_out = invasion
                item_rewards = [invasion_out['rewardsDefender']['items'][0]['name']]
                if invasion.get('rewardsAttacker'):
                    item_rewards.append(invasion_out['rewardsAttacker']['items'][0]['name'])
                for item_reward in item_rewards:
                    triggers += item_reward.lower().split(' ')
                    if item_reward.lower() in aura_list:
                        triggers.append('aura')
    return invasion_out, triggers


async def generate_invasion_embed(data):
    """

    :param data:
    :type data: dict
    :return:
    :rtype: discord.Embed
    """
    timestamp_start = data['start']
    event_datetime = arrow.get(timestamp_start).datetime
    attacker = data['factionAttacker']
    color = faction_colors.get(attacker.lower().split()[0], 0xF9F9F9)
    response = discord.Embed(color=color, timestamp=event_datetime)
    invasion_desc = f'Factions: {data["factionDefender"]} vs {data["factionAttacker"]}'
    invasion_desc += f'\nLocation: {data["location"]}'
    reward_def = data['rewardsDefender']['items'][0]
    reward_one = f'{reward_def["count"]} {reward_def["name"]}'
    invasion_desc += f'\nRewards: {reward_one}'
    if data.get('rewardsAttacker'):
        reward_atk = data['rewardsAttacker']['items'][0]
        reward_two = f'{reward_atk["count"]} {reward_atk["name"]}'
        invasion_desc += f' vs {reward_two}'
    response.add_field(name='Warframe Invasion', value=invasion_desc)
    response.set_thumbnail(url=invasion_icon)
    return response
