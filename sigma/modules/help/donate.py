import discord


async def donate(cmd, message, args):
    if args:
        if args[0] == 'mini':
            mini = True
        else:
            mini = False
    else:
        mini = False
    sigma_image = 'https://i.imgur.com/mGyqMe1.png'
    sigma_title = 'Sigma Donation Information'
    patreon_url = 'https://www.patreon.com/ApexSigma'
    paypal_url = 'https://www.paypal.me/AleksaRadovic'
    support_url = 'https://discordapp.com/invite/aEUCHwX'
    if mini:
        response = discord.Embed(color=0x1B6F5F, title=sigma_title)
        donation_text = f'Care to help out? Come support Sigma on [Patreon]({patreon_url})!'
        response.description = donation_text
    else:
        donor_count = len(cmd.bot.info.get_donors().donors)
        response = discord.Embed(color=0x1B6F5F)
        donation_text = 'If you could spare some money, it would be amazing of you to support my work. '
        donation_text += 'At the moment support from Sigma\'s users is my only source of income. '
        donation_text += f'Come check out my [Patreon]({patreon_url}) and lend a hand! You also get some goodies! '
        donation_text += f'Or if a subscription is too much commitment for you, how about [PayPal]({paypal_url})? '
        donation_text += f'If you do end up being one of the lovely people to give support, '
        donation_text += f'drop by our [Server]({support_url}) so we can properly thank you.'
        donation_text += f'\n**Thank you to the {donor_count} donors who have provided support!**'
        response.set_author(name=sigma_title, icon_url=sigma_image, url=cmd.bot.cfg.pref.website)
        response.add_field(name='Care to help out?', value=donation_text)
    await message.channel.send(embed=response)
