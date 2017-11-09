import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.permission_processing import hierarchy_permit
from sigma.core.utilities.server_bound_logging import log_event


def generate_log_embed(message, target, args):
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name='A Member Has Been Muted', icon_url=user_avatar(target))
    log_embed.add_field(name='🔇 Muted User',
                        value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    log_embed.add_field(name='🛡 Responsible',
                        value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    if len(args) > 1:
        log_embed.add_field(name='📄 Reason', value=f"```\n{' '.join(args[1:])}\n```", inline=False)
    log_embed.set_footer(text=f'UserID: {target.id}')
    return log_embed


async def textmute(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if not message.mentions:
            response = discord.Embed(title='❗ No user targeted.', color=0xBE1931)
        else:
            author = message.author
            target = message.mentions[0]
            if author.id == target.id:
                response = discord.Embed(title='❗ Can\'t mute yourself.', color=0xBE1931)
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier:
                    response = discord.Embed(title='⛔ Can\'t mute someone equal or above you.', color=0xBE1931)
                else:
                    mute_list = cmd.db.get_guild_settings(message.guild.id, 'MutedUsers')
                    if mute_list is None:
                        mute_list = []
                    if target.id in mute_list:
                        resp_title = f'❗ {target.display_name} is already text muted.'
                        response = discord.Embed(title=resp_title, color=0xBE1931)
                    else:
                        mute_list.append(target.id)
                        cmd.db.set_guild_settings(message.guild.id, 'MutedUsers', mute_list)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target.display_name} has been text muted.')
                        log_embed = generate_log_embed(message, target, args)
                        await log_event(cmd.db, message.guild, log_embed)
                        if len(args) > 1:
                            reason = ' '.join(args[1:])
                        else:
                            reason = 'Not stated.'
                        to_target_title = f'🔇 You have been text muted.'
                        to_target = discord.Embed(color=0x696969)
                        to_target.add_field(name=to_target_title, value=f'Reason: {reason}')
                        to_target.set_footer(text=f'On: {message.guild.name}', icon_url=message.guild.icon_url)
                        try:
                            await target.send(embed=to_target)
                        except discord.Forbidden:
                            pass
    await message.channel.send(embed=response)
