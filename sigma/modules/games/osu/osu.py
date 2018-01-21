import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand

osu_logo = 'http://w.ppy.sh/c/c9/Logo.png'


async def osu(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        osu_input = '%20'.join(args)
        try:
            profile_url = 'https://osu.ppy.sh/u/' + osu_input
            async with aiohttp.ClientSession() as session:
                async with session.get(profile_url) as data:
                    page = await data.text()
            root = html.fromstring(page)
            username = root.cssselect('.profile-username')[0].text[:-1]
            user_color = str(message.author.color)[1:]
            sig_url = f'https://lemmmy.pw/osusig/sig.php?colour=hex{user_color}&uname={osu_input}'
            response = discord.Embed(color=message.author.color)
            response.set_image(url=sig_url)
            response.set_author(name=f'{username}\'s osu! Profile', url=profile_url, icon_url=osu_logo)
        except IndexError:
            response = discord.Embed(color=0xBE1931, title='❗ Unable to retrieve profile.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
