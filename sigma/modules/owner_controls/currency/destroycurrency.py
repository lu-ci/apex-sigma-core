from sigma.core.mechanics.command import SigmaCommand
import discord


async def destroycurrency(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        if len(args) >= 2:
            target = message.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(args[0]))
                    target_amount = await cmd.db.get_currency(target, message.guild)
                    target_amount = target_amount['current']
                    if amount <= target_amount:
                        await cmd.db.rmv_currency(target, amount)
                        title_text = f'🔥 Ok, {amount} of {target.display_name}\'s {cmd.bot.cfg.pref.currency} '
                        title_text += 'has been destroyed.'
                        response = discord.Embed(color=0xFFCC4D, title=title_text)
                    else:
                        err_title = f'❗ {target.display_name} does\'t have that much {cmd.bot.cfg.pref.currency}.'
                        response = discord.Embed(color=0xBE1931, title=err_title)
                except ValueError:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid amount.')
            else:
                err_title = f'❗ You can\'t take {cmd.bot.cfg.pref.currency} from bots.'
                response = discord.Embed(color=0xBE1931, title=err_title)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user was mentioned.')
    await message.channel.send(embed=response)
