import aiohttp
import discord
import ftfy

from sigma.core.mechanics.command import SigmaCommand

async def pun(cmd: SigmaCommand, message: discord.Message, args: list):
    pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
    async with aiohttp.ClientSession() as session:
        async with session.get(pun_url) as data:
            pun_req = await data.text()
    pun_text = pun_req.split('&quot;')[1]
    pun_text = ftfy.fix_text(pun_text)
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😒 Have A Pun', value=pun_text)
    await message.channel.send(None, embed=embed)
