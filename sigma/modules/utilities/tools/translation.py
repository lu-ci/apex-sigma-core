# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import translate

from sigma.core.mechanics.command import SigmaCommand


async def translation(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            trans_arg = args[0]
            sentence = ' '.join(args[1:])
            if '>' in trans_arg:
                trans_split = trans_arg.split('>')
                from_lang = trans_split[0].lower()
                to_lang = trans_split[1].lower()
            else:
                from_lang = trans_arg
                to_lang = 'en'
            translator = translate.Translator(to_lang=to_lang, from_lang=from_lang)
            trans_output = translator.translate(sentence)
            title = f'🔠 Translated from {from_lang.upper()} to {to_lang.upper()}'
            response = discord.Embed(color=0x3B88C3, title=title)
            response.description = trans_output
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing language or sentence.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
