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

import operator

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.paginator import PaginatorCore


def make_games_dict(guild):
    """
    :type guild: discord.Guild
    :rtype: dict, int, int
    """
    games = {}
    online_count = 0
    playing_count = 0
    for member in guild.members:
        status = str(member.status)
        if status != 'offline':
            online_count += 1
        if member.bot:
            continue
        if not member.activity:
            continue
        if not member.activity.name:
            continue
        game_name = member.activity.name
        repl_name = game_name.replace(' ', '')
        if repl_name != '':
            playing_count += 1
            if game_name not in games:
                games.update({game_name: 1})
            else:
                curr_count = games[game_name]
                new_count = curr_count + 1
                games.update({game_name: new_count})
    return games, online_count, playing_count


async def ingame(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    response = discord.Embed(color=0x1ABC9C)
    games, online, playing = make_games_dict(pld.msg.guild)
    sorted_games = sorted(games.items(), key=operator.itemgetter(1), reverse=True)
    page = pld.args[0] if pld.args else 1
    game_list, page = PaginatorCore.paginate(sorted_games, page)
    start_range = (page - 1) * 10
    out_table_list = []
    game_count = len(sorted_games)
    index = start_range
    for key, value in game_list:
        index += 1
        if len(key) > 32:
            key = key[:32] + '...'
        out_table_list.append([str(index), key, value, str(value / playing * 100).split('.')[0] + '%'])
    output = boop(out_table_list)
    general_stats_list = [['Online', online], ['In-Game', playing], ['Unique Games', game_count]]
    out_block = f'```hs\n{boop(general_stats_list)}\n```'
    response.add_field(name='👾 Current Gaming Statistics on ' + pld.msg.guild.name, value=out_block, inline=False)
    response.add_field(name=f'🎮 By Game on Page {page}', value=f'```haskell\n{output}\n```', inline=False)
    await pld.msg.channel.send(embed=response)
