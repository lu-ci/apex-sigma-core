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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.searches.safebooru.mech.safe_core import grab_post_list, generate_embed

links = []
embed_titles = ['Touch fluffy ears~']


async def usagimimi(cmd: SigmaCommand, message: discord.Message, args: list):
    global links
    if not links:
        name = cmd.bot.user.name
        filler_message = discord.Embed(color=0xEEEEEE, title=f'🐰 One moment, filling {name} with bunnies...')
        fill_notify = await message.channel.send(embed=filler_message)
        links = await grab_post_list('bunny_ears')
        filler_done = discord.Embed(color=0xEEEEEE, title=f'🐰 We added {len(links)} bunnies!')
        await fill_notify.edit(embed=filler_done)
    rand_pop = secrets.randbelow(len(links))
    post_choice = links.pop(rand_pop)
    icon = 'https://www.nautiljon.com/images/perso/00/27/mini/tippy_11572.jpg?11451061277'
    response = generate_embed(post_choice, embed_titles, 0xEEEEEE, icon=icon)
    await message.channel.send(embed=response)
