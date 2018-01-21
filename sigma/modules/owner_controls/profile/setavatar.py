import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def setavatar(cmd: SigmaCommand, message: discord.Message, args: list):
    if args or message.attachments:
        if message.attachments:
            image_url = message.attachments[0].url
        else:
            image_url = ' '.join(args)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as image_response:
                    img_data = await image_response.read()
            await cmd.bot.user.edit(avatar=img_data)
            response = discord.Embed(color=0x77B255, title=f'✅ My avatar has been changed.')
        except discord.Forbidden:
            response = discord.Embed(color=0xBE1931, title=f'❗ I was unable to change my avatar.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Give me a link or attach an image, please.')
    await message.channel.send(embed=response)
