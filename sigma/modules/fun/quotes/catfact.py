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
import secrets

import aiohttp
import discord

facts = []


async def catfact(cmd, message, args):
    global facts
    if not facts:
        resource = 'http://www.animalplanet.com/xhr.php'
        resource += '?action=get_facts&limit=500&page_id=37397'
        resource += '&module_id=cfct-module-bdff02c2a38ff3c34ce90ffffce76104&used_slots=W10='
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
                data = json.loads(data)
                facts = data
    fact = secrets.choice(facts)
    fact_text = fact['description'].strip()
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='🐱 Did you know...', value=fact_text)
    await message.channel.send(None, embed=embed)
