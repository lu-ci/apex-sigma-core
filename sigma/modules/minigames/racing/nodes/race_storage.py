import copy
import secrets

races = {}

colors = {
    '🐶': 0xccd6dd,
    '🐱': 0xffcb4e,
    '🐭': 0x99aab5,
    '🐰': 0x99aab5,
    '🐙': 0x9266cc,
    '🐠': 0xffcc4d,
    '🦊': 0xf4900c,
    '🦀': 0xbe1931,
    '🐸': 0x77b255,
    '🐧': 0xf5f8fa,
    '🐻': 0xc1694f,
    '🐌': 0xaa8dd8,
    '🐍': 0x77b255,
    '🦄': 0x9266cc,
    '🦉': 0xc1694f,
    '🦋': 0x55acee,
    '🦍': 0x292f33,
    '🐦': 0xdd2e44,
    '🐯': 0xf9f9f9,
    '🦅': 0xf9f9f9
}

names = {
    '🐶': 'dog',
    '🐱': 'cat',
    '🐭': 'mouse',
    '🐰': 'rabbit',
    '🐙': 'octopus',
    '🐠': 'fish',
    '🦊': 'fox',
    '🦀': 'crab',
    '🐸': 'frog',
    '🐧': 'penguin',
    '🐻': 'bear',
    '🐌': 'snail',
    '🐍': 'snake',
    '🦄': 'unicorn',
    '🦉': 'owl',
    '🦋': 'butterfly',
    '🦍': 'gorilla',
    '🐦': 'bird',
    '🐯': 'tiger',
    '🦅': 'eagle'
}
participant_icons = ['🐶', '🐱', '🐭', '🐰', '🐙', '🐠', '🦊', '🦀', '🐸', '🐧',
                     '🐻', '🐌', '🐍', '🦄', '🦉', '🦋', '🦍', '🐦', '🐯', '🦅']


def make_race(channel_id, buyin):
    icon_copy = copy.deepcopy(participant_icons)
    race_data = {
        'icons': icon_copy,
        'users': [],
        'buyin': buyin
    }
    races.update({channel_id: race_data})


def add_participant(channel_id, user):
    race = races[channel_id]
    icons = race['icons']
    users = race['users']
    usr_icon = secrets.choice(icons)
    icons.remove(usr_icon)
    race.update({'icons': icons})
    participant_data = {
        'user': user,
        'icon': usr_icon
    }
    users.append(participant_data)
    race.update({'users': users})
    races.update({channel_id: race})
    return usr_icon
