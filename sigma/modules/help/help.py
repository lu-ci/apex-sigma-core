import discord


async def help(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        cmd_name = ''.join(args).lower()
        if cmd_name in cmd.bot.modules.alts:
            cmd_name = cmd.bot.modules.alts[cmd_name]
        if cmd_name in cmd.bot.modules.commands:
            pfx = await cmd.bot.get_prefix(message)
            command = cmd.bot.modules.commands[cmd_name]
            usage = command.usage.replace('{pfx}', pfx).replace('{cmd}', command.name)
            response = discord.Embed(color=0x1B6F5F, title=f'📄 {command.name.upper()} Usage and Information')
            response.add_field(name='Usage Example', value=f'`{usage}`', inline=False)
            response.add_field(name='Command Description', value=f'```\n{command.desc}\n```', inline=False)
            if command.alts:
                response.add_field(name='Command Aliases', value=f'```\n{", ".join(command.alts)}\n```')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No such command was found...')
    else:
        lucia_image = 'https://i.imgur.com/xpDpHqz.png'
        sigma_image = 'https://i.imgur.com/mGyqMe1.png'
        sigma_title = 'Apex Sigma: The Database Giant'
        patreon_url = 'https://www.patreon.com/ApexSigma'
        paypal_url = 'https://www.paypal.me/AleksaRadovic'
        support_url = 'https://discordapp.com/invite/aEUCHwX'
        response = discord.Embed(color=0x1B6F5F)
        response.set_author(name=sigma_title, icon_url=sigma_image, url=cmd.bot.cfg.pref.website)
        invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
        support_text = f'**Add Me**: [Link]({invite_url})'
        support_text += f' | **Commands**: [Link]({cmd.bot.cfg.pref.website}/commands)'
        support_text += f' | **Server**: [Link]({support_url})'
        support_text += f'\nWanna help? **Patreon**: [Link]({patreon_url}) | **PayPal**: [Link]({paypal_url})'
        response.add_field(name='Help', value=support_text)
        response.set_thumbnail(url=sigma_image)
        response.set_footer(text='© by Lucia\'s Cipher. Released under the GPLv3 license.', icon_url=lucia_image)
    await message.channel.send(embed=response)
