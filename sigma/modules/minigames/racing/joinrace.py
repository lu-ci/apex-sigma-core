import discord

from .nodes.race_storage import *


async def joinrace(cmd: SigmaCommand, message: discord.Message, args: list):
    currency = f'{cmd.bot.cfg.pref.currency}'
    if message.channel.id in races:
        race = races[message.channel.id]
        buyin = race['buyin']
        kud = await cmd.db.get_currency(message.author, message.guild)
        kud = kud['current']
        if kud >= buyin:
            if len(race['users']) < 10:
                user_found = False
                for user in race['users']:
                    if user['user'].id == message.author.id:
                        user_found = True
                        break
                if not user_found:
                    icon = add_participant(message.channel.id, message.author)
                    if names[icon][0] in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'an'
                    else:
                        connector = 'a'
                    join_title = f'{icon} {message.author.display_name} joined as {connector} {names[icon]}!'
                    response = discord.Embed(color=colors[icon], title=join_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You are already in the race!')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Sorry, no more room left!')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ You don\'t have that much {currency}!')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ There is no race in preparation.')
    await message.channel.send(embed=response)
