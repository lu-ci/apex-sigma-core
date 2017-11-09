import asyncio
import secrets

import discord

status_cache = []


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
                game = discord.Game(name=status)
                try:
                    await ev.bot.change_presence(game=game)
                except discord.ConnectionClosed:
                    pass
        await asyncio.sleep(180)
