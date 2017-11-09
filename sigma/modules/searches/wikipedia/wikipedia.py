import discord
import wikipedia as wp


async def wikipedia(cmd, message, args):
    if args:
        q = ' '.join(args).lower()
        try:
            result = wp.summary(q)
            if len(result) >= 650:
                result = result[:650] + '...'
            response = discord.Embed(color=0xF9F9F9)
            response.add_field(name=f'📄 Wikipedia: `{q.upper()}`', value=result)
        except wp.PageError:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
        except wp.DisambiguationError:
            response = discord.Embed(color=0xBE1931, title='❗ Search too broad, please be more specific.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
