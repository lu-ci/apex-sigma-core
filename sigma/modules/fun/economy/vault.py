import discord
from sigma.core.mechanics.command import SigmaCommand


async def vault(cmd: SigmaCommand, message: discord.Message, args: list):
    currency = cmd.bot.cfg.pref.currency
    current_vault = await cmd.db.get_guild_settings(message.guild.id, 'CurrencyVault')
    if current_vault is None:
        current_vault = 0
    current_vault = int(current_vault)
    response = discord.Embed(color=0xa7d28b, title=f'💰 There is {current_vault} {currency} in the Vault.')
    await message.channel.send(embed=response)
