from sigma.core.mechanics.command import SigmaCommand
import discord

from .mech.danbooru_cache import get_dan_post


async def danbooru(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        tag = 'nude'
    else:
        tag = '+'.join(args).lower()
    image_url = await get_dan_post(tag)
    if not image_url:
        response = discord.Embed(color=0x696969, title=f'🔍 Search for {tag} yielded no results.')
        response.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
    else:
        response = discord.Embed(color=0x744EAA)
        response.set_image(url=image_url)
    await message.channel.send(None, embed=response)
