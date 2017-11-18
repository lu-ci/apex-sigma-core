import asyncio

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.server_bound_logging import log_event


def generate_log_embed(message, target, channel, deleted):
    response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'#{channel.name} Has Been Pruned', icon_url=user_avatar(message.author))
    if target:
        target_text = f'{target.mention}\n{target.name}#{target.discriminator}'
    else:
        target_text = 'No Filter'
    response.add_field(name='🗑 Prune Details',
                       value=f'Amount: {len(deleted)} Messages\nTarget: {target_text}', inline=True)
    author = message.author
    response.add_field(name='🛡 Responsible',
                       value=f'{author.mention}\n{author.name}#{author.discriminator}',
                       inline=True)
    response.set_footer(text=f'ChannelID: {channel.id}')
    return response


# noinspection PyBroadException
async def purge(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        valid_count = True
        target = cmd.bot.user
        count = 100
        if message.mentions:
            target = message.mentions[0]
            if len(args) == 2:
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        else:
            if args:
                target = None
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        if count > 100:
            count = 100
        if not valid_count:
            response = discord.Embed(color=0xBE1931, title=f'❗ {args[0]} is not a valid number.')
        else:
            def purge_check(msg):
                if not msg.pinned:
                    if msg.author.id == target.id:
                        clean = True
                    else:
                        clean = False
                else:
                    clean = False
                return clean

            try:
                await message.delete()
            except discord.NotFound:
                pass
            if target:
                try:
                    deleted = await message.channel.purge(limit=count, check=purge_check)
                except Exception:
                    deleted = []
                    pass
            else:
                try:
                    deleted = await message.channel.purge(limit=count)
                except Exception:
                    deleted = []
                    pass
            response = discord.Embed(color=0x77B255, title=f'✅ Deleted {len(deleted)} Messages')
            log_embed = generate_log_embed(message, target, message.channel, deleted)
            await log_event(cmd.db, message.guild, log_embed)
    del_response = await message.channel.send(embed=response)
    await asyncio.sleep(5)
    try:
        await del_response.delete()
    except discord.NotFound:
        pass
