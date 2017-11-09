import arrow
import discord


async def warning(cmd, message, args):
    if args:
        if message.mentions:
            if len(args) == 2:
                target = message.mentions[0]
                lookup = args[1].lower()
                guild_warnings = cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
                if guild_warnings is None:
                    guild_warnings = {}
                uid = str(target.id)
                if uid not in guild_warnings:
                    response = discord.Embed(color=0x696969, title=f'🔍 {target.name} does not have any warnings.')
                else:
                    warning_list = guild_warnings[uid]
                    warn = None
                    for warn_item in warning_list:
                        if warn_item['id'] == lookup:
                            warn = warn_item
                            break
                    if warn:
                        title = f'{warn["id"]} Warning Information'
                        response = discord.Embed(color=0xFFCC4D, title=title,
                                                 timestamp=arrow.get(warn['timestamp']).datetime)
                        response.add_field(name='⚠ Warned User',
                                           value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
                        responsible = discord.utils.find(lambda x: x.id == warn['responsible']['id'],
                                                         cmd.bot.get_all_members())
                        if not responsible:
                            responsible = f'{warn["responsible"]["name"]}#{warn["responsible"]["discriminator"]}'
                        else:
                            responsible = f'{responsible.mention}\n{responsible.name}#{responsible.discriminator}'
                        response.add_field(name='🛡 Responsible',
                                           value=responsible, inline=True)
                        response.add_field(name='📄 Reason', value=f"```\n{warn['reason']}\n```", inline=False)
                        response.set_footer(text=f'UserID: {target.id}')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 Warning {lookup} not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user mentioned.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
