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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.minigames.quiz.mech.utils import scramble

ongoing_list = []
word_cache = {}


async def unscramble(cmd: SigmaCommand, message: discord.Message, args: list):
    if not word_cache:
        dict_docs = await cmd.db[cmd.db.db_nam].DictionaryData.find({}).to_list(None)
        for ddoc in dict_docs:
            word = ddoc.get('word')
            if len(word) > 3 and len(word.split(' ')) == 1:
                word_cache.update({word: ddoc.get('description')})
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
            await cmd.db.add_resource(answer_message.author.id, 'currency', kud_reward, cmd.name, message)
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
