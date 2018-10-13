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
from sigma.modules.minigames.racing.nodes.race_storage import races, add_participant, names, colors


async def joinrace(cmd: SigmaCommand, message: discord.Message, args: list):
    currency = f'{cmd.bot.cfg.pref.currency}'
    if message.channel.id in races:
        race = races[message.channel.id]
        buyin = race['buyin']
        kud = await cmd.db.get_resource(message.author.id, 'currency')
        kud = kud.current
        if not await cmd.db.is_sabotaged(message.author.id):
            if kud >= buyin:
                if len(race['users']) < 10:
                    user_found = False
                    for user in race['users']:
                        if user['user'].id == message.author.id:
                            user_found = True
                            break
                    if not user_found:
                        icon = add_participant(message.channel.id, message.author)
                        if names[icon][0] in ['a', 'e', 'i', 'o', 'u']:
                            connector = 'an'
                        else:
                            connector = 'a'
                        join_title = f'{icon} {message.author.display_name} joined as {connector} {names[icon]}!'
                        response = discord.Embed(color=colors[icon], title=join_title)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ You are already in the race!')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Sorry, no more room left!')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ You don\'t have that much {currency}!')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ We failed to sign you up for the race.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ There is no race in preparation.')
    await message.channel.send(embed=response)
