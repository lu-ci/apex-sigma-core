import discord

from sigma.core.utilities.data_processing import user_avatar


async def wallet(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    currency = await cmd.db.get_currency(target, message.guild)
    currency_name = cmd.bot.cfg.pref.currency
    currency_icon = cmd.bot.cfg.pref.currency_icon
    response = discord.Embed(color=0xaa8dd8)
    response.set_author(name=f'{target.display_name}\'s Currency Data', icon_url=avatar)
    current_title = f'{currency_icon} Current Amount'
    guild_title = '🎪 Earned Here'
    global_title = '🌍 Earned Globally'
    response.add_field(name=current_title, value=f"```py\n{currency['current']} {currency_name}\n```", inline=True)
    response.add_field(name=guild_title, value=f"```py\n{currency['guild']} {currency_name}\n```", inline=True)
    response.add_field(name=global_title, value=f"```py\n{currency['global']} {currency_name}\n```", inline=True)
    response.set_footer(text=f'{currency_icon} {currency_name} is earned by participating in minigames.')
    await message.channel.send(embed=response)
