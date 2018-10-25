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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand

oxford_icon = 'https://i.imgur.com/lrinjBC.png'


async def dictionary(cmd: SigmaCommand, pld: CommandPayload):
    if 'app_id' in cmd.cfg and 'app_key' in cmd.cfg:
        headers = {
            'Accept': 'application/json',
            'app_id': cmd.cfg['app_id'],
            'app_key': cmd.cfg['app_key']
        }
        if args:
            query = '_'.join(args).lower()
            oxford_url = f'https://en.oxforddictionaries.com/definition/{query}'
            api_url = f'https://od-api.oxforddictionaries.com/api/v1/entries/en/{query}'
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as data_response:
                    data = await data_response.read()
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        data = {'results': []}
            if data.get('results'):
                data = data.get('results')[0]
                lex = data.get('lexicalEntries')
                if lex:
                    lex = lex[0]
                    cat = lex.get('lexicalCategory')
                    term = lex.get('text')
                    ent = lex.get('entries')[0]
                    etyms = ent.get('etymologies')
                    feats = ent.get('grammaticalFeatures')
                    feat_block = []
                    if feats:
                        for feat in feats:
                            feat_text = feat.get('text')
                            feat_type = feat.get('type')
                            feat_line = f'{feat_text} {feat_type}'
                            feat_block.append(feat_line)
                    senses = ent.get('senses')
                    definition_block = []
                    example_block = []
                    reference_block = []
                    if senses:
                        for sense in senses:
                            definitions = sense.get('definitions')
                            references = sense.get('crossReferenceMarkers')
                            if definitions:
                                definition_block += definitions
                                examples = sense.get('examples')
                                if examples:
                                    for example in examples:
                                        example = example.get('text')
                                        if example:
                                            example_block.append(example)
                            if references:
                                for reference in references:
                                    if '(' in reference:
                                        reference = reference.split('(')[0]
                                    reference_block.append(reference)
                    term = term.replace("_", " ").upper()
                    response = discord.Embed(color=0x00bef2)
                    response.set_author(name=f'Oxford Dictionary: {term}', icon_url=oxford_icon, url=oxford_url)
                    if etyms:
                        response.add_field(name='Etymologies', value='\n'.join(etyms), inline=False)
                    if definition_block:
                        response.add_field(name='Definitions', value='\n'.join(definition_block), inline=False)
                    if example_block:
                        response.add_field(name='Examples', value=', '.join(example_block), inline=False)
                    if reference_block:
                        response.add_field(name='References', value=', '.join(reference_block), inline=False)
                    if response.fields:
                        response.set_footer(text=f'Category: {cat} | Features: {", ".join(feat_block)}')
                    else:
                        response = discord.Embed(color=0x696969, title='🔍 No lexical data found.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 No lexical data found.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No results.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
