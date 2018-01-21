from sigma.core.mechanics.command import SigmaCommand
import asyncio

import discord


async def purge(cmd: SigmaCommand, message: discord.Message, args: list):
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
            def purge_target_check(msg):
                if not msg.pinned:
                    if msg.author.id == target.id:
                        clean = True
                    else:
                        clean = False
                else:
                    clean = False
                return clean

            def purge_wide_check(msg):
                if not msg.pinned:
                    clean = True
                else:
                    clean = False
                return clean

            try:
                await message.delete()
            except discord.NotFound:
                pass
            if target:
                try:
                    deleted = await message.channel.purge(limit=count, check=purge_target_check)
                except Exception:
                    deleted = []
                    pass
            else:
                try:
                    deleted = await message.channel.purge(limit=count, check=purge_wide_check)
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
