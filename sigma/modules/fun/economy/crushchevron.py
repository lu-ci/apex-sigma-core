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
from sigma.modules.core_functions.chevron.spawn_chevron import chev_cache
from sigma.modules.fun.economy.grabchevron import interact_chevron


async def crushchevron(cmd: SigmaCommand, message: discord.Message, args: list):
    chev_data = chev_cache.get_cache(message.channel.id) if message.guild else None
    if chev_data:
        chev_good, chev_attrib = chev_data
        if args:
            chev_look = ' '.join(args).lower()
            if chev_look.lower() == chev_attrib.lower():
                chev_cache.del_cache(message.channel.id)
                await interact_chevron(cmd.db, message.author, chev_good, chev_attrib, 'crush')
                if chev_good:
                    chevron = '🔷'
                    color = 0x55acee
                    response_text = 'This is a negative chevron, it was purified and added to your inventory.'
                else:
                    chevron = '🔻'
                    color = 0xe75a70
                    response_text = 'This is a positive chevron, it destroyed half of your other chevrons...'
                response = discord.Embed(color=color, title=f'{chevron} You caught a {chev_attrib} chevron!')
                response.description = response_text
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ I don\'t think it\'s a {chev_look} chevron.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ I don\'t know what type of chevron it is.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ I don\'t see any chevron.')
    await message.channel.send(embed=response)
