import discord

from sigma.core.utilities.data_processing import user_avatar


async def announce(cmd, message, args):
    content = ' '.join(args)
    announcement = discord.Embed(color=0x3B88C3)
    author_name = f'{message.author.name}#{message.author.discriminator}'
    announcement.set_author(name=author_name, icon_url=user_avatar(message.author))
    announcement.add_field(name=f'🌐 A Global {cmd.bot.user.name} Announcement', value=content)
    announcement.set_footer(text=f'Announced from {message.guild.name}', icon_url=message.guild.icon_url)
    sent_counter = 0
    for guild in cmd.bot.guilds:
        try:
            await guild.owner.send(embed=announcement)
            sent_counter += 1
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
    response = discord.Embed(color=0x77B255, title=f'✅ Announcement sent to {sent_counter} guilds.')
    await message.channel.send(embed=response)
