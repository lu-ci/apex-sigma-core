import discord


async def byechannel(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
        elif not message.channel_mentions and args:
            channel_name = ' '.join(args).lower()
            target_channel = discord.utils.find(lambda x: x.name.lower() == channel_name, message.guild.channels)
        else:
            target_channel = None
        if target_channel:
            if message.guild.me.permissions_in(target_channel).send_messages:
                await cmd.db.set_guild_settings(message.guild.id, 'ByeChannel', target_channel.id)
                response = discord.Embed(color=0x77B255, title=f'✅ Goodbye Channel Changed To {target_channel.name}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t write in that channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No channel inputted.')
    await message.channel.send(None, embed=response)
