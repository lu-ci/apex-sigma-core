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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.resources import SigmaResource
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name


async def toppatches(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    ongoing_msg = None
    now = arrow.utcnow().timestamp
    guild_sum_list = await cmd.db.cache.get_cache(f'guild_pumpkin_patch')
    leader_timer = await cmd.db.cache.get_cache(f'guild_pumpkin_patch_stamp') or now
    if not guild_sum_list or leader_timer + 180 < now:
        ongoing_response = discord.Embed(color=0x3b88c3, title='🔄 Getting pumpkins might take a little while...')
        ongoing_msg = await pld.msg.channel.send(embed=ongoing_response)
        guild_sums = {}
        guild_counts = {}
        all_weights = await cmd.db[cmd.db.db_nam].WeightResource.find({}).to_list(None)
        for weight in all_weights:
            resource = SigmaResource(weight)
            for guild_key in resource.origins.guilds.keys():
                guild_total = guild_sums.get(guild_key, 0)
                guild_count = guild_counts.get(guild_key, 0)
                guild_total += resource.origins.guilds.get(guild_key)
                guild_count += 1
                guild_sums.update({guild_key: guild_total})
                guild_counts.update({guild_key: guild_count})
        guild_sum_list = []
        for gsk in guild_sums.keys():
            guild_sum_list.append({
                'id': int(gsk),
                'val': guild_sums.get(gsk),
                'cnt': guild_counts.get(gsk),
                'avg': guild_sums.get(gsk) / guild_counts.get(gsk)
            })
        guild_sum_list = list(sorted(guild_sum_list, key=lambda x: x.get('avg'), reverse=True))[:20]
        await cmd.db.cache.set_cache(f'guild_pumpkin_patch', guild_sum_list)
        await cmd.db.cache.set_cache(f'guild_pumpkin_patch_stamp', now)
        leader_timer = now
    table_heads = ['#', 'Guild', 'Avg. Weight']
    table_data = []
    for gsx, gsi in enumerate(guild_sum_list):
        guild = await cmd.bot.get_guild(gsi.get('id'))
        table_data.append([
            str(gsx + 1),
            clean_name(guild.name if guild else str(gsi.get('id')), 'Unknown')[:18],
            f'{round(gsi.get("avg") / 1000, 2)}kg'
        ])
    table_body = boop(table_data, table_heads)
    curr_icon = '🎃'
    response = f'{curr_icon} **Guild Pumpkin Patch Leaderboard**'
    response += f'\n```hs\n{table_body}\n```'
    response += f'\nLeaderboard last updated **{arrow.get(leader_timer).humanize()}**.'
    if ongoing_msg:
        try:
            await ongoing_msg.delete()
        except (discord.NotFound, discord.Forbidden):
            pass
    await pld.msg.channel.send(response)
