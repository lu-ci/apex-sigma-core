import json

import aiohttp
import discord


async def homophones(cmd: SigmaCommand, message: discord.Message, args: list):
    # strip spaces from args
    args = list(filter(lambda a: a != '', args))
    response = discord.Embed()
    if args:
        query = ' '.join(args)
        site_url = f'http://www.rhymezone.com/r/rhyme.cgi?Word={query}&typeofrhyme=hom'
        api_url = f'https://api.datamuse.com/words?rel_hom={query}&max=11'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data_response:
                data = await data_response.read()
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    data = []

        data = list(filter(lambda r: 'score' in r, data))
        if data:
            data = list(map(lambda s: '- ' + s['word'], data))
            response.set_author(name=f'Homophones for {query}', url=site_url,
                                icon_url='https://i.imgur.com/GKM6AMT.png')
            response.colour = 0xFBB429
            response.description = '\n'.join(data[:10])
            if len(data) > 10:
                response.set_footer(text='Follow the link in the title to see more')
        else:
            response.title = '🔍 No results.'
            response.colour = 0x696969
    else:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931

    await message.channel.send(embed=response)
