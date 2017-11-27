import json

import aiohttp
import discord


async def famousquote(cmd, message, args):
    resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    data = None
    tries = 0
    while not data and tries < 5:
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as page_data:
                try:
                    byte_data = await page_data.read()
                    data = json.loads(byte_data)
                except json.JSONDecodeError:
                    tries += 1
    if data:
        text = data['quoteText']
        while text.endswith(' '):
            text = text[:-1]
        if 'quoteAuthor' in data:
            author = data['quoteAuthor']
        else:
            author = 'Unknown'
        if not author:
            author = 'Unknown'
        quote_text = f'\"{text}\"'
    else:
        author = 'Sir Winston Churchill'
        quote_text = '"Some people\'s " idea of free speech is that they are free to say'
        quote_text += f' what the like, but if anyone says anything back, that is an outrage."'
    response = discord.Embed(color=0xF9F9F9)
    response.add_field(name=f'📑 A Quote From {author}', value=quote_text)
    await message.channel.send(None, embed=response)
