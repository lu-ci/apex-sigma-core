import discord

from sigma.core.mechanics.command import SigmaCommand


async def cookies(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    cookie_coll = cmd.db[cmd.db.db_cfg.database].Cookies
    cookie_file = await cookie_coll.find_one({'UserID': target.id})
    if cookie_file:
        cookie_count = cookie_file['Cookies']
    else:
        cookie_count = 0
    if cookie_count == 1:
        ender = 'cookie'
    else:
        ender = 'cookies'
    title = f'🍪 {target.display_name} has {cookie_count} {ender}.'
    response = discord.Embed(color=0xd99e82, title=title)
    await message.channel.send(embed=response)
