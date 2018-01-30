# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import arrow
import discord

wows_icon = 'https://i.imgur.com/Cv53UoN.png'
wows_color = 0x066661
regions = {
    'eu': 'eu',
    'europe': 'eu',
    'na': 'com',
    'us': 'com'
}


async def worldofwarships(cmd, message, args):
    if 'app_id' in cmd.cfg:
        app_id = cmd.cfg['app_id']
        if args:
            if len(args) > 1:
                game_region = args[0].lower()
                if game_region in regions:
                    game_region = regions.get(game_region)
                    username = ' '.join(args[1:])
                    user_search_url_base = f'https://api.worldofwarships.{game_region}'
                    user_search_url_base += f'/wows/account/list/?application_id={app_id}&search={username}'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(user_search_url_base) as data:
                            data = await data.read()
                            data = json.loads(data)
                            if 'data' in data:
                                data = data['data']
                            else:
                                data = None
                    if data:
                        data = data[0]
                        account_id = data['account_id']
                        nickname = data['nickname']
                        profile_url = f'https://api.worldofwarships.{game_region}'
                        profile_url += f'/wows/account/info/?application_id={app_id}&account_id={account_id}'
                        async with aiohttp.ClientSession() as session:
                            async with session.get(profile_url) as data:
                                data = await data.read()
                                data = json.loads(data)
                                data = data['data'][str(account_id)]
                        if data:
                            stats = data['statistics']
                            distance = stats['distance']
                            battle_count = stats['battles']
                            pvp_stats = stats['pvp']
                            main_battery = pvp_stats['main_battery']
                            max_frags = main_battery['max_frags_battle']
                            frags = main_battery['frags']
                            hits = main_battery['hits']
                            shots = main_battery['shots']
                            profile_stats = f'Level: {data["leveling_tier"]}'
                            profile_stats += f'\nDistance: {distance} KM'
                            profile_stats += f'\nJoin Date: {arrow.get(data["created_at"]).format("DD. MMMM YYYY")}'
                            last_played = f'Last Played: {arrow.get(data["last_battle_time"]).format("DD. MMMM YYYY")}'
                            profile_stats += f'\n{last_played}'
                            profile_stats += f'\nBattles: {battle_count}'
                            profile_stats += f'\nShots: {shots}'
                            profile_stats += f'\nHits: {hits} ({int((hits / shots) * 100)}%)'
                            profile_stats += f'\nKills: {frags} (Max: {max_frags})'
                            response = discord.Embed(color=wows_color)
                            response.set_footer(text='World of Warships Statistics.', icon_url=wows_icon)
                            response.add_field(name=f'📇 {nickname}\'s Profile', value=profile_stats, inline=False)
                        else:
                            response = discord.Embed(color=0x696969, title=f'🔍 No statistics found for {nickname}.')
                    else:
                        response = discord.Embed(color=0x696969, title='🔍 User not found.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid game region.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing API key.')
    await message.channel.send(embed=response)
