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


def generate_small_embed(icon, color, text):
    """
    Creates an embed object for generic responses.
    :param icon: The icon to use for this embed.
    :type icon: str
    :param color: The color to use for this embed.
    :type color: int
    :param text: The text to use for this embed.
    :type text: str
    :return:
    :rtype: discord.Embed
    """
    return discord.Embed(color=color, title=f'{icon} {text}')


def denied(content):
    """
    Creates a generic denial response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('⛔', 0xBE1931, content)


def ok(content):
    """
    Creates a generic success response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('✅', 0x77B255, content)


def info(content):
    """
    Creates a generic information response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('ℹ', 0x3B88C3, content)


def warn(content):
    """
    Creates a generic warning response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('⚠', 0xFFCC4D, content)


def error(content):
    """
    Creates a generic error response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('❗', 0xBE1931, content)


def not_found(content):
    """
    Creates a generic not-found response.
    :param content: The text to use for this response.
    :type content: str
    :return:
    :rtype: discord.Embed
    """
    return generate_small_embed('🔍', 0x696969, content)
