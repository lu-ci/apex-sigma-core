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

import discord


def generate_small_embed(icon: str, color: int, text: str):
    return discord.Embed(color=color, title=f'{icon} {text}')


def denied(permission: str):
    return generate_small_embed('⛔', 0xBE1931, f'Access Denied. {permission} needed.')


def ok(content: str):
    return generate_small_embed('✅', 0x77B255, content)


def info(content: str):
    return generate_small_embed('ℹ', 0x3B88C3, content)


def warn(content: str):
    return generate_small_embed('⚠', 0xFFCC4D, content)


def not_found(content: str):
    return generate_small_embed('🔍', 0x696969, content)
