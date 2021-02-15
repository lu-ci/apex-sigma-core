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

alive, dead = '🔵', '🔴'
body_parts = {
    'head': ' Head',
    'torso': ' Torso',
    'larm': ' Left Arm',
    'rarm': ' Right Arm',
    'lleg': ' Left Leg',
    'rleg': ' Right Leg'
}


class Gallows(object):
    """
    A simple hangman game manager.
    """

    def __init__(self, word):
        """
        :type word: str
        """
        self.unused = list(body_parts.copy().keys())
        self.used = []
        self.word = word.lower()
        self.right_letters = []
        self.wrong_letters = []
        self.count = len(self.word)

    @property
    def victory(self):
        """
        Checks if the word has been successfully guessed.
        :rtype: bool
        """
        return not set(self.word) - set(self.right_letters)

    @property
    def dead(self):
        """
        Checks if the hangman is completely dead.
        :rtype: bool
        """
        return not self.unused

    def use_part(self):
        """
        Marks a single part of the hangman as used.
        """
        self.used.append(self.unused.pop(secrets.randbelow((len(self.unused)))))

    def make_gallows_man(self):
        """
        Creates the visual representation of the hangman.
        :rtype: str
        """
        parts = []
        for name, part in body_parts.items():
            state = alive if name in self.unused else dead
            parts.append(state + part)
        return '\n'.join(parts)

    def make_word_space(self):
        """
        Creates the visual representation of the word.
        :rtype: str
        """
        word_space = []
        for letter in self.word:
            if letter in self.right_letters:
                char = letter if word_space else letter.upper()
                word_space.append(char)
            else:
                word_space.append(r'\_\_')
        return ' '.join(word_space)
