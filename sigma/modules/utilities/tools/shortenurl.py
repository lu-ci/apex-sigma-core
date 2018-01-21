import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def shortenurl(cmd: SigmaCommand, message: discord.Message, args: list):
    text_cont = None
    if 'access_token' in cmd.cfg:
        access_token = cmd.cfg['access_token']
        if args:
            if args[-1].lower() == 'text':
                text_mode = True
                long_url = '%20'.join(args[:-1])
            else:
                text_mode = False
                long_url = '%20'.join(args)
            api_url = 'https://api-ssl.bitly.com/v3/shorten'
            api_url += f'?longUrl={long_url}&domain=bit.ly&format=json'
            api_url += f'&access_token={access_token}'
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as data:
                    data = await data.read()
                    data = json.loads(data)
            status_code = data['status_code']
            if status_code == 200:
                short_url = data['data']['url']
                if text_mode:
                    response = None
                    text_cont = f'Your URL: <{short_url}>'
                else:
                    response = discord.Embed(color=0x66CC66)
                    response.add_field(name='✅ URL Shortened', value=short_url)
            elif status_code == 500:
                response = discord.Embed(color=0xBE1931, title='❗ Bad URL.')
            else:
                response = discord.Embed(color=0xBE1931,
                                         title=f'❗ Error {status_code} - {data["status_txt"]} occurred.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Bit.ly Access Token.')
    await message.channel.send(text_cont, embed=response)
