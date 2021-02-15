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

import asyncio
import gzip
import json
import os
import string

import arrow
import discord
import markovify

from sigma.core.utilities.generic_responses import GenericResponse

collector_loop_running = False
current_user_collecting = None


async def check_queued(db, aid, uid):
    """
    :type db: sigma.core.mechanics.database.Database
    :type aid: int
    :type uid: int
    :rtype: bool
    """
    target_in_queue = bool(await db[db.db_nam].CollectorQueue.find_one({'user_id': uid}))
    author_in_queue = bool(await db[db.db_nam].CollectorQueue.find_one({'author_id': aid}))
    in_current = current_user_collecting == uid
    return target_in_queue or author_in_queue or in_current


async def add_to_queue(db, collector_item):
    """
    :type db: sigma.core.mechanics.database.Database
    :type collector_item: dict
    """
    await db[db.db_nam].CollectorQueue.insert_one(collector_item)


async def get_queue_size(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: int
    """
    return await db[db.db_nam].CollectorQueue.count_documents({})


def check_for_bot_prefixes(prefix, text):
    """
    :type prefix: str
    :type text: str
    :rtype: bool
    """
    common_pfx = [prefix, '!', '/', '\\', '~', '.', '>', '<', '-', '_', '?']
    prefixed = False
    for pfx in common_pfx:
        if text.startswith(pfx):
            prefixed = True
            break
    return prefixed


def get_channel(msg):
    """
    :type msg: discord.Message
    :rtype: discord.TextChannel
    """
    target_chn = msg.channel
    if msg.channel_mentions:
        for tcn in msg.channel_mentions:
            if isinstance(tcn, discord.TextChannel):
                target_chn = tcn
                break
    return target_chn


def get_target(msg):
    """
    :type msg: discord.Message
    :rtype: discord.Member or discord.User
    """
    if msg.mentions:
        target_usr = msg.mentions[0]
    else:
        target_usr = msg.author
    return target_usr


def check_for_bad_content(text):
    """
    :type text: str
    :rtype: bool
    """
    disallowed = ['```', 'http', '"', ':gw']
    bad = False
    for cont in disallowed:
        if cont in text or cont in text.lower():
            bad = True
            break
    return bad


def clean_bad_chars(text):
    """
    :type text: str
    :rtype: str
    """
    disallowed = ['`', '\n', '\\', '\\n']
    for char in disallowed:
        text = text.replace(char, '')
    return text


def replace_mentions(log, text):
    """
    :type log: discord.Message
    :type text: str
    :rtype: str
    """
    if log.mentions:
        for mention in log.mentions:
            text = text.replace(mention.mention, mention.name)
    if log.channel_mentions:
        for mention in log.channel_mentions:
            text = text.replace(mention.mention, mention.name)
    return text


def punctuate_content(text):
    """
    :type text: str
    :rtype: str
    """
    text = text.strip()
    last_char = text[-1]
    if last_char not in string.punctuation:
        text += '.'
    return text


def cleanse_content(log, text):
    """
    :type log: discord.Message
    :type text: str
    :rtype: str
    """
    text = replace_mentions(log, text)
    text = clean_bad_chars(text)
    text = punctuate_content(text)
    return text


async def notify_target(ath, tgt_usr, tgt_chn, cltd, cltn):
    """
    :type ath: discord.User
    :type tgt_usr: discord.User
    :type tgt_chn: discord.TextChannel
    :type cltd: int
    :type cltn: list[str]
    """
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon_url) if tgt_chn.guild.icon_url else 'https://i.imgur.com/xpDpHqz.png'
    response = GenericResponse(f'Parsed {cltd} entries for your chain, {len(cltn)} corpus size.').ok()
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = GenericResponse(f'Parsed {cltd} entries for {tgt_usr.name}\'s chain, {len(cltn)} corpus size.').ok()
        req_resp.set_footer(text=footer, icon_url=guild_icon)
        # noinspection PyBroadException
        try:
            await ath.send(embed=req_resp)
        except Exception:
            pass


async def notify_failure(ath, tgt_usr, tgt_chn):
    """
    :type ath: discord.Member or discord.User
    :type tgt_usr: discord.Member or discord.User
    :type tgt_chn: discord.TextChannel
    """
    desc = "This usually happens if there isn't enough data."
    desc += " Try targeting a channel where you talk frequently or have sent a lot of messages recently."
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon_url) if tgt_chn.guild.icon_url else 'https://i.imgur.com/xpDpHqz.png'
    response = GenericResponse('Failed to parse entries for your chain.').error()
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = GenericResponse(f'Failed to parse entries for {tgt_usr.name}\'s chain.').error()
        req_resp.set_footer(text=footer, icon_url=guild_icon)
        # noinspection PyBroadException
        try:
            await ath.send(embed=req_resp)
        except Exception:
            pass


def serialize(item):
    """
    :type item: dict
    :rtype: bytes
    """
    as_str = json.dumps(item)
    as_comp = gzip.compress(as_str.encode('utf-8'))
    return as_comp


def deserialize(item):
    """
    :type item: io.BytesIO
    :rtype: dict
    """
    as_decomp = gzip.decompress(item)
    as_str = json.loads(as_decomp.decode('utf-8'))
    return as_str


def load(uid):
    """
    :type uid: int
    :rtype: io.BytesIO
    """
    data = None
    fdir = 'chains'
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    fname = f'{fdir}/{uid}.json.gz'
    if os.path.exists(fname):
        with open(fname, 'rb') as out_file:
            data = out_file.read()
    return data


def save(uid, data):
    """
    :type uid: int
    :type data: bytes
    """
    fdir = 'chains'
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    fname = f'{fdir}/{uid}.json.gz'
    with open(fname, 'wb') as out_file:
        out_file.write(data)


async def collector_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global collector_loop_running
    if not collector_loop_running:
        collector_loop_running = True
        ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global current_user_collecting
    coll = ev.db[ev.db.db_nam].CollectorQueue
    while True:
        if ev.bot.is_ready():
            now = arrow.utcnow().int_timestamp
            await coll.delete_many({'stamp': {'$lt': now - 3600}})
            cltr_items = await coll.find({}).to_list(None)
            for cltr_item in cltr_items:
                cl_usr = await ev.bot.get_user(cltr_item.get('user_id'))
                cl_chn = await ev.bot.get_channel(cltr_item.get('channel_id'))
                cl_ath = await ev.bot.get_user(cltr_item.get('author_id'))
                if cl_usr and cl_chn:
                    ev.log.info(f'Collecting a chain for {cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]...')
                    await coll.delete_one(cltr_item)
                    current_user_collecting = cl_usr.id
                    collection = load(cl_usr.id)
                    chain = markovify.Text.from_dict(deserialize(collection)) if collection is not None else None
                    messages = []
                    pfx = await ev.db.get_guild_settings(cl_chn.guild.id, 'prefix') or ev.bot.cfg.pref.prefix
                    # noinspection PyBroadException
                    try:
                        async for log in cl_chn.history(limit=100_000):
                            cnt = log.content
                            if log.author.id == cl_usr.id and len(log.content) > 8:
                                if not check_for_bot_prefixes(pfx, cnt) and not check_for_bad_content(cnt):
                                    cnt = cleanse_content(log, cnt)
                                    if cnt not in messages and cnt and len(cnt) > 1:
                                        messages.append(cnt)
                    except Exception as e:
                        ev.log.warn(f'Collection issue for {cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]: {e}')
                    try:
                        new_chain = markovify.Text(f'{". ".join(messages)}.')
                        combined = markovify.combine([chain, new_chain]) if chain else new_chain
                        save(cl_usr.id, serialize(combined.to_dict()))
                        await notify_target(cl_ath, cl_usr, cl_chn, len(messages), combined.parsed_sentences)
                        ev.log.info(f'Collected a chain for {cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]')
                    except Exception as e:
                        await notify_failure(cl_ath, cl_usr, cl_chn)
                        ev.log.error(f"Markov generation failure for {cl_usr.id}: {e}.")
                    current_user_collecting = None
        await asyncio.sleep(1)
