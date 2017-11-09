import secrets
import discord

responses = {
    211922001546182656: ['🍆']
}


async def nablie_plant(ev, message):
    if message.author.id in responses:
        roll = secrets.randbelow(5)
        if roll == 0:
            try:
                symbol = secrets.choice(responses.get(message.author.id))
                await message.add_reaction(symbol)
            except discord.Forbidden:
                pass
