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


def scramble(text, full=False):
    """

    :param text:
    :type text: str
    :param full:
    :type full: bool
    :return:
    :rtype: str
    """
    separated_text = text.split()
    char_list = list(text.replace(' ', ''))
    chunks = []
    for word in separated_text:
        chunk = ''
        if not full:
            char_list = list(word)
        for _ in range(len(word)):
            chunk += char_list.pop(secrets.randbelow(len(char_list)))
        chunks.append(chunk)
    end_text = ' '.join(chunks)
    return end_text
