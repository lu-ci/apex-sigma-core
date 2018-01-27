import asyncio
import secrets

import discord

ongoing = []
symbols = ['❤', '♦', '♠', '♣', '⭐', '⚡']


def check_answer(arguments, sequence):
    arguments = [char for char in arguments if char in symbols]
    results = []
    correct = True
    for loop_index, arg in enumerate(arguments):
        if arg == sequence[loop_index]:
            sign = '🔷'
        elif arg in sequence:
            sign = '🔶'
            correct = False
        else:
            sign = '🔻'
            correct = False
        results.append(sign)
    return correct, results


async def sequencegame(cmd, message, args):
    if message.author.id not in ongoing:
        chosen = []
        while len(chosen) < 4:
            symbol = secrets.choice(symbols)
            chosen.append(symbol)
        title = f'🎯 {message.author.display_name}, you have 90 seconds for each attempt.'
        desc = f'Symbols you can use: {"".join(symbols)}'
        start_embed = discord.Embed(color=0xf9f9f9)
        start_embed.add_field(name=title, value=desc)
        await message.channel.send(embed=start_embed)

        def answer_check(msg):
            if message.author.id == msg.author.id:
                if message.channel.id == msg.channel.id:
                    message_args = [char for char in msg.content if char in symbols]
                    if len(message_args) == 4:
                        good = False
                        for arg in message_args:
                            if arg in symbols:
                                good = True
                                break
                    else:
                        good = False
                else:
                    good = False
            else:
                good = False
            return good

        finished = False
        victory = False
        timeout = False
        tries = 0
        while not finished and tries < 6:
            try:
                answer = await cmd.bot.wait_for('message', check=answer_check, timeout=90)
                correct, results = check_answer(answer.content, chosen)
                tries += 1
                if correct:
                    finished = True
                    victory = True
                    await cmd.db.add_currency(answer.author, message.guild, 50)
                    win_title = f'🎉 Correct, {answer.author.display_name}. You won 50 Kud!'
                    win_embed = discord.Embed(color=0x77B255, title=win_title)
                    await message.channel.send(embed=win_embed)
                else:
                    attempt_title = f'💣 {answer.author.display_name} {tries}/6: {"".join(results)}'
                    attempt_embed = discord.Embed(color=0x262626, title=attempt_title)
                    await message.channel.send(embed=attempt_embed)
            except asyncio.TimeoutError:
                finished = True
                victory = False
                timeout = True
                timeout_title = f'🕙 Time\'s up {message.author.display_name}! It was {"".join(chosen)}'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await message.channel.send(embed=timeout_embed)
        if not victory and not timeout:
            lose_title = f'💥 Ooh, sorry {message.author.display_name}, it was {"".join(chosen)}'
            final_embed = discord.Embed(color=0xff3300, title=lose_title)
            await message.channel.send(embed=final_embed)
    else:
        ongoing_error = discord.Embed(color=0xBE1931,
                                      title=f'❗ {message.author.display_name}, there is one already ongoing.')
        await message.channel.send(embed=ongoing_error)
