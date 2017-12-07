import discord


async def byemessage(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        if args:
            goodbye_text = ' '.join(args)
            await cmd.db.set_guild_settings(message.guild.id, 'ByeMessage', goodbye_text)
            response = discord.Embed(title='✅ New Goodbye Message Set', color=0x77B255)
        else:
            current_goodbye = await cmd.db.get_guild_settings(message.guild.id, 'ByeMessage')
            if current_goodbye is None:
                current_goodbye = '{user_name} has left {server_name}.'
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name='ℹ Current Goodbye Message', value=f'```\n{current_goodbye}\n```')
    await message.channel.send(embed=response)
