import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, args):
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name='A Member Has Been Unmuted', icon_url=user_avatar(target))
    log_embed.add_field(name='🔊 Unmuted User',
                        value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
    author = message.author
    log_embed.add_field(name='🛡 Responsible',
                        value=f'{author.mention}\n{author.name}#{author.discriminator}', inline=True)
    if len(args) > 1:
        log_embed.add_field(name='📄 Reason', value=f"```\n{' '.join(args[1:])}\n```", inline=False)
    log_embed.set_footer(text=f'UserID: {target.id}')
    return log_embed


async def textunmute(cmd, message, args):
    if not message.a(cmd: SigmaCommand, message: discord.Message, args: list)(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if not message.mentions:
            response = discord.Embed(title='❗ No user targeted.', color=0xBE1931)
        else:
            author = message.author
            target = message.mentions[0]
            is_admin = author.permissions_in(message.channel).administrator
            if author.id == target.id and not is_admin:
                response = discord.Embed(title='❗ Can\'t unmute yourself.', color=0xBE1931)
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier and not is_admin:
                    response = discord.Embed(title='⛔ Can\'t unmute someone equal or above you.', color=0xBE1931)
                else:
                    mute_list = await cmd.db.get_guild_settings(message.guild.id, 'MutedUsers')
                    if mute_list is None:
                        mute_list = []
                    if target.id not in mute_list:
                        resp_title = f'❗ {target.display_name} is not text muted.'
                        response = discord.Embed(title=resp_title, color=0xBE1931)
                    else:
                        mute_list.remove(target.id)
                        await cmd.db.set_guild_settings(message.guild.id, 'MutedUsers', mute_list)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target.display_name} has been unmuted.')
                        log_embed = generate_log_embed(message, target, args)
    await message.channel.send(embed=response)
