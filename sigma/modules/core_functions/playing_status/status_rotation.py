import asyncio
import hashlib
import secrets

import discord

status_cache = []


def random_capitalize(text):
    new_text = ''
    char_list = list(text)
    while char_list:
        char_choice = char_list.pop(0)
        cap_roll = secrets.randbelow(2)
        if cap_roll == 0:
            char_choice = char_choice.upper()
        new_text += char_choice
    return new_text


async def status_rotation(ev):
    if ev.bot.cfg.pref.status_rotation:
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    while True:
        if ev.bot.cfg.pref.status_rotation:
            if not status_cache:
                status_files = ev.db[ev.db.db_cfg.database].StatusFiles.find()
                for status_file in status_files:
                    status_text = status_file.get('Text')
                    status_cache.append(status_text)
            if status_cache:
                status = status_cache.pop(secrets.randbelow(len(status_cache)))
                mode_roll = secrets.randbelow(3)
                if mode_roll == 0:
                    hashes = list(hashlib.algorithms_guaranteed)
                    hgen = hashlib.new(secrets.choice(hashes))
                    hgen.update(status.encode('utf-8'))
                    digest = hgen.hexdigest()
                    cut = secrets.randbelow(11)
                    cut_text = digest[cut:-(cut + 10)]
                    status = random_capitalize(cut_text)
                    sign_roll = secrets.randbelow(2)
                    if sign_roll:
                        status += '='
                game = discord.Game(name=status)
                try:
                    await ev.bot.change_presence(game=game)
                except discord.ConnectionClosed:
                    pass
        await asyncio.sleep(60)
