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

import functools
from concurrent.futures import ThreadPoolExecutor

import discord
import wikipedia as wiki


async def wikipedia(cmd, message, args):
    if args:
        try:
            summary_task = functools.partial(wiki.page, ' '.join(args).lower())
            with ThreadPoolExecutor() as threads:
                page = await cmd.bot.loop.run_in_executor(threads, summary_task)

            response = discord.Embed(color=0xF9F9F9)
            response.set_author(
                name=f'Wikipedia: {page.title}',
                url=page.url,
                icon_url='https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'
            )
            response.description = f'{page.summary[:800]}...'
        except wiki.PageError:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
        except wiki.DisambiguationError:
            response = discord.Embed(color=0xBE1931, title='❗ Search too broad, please be more specific.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
