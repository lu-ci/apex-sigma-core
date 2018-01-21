import discord

from sigma.core.mechanics.command import SigmaCommand


async def asciitempname(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            new_name = ' '.join(args)
            temp_name = await cmd.db.get_guild_settings(message.guild.id, 'ASCIIOnlyTempName')
            if temp_name is None:
                temp_name = '<ChangeMyName>'
            await cmd.db.set_guild_settings(message.guild.id, 'ASCIIOnlyTempName', new_name)
            title = f'✅ ASCII temp name changed from `{temp_name}` to `{new_name}`.'
            response = discord.Embed(color=0x66CC66, title=title)
        else:
            response = discord.Embed(title='⛔ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
