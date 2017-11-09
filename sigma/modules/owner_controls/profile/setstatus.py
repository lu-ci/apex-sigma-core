import discord


async def setstatus(cmd, message, args):
    if cmd.bot.cfg.pref.status_rotation:
        response = discord.Embed(color=0xBE1931, title='❗ I can\'t, automatic rotation is enabled.')
    else:
        status = ' '.join(args)
        game = discord.Game(name=status)
        await cmd.bot.change_presence(game=game)
        response = discord.Embed(color=0x77B255, title=f'✅ New playing status set to {status}.')
    await message.channel.send(embed=response)
