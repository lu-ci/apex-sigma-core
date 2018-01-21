import json

import discord


async def httpstatus(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0]
        with open(cmd.resource('http_status.json'), 'r', encoding='utf-8') as status_file:
            status_data = json.loads(status_file.read())
        if lookup in status_data:
            status_id = lookup
            status_data = status_data[status_id]
            status_message = status_data['message']
            status_description = status_data['description']
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name=f'🌐 {status_id}: {status_message}', value=f'{status_description}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid status code.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
