from sigma.core.mechanics.command import SigmaCommand
import discord


async def greetdm(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        out_content = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        active = await cmd.db.get_guild_settings(message.guild.id, 'GreetDM')
        if active:
            await cmd.db.set_guild_settings(message.guild.id, 'GreetDM', False)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been disabled.')
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'GreetDM', True)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been enabled.')
    await message.channel.send(None, embed=out_content)
