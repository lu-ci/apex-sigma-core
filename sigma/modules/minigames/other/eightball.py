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
import secrets

import discord

positive = [
    'Absolutely.',
    'I am certain that that\'s a yes.',
    'Of course.',
    'Yes.',
    'No shit Sherlock.',
    'Is water wet?',
    'Maybe, probably, certainly, yeah.',
    'Yup.',
    'Yeah.',
    'For sure.',
    'Undoubtedly.',
    '100% Certainty.',
    'This is an absolute.',
    'True enough.',
    'True.',
    'Senpai says yes.',
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes. Definitely.',
    'You may rely on it.',
    'I find it highly plausible.',
    'Most likely.',
    'Outlook good.'
]

neural = [
    'I\'m not sure.',
    'Ask me later.',
    'I can\'t say for certain.',
    'I don\'t have enough data.',
    'I\'m on a break, ask again later.',
    'Too tired, ask me after a nap.',
    'Too lazy to calculate now.',
    'Maybe, I\'m not really sure.',
    'Ughhhh... Not sure...',
    'Lunch time, piss off and ask me later.',
    'Senpai failed to notice your question.',
    'Is that even a valid question?',
    'I am drawing a blank.'
]

negative = [
    'No.',
    'Nope.',
    'Nu-uh.',
    'Negative.',
    'False.',
    'That would be a no.',
    'Sorry, that\'s a negative.',
    'Nothing like that.',
    'Not how it goes.',
    'Nah bro, ain\'t nothing like that.',
    'Senpai says no.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]


async def eightball(cmd, message, args):
    if args:
        roll = secrets.randbelow(4)
        if roll == 0:
            answers = negative
        elif roll == 1:
            answers = neural
        else:
            answers = positive
        answer = secrets.choice(answers)
        response = discord.Embed(color=0x232323, title=f'🎱 {answer}')
    else:
        response = discord.Embed(color=0x696969, title='❔ No question was asked.')
    await message.channel.send(embed=response)
