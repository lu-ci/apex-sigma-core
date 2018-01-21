from sigma.core.mechanics.command import SigmaCommand
import discord


async def shutdown(cmd: SigmaCommand, message: discord.Message, args: list):
    status = discord.Embed(title=f'☠ {cmd.bot.user.name} Shutting Down.', color=0x808080)
    await message.channel.send(None, embed=status)
    cmd.log.info(f'Terminated by {message.author.name}#{message.author.discriminator}')
    await cmd.bot.logout()
    await cmd.bot.close()
    exit()
