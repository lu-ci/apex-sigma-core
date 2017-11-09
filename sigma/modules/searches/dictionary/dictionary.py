import json

import aiohttp
import discord


async def dictionary(cmd, message, args):
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
                data = data['results'][0]['lexicalEntries'][0]['entries'][0]
                if 'etymologies' in data:
                    etymology = data['etymologies'][0]
                else:
                    etymology = 'No etymology found.'
                senses = []
                for sense in data['senses']:
                    if "domains" in sense and 'definitions' in sense:
                        senses.append(f'{sense["domains"][0]}: {sense["definitions"][0]}.')
                notes = []
                if 'notes' in data:
                    for note in data['notes']:
                        notes.append(f"{note['text']}.")
                response = discord.Embed(color=0x3B88C3, title=f'📘 Oxford Dictionary: `{qry}`')
                response.add_field(name='Etymology', value=etymology, inline=False)
                if senses:
                    response.add_field(name='Senses', value='\n'.join(senses[:10]), inline=False)
                if notes:
                    response.add_field(name='Notes', value='\n'.join(notes[:3]))
            else:
                response = discord.Embed(color=0x696969, title='🔍 No results.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
