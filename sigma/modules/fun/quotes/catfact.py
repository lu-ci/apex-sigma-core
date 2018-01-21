import json
import secrets
from sigma.core.mechanics.command import SigmaCommand

import aiohttp
import discord

facts = []


async def catfact(cmd: SigmaCommand, message: discord.Message, args: list):
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
