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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list


def calculate_upgrade(up_id, level):
    up_table = {
        'stamina': {
            'amount': -(60 - (int(60 - ((60 / 100) * ((level * 0.5) / (1.25 + (0.01 * level))))))),
            'end': 'Seconds'
        },
        'luck': {
            'amount': int((0.5 * level) / (1.5 + (0.0018 * level))),
            'end': '% Luckier'
        },
        'storage': {
            'amount': 64 + (level * 8),
            'end': 'Spaces'
        },
        'oven': {
            'amount': -(3600 - (int(3600 - ((3600 / 100) * (level / (1.25 + (0.01 * level))))))),
            'end': 'Seconds'
        },
        'casino': {
            'amount': -(60 - (int(60 - ((60 / 100) * ((level * 0.5) / (1.25 + (0.01 * level))))))),
            'end': 'Seconds'
        },
        'harem': {
            'amount': 10 + level,
            'end': 'Spaces'
        }
    }
    return up_table[up_id]


async def upgrades(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    upgrade_file = await cmd.db[cmd.db.db_nam].Upgrades.find_one({'UserID': target.id})
    if upgrade_file is None:
        await cmd.db[cmd.db.db_nam].Upgrades.insert_one({'UserID': target.id})
        upgrade_file = {}
    upgrade_text = ''
    upgrade_index = 0
    for upgrade in upgrade_list:
        upgrade_index += 1
        upgrade_id = upgrade['id']
        if upgrade_id in upgrade_file:
            upgrade_level = upgrade_file[upgrade_id]
        else:
            upgrade_level = 0
        up_data = calculate_upgrade(upgrade_id, upgrade_level)
        upgrade_text += f'\n**Level {upgrade_level}** {upgrade["name"]}: **{up_data["amount"]} {up_data["end"]}**'
    upgrade_list_embed = discord.Embed(color=0xF9F9F9, title=f'🛍 {target.display_name}\'s Sigma Upgrades')
    upgrade_list_embed.description = upgrade_text
    await message.channel.send(embed=upgrade_list_embed)
