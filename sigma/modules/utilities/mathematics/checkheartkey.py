import discord


async def checkheartkey(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = ''.join(args)
        key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
        if key:
            if lookup == key:
                response = discord.Embed(color=0xe75a70, title='💟 That is the correct key.')
            elif lookup in key:
                response = discord.Embed(color=0xe75a70, title='💟 The key does contain this, but there is more.')
            else:
                response = discord.Embed(color=0xe75a70, title='💔 Sorry, I don\'t see that in the key!')
        else:
            response = discord.Embed(color=0xe75a70, title='💔 You have no key set.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing to check.')
    await message.channel.send(embed=response)
