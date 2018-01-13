import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.server_bound_logging import log_event


def generate_clean_log_embed(message, target):
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'A User\'s Warnings Have Been Removed', icon_url=user_avatar(target))
    response.add_field(name='⚠ Unwarned User',
                       value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    response.add_field(name='🛡 Responsible',
                       value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    response.set_footer(text=f'UserID: {target.id}')
    return response


def generate_specific_log_embed(message, target, warning):
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'Warning {warning["id"]} Have Been Removed', icon_url=user_avatar(target))
    response.add_field(name='⚠ Unwarned User',
                       value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    response.add_field(name='🛡 Responsible',
                       value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    response.set_footer(text=f'UserID: {target.id}')
    return response


async def unwarn(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if message.mentions:
            if len(args) == 2:
                target = message.mentions[0]
                is_admin = message.author.permissions_in(message.channel).administrator
                if message.author.id != target.id or is_admin:
                    warn_id = args[1].lower()
                    guild_warnings = await cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
                    if guild_warnings is None:
                        guild_warnings = {}
                    uid = str(target.id)
                    if uid in guild_warnings:
                        if warn_id == 'all':
                            del guild_warnings[uid]
                            await cmd.db.set_guild_settings(message.guild.id, 'WarnedUsers', guild_warnings)
                            response = discord.Embed(color=0x77B255,
                                                     title=f'✅ {target.name}\'s warnings have been cleared.')
                            log_embed = generate_clean_log_embed(message, target)
                            await log_event(cmd.db, message.guild, log_embed)
                        else:
                            warn_list = guild_warnings[uid]
                            warning = None
                            for warn_item in warn_list:
                                if warn_item['id'] == warn_id:
                                    warning = warn_item
                                    break
                            if warning:
                                warn_list.remove(warning)
                                await cmd.db.set_guild_settings(message.guild.id, 'WarnedUsers', guild_warnings)
                                response = discord.Embed(color=0x77B255,
                                                         title=f'✅ {target.name}\'s warning {warn_id} has been removed.')
                                log_embed = generate_specific_log_embed(message, target, warning)
                                await log_event(cmd.db, message.guild, log_embed)
                            else:
                                response = discord.Embed(color=0x696969, title=f'🔍 Warning {warn_id} not found.')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 {target.name} does not have any warnings.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You can\'t unmute yourself.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user tagged.')
    await message.channel.send(embed=response)
