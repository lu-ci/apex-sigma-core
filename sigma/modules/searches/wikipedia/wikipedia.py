import functools
from concurrent.futures import ThreadPoolExecutor

import discord
import wikipedia as wiki


async def wikipedia(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        try:
            summary_task = functools.partial(wiki.page, ' '.join(args).lower())
            with ThreadPoolExecutor() as threads:
                page = await cmd.bot.loop.run_in_executor(threads, summary_task)

            response = discord.Embed(color=0xF9F9F9)
            response.set_author(
                name=f'Wikipedia: {page.title}',
                url=page.url,
                icon_url='https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'
            )
            response.description = f'{page.summary[:800]}...'
        except wiki.PageError:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
        except wiki.DisambiguationError:
            response = discord.Embed(color=0xBE1931, title='❗ Search too broad, please be more specific.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
