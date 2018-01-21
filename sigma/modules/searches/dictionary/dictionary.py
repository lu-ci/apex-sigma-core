import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def dictionary(cmd: SigmaCommand, message: discord.Message, args: list):
    if 'app_id' in cmd.cfg and 'app_key' in cmd.cfg:
        headers = {
            'Accept': 'application/json',
            'app_id': cmd.cfg['app_id'],
            'app_key': cmd.cfg['app_key']
        }
        if args:
            qry = ' '.join(args)
            api_url = f'https://od-api.oxforddictionaries.com/api/v1/entries/en/{qry}'
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as data_response:
                    data = await data_response.read()
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        data = {'results': []}
            if data['results']:
                data = data['results'][0]
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
                    if senses:
                        for sense in senses:
                            definitions = sense.get('definitions')
                            definition_block += definitions
                            examples = sense.get('examples')
                            if examples:
                                for example in examples:
                                    example = example.get('text')
                                    if example:
                                        example_block.append(example)
                    response = discord.Embed(color=0x3B88C3, title=f'📘 Oxford Dictionary: `{term}`')
                    if etyms:
                        response.add_field(name='Etymologies', value='\n'.join(etyms), inline=False)
                    if definition_block:
                        response.add_field(name='Definitions', value='\n'.join(definition_block), inline=False)
                    if example_block:
                        response.add_field(name='Examples', value=', '.join(example_block), inline=False)
                    response.set_footer(text=f'Category: {cat} | Features: {", ".join(feat_block)}')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 No lexical data found.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No results.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
