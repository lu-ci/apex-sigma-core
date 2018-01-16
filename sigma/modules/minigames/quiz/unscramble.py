import asyncio
import secrets

import yaml
import discord

from .mech.utils import scramble


def load_word_cache():
    global word_cache
    with open('sigma/modules/minigames/quiz/res/words.yml', encoding='utf-8') as word_file:
        word_cache = yaml.safe_load(word_file)


ongoing_list = []
word_cache = {}
load_word_cache()


async def unscramble(cmd, message, args):
    if message.channel.id not in ongoing_list:
        ongoing_list.append(message.channel.id)
        words = list(word_cache.keys())
        word_choice = secrets.choice(words)
        word_description = word_cache.get(word_choice)
        kud_reward = len(word_choice)
        scrambled = scramble(word_choice.title())
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
            timeout_title = f'🕙 Time\'s up!'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            timeout_embed.add_field(name=f'It was {word_choice.lower()}.', value=word_description)
            await message.channel.send(embed=timeout_embed)
        if message.channel.id in ongoing_list:
            ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)
