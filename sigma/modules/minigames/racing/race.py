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

import asyncio
import secrets

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.racing.nodes.race_storage import colors, make_race, races


async def check_resources(db, users, amt):
    """
    :type db: sigma.core.mechanics.database.Database
    :type users: list
    :type amt: int
    :rtype: bool
    """
    ok = True
    if amt:
        for user in users:
            res = await db.get_resource(user['user'].id, 'currency')
            if res.current < amt:
                ok = False
                break
    return ok


async def race(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lines = None
    # noinspection PyBroadException
    try:
        if pld.msg.channel.id not in races:
            if pld.args:
                try:
                    buyin = abs(int(pld.args[0]))
                except ValueError:
                    buyin = 0
            else:
                buyin = 0
            if not len(str(buyin)) > 200:
                currency = f'{cmd.bot.cfg.pref.currency}'
                make_race(pld.msg.channel.id, buyin)
                start_title = '🚀 A race is starting in 30 seconds.'
                if buyin > 0:
                    start_title = f'🚀 A {buyin} {currency} race is starting in 30 seconds.'
                create_response = discord.Embed(color=0x3B88C3, title=start_title)
                pfx = cmd.db.get_prefix(pld.settings)
                create_response.set_footer(text=f'We need 2 participants! Type {pfx}joinrace to join!')
                await pld.msg.channel.send(embed=create_response)
                await asyncio.sleep(30)
                race_instance = races[pld.msg.channel.id]
                if len(race_instance['users']) >= 2:
                    values = {}
                    highest = 0
                    leader = None
                    skip = False
                    while highest < 20:
                        lines = '```\n'
                        for participant in race_instance['users']:
                            if not skip:
                                move = secrets.randbelow(5) + 1
                            else:
                                move = 0
                            val = values.get(participant['user'].id, 0)
                            val += move
                            if val >= 20:
                                val = 20
                                win = True
                                skip = True
                            else:
                                win = False
                            values.update({participant['user'].id: val})
                            lines += f'\n⏩ {" " * val}{participant["icon"]}{" " * (20 - val)} ⏸'
                            if win:
                                lines += f' 🏆: {participant["user"].display_name}'
                            else:
                                part_name = participant["user"].display_name
                                if len(part_name) > 10:
                                    part_name = part_name[:7] + '...'
                                lines += f' {int((val / 20) * 100)}%: {part_name}'
                            if highest < val:
                                highest = val
                                leader = participant
                        lines += '\n```'
                    await pld.msg.channel.send(lines)
                    have_buyin = await check_resources(cmd.db, race_instance['users'], buyin)
                    if have_buyin:
                        win_title = f'{leader["icon"]} {leader["user"].display_name} has won!'
                        for user in race_instance['users']:
                            await cmd.db.del_resource(user['user'].id, 'currency', buyin, cmd.name, pld.msg)
                        if race_instance['buyin']:
                            winnings = race_instance["buyin"] * len(race_instance['users'])
                            await cmd.db.add_resource(leader['user'].id, 'currency', winnings, cmd.name, pld.msg, False)
                            win_title = f'{win_title[:-1]} and got {winnings} {currency}!'
                        response = discord.Embed(color=colors[leader['icon']], title=win_title)
                    else:
                        response = GenericResponse('Some participants lost their funds in the meantime!').error()
                        response.description = f'Someone spent their {currency} before the race finished.'
                else:
                    response = GenericResponse('Not enough participants in the race!').error()
            else:
                response = GenericResponse('Buyin can\'t be longer than 200 digits.').error()
        else:
            response = GenericResponse('There is already one ongoing.').error()
    except Exception:
        response = GenericResponse('Something broke so we are canceling the race.').error()
    if pld.msg.channel.id in races:
        del races[pld.msg.channel.id]
    await pld.msg.channel.send(content=lines, embed=response)
