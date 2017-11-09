import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.server_bound_logging import log_event


def generate_log_embed(message, target, warning_text, warning_id):
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'A User Has Been Warned', icon_url=user_avatar(target))
    response.add_field(name='⚠ Warned User',
                       value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    response.add_field(name='🛡 Responsible',
                       value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    if warning_text:
        response.add_field(name='📄 Reason', value=f"```\n{warning_text}\n```", inline=False)
    response.set_footer(text=f'UserID: {target.id} | Warning: {warning_id}')
    return response


async def warn(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if message.mentions:
            target = message.mentions[0]
            if len(args) > 1:
                reason = ' '.join(args[1:])
            else:
                reason = 'Reason not provided.'
            guild_warnings = cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
            if guild_warnings is None:
                guild_warnings = {}
            uid = str(target.id)
            if uid in guild_warnings:
                warning_list = guild_warnings[uid]
            else:
                warning_list = []
            warning_id = secrets.token_hex(2)
            warning_data = {
                'responsible': {
                    'name': message.author.name,
                    'discriminator': message.author.discriminator,
                    'id': message.author.id
                },
                'reason': reason,
                'timestamp': arrow.utcnow().timestamp,
                'id': warning_id
            }
            warning_list.append(warning_data)
            guild_warnings.update({uid: warning_list})
            cmd.db.set_guild_settings(message.guild.id, 'WarnedUsers', guild_warnings)
            response = discord.Embed(color=0x77B255, title=f'✅ {target.name}#{target.discriminator} has been warned.')
            to_target = discord.Embed(color=0xFFCC4D)
            to_target.add_field(name='⚠ You received a warning.', value=f'Reason: {reason}')
            to_target.set_footer(text=f'From: {message.guild.name}', icon_url=message.guild.icon_url)
            try:
                await target.send(embed=to_target)
            except discord.Forbidden:
                pass
            log_embed = generate_log_embed(message, target, reason, warning_id)
            await log_event(cmd.db, message.guild, log_embed)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user tagged.')
    await message.channel.send(embed=response)
