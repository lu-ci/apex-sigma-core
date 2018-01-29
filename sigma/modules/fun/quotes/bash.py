import aiohttp
from discord import Embed
from lxml import html

cache = []


async def bash(cmd, message, args):
    if len(cache) == 0:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://bash.org/?random1') as page:
                page = await page.text()
                quotes = html.fromstring(page).cssselect('body center table tr td[valign="top"]')[0]
        for index in range(1, len(quotes), 2):
            qid = quotes[index - 1][0][0].text
            score = quotes[index - 1][2].text
            quote = quotes[index].text_content()
            quote = {
                'id': qid[1:],
                'score': score,
                'quote': quote
            }
            cache.append(quote)
    quote = cache.pop()
    # skip quotes that are not fitting into message character limit
    while len(quote['quote']) > 2037:
        quote = cache.pop()
    text = quote['quote']
    highlight = 'xml' if text.strip()[0] == '<' else 'yaml'
    embed = Embed(type='rich', color=0xf7d7c4, description=f'```{highlight}\n{text}\n```')
    embed.set_author(name=f"📜 #{quote['id']} | Score: {quote['score']}", url=f"http://bash.org/?{quote['id']}")
    await message.channel.send(None, embed=embed)
