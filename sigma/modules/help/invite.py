import discord


async def invite(cmd, message, args):
    inv_title = 'Click here to invite me.'
    sigma_image = 'https://i.imgur.com/mGyqMe1.png'
    invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
    response = discord.Embed(color=0x1B6F5F).set_author(name=inv_title, icon_url=sigma_image, url=invite_url)
    await message.channel.send(embed=response)
