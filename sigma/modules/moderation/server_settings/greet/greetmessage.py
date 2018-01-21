import discord

from sigma.core.mechanics.command import SigmaCommand


async def greetmessage(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        if args:
            greeting_text = ' '.join(args)
            await cmd.db.set_guild_settings(message.guild.id, 'GreetMessage', greeting_text)
            response = discord.Embed(title='✅ New Greeting Message Set', color=0x77B255)
        else:
            current_greeting = await cmd.db.get_guild_settings(message.guild.id, 'GreetMessage')
            if current_greeting is None:
                current_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name='ℹ Current Greet Message', value=f'```\n{current_greeting}\n```')
    await message.channel.send(embed=response)
