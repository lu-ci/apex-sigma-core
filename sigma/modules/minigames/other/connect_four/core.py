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


class ConnectFourBoard(object):
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

    def bot_move(self, last: int):
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
