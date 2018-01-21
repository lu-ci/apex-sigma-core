import aiohttp
import discord
from lxml import html
from sigma.core.mechanics.command import SigmaCommand


async def leetspeak(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        levels = ['basic', 'advanced', 'ultimate']
        if args[-1].startswith('level:'):
            level = args[-1].split(':')[1].lower()
            text = ' '.join(args[:-1])
            if level not in levels:
                level = None
        else:
            text = ' '.join(args)
            level = 'basic'
        if level:
            leet_url = 'http://www.robertecker.com/hp/research/leet-converter.php?lang=en'
            data = {
                'textbox_input': text,
                'language': 'en',
                'encode': 'encode',
                'modus': level
            }
            async with aiohttp.ClientSession() as session:
                api_data = await session.post(leet_url, data=data)
                page = await api_data.text()
                page = html.fromstring(page)
                table = page.cssselect('.mytable')
                text = table[0][0][1][2].text_content()
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name=f'🔣 {level.title()} L33t Converter', value=text)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid l33t level.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
