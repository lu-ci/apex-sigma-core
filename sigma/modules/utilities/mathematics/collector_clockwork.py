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
import string

import discord
import markovify

from sigma.core.utilities.generic_responses import ok, error

collector_loop_running = False
current_user_collecting = None


async def check_queued(db, aid, uid):
    """

    :param db:
    :type db:
    :param aid:
    :type aid:
    :param uid:
    :type uid:
    :return:
    :rtype:
    """
    target_in_queue = bool(await db[db.db_nam].CollectorQueue.find_one({'user_id': uid}))
    author_in_queue = bool(await db[db.db_nam].CollectorQueue.find_one({'author_id': aid}))
    in_current = current_user_collecting == uid
    return target_in_queue or author_in_queue or in_current


async def add_to_queue(db, collector_item):
    """

    :param db:
    :type db:
    :param collector_item:
    :type collector_item:
    """
    await db[db.db_nam].CollectorQueue.insert_one(collector_item)


async def get_queue_size(db):
    """

    :param db:
    :type db:
    :return:
    :rtype:
    """
    return await db[db.db_nam].CollectorQueue.count_documents({})


def check_for_bot_prefixes(prefix, text):
    """

    :param prefix:
    :type prefix:
    :param text:
    :type text:
    :return:
    :rtype:
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

    :param msg:
    :type msg:
    :return:
    :rtype:
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

    :param msg:
    :type msg:
    :return:
    :rtype:
    """
    if msg.mentions:
        target_usr = msg.mentions[0]
    else:
        target_usr = msg.author
    return target_usr


def check_for_bad_content(text):
    """

    :param text:
    :type text:
    :return:
    :rtype:
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

    :param text:
    :type text:
    :return:
    :rtype:
    """
    disallowed = ['`', '\n', '\\', '\\n']
    for char in disallowed:
        text = text.replace(char, '')
    return text


def replace_mentions(log, text):
    """

    :param log:
    :type log:
    :param text:
    :type text:
    :return:
    :rtype:
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

    :param text:
    :type text:
    :return:
    :rtype:
    """
    text = text.strip()
    last_char = text[-1]
    if last_char not in string.punctuation:
        text += '.'
    return text


def cleanse_content(log, text):
    """

    :param log:
    :type log:
    :param text:
    :type text:
    :return:
    :rtype:
    """
    text = replace_mentions(log, text)
    text = clean_bad_chars(text)
    text = punctuate_content(text)
    return text


async def notify_target(ath, tgt_usr, tgt_chn, cltd, cltn):
    """

    :param ath:
    :type ath:
    :param tgt_usr:
    :type tgt_usr:
    :param tgt_chn:
    :type tgt_chn:
    :param cltd:
    :type cltd:
    :param cltn:
    :type cltn:
    """
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon_url) if tgt_chn.guild.icon_url else 'https://i.imgur.com/xpDpHqz.png'
    response = ok(f'Parsed {cltd} entries for your chain, {len(cltn)} corpus size.')
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = ok(f'Parsed {cltd} entries for {tgt_usr.name}\'s chain, {len(cltn)} corpus size.')
        req_resp.set_footer(text=footer, icon_url=guild_icon)
        # noinspection PyBroadException
        try:
            await ath.send(embed=req_resp)
        except Exception:
            pass


async def notify_failure(ath, tgt_usr, tgt_chn):
    """

    :param ath:
    :type ath:
    :param tgt_usr:
    :type tgt_usr:
    :param tgt_chn:
    :type tgt_chn:
    """
    desc = "This usually happens if there isn't enough data."
    desc += " Try targetting a channel where you talk frequently or have sent a lot of messages recently."
    req_usr = ('you' if ath.id == tgt_usr.id else ath.name) if ath else 'Unknown User'
    footer = f'Chain requested by {req_usr} in #{tgt_chn.name} on {tgt_chn.guild.name}.'
    guild_icon = str(tgt_chn.guild.icon_url) if tgt_chn.guild.icon_url else 'https://i.imgur.com/xpDpHqz.png'
    response = error('Failed to parse entries for your chain.')
    response.set_footer(text=footer, icon_url=guild_icon)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass
    if ath.id != tgt_usr.id:
        req_resp = error(f'Failed to parse entries for {tgt_usr.name}\'s chain.')
        req_resp.set_footer(text=footer, icon_url=guild_icon)
        # noinspection PyBroadException
        try:
            await ath.send(embed=req_resp)
        except Exception:
            pass


def serialize(item):
    """
    :type item: dict
    :rtype: str
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
    while True:
        if ev.bot.is_ready():
            cltr_items = await ev.db[ev.db.db_nam].CollectorQueue.find({}).to_list(None)
            for cltr_item in cltr_items:
                cl_usr = await ev.bot.get_user(cltr_item.get('user_id'))
                cl_chn = await ev.bot.get_channel(cltr_item.get('channel_id'))
                cl_ath = await ev.bot.get_user(cltr_item.get('author_id'))
                if cl_usr and cl_chn:
                    await ev.db[ev.db.db_nam].CollectorQueue.delete_one(cltr_item)
                    current_user_collecting = cl_usr.id
                    collection = await ev.db[ev.db.db_nam].MarkovChains.find_one({'user_id': cl_usr.id})
                    collection = collection.get('chain') if collection else None
                    chain = markovify.Text.from_dict(deserialize(collection)) if collection is not None else None
                    messages = []
                    pfx = await ev.db.get_guild_settings(cl_chn.guild.id, 'prefix') or ev.bot.cfg.pref.prefix
                    # noinspection PyBroadException
                    try:
                        async for log in cl_chn.history(limit=100000):
                            cnt = log.content
                            if log.author.id == cl_usr.id and len(log.content) > 8:
                                if not check_for_bot_prefixes(pfx, cnt) and not check_for_bad_content(cnt):
                                    cnt = cleanse_content(log, cnt)
                                    if cnt not in messages and cnt and len(cnt) > 1:
                                        messages.append(cnt)
                                        if len(messages) >= 5000:
                                            break
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        new_chain = markovify.Text(f'{". ".join(messages)}.')
                        combined = markovify.combine([chain, new_chain]) if chain else new_chain
                        insert_data = {'user_id': cl_usr.id, 'chain': serialize(combined.to_dict())}
                        await ev.db[ev.db.db_nam].MarkovChains.delete_one({'user_id': cl_usr.id})
                        await ev.db[ev.db.db_nam].MarkovChains.insert_one(insert_data)
                        await notify_target(cl_ath, cl_usr, cl_chn, len(messages), combined.parsed_sentences)
                        current_user_collecting = None
                        ev.log.info(f'Collected a chain for {cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]')
                    except Exception as e:
                        await notify_failure(cl_ath, cl_usr, cl_chn)
                        ev.log.error(f"Markov generation failure for {cl_usr.id}: {e}.")
        await asyncio.sleep(1)
