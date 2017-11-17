import functools
from concurrent.futures import ThreadPoolExecutor

import discord
import wikipedia as wp


async def wikipedia(cmd, message, args):
    if args:
        q = ' '.join(args).lower()
        try:
            summary_task = functools.partial(wp.summary, q)
            with ThreadPoolExecutor() as threads:
                result = await cmd.bot.loop.run_in_executor(threads, summary_task)
            title = f'Wikipedia: {q.upper()}'
            title_url = f'https://en.wikipedia.org/wiki/{q}'
            wiki_icon = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'
            if len(result) >= 800:
                result = result[:800] + '...'
            response = discord.Embed(color=0xF9F9F9)
            response.set_author(name=title, url=title_url, icon_url=wiki_icon)
            response.description = result
        except wp.PageError:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
        except wp.DisambiguationError:
            response = discord.Embed(color=0xBE1931, title='❗ Search too broad, please be more specific.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
