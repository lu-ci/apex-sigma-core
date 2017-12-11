import functools
import secrets
from concurrent.futures import ThreadPoolExecutor

import discord
import markovify
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature

files = {
    'm': 'just_monika',
    'y': 'blade_flicker',
    's': 'happy_thoughts',
    'n': 'family_values'
}


def get_file_data(file_name, key):
    key = key.encode('utf-8')
    cipher = Fernet(key)
    with open(f'doki/{file_name}.luci', 'rb') as quote_file:
        quotes = quote_file.read()
    try:
        string_out = cipher.decrypt(quotes).decode('utf-8')
    except (InvalidToken, InvalidSignature):
        string_out = None
    return string_out


def get_char_file(args):
    if args:
        char_qry = args[-1].lower()
        if char_qry[0] in files:
            quote_files = files.get(char_qry[0])
        else:
            quote_files = files.get(secrets.choice(list(files)))
    else:
        quote_files = files.get(secrets.choice(list(files)))
    return quote_files


async def generate_chains(loop, string_list):
    chain_list = []
    for string_coll in string_list:
        with ThreadPoolExecutor() as threads:
            chain_task = functools.partial(markovify.Text, string_coll)
            chain_data = await loop.run_in_executor(threads, chain_task)
            chain_list.append(chain_data)
    return chain_list


def glitch_name(name):
    out_name = ''
    non_unicode = '¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿'
    for char in name:
        glitch_roll = secrets.randbelow(5)
        if glitch_roll == 0:
            add_char = secrets.choice(non_unicode)
        else:
            add_char = char
        out_name += add_char
    return out_name


async def dokidokimix(cmd, message, args):
    key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
    if key:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
        target_chain = await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target.id})
        if target_chain:
            if target_chain['Chain']:
                quote_file = get_char_file(args)
                string_list = [get_file_data(quote_file, key)]
                if string_list is not None:
                    user_string = ' '.join(target_chain['Chain'])
                    string_list.append(user_string)
                    chain_collection = await generate_chains(cmd.bot.loop, string_list)
                    disposition = [1.5, 0.5]
                    combine_task = functools.partial(markovify.combine, chain_collection, disposition)
                    sentences = []
                    with ThreadPoolExecutor() as threads:
                        combination = await cmd.bot.loop.run_in_executor(threads, combine_task)
                        sentence_function = functools.partial(combination.make_short_sentence, 500)
                        while len(sentences) < 3:
                            sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                            if sentence:
                                sentences.append(sentence)
                            else:
                                break
                    if sentences:
                        g_nam = glitch_name(target.name)
                        response = discord.Embed(color=0xE75A70, title=f'💟 {g_nam}')
                        response.description = '. '.join(sentences)
                    else:
                        response = discord.Embed(color=0xBE1931, title='😖 I could not think of anything...')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ A decryption error occurred, check the key.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ {target.name}\'s chain has no data.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {target.name} doesn\'t have a chain.')
    else:
        response = discord.Embed(color=0xe75a70, title='💔 You are missing the key to my heart!')
    await message.channel.send(embed=response)
