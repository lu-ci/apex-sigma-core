import discord


async def unflip(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        flip_settings = await cmd.db.get_guild_settings(message.guild.id, 'Unflip')
        if flip_settings is None:
            unflip_set = False
        else:
            unflip_set = flip_settings
        if unflip_set:
            await cmd.db.set_guild_settings(message.guild.id, 'Unflip', False)
            response_title = f'✅ Table unflipping has been **disabled**.'
            response = discord.Embed(color=0x77B255, title=response_title)
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'Unflip', True)
            response_title = f'✅ Table unflipping has been **enabled**.'
            response = discord.Embed(color=0x77B255, title=response_title)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
