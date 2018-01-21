from sigma.core.mechanics.command import SigmaCommand
import discord


async def asciionlynames(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        active = await cmd.db.get_guild_settings(message.guild.id, 'ASCIIOnlyNames')
        if active is None:
            active = False
        if active:
            await cmd.db.set_guild_settings(message.guild.id, 'ASCIIOnlyNames', False)
            state = 'disabled'
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'ASCIIOnlyNames', True)
            state = 'enabled'
        response = discord.Embed(color=0x66CC66, title=f'✅ ASCII name enforcement has been {state}.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
