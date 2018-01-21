import discord


async def lmgtfy(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = '%20'.join(args)
        google_icon = 'https://maxcdn.icons8.com/Share/icon/Logos/google_logo1600.png'
        query_url = f'http://lmgtfy.com/?q={lookup}'
        response = discord.Embed(color=0xF9F9F9)
        response.set_author(name='Click here to go to the results.', icon_url=google_icon, url=query_url)
    else:
        response = discord.Embed(title='❗ No search inputted.', color=0xBE1931)
    await message.channel.send(embed=response)
