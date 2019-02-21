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

import datetime
import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import not_found, warn


def time_to_seconds(time):
    hrs, mins, secs = time.split(':')
    output = (int(hrs) * 3600) + (int(mins) * 60) + int(secs)
    return output


def get_usercaps(username, trials):
    output = username
    for trial in trials:
        for player in trial['players']:
            if player.lower() == username.lower():
                output = player
                break
    return output


async def wftrials(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        username = ' '.join(pld.args)
        trials_url = f'https://api.trials.wf/api/player/pc/{username}/completed'
        async with aiohttp.ClientSession() as session:
            async with session.get(trials_url) as data:
                trial_data = await data.read()
                trial_data = json.loads(trial_data)
        if len(trial_data) == 0:
            response = not_found(f'User {username} Not Found.')
        else:
            # noinspection PyBroadException
            try:
                username_proper = get_usercaps(username, trial_data)
                raidlist_url = f'https://trials.wf/player/?user={username_proper}'
                # LoR
                lor_deaths = 0
                lor_kills = 0
                lor_time_total = 0
                lor_time_short = 0
                lor_count = 0
                lor_won = 0
                lor_failed = 0

                # LoR NM
                lornm_deaths = 0
                lornm_kills = 0
                lornm_time_total = 0
                lornm_time_short = 0
                lornm_count = 0
                lornm_won = 0
                lornm_failed = 0

                # JV
                jv_deaths = 0
                jv_kills = 0
                jv_time_total = 0
                jv_time_short = 0
                jv_count = 0
                jv_won = 0
                jv_failed = 0

                # Calculate Data
                for trial in trial_data:
                    if trial['type'] == 'lor':
                        lor_deaths += trial['deaths']
                        lor_kills += trial['kills']
                        lor_time_total += time_to_seconds(trial['time'])
                        if lor_time_short == 0:
                            lor_time_short = time_to_seconds(trial['time'])
                        else:
                            if lor_time_short > time_to_seconds(trial['time']):
                                if trial['objective'] == 'VICTORY':
                                    lor_time_short = time_to_seconds(trial['time'])
                        lor_count += 1
                        if trial['objective'] == 'VICTORY':
                            lor_won += 1
                        elif trial['objective'] == 'FAILED':
                            lor_failed += 1
                    elif trial['type'] == 'lornm':
                        lornm_deaths += trial['deaths']
                        lornm_kills += trial['kills']
                        lornm_time_total += time_to_seconds(trial['time'])
                        lornm_count += 1
                        if trial['objective'] == 'VICTORY':
                            lornm_won += 1
                        elif trial['objective'] == 'FAILED':
                            lornm_failed += 1
                        if lornm_time_short == 0:
                            lornm_time_short = time_to_seconds(trial['time'])
                        else:
                            if lornm_time_short > time_to_seconds(trial['time']):
                                if trial['objective'] == 'VICTORY':
                                    lornm_time_short = time_to_seconds(trial['time'])
                    elif trial['type'] == 'jv':
                        jv_deaths += trial['deaths']
                        jv_kills += trial['kills']
                        jv_time_total += time_to_seconds(trial['time'])
                        jv_count += 1
                        if trial['objective'] == 'VICTORY':
                            jv_won += 1
                        elif trial['objective'] == 'FAILED':
                            jv_failed += 1
                        if jv_time_short == 0:
                            jv_time_short = time_to_seconds(trial['time'])
                        else:
                            if jv_time_short > time_to_seconds(trial['time']):
                                if trial['objective'] == 'VICTORY':
                                    jv_time_short = time_to_seconds(trial['time'])

                # Total
                total_deaths = lor_deaths + lornm_deaths + jv_deaths
                total_kills = lor_kills + lornm_kills + jv_kills
                total_time_total = lor_time_total + lornm_time_total + jv_time_total
                total_time_short = 0
                short_times = [lor_time_short, lornm_time_short, jv_time_short]
                for short_time in short_times:
                    if total_time_short == 0:
                        total_time_short = short_time
                    else:
                        if total_time_short > short_time:
                            total_time_short = short_time
                total_count = lor_count + lornm_count + jv_count
                total_won = lor_won + lornm_won + jv_won
                total_failed = lor_failed + lornm_failed + jv_failed

                # Make Descriptions
                try:
                    lor_desc = f'Total: {lor_count}'
                    lor_desc += f'\nWin/Lose: {lor_won}/{lor_failed}'
                    lor_desc += f'\nTotal Time: {str(datetime.timedelta(seconds=lor_time_total))}'
                    lor_desc += f'\nAverage Time: {str(datetime.timedelta(seconds=(lor_time_total // lor_count)))}'
                    lor_desc += f'\nShortest Time: {str(datetime.timedelta(seconds=lor_time_short))}'
                    lor_desc += f'\nKills: {lor_kills}'
                    lor_desc += f'\nAverage Kills: {lor_kills // lor_count}'
                    lor_desc += f'\nDeaths: {lor_deaths}'
                    lor_desc += f'\nAverage Deaths: {lor_deaths // lor_count}'
                except ZeroDivisionError:
                    lor_desc = 'Invalid Data'
                try:
                    lornm_desc = f'Total: {lornm_count}'
                    lornm_desc += f'\nWin/Lose: {lornm_won}/{lornm_failed}'
                    lornm_desc += f'\nTotal Time: {str(datetime.timedelta(seconds=lornm_time_total))}'
                    lornm_avg_sec = lornm_time_total // lornm_count
                    lornm_desc += f'\nAverage Time: {str(datetime.timedelta(seconds=lornm_avg_sec))}'
                    lornm_desc += f'\nShortest Time: {str(datetime.timedelta(seconds=lornm_time_short))}'
                    lornm_desc += f'\nKills: {lornm_kills}'
                    lornm_desc += f'\nAverage Kills: {lornm_kills // lornm_count}'
                    lornm_desc += f'\nDeaths: {lornm_deaths}'
                    lornm_desc += f'\nAverage Deaths: {lornm_deaths // lornm_count}'
                except ZeroDivisionError:
                    lornm_desc = 'Invalid Data'
                try:
                    jv_desc = f'Total: {jv_count}'
                    jv_desc += f'\nWin/Lose: {jv_won}/{jv_failed}'
                    jv_desc += f'\nTotal Time: {str(datetime.timedelta(seconds=jv_time_total))}'
                    jv_desc += f'\nAverage Time: {str(datetime.timedelta(seconds=(jv_time_total // jv_count)))}'
                    jv_desc += f'\nShortest Time: {str(datetime.timedelta(seconds=jv_time_short))}'
                    jv_desc += f'\nKills: {jv_kills}'
                    jv_desc += f'\nAverage Kills: {jv_kills // jv_count}'
                    jv_desc += f'\nDeaths: {jv_deaths}'
                    jv_desc += f'\nAverage Deaths: {jv_deaths // jv_count}'
                except ZeroDivisionError:
                    jv_desc = 'Invalid Data'
                try:
                    total_desc = f'Total: {total_count}'
                    total_desc += f'\nWin/Lose: {total_won}/{total_failed}'
                    total_desc += f'\nTotal Time: {str(datetime.timedelta(seconds=total_time_total))}'
                    total_desc += '\nAverage Time: '
                    total_desc += f'{str(datetime.timedelta(seconds=(total_time_total // total_count)))}'
                    total_desc += f'\nShortest Time: {str(datetime.timedelta(seconds=total_time_short))}'
                    total_desc += f'\nKills: {total_kills}'
                    total_desc += f'\nAverage Kills: {total_kills // total_count}'
                    total_desc += f'\nDeaths: {total_deaths}'
                    total_desc += f'\nAverage Deaths: {total_deaths // total_count}'
                except ZeroDivisionError:
                    total_desc = 'Invalid Data'
                response = discord.Embed(color=0xa12626)
                response.set_thumbnail(url='https://i.imgur.com/pf89nIk.png')
                response.set_author(name=username_proper, icon_url='https://i.imgur.com/n0EESkn.png', url=raidlist_url)
                response.add_field(name='Law of Retribution', value=lor_desc)
                response.add_field(name='Nightmare LoR', value=lornm_desc)
                response.add_field(name='Jordas Verdict', value=jv_desc)
                response.add_field(name='Total Trials', value=total_desc)
            except Exception:
                response = warn(f'Stats for {username} were found but contained errors.')
        await pld.msg.channel.send(embed=response)
