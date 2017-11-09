import discord

from .nodes.read_frame_data import read_frame_data, read_item_data

icon_url = 'https://i.imgur.com/nuZsqIL.png'


async def wfloc(cmd, message, args):
    if args:
        try:
            qry = '/'.join(args).title().replace('And', '&')
            wiki_url = f'http://warframe.wikia.com/wiki/{qry}'
            embed = await read_frame_data(wiki_url)
            embed.set_author(name='Prime Locator', icon_url=icon_url, url=wiki_url)
            await message.channel.send(None, embed=embed)
        except IndexError:
            try:
                qry = '_'.join(args).title().replace('And', '&')
                wiki_url = f'http://warframe.wikia.com/wiki/{qry}'
                embed = await read_item_data(wiki_url)
                embed.set_author(name='Prime Locator', icon_url=icon_url, url=wiki_url)
                await message.channel.send(None, embed=embed)
            except IndexError:
                embed = discord.Embed(color=0x696969, title='🔍 Nothing Found')
                await message.channel.send(None, embed=embed)
