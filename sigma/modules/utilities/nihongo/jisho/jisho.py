from sigma.core.mechanics.command import SigmaCommand
import json

import aiohttp
import discord


async def jisho(cmd: SigmaCommand, message: discord.Message, args: list):
    jisho_q = ' '.join(args)

    async with aiohttp.ClientSession() as session:
        async with session.get('http://jisho.org/api/v1/search/words?keyword=' + jisho_q) as data:
            rq_text = await data.text()
            rq_data = await data.read()
            rq_json = json.loads(rq_data)

    if rq_text.find('503 Service Unavailable') != -1:
        embed_content = discord.Embed(title='❗ Jisho responded with 503 Service Unavailable.',
                                      color=0xDB0000)
        await message.channel.send(None, embed=embed_content)
        return

    request = rq_json

    # check if response contains data or nothing was found
    if request['data']:
        request = request['data'][0]
    else:
        embed_content = discord.Embed(title="Sorry, couldn't find anything matching `{}`".format(jisho_q),
                                      color=0xDB0000)
        await message.channel.send(None, embed=embed_content)
        return

    output = ''
    starter = ''
    # if the word doesn't have kanji, print out the kana alone
    try:
        starter += "{} [{}]".format(request['japanese'][0]['word'], request['japanese'][0]['reading'])
    except KeyError:
        starter += "{}".format(request['japanese'][0]['reading'])

    wk_lvls = []

    for tag in request['tags']:
        if tag.find('wanikani') != -1:
            wk_lvls.append(tag[8:])

    if len(request['senses']) > 5:
        definitons_len = 5
    else:
        definitons_len = len(request['senses'])

    for i in range(0, definitons_len):
        etc = []
        if 'english_definitions' in request['senses'][i]:
            output += '\n{}. {}'.format(i + 1, '; '.join(request['senses'][i]['english_definitions']))
        if request['senses'][i]['parts_of_speech']:
            parts_of_speech = ''
            for part_of_speech in request['senses'][i]['parts_of_speech']:
                if part_of_speech:
                    parts_of_speech += part_of_speech + ', '
            etc.append(parts_of_speech[:-2])

        if request['senses'][i]['tags']:
            try:
                etc.append('; '.join(request['senses'][i]['tags']))
            except IndexError:
                pass
            except KeyError:
                pass
        if request['senses'][i]['see_also']:
            etc.append('See also {}'.format(', '.join(request['senses'][i]['see_also'])))

        if request['senses'][i]['info']:
            etc.append('; '.join(request['senses'][i]['info']))

        # attaching definition tags
        if etc:
            if etc[0]:
                etc_string = ', '.join(etc)
                output += f'\n| *{etc_string}*'

    if len(request['senses']) > 5:
        hidden = len(request['senses']) - 5
        if hidden == 1:
            output += '\n\n- {} definition is hidden'.format(hidden)
        else:
            output += '\n\n- {} definitions are hidden'.format(hidden)

    other_forms = ''
    if len(request['japanese']) > 1:
        other_forms = ''
        for i in range(1, len(request['japanese'])):
            if 'word' in request['japanese'][i]:
                other_forms += request['japanese'][i]['word'] + '、'
    search_url = f'http://jisho.org/search/{jisho_q}'
    jisho_icon = 'https://i.imgur.com/X1fCJLV.png'
    embed = discord.Embed(color=0xF9F9F9)
    embed.set_author(name='Jisho.org', url=search_url, icon_url=jisho_icon)
    embed.add_field(name=f'{starter}', value=output)
    if other_forms:
        footer_text = f'Other forms: {other_forms[:-1]}'
        if request['is_common']:
            footer_text += ' | Common Word'
        if wk_lvls:
            footer_text += ' | Wanikani Level {}'.format(', '.join(wk_lvls))
        embed.set_footer(text=footer_text)
    await message.channel.send(None, embed=embed)
