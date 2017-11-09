import asyncio

import discord

from .nodes.race_storage import *


async def race(cmd, message, args):
    if message.channel.id not in races:
        if args:
            try:
                buyin = abs(int(args[0]))
            except ValueError:
                buyin = 0
        else:
            buyin = 0
        currency = f'{cmd.bot.cfg.pref.currency}'
        make_race(message.channel.id, buyin)
        start_title = '🚀 A race is starting in 30 seconds.'
        if buyin > 0:
            start_title = f'🚀 A {buyin} {currency} race is starting in 30 seconds.'
        create_response = discord.Embed(color=0x3B88C3, title=start_title)
        create_response.set_footer(text=f'We need 2 participants! Type {cmd.bot.get_prefix(message)}joinrace to join!')
        await message.channel.send(embed=create_response)
        await asyncio.sleep(30)
        race_instance = races[message.channel.id]
        del races[message.channel.id]
        if len(race_instance['users']) >= 2:
            values = {}
            highest = 0
            leader = None
            race_msg = None
            skip = False
            for participant in race_instance['users']:
                values.update({participant['user'].id: 0})
            while highest < 20:
                lines = '```\n'
                for participant in race_instance['users']:
                    if not skip:
                        move = secrets.randbelow(5)
                    else:
                        move = 0
                    val = values[participant['user'].id]
                    val += move
                    if val >= 20:
                        val = 20
                        win = True
                        skip = True
                    else:
                        win = False
                    values.update({participant['user'].id: val})
                    lines += f'\n⏩ {" " * val}{participant["icon"]}{" " * (20 - val)} ⏸'
                    if win:
                        lines += f' 🏆: {participant["user"].display_name}'
                    else:
                        part_name = participant["user"].display_name
                        if len(part_name) > 10:
                            part_name = part_name[:7] + '...'
                        lines += f' {int((val / 20) * 100)}%: {part_name}'
                    if highest < val:
                        highest = val
                        leader = participant
                lines += '\n```'
                if race_msg:
                    await race_msg.edit(content=lines)
                else:
                    race_msg = await message.channel.send(lines)
                await asyncio.sleep(2)
            win_title = f'{leader["icon"]} {leader["user"].display_name} has won!'
            for user in race_instance['users']:
                cmd.db.rmv_currency(user['user'], buyin)
            if race_instance['buyin']:
                winnings = race_instance["buyin"] * len(race_instance['users'])
                cmd.db.add_currency(leader['user'], message.guild, int(winnings * 0.9), additive=False)
                win_title += f' And got {int(winnings * 0.9)} {currency}.'
            win_response = discord.Embed(color=colors[leader['icon']], title=win_title)
            await message.channel.send(embed=win_response)
        else:
            not_enough_response = discord.Embed(color=0xBE1931, title='❗ Not enough participants in the race!')
            await message.channel.send(embed=not_enough_response)
    else:
        exist_response = discord.Embed(color=0xBE1931, title='❗ A race already exists here!')
        await message.channel.send(embed=exist_response)
