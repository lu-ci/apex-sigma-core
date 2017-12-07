import discord


async def givecurrency(cmd, message, args):
    if args:
        if len(args) >= 2:
            if message.mentions:
                target = message.mentions[0]
                try:
                    amount = abs(int(args[0]))
                except ValueError:
                    amount = None
                if amount:
                    current_kud = await cmd.db.get_currency(message.author, message.guild)['current']
                    if current_kud >= amount:
                        await cmd.db.rmv_currency(message.author, amount)
                        await cmd.db.add_currency(target, message.guild, amount, additive=False)
                        title = f'✅ Transfered {amount} to {target.display_name}.'
                        response = discord.Embed(color=0x77B255, title=title)
                    else:
                        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have that much.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    await message.channel.send(embed=response)
