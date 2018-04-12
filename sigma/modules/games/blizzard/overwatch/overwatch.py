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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.games.blizzard.overwatch.mech.utility import ow_icon, region_convert, clean_numbers, get_profile


async def overwatch(cmd: SigmaCommand, message: discord.Message, args: list):
    init_resp = discord.Embed(color=0xff9c00)
    init_resp.set_author(name='Processing information...', icon_url=ow_icon)
    init_resp_msg = await message.channel.send(embed=init_resp)
    if args:
        if len(args) >= 2:
            region = args[0].lower()
            if region in region_convert:
                region = region_convert.get(region)
            region_list = ['eu', 'kr', 'us', 'cn', 'jp']
            if region in region_list:
                battletag = ' '.join(args[1:])
                profile, timeout, failed = await get_profile(battletag, region)
                if not failed:
                    if not timeout:
                        if profile:
                            profile = profile.get(region)
                            stats = profile.get('stats').get('quickplay')
                            profile_url = 'https://playoverwatch.com/en-us/career/pc/'
                            profile_url += f'{region}/{battletag.replace("#", "-")}'
                            gen = clean_numbers(stats.get('overall_stats'))
                            gms = clean_numbers(stats.get('game_stats'))
                            gen_section = f'Level: **{((gen.get("prestige") or 0) * 100) + gen.get("level")}**'
                            gen_section += f' | Won: **{gen.get("wins")}**'
                            gen_section += f' | Rank: **{gen.get("comprank")}**'
                            gen_section += f'\nBronze: **{gms.get("medals_bronze")}**'
                            gen_section += f' | Silver: **{gms.get("medals_silver")}**'
                            gen_section += f' | Gold: **{gms.get("medals_gold")}**'
                            gms_section = f'Cards: **{gms.get("cards")}**'
                            gms_section += f' | Healing Done: **{gms.get("healing_done")}**'
                            gms_section += f'\nKills: **{gms.get("eliminations")}**'
                            gms_section += f' | Deaths: **{gms.get("deaths")}**'
                            gms_section += f' | Kill Streak: **{gms.get("kill_streak_best")}**'
                            gms_section += f'\nMelee Kills: **{gms.get("melee_final_blows")}**'
                            gms_section += f' | Best Multikill: **{gms.get("multikill_best")}**'
                            gms_section += f' | Solo Kills: **{gms.get("solo_kills")}**'
                            gms_section += f'\nTotal Damage: **{gms.get("all_damage_done")}**'
                            gms_section += f' | Most Hero Damage: **{gms.get("hero_damage_done_most_in_game")}**'
                            gms_section += f'\nTime Played: **{gms.get("time_played")}**h'
                            gms_section += f' | Objective Time: **{gms.get("objective_time")}**h'
                            gms_section += f' | Time on Fire: **{gms.get("time_spent_on_fire")}**h'
                            response = discord.Embed(color=0xff9c00)
                            response.set_author(name=battletag, icon_url=gen.get("avatar"), url=profile_url)
                            response.set_thumbnail(url=gen.get("avatar"))
                            response.add_field(name='Profile Info', value=gen_section, inline=False)
                            response.add_field(name='Combat Stats', value=gms_section, inline=False)
                            footer_text = 'Click the battletag at the top to see the user\'s profile.'
                            response.set_footer(text=footer_text, icon_url=ow_icon)
                        else:
                            response = discord.Embed(color=0x696969, title='🔍 No results.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Sorry, my request timed out.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Sorry, I failed to retrieve any data.')
            else:
                region_error_text = f'Supported: {", ".join(region_list)}.\nOr: {", ".join(list(region_convert))}.'
                response = discord.Embed(color=0xBE1931)
                response.add_field(name='❗ Invalid region.', value=region_error_text)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Region and Battletag needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await init_resp_msg.edit(embed=response)
