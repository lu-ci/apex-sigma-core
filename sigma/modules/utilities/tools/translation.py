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
import translate

from sigma.core.utilities.generic_responses import GenericResponse

wiki_url = 'https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'


async def translation(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        trans_arg = pld.args[0].lower()
        sentence = ' '.join(pld.args[1:])
        if '\n' in trans_arg:
            trans_arg, _, first_arg = trans_arg.partition('\n')
            sentence = f'{first_arg} {sentence}'
        if '>' in trans_arg:
            trans_split = trans_arg.split('>')
            from_lang = trans_split[0]
            to_lang = trans_split[1]
        else:
            from_lang = trans_arg
            to_lang = 'en'
        if sentence:
            translator = translate.Translator(to_lang=to_lang, from_lang=from_lang)
            trans_output = translator.translate(sentence)
            if 'is an invalid' in trans_output.lower():
                lang_iso = trans_output.split()[0].strip("'")
                response = GenericResponse(f'{lang_iso} is an invalid language code.').error()
                response.description = f'[Click for a list of language ISO codes]({wiki_url})'
            # 'excedeed' is misspelled intentionally
            elif 'length limit excedeed' in trans_output.lower():
                response = GenericResponse('Maximum query limit is 500 characters.').error()
            elif 'mymemory warning' in trans_output.lower():
                time_pieces = []
                for word in trans_output.split(' '):
                    if word.isdigit():
                        time_pieces.append(word)
                time = ':'.join(time_pieces)
                response = GenericResponse('Unable to translate more due to rate limits.').error()
                response.set_footer(text=f'More translations available in {time}.')
            else:
                title = f'🔠 Translated from {from_lang.upper()} to {to_lang.upper()}'
                response = discord.Embed(color=0x3B88C3, title=title)
                response.description = trans_output
        else:
            response = GenericResponse('Missing language or sentence.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
