import discord

from sigma.core.mechanics.command import SigmaCommand


async def generatecurrency(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        if len(args) >= 2:
            target = message.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(args[0]))
                    await cmd.db.add_currency(target, message.guild, amount, additive=False)
                    title_text = f'✅ Ok, I\'ve given {amount} {cmd.bot.cfg.pref.currency} to {target.display_name}.'
                    response = discord.Embed(color=0x77B255, title=title_text)
                except ValueError:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                err_title = f'❗ You can\'t give {cmd.bot.cfg.pref.currency} to bots.'
                response = discord.Embed(color=0xBE1931, title=err_title)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    await message.channel.send(embed=response)
