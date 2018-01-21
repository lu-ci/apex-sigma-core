import secrets

import discord

from sigma.modules.nsfw.mech.visual_novels import key_vn_list


async def keyvis(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        keys = []
        for key in key_vn_list:
            keys.append(key)
        choice = secrets.choice(keys)
    else:
        choice = [x.lower() for x in args][0]
    try:
        item = key_vn_list[choice]
    except KeyError:
        embed = discord.Embed(color=0x696969, title='🔍 Nothing found for {:s}...'.format(
            ' '.join(['`{:s}`'.format(x) for x in args])))
        await message.channel.send(None, embed=embed)
        return
    image_number = secrets.randbelow(item[2]) + item[1]
    url_base = 'https://vncg.org'
    image_url = f'{url_base}/f{image_number}.jpg'
    embed = discord.Embed(color=0x744EAA)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
