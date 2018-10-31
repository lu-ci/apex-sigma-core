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
import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar

ongoing_list = []


class Board(object):
    def __init__(self):
        self.rows = []
        self.r = '🔴'
        self.b = '🔵'
        self.e = '⚫'

    @property
    def make(self):
        [self.rows.append([self.e for _ in range(7)]) for _ in range(6)]
        return self.rows

    def edit(self, column: int, player: str):
        piece = getattr(self, player)
        for i, cell in reversed(list(enumerate(self.column(column)))):
            if cell == self.e:
                self.rows[i][column] = piece
                break
        return self.rows

    def column(self, column: int):
        return [row[column] for row in self.rows]

    @property
    def columns(self):
        return [self.column(i) for i, r in enumerate(self.rows)]

    def column_full(self, column: int):
        return self.rows[0][column] != self.e

    @property
    def full(self):
        return all([self.rows[0][i] != self.e for i in range(len(self.rows))])

    @property
    def winner(self):
        full = self.full
        for row in self.rows:
            chunks = [row[0:4], row[1:5], row[2:6], row[3:7]]
            winner, win = self.first_check(chunks)
            if win:
                return full, winner, win
        for column in self.columns:
            chunks = [column[0:4], column[1:5], column[2:6]]
            winner, win = self.first_check(chunks)
            if win:
                return full, winner, win
        winner, win = self.second_check()
        return full, winner, win

    def first_check(self, chunks: list):
        winner, win = None, False
        for chunk in chunks:
            if all(x == chunk[0] != self.e for x in chunk):
                winner, win = chunk[0], True
                break
        return winner, win

    def second_check(self):
        for chunk in self.chunks(self.rows):
            if all(x == chunk[0] != self.e for x in chunk):
                return chunk[0], True
        reversed_rows = [list(reversed(row)) for row in self.rows]
        for chunk in self.chunks(reversed_rows):
            if all(x == chunk[0] != self.e for x in chunk):
                return chunk[0], True
        return None, False

    @staticmethod
    def chunks(rows: list):
        # Gets all diagonal winning positions in one direction
        bases = [[(3, 0), (2, 1), (1, 2), (0, 3)], [(4, 0), (3, 1), (2, 2), (1, 3)], [(5, 0), (4, 1), (3, 2), (2, 3)]]
        chunks = []
        for chunk in bases:
            for _ in range(4):
                chunks.append(chunk)
                chunk = [(x, y + 1) for x, y in chunk]
        rows = [[rows[x][y] for x, y in chunk] for chunk in chunks]
        return rows


def bot_move(board, last: int):
    choice, bad_col = None, True
    while bad_col:
        move = secrets.randbelow(3)
        if move == 0:
            mod = secrets.choice([-1, 0, 1])
            choice = max(min(6, last + mod), 0)
        else:
            choice = secrets.randbelow(6)
        if not board.column_full(choice):
            bad_col = False
    return choice


def generate_response(avatar, current: discord.Member, rows: list):
    board_out = "\n".join([' '.join(row) for row in rows])
    board_resp = discord.Embed(color=0x2156be, description=board_out)
    board_resp.set_author(icon_url=avatar, name='Connect Four')
    board_resp.set_footer(text=f'{current.display_name}\'s Turn.')
    return board_resp


async def send_board_msg(message: discord.Message, board_msg: discord.Message, board_resp: discord.Embed):
    if board_msg:
        try:
            await board_msg.edit(embed=board_resp)
        except discord.NotFound:
            board_msg = await message.channel.send(embed=board_resp)
    else:
        board_msg = await message.channel.send(embed=board_resp)
    return board_msg


async def connectfour(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author.id not in ongoing_list:
        ongoing_list.append(message.channel.id)
        competitor, curr_turn = None, message.author
        color = args[0][0].lower() if args else None
        player = 'b' if color == 'b' else 'r'
        bot = 'r' if color == 'b' else 'b'
        if message.mentions:
            if message.mentions[0].id != message.author.id and not message.mentions[0].bot:
                competitor = bot
                bot = None
            else:
                ender = 'another bot' if message.mentions[0].bot else 'yourself'
                self_embed = discord.Embed(color=0xBE1931, title=f'❗ You can\'t play against {ender}.')
                await message.channel.send(embed=self_embed)
                return

        board = Board()
        user_av = user_avatar(message.author)
        board_resp = generate_response(user_av, message.author, board.make)
        board_msg = await message.channel.send(embed=board_resp)

        def check_answer(msg):
            if curr_turn.id != msg.author.id:
                return
            if message.channel.id != msg.channel.id:
                return

            choice = msg.content
            if choice.lower() == 'cancel':
                valid = True
            elif choice.isdigit():
                if 0 < int(choice) <= 7:
                    if not board.column_full(int(choice) - 1):
                        valid = True
                    else:
                        valid = False
                else:
                    valid = False
            else:
                valid = False
            return valid

        finished, winner, win = False, None, False
        last_bot_move = 3
        while not finished:
            try:
                answer = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
                if answer:
                    if answer.content.lower() != 'cancel':
                        try:
                            await answer.delete()
                        except (discord.NotFound, discord.Forbidden):
                            pass
                        column = int(answer.content) - 1
                        piece = player if curr_turn.id == message.author.id else competitor
                        if bot:
                            next_player = cmd.bot.user
                        else:
                            next_player = message.author if curr_turn != message.author else message.mentions[0]
                        board_resp = generate_response(user_av, next_player, board.edit(column, piece))
                        board_msg = await send_board_msg(message, board_msg, board_resp)
                        full, winner, win = board.winner
                        finished = win or full
                        if not finished:
                            if not competitor:
                                # Bot takes turn
                                await asyncio.sleep(2)
                                last_bot_move = bot_choice = bot_move(board, last_bot_move)
                                board_resp = generate_response(user_av, cmd.bot.user, board.edit(bot_choice, bot))
                                board_msg = await send_board_msg(message, board_msg, board_resp)
                                full, winner, win = board.winner
                                finished = win or full
                            else:
                                if curr_turn == message.author:
                                    curr_turn = message.mentions[0]
                                else:
                                    curr_turn = message.author
                    else:
                        cancel_embed = discord.Embed(color=0xFFCC4D, title='🔥 Game canceled!')
                        await message.channel.send(embed=cancel_embed)
                        return
            except asyncio.TimeoutError:
                timeout_title = f'🕙 Time\'s up {curr_turn.display_name}!'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await message.channel.send(embed=timeout_embed)
                return

        if winner:
            if bot:
                if winner == getattr(board, player):
                    color, icon, resp = 0x3B88C3, '💎', 'You win'
                else:
                    color, icon, resp = 0x292929, '💣', 'You lose'
            else:
                color, icon, resp = 0x3B88C3, '💎', f'{curr_turn.display_name} wins'
        else:
            color, icon, resp = 0xFFCC4D, '🔥', 'It\'s a draw'
        response = discord.Embed(color=color, title=f'{icon} {resp}!')
        await message.channel.send(embed=response)
        if message.channel.id in ongoing_list:
            ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is already one ongoing.')
        await message.channel.send(embed=ongoing_error)
