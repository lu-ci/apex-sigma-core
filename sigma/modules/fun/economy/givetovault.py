import discord


async def givetovault(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        try:
            amount = int(abs(int(args[0])))
        except ValueError:
            amount = None
        if amount:
            currency = cmd.bot.cfg.pref.currency
            current_kud = await cmd.db.get_currency(message.author, message.guild)
            current_kud = current_kud['current']
            if current_kud >= amount:
                current_vault = await cmd.db.get_guild_settings(message.guild.id, 'CurrencyVault')
                if current_vault is None:
                    current_vault = 0
                await cmd.db.rmv_currency(message.author, amount)
                current_vault += amount
                await cmd.db.set_guild_settings(message.guild.id, 'CurrencyVault', current_vault)
                title_text = f'✅ You added {amount} {currency} to the Vault.'
                response = discord.Embed(color=0x77B255, title=title_text)
            else:
                response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input an amount.')
    await message.channel.send(embed=response)
