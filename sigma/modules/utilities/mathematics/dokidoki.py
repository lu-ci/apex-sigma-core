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

import secrets

import discord
import markovify

from sigma.modules.utilities.mathematics.nodes.encryption import get_encryptor

titles = {
    'n': 'People can try...',
    'y': 'I flicker back...',
    's': 'Happy thoughts...',
    'm': 'Cacophony of colors...'
}

title_glitches = {
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

char_glitches = {
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
    """
    :type text: str
    :type author: discord.Member
    :rtype: str
    """
    output = text.replace('{i}', '*')
    output = output.replace('{/i}', '*')
    output = output.replace('[player]', author.display_name)
    output = output.replace('[currentuser]', author.name)
    return output


async def dokidoki(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    char = None
    glitch = False
    if pld.args:
        if pld.args[0][0].lower() in files:
            char = pld.args[0][0].lower()
        if pld.args[-1].startswith(':g'):
            glitch = True
    if not char:
        char = secrets.choice(list(files))
    char_file = files[char]
    with open(f'doki/{char_file}.lc', 'r') as quote_file:
        ciphered = quote_file.read()
    if not glitch:
        glitch = secrets.randbelow(6)
        glitch = not bool(glitch)
    if glitch:
        line_count = 1
        thumbnail = char_glitches[char]
    else:
        line_count = 3
        thumbnail = secrets.choice(chars[char])
    lines = []
    for x in range(0, line_count):
        output = markovify.Text(ciphered).make_short_sentence(500, tries=100)
        output = clean(output, pld.msg.author)
        if glitch:
            cipher = get_encryptor(cmd.bot.cfg)
            if cipher:
                output = cipher.encrypt(output.encode('utf-8')).decode('utf-8')
        lines.append(output)
    output_final = ' '.join(lines)
    if glitch:
        title = title_glitches[char]
    else:
        title = titles[char]
    response = discord.Embed(color=0xe75a70)
    response.add_field(name=f'💟 {title}', value=output_final)
    response.set_thumbnail(url=thumbnail)
    await pld.msg.channel.send(embed=response)
