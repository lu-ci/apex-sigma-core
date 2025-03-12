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
from typing import Optional

import arrow
import discord
import markovify

from sigma.core.utilities.generic_responses import GenericResponse

collector_limit = 100_000
collector_loop_running = False
current_doc_collecting: Optional[dict] = None
current_cancel_request = False


async def collector_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global collector_loop_running
    if not collector_loop_running:
        collector_loop_running = True
        ev.bot.loop.create_task(collector_cycler(ev))


async def check_queued(db, aid, uid):
    """
    :type db: sigma.core.mechanics.database.Database
    :type aid: int
    :type uid: int
    :rtype: dict
    """
    target_doc = await db.col.CollectorQueue.find_one({'user_id': uid})
    author_doc = await db.col.CollectorQueue.find_one({'author_id': aid})
    target_in_queue = bool(target_doc)
    author_in_queue = bool(author_doc)
    in_current = current_doc_collecting.get('user_id') == uid if current_doc_collecting is not None else False
    result = {
        'queued': target_in_queue or author_in_queue or in_current,
        'target': target_in_queue,
        'author': author_in_queue,
        'document': current_doc_collecting if in_current else (target_doc or author_doc),
        'current': in_current
    }
    return result


async def add_to_queue(db, collector_item):
    """
    :type db: sigma.core.mechanics.database.Database
    :type collector_item: dict
    """
    await db.col.CollectorQueue.insert_one(collector_item)


async def get_queue_size(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: int
    """
    return await db.col.CollectorQueue.count_documents({})


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
    :type cltn: list
    """
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon.url) if tgt_chn.guild.icon else 'https://i.imgur.com/xpDpHqz.png'
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


async def notify_empty(ath, tgt_usr, tgt_chn):
    """
    :type ath: discord.User
    :type tgt_usr: discord.User
    :type tgt_chn: discord.TextChannel
    """
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon.url) if tgt_chn.guild.icon else 'https://i.imgur.com/xpDpHqz.png'
    response = GenericResponse(f'{req_usr.title()} did not have a chain and no new entries were found.').not_found()
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = GenericResponse(f'{tgt_usr.name} did not have a chain and no new entries were found.').not_found()
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
    guild_icon = str(tgt_chn.guild.icon.url) if tgt_chn.guild.icon else 'https://i.imgur.com/xpDpHqz.png'
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


async def notify_cancel(ath, tgt_usr, tgt_chn):
    """
    :type ath: discord.Member or discord.User
    :type tgt_usr: discord.Member or discord.User
    :type tgt_chn: discord.TextChannel
    """
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon.url) if tgt_chn.guild.icon else 'https://i.imgur.com/xpDpHqz.png'
    response = GenericResponse('Cancelled parsing entries for your chain.').error()
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = GenericResponse(f'Cancelled parsing entries for {tgt_usr.name}\'s chain.').error()
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


def get_current():
    return current_doc_collecting


def cancel_current():
    global current_cancel_request
    current_cancel_request = True


async def get_collected_ids(db, cid: int, uid: int) -> list[int]:
    col = db.col.CollectedMessages
    base = {
        'user_id': uid,
        'channel_id': cid,
    }
    doc = await col.find_one(base) or base
    return doc.get('collected', [])


async def update_collected_ids(db, cid: int, uid: int, collected_ids: list[int]):
    col = db.col.CollectedMessages
    base = {
        'user_id': uid,
        'channel_id': cid,
    }
    doc = await col.find_one(base) or base
    doc.update({'collected': collected_ids})
    await col.update_one({'user_id': uid}, {'$set': doc}, upsert=True)


async def collector_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global current_doc_collecting
    global current_cancel_request
    while True:
        if ev.bot.is_ready():
            now = arrow.utcnow().int_timestamp
            await ev.db.col.CollectorQueue.delete_many({'stamp': {'$lt': now - (60 * 60 * 24)}})
            cltr_items = await ev.db.col.CollectorQueue.find().to_list(None)
            for cltr_item in cltr_items:
                cl_usr = await ev.bot.get_user(cltr_item.get('user_id'))
                cl_chn = await ev.bot.get_channel(cltr_item.get('channel_id'))
                cl_ath = await ev.bot.get_user(cltr_item.get('author_id'))
                if cl_usr and cl_chn:
                    cancelled = False
                    usr_info = f'{cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]'
                    ev.log.info(f'Collecting a chain for {usr_info}...')
                    current_doc_collecting = cltr_item
                    await ev.db.col.CollectorQueue.delete_one(cltr_item)
                    collection = load(cl_usr.id)
                    chain = markovify.Text.from_dict(deserialize(collection)) if collection is not None else None
                    pfx = await ev.db.get_guild_settings(cl_chn.guild.id, 'prefix') or ev.bot.cfg.pref.prefix
                    messages = []
                    collected = await get_collected_ids(ev.db, cl_chn.id, cl_usr.id)
                    # noinspection PyBroadException
                    try:
                        async for log in cl_chn.history(limit=collector_limit):
                            if current_cancel_request:
                                cancelled = True
                                break
                            cnt = log.content
                            if log.id not in collected:
                                if log.author.id == cl_usr.id and len(log.content) > 8:
                                    if not check_for_bot_prefixes(pfx, cnt) and not check_for_bad_content(cnt):
                                        cnt = cleanse_content(log, cnt)
                                        if cnt not in messages and cnt and len(cnt) > 1:
                                            messages.append(cnt)
                                            collected.append(log.id)
                            else:
                                break
                        await update_collected_ids(ev.db, cl_chn.id, cl_usr.id, collected)
                    except Exception as e:
                        ev.log.warn(f'Collection issue for {usr_info}: {e}')
                    if not cancelled:
                        try:
                            new_chain = markovify.Text(f'{". ".join(messages)}.')
                            if new_chain.rejoined_text == '.':
                                combined = chain if chain else None
                            else:
                                combined = markovify.combine([chain, new_chain]) if chain else new_chain
                            if combined:
                                save(cl_usr.id, serialize(combined.to_dict()))
                                await notify_target(cl_ath, cl_usr, cl_chn, len(messages), combined.parsed_sentences)
                                stats = f'{len(messages)} / {len(combined.parsed_sentences)}'
                                ev.log.info(f'Collected a chain for {usr_info} ({stats}).')
                            else:
                                await notify_empty(cl_ath, cl_usr, cl_chn)
                                ev.log.warn(f'Collected an empty chain for {usr_info}.')
                        except Exception as e:
                            current_doc_collecting = None
                            current_cancel_request = False
                            await notify_failure(cl_ath, cl_usr, cl_chn)
                            ev.log.error(f"Markov generation failure for {cl_usr.id}: {e}")
                    else:
                        await notify_cancel(cl_ath, cl_usr, cl_chn)
                        ev.log.info(f'Collection cancelled for {usr_info}.')
                    current_doc_collecting = None
                    current_cancel_request = False
                # else:
                #     uid = cltr_item.get('user_id')
                #     cid = cltr_item.get('channel_id')
                #     aid = cltr_item.get('author_id')
                #     ev.log.warn(f'Couldn\'t find user {uid} or channel {cid} requested by {aid}.')
        await asyncio.sleep(1)
