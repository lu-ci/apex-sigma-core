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
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

symbol_groups = (
    ('♥', '❤'),  # :hearts:, :heart:
    ('♦',),  # :diamonds:
    ('♠',),  # :spades:
    ('♣',),  # :clubs:
    ('⭐',),  # :star:
    ('⚡',)  # :zap:
)
all_symbols = [symbol for group in symbol_groups for symbol in group]
first_symbols = [group[0] for group in symbol_groups]


def check_answer(content, sequence):
    """
    :type content: str
    :type sequence: list[str]
    :rtype: bool, list[str]
    """
    filtered_args = [group[0] for char in content for group in symbol_groups if char in group]
    results = []
    correct = True
    for loop_index, arg in enumerate(filtered_args):
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


async def sequencegame(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
        ongoing_error = GenericResponse('There is already one ongoing.').error()
        await pld.msg.channel.send(embed=ongoing_error)
        return
    try:
        Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
        chosen = [secrets.choice(first_symbols) for _ in range(4)]
        title = f'🎯 {pld.msg.author.display_name}, you have 90 seconds for each attempt.'
        desc = f'Symbols you can use: {"".join(first_symbols)}'
        start_embed = discord.Embed(color=0xf9f9f9)
        start_embed.add_field(name=title, value=desc)
        await pld.msg.channel.send(embed=start_embed)

        def answer_check(msg):
            """
            :type msg: discord.Message
            :rtype: bool
            """
            if pld.msg.author.id != msg.author.id:
                return
            if pld.msg.channel.id != msg.channel.id:
                return

            message_args = [char for char in msg.content if char in all_symbols]
            if len(message_args) != 4:
                return

            for arg in message_args:
                if arg in all_symbols:
                    return True

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
                    currency = cmd.bot.cfg.pref.currency
                    await cmd.db.add_resource(answer.author.id, 'currency', 50, cmd.name, pld.msg)
                    win_title = f'🎉 Correct, {answer.author.display_name}. You won 50 {currency}!'
                    win_embed = discord.Embed(color=0x77B255, title=win_title)
                    await pld.msg.channel.send(embed=win_embed)
                else:
                    attempt_title = f'💣 {answer.author.display_name} {tries}/6: {"".join(results)}'
                    attempt_embed = discord.Embed(color=0x262626, title=attempt_title)
                    await pld.msg.channel.send(embed=attempt_embed)
            except asyncio.TimeoutError:
                finished = True
                victory = False
                timeout = True
                timeout_title = f'🕙 Time\'s up {pld.msg.author.display_name}! It was {"".join(chosen)}'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await pld.msg.channel.send(embed=timeout_embed)

        if not victory and not timeout:
            lose_title = f'💥 Ooh, sorry {pld.msg.author.display_name}, it was {"".join(chosen)}'
            final_embed = discord.Embed(color=0xff3300, title=lose_title)
            await pld.msg.channel.send(embed=final_embed)
        Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
    except Exception:
        if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
        raise
