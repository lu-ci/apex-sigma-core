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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.racing.nodes.race_storage import add_participant, colors, names, races


async def joinrace(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    currency = f'{cmd.bot.cfg.pref.currency}'
    if pld.msg.channel.id in races:
        race = races[pld.msg.channel.id]
        buyin = race['buyin']
        kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
        kud = kud.current
        if not await cmd.db.is_sabotaged(pld.msg.author.id):
            if kud >= buyin:
                if len(race['users']) < 10:
                    user_found = False
                    for user in race['users']:
                        if user['user'].id == pld.msg.author.id:
                            user_found = True
                            break
                    if not user_found:
                        icon = add_participant(pld.msg.channel.id, pld.msg.author)
                        if names[icon][0] in ['a', 'e', 'i', 'o', 'u']:
                            connector = 'an'
                        else:
                            connector = 'a'
                        join_title = f'{icon} {pld.msg.author.display_name} joined as {connector} {names[icon]}!'
                        response = discord.Embed(color=colors[icon], title=join_title)
                    else:
                        response = GenericResponse('You are already in the race!').error()
                else:
                    response = GenericResponse('Sorry, no more room left!').error()
            else:
                response = GenericResponse(f'You don\'t have that much {currency}!').error()
        else:
            response = GenericResponse('We failed to sign you up for the race.').error()
    else:
        response = GenericResponse('There is no race in preparation.').error()
    await pld.msg.channel.send(embed=response)
