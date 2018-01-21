import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand

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


async def eightball(cmd: SigmaCommand, message: discord.Message, args: list):
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
