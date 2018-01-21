import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def numberfact(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = ''.join(args)
        if ':' in lookup:
            num_type = lookup.split(':')[0].lower()
            num_argument = lookup.split(':')[1].lower()
        else:
            num_type = 'trivia'
            num_argument = lookup.lower()
        if '/' in num_argument:
            num_type = 'date'
            mon = num_argument.split('/')[1]
            day = num_argument.split('/')[0]
            num_argument = f'{mon}/{day}'
    else:
        num_type = 'trivia'
        num_argument = 'random'
    num_fact_url = f'http://numbersapi.com/{num_argument}/{num_type}'
    async with aiohttp.ClientSession() as session:
        async with session.get(num_fact_url) as number_get:
            number_response = await number_get.text()
    if not number_response.lower().startswith('cannot'):
        response = discord.Embed(color=0x3B88C3, title=f'#⃣  Number Fact')
        response.description = number_response
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API couldn\'t process that.')
    await message.channel.send(embed=response)
