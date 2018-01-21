import discord

from sigma.core.mechanics.command import SigmaCommand


async def loggingchannel(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        if message.channel_mentions:
            target_chn = message.channel_mentions[0]
        else:
            if args:
                if args[0].lower() == 'disable':
                    await cmd.db.set_guild_settings(message.guild.id, 'LoggingChannel', None)
                    response = discord.Embed(color=0x77B255, title=f'✅ Logging channel disabled.')
                    await message.channel.send(embed=response)
                    return
                else:
                    target_chn = message.channel
            else:
                target_chn = None
        if target_chn:
            me = message.guild.me
            if me.permissions_in(target_chn).send_messages:
                await cmd.db.set_guild_settings(message.guild.id, 'LoggingChannel', target_chn.id)
                response = discord.Embed(color=0x77B255, title=f'✅ #{target_chn.name} set as the logging channel.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t write to that channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No channel tagged.')
    await message.channel.send(embed=response)
