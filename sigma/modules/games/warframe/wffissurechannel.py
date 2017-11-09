import discord


async def wffissurechannel(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_channels:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
        else:
            if args:
                if args[0].lower() == 'disable':
                    cmd.db.set_guild_settings(message.guild.id, 'WarframeFissureChannel', None)
                    response = discord.Embed(title=f'✅ Warframe Void Fissure Channel Disabled', color=0x66CC66)
                    await message.channel.send(embed=response)
                    return
                else:
                    return
            else:
                target_channel = message.channel
        cmd.db.set_guild_settings(message.guild.id, 'WarframeFissureChannel', target_channel.id)
        response = discord.Embed(title=f'✅ Warframe Void Fissure Channel set to #{target_channel.name}', color=0x66CC66)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Channels needed.', color=0xBE1931)
    await message.channel.send(embed=response)
