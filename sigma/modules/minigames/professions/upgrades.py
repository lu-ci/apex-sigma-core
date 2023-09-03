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

from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list


def get_stamina_effect(level: int) -> int:
    limit = 2
    base_cooldown = 20
    cooldown = int(base_cooldown - ((base_cooldown / 100) * ((level * 0.5) / (1.25 + (0.01 * level)))))
    cooldown = cooldown if cooldown >= limit else limit
    return base_cooldown - cooldown


def get_oven_effect(level: int) -> int:
    base_cooldown = 3600
    stamina_mod = level / (1.25 + (0.01 * level))
    cooldown = int(base_cooldown - ((base_cooldown / 100) * stamina_mod))
    return base_cooldown - cooldown


def get_casino_effect(level: int) -> int:
    limit = 5
    base_cooldown = 60
    cooldown = int(base_cooldown - ((base_cooldown / 100) * ((level * 0.5) / (1.25 + (0.01 * level)))))
    cooldown = cooldown if cooldown >= limit else limit
    return base_cooldown - cooldown


def calculate_upgrade(up_id, level):
    """
    :type up_id: str
    :type level: int
    :rtype: dict
    """
    up_table = {
        'stamina': {
            'amount': -get_stamina_effect(level),
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
            'amount': -get_oven_effect(level),
            'end': 'Seconds'
        },
        'casino': {
            'amount': -get_casino_effect(level),
            'end': 'Seconds'
        },
        'harem': {
            'amount': 10 + level,
            'end': 'Spaces'
        }
    }
    return up_table[up_id]


async def upgrades(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    upgrade_file = await cmd.db.get_profile(target.id, 'upgrades') or {}
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
        amount = up_data["amount"]
        suffix = up_data["end"]
        if suffix.endswith('s'):
            if abs(amount) == 1:
                suffix = suffix[:-1]
        upgrade_text += f'\n**Level {upgrade_level}** {upgrade["name"]}: **{amount} {suffix}**'
    upgrade_list_embed = discord.Embed(color=0xF9F9F9, title=f'🛍 {target.display_name}\'s Sigma Upgrades')
    upgrade_list_embed.description = upgrade_text
    await pld.msg.channel.send(embed=upgrade_list_embed)
