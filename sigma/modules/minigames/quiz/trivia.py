# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
import secrets

import aiohttp
import discord
import ftfy

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar

ongoing_list = []

awards = {
    'easy': 10,
    'medium': 20,
    'hard': 50
}

categories = {
    9: ['general'],
    10: ['books', 'book'],
    11: ['film', 'films', 'movie', 'movies'],
    12: ['music'],
    13: ['musical', 'musicals', 'theatre', 'theater'],
    14: ['tv', 'television'],
    15: ['games', 'gaming'],
    16: ['boardgames', 'board'],
    17: ['science', 'nature'],
    18: ['computers', 'it', 'technology', 'tech'],
    19: ['mathematics', 'math'],
    20: ['mythology', 'myth'],
    21: ['sports', 'sport'],
    22: ['geography', 'geo'],
    23: ['history'],
    24: ['politics'],
    25: ['art'],
    26: ['celebrities', 'celebrity', 'celebs', 'celeb'],
    27: ['animals'],
    28: ['vehicles'],
    29: ['comics'],
    30: ['gadgets'],
    31: ['japan', 'japanese', 'anime', 'manga', 'animu', 'mango'],
    32: ['cartoons', 'cartoon', 'animations', 'animation']
}

streaks = {}


def shuffle_questions(question_list):
    output = []
    while question_list:
        question_choice = question_list.pop(secrets.randbelow(len(question_list)))
        output.append(question_choice)
    return output


def get_correct_index(question_list, answer):
    index = 0
    for item in question_list:
        if item == answer:
            break
        else:
            index += 1
    return index


async def trivia(cmd: SigmaCommand, message: discord.Message, args: list):
    global streaks
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
        if message.author.id not in ongoing_list:
            ongoing_list.append(message.author.id)
            allotted_time = 20
            trivia_api_url = 'https://opentdb.com/api.php?amount=1'
            if args:
                catlook = args[0].lower()
                for cat in categories:
                    cat_alts = categories.get(cat)
                    if catlook in cat_alts:
                        trivia_api_url += f'&category={cat}'
                        break
            async with aiohttp.ClientSession() as session:
                async with session.get(trivia_api_url) as number_get:
                    number_response = await number_get.read()
                    try:
                        data = json.loads(number_response).get('results')[0]
                    except json.JSONDecodeError:
                        if message.author.id in ongoing_list:
                            ongoing_list.remove(message.author.id)
                        decode_error = discord.Embed(color=0xBE1931, title='❗ Couldn\'t retrieve a question.')
                        await message.channel.send(embed=decode_error)
                        return
            await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, 30)
            question = data['question']
            question = ftfy.fix_text(question)
            category = data['category']
            correct_answer = data['correct_answer']
            correct_answer = ftfy.fix_text(correct_answer)
            incorrect_answers = data['incorrect_answers']
            difficulty = data['difficulty']
            reward_mult = streaks.get(message.author.id) or 0
            kud_reward = int((awards.get(difficulty) or '10') * (1 + (reward_mult * 3.25)))
            choice_list = [correct_answer] + incorrect_answers
            choice_list = shuffle_questions(choice_list)
            choice_number = 0
            choice_lines = []
            for choice in choice_list:
                choice_number += 1
                choice_line = f'[{choice_number}] {choice}'
                choice_lines.append(choice_line)
            choice_text = '\n'.join(choice_lines)
            choice_text = ftfy.fix_text(choice_text)
            if difficulty == 'easy':
                starter = 'An'
            else:
                starter = 'A'
            question_embed = discord.Embed(color=0xF9F9F9, title='❔ Here\'s a question!')
            question_embed.description = f'{starter} {difficulty} one from the {category} category.'
            question_embed.add_field(name='Question', value=question, inline=False)
            question_embed.add_field(name='Choices', value=f'```py\n{choice_text}\n```', inline=False)
            question_embed.set_footer(text='Input the number of your chosen answer.')
            question_embed.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
            await message.channel.send(embed=question_embed)

            def check_answer(msg):
                if message.channel.id == msg.channel.id:
                    if message.author.id == msg.author.id:
                        try:
                            int(msg.content)
                            number = True
                        except ValueError:
                            number = False
                        if number or (msg.content.title() in choice_list):
                            correct = True
                        else:
                            correct = False
                    else:
                        correct = False
                else:
                    correct = False
                return correct

            try:
                answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=allotted_time)
                try:
                    answer_index = int(answer_message.content) - 1
                except ValueError:
                    answer_index = None
                correct_index = get_correct_index(choice_list, correct_answer)
                if answer_index == correct_index or answer_message.content.lower() == correct_answer.lower():
                    streaks.update({message.author.id: reward_mult + 1})
                    await cmd.db.add_currency(answer_message.author, message.guild, kud_reward)
                    author = answer_message.author.display_name
                    currency = cmd.bot.cfg.pref.currency
                    win_title = f'🎉 Correct, {author}, it was {correct_answer}. You won {kud_reward} {currency}!'
                    final_embed = discord.Embed(color=0x77B255, title=win_title)
                else:
                    if message.author.id in streaks:
                        streaks.pop(message.author.id)
                    lose_title = f'💣 Ooh, sorry, it was {correct_answer}...'
                    final_embed = discord.Embed(color=0x262626, title=lose_title)
                await message.channel.send(embed=final_embed)
            except asyncio.TimeoutError:
                if message.author.id in streaks:
                    streaks.pop(message.author.id)
                timeout_title = f'🕙 Time\'s up! It was {correct_answer}...'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await message.channel.send(embed=timeout_embed)
            if message.author.id in ongoing_list:
                ongoing_list.remove(message.author.id)
        else:
            ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
            await message.channel.send(embed=ongoing_error)
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
        on_cooldown = discord.Embed(color=0xccffff, title=f'❄ On cooldown for another {timeout} seconds.')
        await message.channel.send(embed=on_cooldown)
