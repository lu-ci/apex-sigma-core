import discord

from sigma.core.mechanics.command import SigmaCommand


async def blockedwords(cmd: SigmaCommand, message: discord.Message, args: list):
    blocked_words = await cmd.db.get_guild_settings(message.guild.id, 'BlockedWords')
    if not blocked_words:
        response = discord.Embed(color=0x3B88C3, title='ℹ There are no blocked words.')
    else:
        response = discord.Embed(color=0x3B88C3)
        response.add_field(name=f'ℹ There are {len(blocked_words)} blocked words.', value=', '.join(blocked_words))
    await message.channel.send(embed=response)
