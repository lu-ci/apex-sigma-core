import secrets

import discord
import markovify
from cryptography.fernet import Fernet, InvalidToken

from sigma.core.mechanics.command import SigmaCommand

titles = {
    'n': 'People can try...',
    'y': 'I flicker back...',
    's': 'Happy thoughts...',
    'm': 'Cacophony of colors...'
}

titles_glitch = {
    'm': 'Flash ng, exp nd ng, piercing...',
    'y': 'Slipping cogwheels...',
    's': 'It just stops moving...',
    'n': 'Because you, because you...'
}

chars = {
    'n': [
        'https://i.imgur.com/Xr19wxI.png',
        'https://i.imgur.com/RnyKBBn.png'
    ],
    'y': [
        'https://i.imgur.com/isyOw8Y.png',
        'https://i.imgur.com/0bbIGq4.png'
    ],
    's': [
        'https://i.imgur.com/SxnYDHH.png',
        'https://i.imgur.com/cQWGAul.png'
    ],
    'm': [
        'https://i.imgur.com/wJazxfj.png',
        'https://i.imgur.com/6qqfqC7.png'
    ]
}

chars_glitch = {
    'm': 'https://i.imgur.com/im1H8jA.png',
    'n': 'https://i.imgur.com/J65D1Di.png',
    'y': 'https://i.imgur.com/0b3fthJ.png',
    's': 'https://i.imgur.com/IM9fHVL.png'
}

files = {
    'm': 'just_monika',
    'y': 'blade_flicker',
    's': 'happy_thoughts',
    'n': 'family_values'
}


def clean(text, author):
    output = text.replace('{i}', '*')
    output = output.replace('{/i}', '*')
    output = output.replace('[player]', author.display_name)
    output = output.replace('[currentuser]', author.name)
    return output


async def dokidoki(cmd: SigmaCommand, message: discord.Message, args: list):
    char = None
    glitch = False
    if args:
        if args[0][0].lower() in files:
            char = args[0][0].lower()
        if args[-1].startswith(':g'):
            glitch = True
    if not char:
        char = secrets.choice(list(files))
    char_file = files[char]
    with open(f'doki/{char_file}.luci', 'rb') as quote_file:
        quotes = quote_file.read()
    key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
    if key:
        key = key.encode('utf-8')
        cipher = Fernet(key)
        try:
            ciphered = cipher.decrypt(quotes).decode('utf-8')
        except InvalidToken:
            ciphered = None
        if ciphered:
            if not glitch:
                glitch = secrets.randbelow(6)
                glitch = not bool(glitch)
            if glitch:
                line_count = 1
                thumbnail = chars_glitch[char]
            else:
                line_count = 3
                thumbnail = secrets.choice(chars[char])
            lines = []
            for x in range(0, line_count):
                output = markovify.Text(ciphered).make_short_sentence(500, tries=100)
                output = clean(output, message.author)
                if glitch:
                    output = cipher.encrypt(output.encode('utf-8')).decode('utf-8')
                lines.append(output)
            output_final = ' '.join(lines)
            if glitch:
                title = titles_glitch[char]
            else:
                title = titles[char]
            response = discord.Embed(color=0xe75a70)
            response.add_field(name=f'💟 {title}', value=output_final)
            response.set_thumbnail(url=thumbnail)
        else:
            response = discord.Embed(color=0xe75a70, title='💔 Sorry but that key is incorrect!')
    else:
        response = discord.Embed(color=0xe75a70, title='💔 You are missing the key to my heart!')
    await message.channel.send(embed=response)
