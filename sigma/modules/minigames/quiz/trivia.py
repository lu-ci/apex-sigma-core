"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import json
import re
import secrets

import aiohttp
import discord
import ftfy

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

awards = {
    'easy': 10,
    'medium': 20,
    'hard': 50
}

categories = {
    9: ['general'],
    10: ['books', 'book'],
    11: ['films', 'film', 'movies', 'movie'],
    12: ['music'],
    13: ['musicals', 'musical', 'theatre', 'theater'],
    14: ['tv', 'television'],
    15: ['games', 'game', 'gaming'],
    16: ['boardgames', 'boardgame', 'boards', 'board'],
    17: ['science', 'nature'],
    18: ['computers', 'computer', 'it', 'technology', 'tech'],
    19: ['mathematics', 'math', 'maths'],
    20: ['mythology', 'myths', 'myth'],
    21: ['sports', 'sport'],
    22: ['geography', 'geo'],
    23: ['history'],
    24: ['politics'],
    25: ['art'],
    26: ['celebrities', 'celebrity', 'celebs', 'celeb'],
    27: ['animals', 'animal'],
    28: ['vehicles', 'vehicle'],
    29: ['comics', 'comic'],
    30: ['gadgets', 'gadget'],
    31: ['japan', 'japanese', 'anime', 'manga', 'animu', 'mango'],
    32: ['cartoons', 'cartoon', 'animations', 'animation']
}

streaks = {}


def shuffle_questions(question_list):
    """

    :param question_list:
    :type question_list:
    :return:
    :rtype:
    """
    output = []
    while question_list:
        question_choice = question_list.pop(secrets.randbelow(len(question_list)))
        output.append(question_choice)
    return output


def get_correct_index(question_list, answer):
    """

    :param question_list:
    :type question_list:
    :param answer:
    :type answer:
    :return:
    :rtype:
    """
    index = 0
    for item in question_list:
        if item == answer:
            break
        else:
            index += 1
    return index


async def trivia(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    global streaks
    if await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        on_cooldown = discord.Embed(color=0xccffff, title=f'❄ On cooldown for another {timeout} seconds.')
        await pld.msg.channel.send(embed=on_cooldown)
        return
    try:
        if not Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
            Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
            allotted_time = 20
            trivia_api_url = 'https://opentdb.com/api.php?amount=1'
            cat_chosen = False
            if pld.args:
                catlook = pld.args[-1].lower()
                for cat in categories:
                    cat_alts = categories.get(cat)
                    if catlook in cat_alts:
                        trivia_api_url += f'&category={cat}'
                        cat_chosen = True
                        break
                diflook = pld.args[0].lower()
                if diflook in ['easy', 'medium', 'hard']:
                    trivia_api_url += f'&difficulty={diflook}'
                    cat_chosen = True
            async with aiohttp.ClientSession() as session:
                async with session.get(trivia_api_url) as number_get:
                    number_response = await number_get.read()
                    try:
                        data = json.loads(number_response).get('results')[0]
                    except json.JSONDecodeError:
                        if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
                            Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
                        decode_error = error('Could not retrieve a question.')
                        await pld.msg.channel.send(embed=decode_error)
                        return
            await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, 30)
            question = data['question']
            question = ftfy.fix_text(question)
            question = re.sub(r'([*_~`])', r'\\\1', question)  # escape markdown formatting
            category = data['category']
            correct_answer = data['correct_answer']
            correct_answer = ftfy.fix_text(correct_answer)
            incorrect_answers = data['incorrect_answers']
            difficulty = data['difficulty']
            reward_mult = streaks.get(pld.msg.author.id) or 0 if not cat_chosen else 0
            kud_reward = int(
                (awards.get(difficulty) or '10') * (1 + (reward_mult * 2.25) / (1.75 + (0.03 * reward_mult))))
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
            starter = 'An' if difficulty == 'easy' else 'A'
            question_embed = discord.Embed(color=0xF9F9F9, title='❔ Here\'s a question!')
            question_embed.description = f'{starter} {difficulty} one from the {category} category.'
            question_embed.add_field(name='Question', value=question, inline=False)
            question_embed.add_field(name='Choices', value=f'```py\n{choice_text}\n```', inline=False)
            question_embed.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
            footer_text = 'Input the number of your chosen answer.'
            if reward_mult:
                footer_text += f' | Streak: {int(reward_mult)}'
            question_embed.set_footer(text=footer_text)
            await pld.msg.channel.send(embed=question_embed)

            def check_answer(msg):
                """

                :param msg:
                :type msg:
                :return:
                :rtype:
                """
                if pld.msg.channel.id != msg.channel.id:
                    return
                if pld.msg.author.id != msg.author.id:
                    return
                if msg.content.isdigit():
                    try:
                        int_content = int(msg.content)
                    except ValueError:
                        return
                    if abs(int_content) <= len(choice_lines):
                        return True
                    else:
                        return
                elif msg.content.title() in choice_list:
                    return True

            try:
                answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=allotted_time)
                try:
                    answer_index = int(answer_message.content) - 1
                except ValueError:
                    answer_index = None
                correct_index = get_correct_index(choice_list, correct_answer)
                if answer_index == correct_index or answer_message.content.lower() == correct_answer.lower():
                    if cat_chosen:
                        streaks.update({pld.msg.author.id: reward_mult + 0.005})
                    else:
                        streaks.update({pld.msg.author.id: reward_mult + 1})
                    await cmd.db.add_resource(answer_message.author.id, 'currency', kud_reward, cmd.name, pld.msg)
                    author = answer_message.author.display_name
                    currency = cmd.bot.cfg.pref.currency
                    win_title = f'🎉 Correct, {author}, it was {correct_answer}. You won {kud_reward} {currency}!'
                    final_embed = discord.Embed(color=0x77B255, title=win_title)
                else:
                    if pld.msg.author.id in streaks:
                        streaks.pop(pld.msg.author.id)
                    lose_title = f'💣 Ooh, sorry, it was {correct_answer}...'
                    final_embed = discord.Embed(color=0x262626, title=lose_title)
                await pld.msg.channel.send(embed=final_embed)
            except asyncio.TimeoutError:
                if pld.msg.author.id in streaks:
                    streaks.pop(pld.msg.author.id)
                timeout_title = f'🕙 Time\'s up! It was {correct_answer}...'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await pld.msg.channel.send(embed=timeout_embed)
            if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
                Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
        else:
            ongoing_error = error('There is already one ongoing.')
            await pld.msg.channel.send(embed=ongoing_error)
    except Exception:
        if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
        raise
