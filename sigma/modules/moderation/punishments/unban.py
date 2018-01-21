import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


def generate_log_embed(message, target):
    log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name=f'A User Has Been Unbanned', icon_url=user_avatar(target))
    log_response.add_field(name='🔨 Unbanned User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    log_response.set_footer(text=f'UserID: {target.id}')
    return log_response


async def unban(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).ban_members:
        if args:
            lookup = ' '.join(args)
            target = None
            banlist = await message.guild.bans()
            for entry in banlist:
                if entry.user.name.lower() == lookup.lower():
                    target = entry.user
                    break
            if target:
                await message.guild.unban(target, reason=f'By {message.author.name}.')
                log_embed = generate_log_embed(message, target)
                await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'LogBans')
                response = discord.Embed(title=f'✅ {target.name} has been unbanned.', color=0x77B255)
            else:
                response = discord.Embed(title=f'🔍 {lookup} not found in the ban list.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Ban permissions needed.', color=0xBE1931)
    await message.channel.send(embed=response)
