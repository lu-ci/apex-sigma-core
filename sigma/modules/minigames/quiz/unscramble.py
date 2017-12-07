import asyncio
import secrets

import aiohttp
import discord

from .mech.utils import scramble

ongoing_list = []


async def unscramble(cmd, message, args):
    if message.channel.id not in ongoing_list:
        ongoing_list.append(message.channel.id)
        source_urls = [
            'http://www.wordgenerator.net/application/p.php?type=1&id=dictionary_words&spaceflag=false',
            'http://www.wordgenerator.net/application/p.php?type=1&id=charades_easy&spaceflag=false',
            'http://www.wordgenerator.net/application/p.php?type=1&id=charades_moderate&spaceflag=false',
            'http://www.wordgenerator.net/application/p.php?type=1&id=charades_hard&spaceflag=false',
            'http://www.wordgenerator.net/application/p.php?type=1&id=charades_very_hard&spaceflag=false',
            'http://www.wordgenerator.net/application/p.php?type=1&id=animal_names&spaceflag=false'
        ]
        source_url = secrets.choice(source_urls)
        async with aiohttp.ClientSession() as session:
            async with session.get(source_url) as source_session:
                source_text = await source_session.text()
        words = source_text.split(',')
        clean_words = []
        for word in words:
            if word:
                if len(word) > 3:
                    clean_words.append(word)
        word_choice = secrets.choice(clean_words)
        kud_reward = len(word_choice)
        scrambled = scramble(word_choice)
        question_embed = discord.Embed(color=0x3B88C3, title=f'🔣 {scrambled}')
        await message.channel.send(embed=question_embed)

        def check_answer(msg):
            if message.channel.id == msg.channel.id:
                if msg.content.lower() == word_choice.lower():
                    correct = True
                else:
                    correct = False
            else:
                correct = False
            return correct

        try:
            answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
            await cmd.db.add_currency(answer_message.author, message.guild, kud_reward)
            author = answer_message.author.display_name
            currency = cmd.bot.cfg.pref.currency
            win_title = f'🎉 Correct, {author}, it was {word_choice}. You won {kud_reward} {currency}!'
            win_embed = discord.Embed(color=0x77B255, title=win_title)
            await message.channel.send(embed=win_embed)
        except asyncio.TimeoutError:
            timeout_title = f'🕙 Time\'s up! It was {word_choice}...'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            await message.channel.send(embed=timeout_embed)
        if message.channel.id in ongoing_list:
            ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)
