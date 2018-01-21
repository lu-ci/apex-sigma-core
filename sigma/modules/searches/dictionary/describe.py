from sigma.core.mechanics.command import SigmaCommand
import json

import aiohttp
import discord


async def describe(cmd: SigmaCommand, message: discord.Message, args: list):
    response = discord.Embed()
    if args:
        mode = args[0]
        if mode in ['adjectives', 'adjective', 'adj', 'a', 'nouns', 'noun', 'n']:
            query = ' '.join(args[1:])
            if mode[0] == 'a':
                header = f'Adjectives used to describe {query}'
                site_url = f'http://www.rhymezone.com/r/rhyme.cgi?Word={query}&typeofrhyme=jja'
                api_url = f'https://api.datamuse.com/words?rel_jja={query}&max=11'
            elif mode[0] == 'n':
                header = f'Nouns described by the adjective {query}'
                site_url = f'http://www.rhymezone.com/r/rhyme.cgi?Word={query}&typeofrhyme=jjb'
                api_url = f'https://api.datamuse.com/words?rel_jjb={query}&max=11'
            else:
                header = None
                site_url = None
                api_url = None
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
                response.set_author(name=header, url=site_url, icon_url='https://i.imgur.com/GKM6AMT.png')
                response.colour = 0xFBB429
                response.description = '\n'.join(data[:10])
                if len(data) > 10:
                    response.set_footer(text='Follow the link in the title to see more')
            else:
                response.title = '🔍 No results.'
                response.colour = 0x696969
        else:
            response.title = '❗ Mode is not specified.'
            response.colour = 0xBE1931
    else:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931
    await message.channel.send(embed=response)
