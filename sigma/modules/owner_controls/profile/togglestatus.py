import discord


async def togglestatus(cmd, message, args):
    if cmd.bot.cfg.pref.status_rotation:
        cmd.bot.cfg.pref.status_rotation = False
        response = discord.Embed(color=0x77B255, title=f'✅ Status rotation **disabled**.')
    else:
        cmd.bot.cfg.pref.status_rotation = True
        response = discord.Embed(color=0x77B255, title=f'✅ Status rotation **enabled**.')
    await message.channel.send(embed=response)
