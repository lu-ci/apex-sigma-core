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

from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


async def mathgame(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
        Ongoing.set_ongoing(cmd.name, pld.msg.channel.id)
        if pld.args:
            try:
                diff = int(pld.args[0])
                if diff < 1:
                    diff = 1
                elif diff > 9:
                    diff = 9
            except ValueError:
                diff = 3
        else:
            diff = 3
        max_num = diff * 8
        easy_operators = ['+', '-']
        hard_operators = ['*', '/']
        math_operators = easy_operators + hard_operators
        problem_string = str(secrets.randbelow(max_num))
        allotted_time = 7
        kud_reward = 2
        for x in range(0, diff):
            num = secrets.randbelow(max_num) + 1
            oper = secrets.choice(math_operators)
            if oper in easy_operators:
                kud_reward += 1
                allotted_time += 3
            else:
                kud_reward += 4
                allotted_time += 9
            problem_string += f' {oper} {num}'
        result = round(eval(problem_string), 2)
        problem_string = problem_string.replace('*', 'x').replace('/', '÷')
        question_embed = discord.Embed(color=0x3B88C3, title=f'#⃣  You have {allotted_time} seconds.')
        question_embed.description = f'{problem_string} = ?'
        await pld.msg.channel.send(embed=question_embed)

        def check_answer(msg):
            """

            :param msg:
            :type msg:
            :return:
            :rtype:
            """
            if pld.msg.channel.id == msg.channel.id:
                try:
                    an_num = float(msg.content)
                    if an_num == result:
                        correct = True
                    else:
                        correct = False
                except ValueError:
                    correct = False
            else:
                correct = False
            return correct

        try:
            answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=allotted_time)
            await cmd.db.add_resource(answer_message.author.id, 'currency', kud_reward, cmd.name, pld.msg)
            author = answer_message.author.display_name
            currency = cmd.bot.cfg.pref.currency
            win_title = f'🎉 Correct, {author}, it was {result}. You won {kud_reward} {currency}!'
            win_embed = discord.Embed(color=0x77B255, title=win_title)
            await pld.msg.channel.send(embed=win_embed)
        except asyncio.TimeoutError:
            timeout_title = f'🕙 Time\'s up! It was {result}...'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            await pld.msg.channel.send(embed=timeout_embed)
        if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
    else:
        ongoing_error = error('There is already one ongoing.')
        await pld.msg.channel.send(embed=ongoing_error)
