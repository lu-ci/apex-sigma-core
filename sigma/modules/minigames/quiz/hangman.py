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
import secrets

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.quiz.hang_man.core import Gallows
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


def generate_response(gallows):
    """
    :type gallows: sigma.modules.minigames.quiz.hang_man.core.Gallows
    :rtype: discord.Embed
    """
    hangman_resp = discord.Embed(color=0x3B88C3, title='🔣 Hangman')
    hangman_resp.add_field(name='Gallows', value=f'```\n{gallows.make_gallows_man()}\n```', inline=False)
    used_letters = ', '.join(sorted(gallows.wrong_letters)) if gallows.wrong_letters else 'Nothing Yet.'
    hangman_resp.add_field(name='Used Letters', value=used_letters, inline=False)
    hangman_resp.add_field(name='Word', value=gallows.make_word_space(), inline=False)
    return hangman_resp


async def send_hangman_msg(message, hangman_msg, hangman_resp):
    """
    :type message: discord.Message
    :type hangman_msg: discord.Message
    :type hangman_resp: discord.Embed
    :rtype: discord.Message
    """
    if hangman_msg:
        try:
            await hangman_msg.edit(embed=hangman_resp)
        except discord.NotFound:
            hangman_msg = await message.channel.send(embed=hangman_resp)
    else:
        hangman_msg = await message.channel.send(embed=hangman_resp)
    return hangman_msg


async def hangman(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    cache_key = 'hangman_word_cache'
    word_cache = await cmd.db.cache.get_cache(cache_key) or {}
    if not word_cache:
        dict_docs = await cmd.db[cmd.db.db_name].DictionaryData.find().to_list(None)
        for ddoc in dict_docs:
            word = ddoc.get('word')
            if len(word) > 3 and len(word.split(' ')) == 1 and '-' not in word:
                word_cache.update({word: ddoc.get('description')})
        await cmd.db.cache.set_cache(cache_key, word_cache)
    if not Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
        Ongoing.set_ongoing(cmd.name, pld.msg.channel.id)
        words = list(word_cache.keys())
        gallows = Gallows(secrets.choice(words))
        word_description = word_cache.get(gallows.word)
        kud_reward = gallows.count
        author = pld.msg.author.display_name
        hangman_resp = generate_response(gallows)
        hangman_msg = await pld.msg.channel.send(embed=hangman_resp)

        def check_answer(msg):
            """
            Checks if the answer message is correct.
            :type msg: discord.Message
            :rtype: bool
            """
            if pld.msg.channel.id != msg.channel.id:
                return
            if pld.msg.author.id != msg.author.id:
                return
            if len(msg.content) == 1:
                if msg.content.isalpha():
                    correct = True
                else:
                    correct = False
            else:
                correct = False
            return correct

        finished = False
        timeout = False
        while not timeout and not finished:
            try:
                answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
                letter = answer_message.content.lower()
                if letter in gallows.word:
                    if letter not in gallows.right_letters:
                        gallows.right_letters.append(letter)
                else:
                    if letter.upper() not in gallows.wrong_letters:
                        gallows.wrong_letters.append(letter.upper())
                        gallows.use_part()
                hangman_msg = await send_hangman_msg(pld.msg, hangman_msg, generate_response(gallows))
                finished = gallows.victory or gallows.dead
            except asyncio.TimeoutError:
                timeout = True
                timeout_title = '🕙 Time\'s up!'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                timeout_embed.add_field(name=f'It was {gallows.word}.', value=word_description)
                await pld.msg.channel.send(embed=timeout_embed)

        if gallows.dead:
            lose_title = f'💥 Ooh, sorry {author}, it was {gallows.word}.'
            final_embed = discord.Embed(color=0xff3300, title=lose_title)
            await pld.msg.channel.send(embed=final_embed)
        elif gallows.victory:
            await cmd.db.add_resource(pld.msg.author.id, 'currency', kud_reward, cmd.name, pld.msg)
            currency = cmd.bot.cfg.pref.currency
            win_title = f'🎉 Correct, {author}, it was {gallows.word}. You won {kud_reward} {currency}!'
            win_embed = discord.Embed(color=0x77B255, title=win_title)
            await pld.msg.channel.send(embed=win_embed)

        if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
    else:
        ongoing_error = GenericResponse('There is one already ongoing.').error()
        await pld.msg.channel.send(embed=ongoing_error)
