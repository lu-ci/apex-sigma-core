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

import secrets


class ConnectFourGame(object):
    """
    Very basic container for connect four games.
    """

    __slots__ = (
        'raw', 'board', 'p_one', 'p_two', 'po_piece',
        'pt_piece', 'current_turn', 'last_bot_move',
        'is_bot', 'expiry', 'channel_id'
    )

    def __init__(self, data):
        self.raw = data
        self.board = self.raw.get('board')
        self.p_one = self.raw.get('p_one')
        self.p_two = self.raw.get('p_two')
        self.po_piece = self.raw.get('po_piece')
        self.pt_piece = self.raw.get('pt_piece')
        self.current_turn = self.raw.get('current_turn')
        self.last_bot_move = self.raw.get('last_bot_move')
        self.is_bot = self.raw.get('is_bot')
        self.expiry = self.raw.get('expiry')
        self.channel_id = self.raw.get('channel_id')


class ConnectFourBoard(object):
    """
    Container for the connect four board.
    Handles making and editing of the board,
    as well as checking for winners.
    """

    __slots__ = ('rows', 'r', 'b', 'e')

    def __init__(self):
        self.rows = []
        self.r = '🔴'
        self.b = '🔵'
        self.e = '⚫'

    @property
    def make(self):
        """
        :return:
        :rtype: list[list[str]]
        """
        [self.rows.append([self.e for _ in range(7)]) for _ in range(6)]
        return self.rows

    def edit(self, column, player):
        """
        :param column:
        :type column: int
        :param player:
        :type player: str
        :return:
        :rtype: list[list[str]]
        """
        piece = getattr(self, player)
        for i, cell in reversed(list(enumerate(self.column(column)))):
            if cell == self.e:
                self.rows[i][column] = piece
                break
        return self.rows

    def column(self, column):
        """
        :param column:
        :type column: int
        :return:
        :rtype: list[str]
        """
        return [row[column] for row in self.rows]

    @property
    def columns(self):
        """
        :return:
        :rtype: list[list[str]]
        """
        return [self.column(i) for i, r in enumerate(self.rows)]

    def column_full(self, column):
        """
        :param column:
        :type column: int
        :return:
        :rtype: bool
        """
        return self.rows[0][column] != self.e

    @property
    def full(self):
        """
        :return:
        :rtype: bool
        """
        return all([self.rows[0][i] != self.e for i in range(len(self.rows))])

    @property
    def winner(self):
        """
        :return:
        :rtype: (bool, str or None, bool)
        """
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

    def first_check(self, chunks):
        """
        :param chunks:
        :type chunks: list[list[str]]
        :return:
        :rtype: (str or None, bool)
        """
        winner, win = None, False
        for chunk in chunks:
            if all(x == chunk[0] != self.e for x in chunk):
                winner, win = chunk[0], True
                break
        return winner, win

    def second_check(self):
        """
        :return:
        :rtype: (str or None, bool)
        """
        for chunk in self.chunks(self.rows):
            if all(x == chunk[0] != self.e for x in chunk):
                return chunk[0], True
        reversed_rows = [list(reversed(row)) for row in self.rows]
        for chunk in self.chunks(reversed_rows):
            if all(x == chunk[0] != self.e for x in chunk):
                return chunk[0], True
        return None, False

    @staticmethod
    def chunks(rows):
        """
        :param rows:
        :type rows: list[list[str]]
        :return:
        :rtype: list[list[str]]
        """
        # Gets all diagonal winning positions in one direction
        bases = [
            [(3, 0), (2, 1), (1, 2), (0, 3)],
            [(4, 0), (3, 1), (2, 2), (1, 3)],
            [(5, 0), (4, 1), (3, 2), (2, 3)]
        ]
        chunks = []
        for chunk in bases:
            for _ in range(4):
                chunks.append(chunk)
                chunk = [(x, y + 1) for x, y in chunk]
        rows = [[rows[x][y] for x, y in chunk] for chunk in chunks]
        return rows

    def bot_move(self, last):
        """
        :param last:
        :type last: int
        :return:
        :rtype: int
        """
        choice, bad_col = None, True
        while bad_col:
            move = secrets.randbelow(3)
            if move == 0:
                mod = secrets.choice([-1, 0, 1])
                choice = max(min(6, last + mod), 0)
            else:
                choice = secrets.randbelow(6)
            if not self.column_full(choice):
                bad_col = False
        return choice
