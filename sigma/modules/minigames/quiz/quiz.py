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
import os
import secrets

import discord
import yaml

from sigma.core.mechanics.command import SigmaCommand

active_quizzes = {}


async def quiz(cmd: SigmaCommand, message: discord.Message, args: list):
    # exit if quiz is already active in the channel
    if message.channel.id in active_quizzes:
        return

    # load quizzes from the resources
    quizzes = []
    for root, dirs, files in os.walk(cmd.resource('')):
        index = 1
        for file in files:
            if file.endswith('.yml'):
                file_path = (os.path.join(root, file))
                with open(file_path, encoding='utf-8') as quiz_file:
                    data = yaml.safe_load(quiz_file)
                    data.update({'index': index})
                    quizzes.append(data)
                    index += 1
    # respond with a list of available quizzes
    response_body = ''
    for quiz_item in quizzes:
        response_body += f"`#{quiz_item['index']}.` {quiz_item['quiz']}"
    response = discord.Embed(color=message.guild.me.color, title='Pick a quiz', description=response_body)
    quiz_list = await message.channel.send(embed=response)

    def check_value(msg):
        # check if the message is an integer
        try:
            int(msg.content)
            return True
        except ValueError:
            return False

    # wait for user response
    response = discord.Embed(color=message.guild.me.color)  # response for user response
    try:
        index = await cmd.bot.wait_for('message', check=check_value, timeout=5)
        active_quizzes[message.channel.id] = True
        await quiz_list.delete()  # delete the quiz list
        await index.delete()  # delete the user response
        index = index.content
        queue = []
        # look for the chosen index in the data
        for quiz_item in quizzes:
            if str(quiz_item['index']) == str(index):
                # grab 10 random items
                while len(queue) != 2:
                    addition = quiz_item['questions'].pop(secrets.randbelow(len(quiz_item['questions'])))
                    queue.append(addition)
        if not queue:
            response.title = 'Selected quiz was not found'
            await message.channel.send(embed=response)
        else:
            # start the quiz
            unanswered = []
            scores = {}
            for item in queue:
                response = discord.Embed(color=message.guild.me.color, title=quiz_item['quiz'])
                response.description = quiz_item['question_template']
                response.description = response.description.replace('${question}', 'or '.join(item['questions']))
                await message.channel.send(embed=response)
                # awaiting for the user answer
                response = discord.Embed(color=message.guild.me.color, title=quiz_item['quiz'])
                try:
                    def check_answer(msg):
                        if msg.content in item['answers']:
                            out = True
                        else:
                            out = False
                        return out

                    answer = await cmd.bot.wait_for('message', check=check_answer, timeout=12)
                    await answer.delete()
                    response = discord.Embed(color=0x00FF00, title=quiz_item['quiz'])
                    desc_text = f"Correct answer by {answer.author.mention}!"
                    desc_text += f" The answer was {'or '.join(item['answers'])}"
                    response.description = desc_text
                    await message.channel.send(embed=response)
                    try:
                        scores[answer.author.id] += 1
                    except KeyError:
                        scores[answer.author.id] = 1
                except asyncio.TimeoutError:
                    response = discord.Embed(color=0xFF0000, title=quiz_item['quiz'])
                    response.description = f"Correct answer was {'or '.join(item['answers'])}"
                    await message.channel.send(embed=response)
                    unanswered.append(item)
            summary = discord.Embed(color=message.guild.me.color, title='Quiz end')
            summary_body = '**Final scores**\n'
            for uid in scores:
                summary_body += f"<@{uid}> - {scores[uid]} point(s) \n"
            if unanswered:
                summary_body += '\n**Unanswered questions**\n'
                for item in unanswered:
                    summary_body += f"{', '.join(item['questions'])} ({', '.join(item['answers'])})\n"
            summary.description = summary_body
            await message.channel.send(embed=summary)
            del active_quizzes[message.channel.id]
    except asyncio.TimeoutError:
        response.title = 'Timed out, please use the command again to pick a quiz'
        await message.channel.send(embed=response)
