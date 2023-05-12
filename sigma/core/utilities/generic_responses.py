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

import discord


class GenericResponse(object):
    """
    Handles the creation of generic response embeds.
    """

    def __init__(self, desc):
        """
        :type desc: str
        """
        self.desc = desc

    @staticmethod
    def generic_embed(color, title):
        """
        Creates a generic response embed.
        :type color: int
        :type title: str
        :rtype: discord.Embed
        """
        return discord.Embed(color=color, title=title)

    def ok(self):
        """
        Creates a generic success response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0x77B255, f'✅ {self.desc}')

    def info(self):
        """
        Creates a generic information response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0x3B88C3, f'ℹ️ {self.desc}')

    def not_found(self):
        """
        Creates a generic not-found response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0x696969, f'🔍 {self.desc}')

    def denied(self):
        """
        Creates a generic denial response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0xBE1931, f'⛔ {self.desc}')

    def warn(self):
        """
        Creates a generic warning response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0xFFCC4D, f'⚠ {self.desc}')

    def error(self):
        """
        Creates a generic error response.
        :rtype: discord.Embed
        """
        return self.generic_embed(0xBE1931, f'❗ {self.desc}')
