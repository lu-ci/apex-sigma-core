import arrow
import discord


async def warnings(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        target = message.author
    else:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
    guild_warnings = await cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
    if guild_warnings is None:
        guild_warnings = {}
    uid = str(target.id)
    if uid not in guild_warnings:
        response = discord.Embed(color=0x696969, title=f'🔍 {target.name} does not have any warnings.')
    else:
        if guild_warnings[uid]:
            warning_list = guild_warnings[uid]
            warning_output = ''
            for warning in warning_list:
                responsible = discord.utils.find(lambda x: x.id == warning['responsible']['id'],
                                                 cmd.bot.get_all_members())
                if not responsible:
                    responsible = f'{warning["responsible"]["name"]}#{warning["responsible"]["discriminator"]}'
                else:
                    responsible = f'{responsible.name}#{responsible.discriminator}'
                stampdate = arrow.get(warning['timestamp']).format('DD. MMM. YYYY')
                warning_output += f'\n`{warning["id"]}` by {responsible} on {stampdate}'
            if len(warning_output) > 800:
                warning_output = warning_output[:800] + '\n...'
            if len(warning_list) == 1:
                ender = 'time'
            else:
                ender = 'times'
            warning_title = f'⚠ {target.name} was warned {len(warning_list)} {ender}'
            pfx = await cmd.bot.get_prefix(message)
            response = discord.Embed(color=0xFFCC4D)
            response.add_field(name=warning_title, value=warning_output, inline=False)
            response.set_footer(text=f'Use {pfx}warning [target] [id] to see the details.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 {target.name} does not have any warnings.')
    await message.channel.send(embed=response)
