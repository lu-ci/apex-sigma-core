import json
import secrets

import discord


async def dadjoke(cmd: SigmaCommand, message: discord.Message, args: list):
    with open(cmd.resource('dadjokes.json'), 'r', encoding='utf-8') as dadjokes_file:
        jokes = dadjokes_file.read()
        jokes = json.loads(jokes)
    joke_list = jokes['JOKES']
    end_joke_choice = secrets.choice(joke_list)
    end_joke = end_joke_choice['setup']
    punchline = end_joke_choice['punchline']
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😖 Have An Awful Dad Joke', value=f'{end_joke}\n...\n{punchline}')
    await message.channel.send(None, embed=embed)
