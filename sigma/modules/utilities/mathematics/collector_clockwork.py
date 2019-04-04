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
import string

from sigma.core.utilities.generic_responses import ok

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
    if msg.channel_mentions:
        target_chn = msg.channel_mentions[0]
    else:
        target_chn = msg.channel
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
    ftr_icn = tgt_chn.guild.icon_url or 'https://i.imgur.com/xpDpHqz.png'
    response = ok(f'Added {cltd} entries to your chain, {len(cltn)} entries total.')
    response.set_footer(text=footer, icon_url=ftr_icn)
    # noinspection PyBroadException
    try:
        await tgt_usr.send(embed=response)
    except Exception:
        pass


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
                    collected = 0
                    collection = await ev.db[ev.db.db_nam].MarkovChains.find_one({'user_id': cl_usr.id})
                    collection = collection.get('chain') if collection else []
                    pfx = await ev.db.get_guild_settings(cl_chn.guild.id, 'prefix') or ev.bot.cfg.pref.prefix
                    # noinspection PyBroadException
                    try:
                        async for log in cl_chn.history(limit=100000):
                            cnt = log.content
                            if log.author.id == cl_usr.id and len(log.content) > 8:
                                if not check_for_bot_prefixes(pfx, cnt) and not check_for_bad_content(cnt):
                                    cnt = cleanse_content(log, cnt)
                                    if cnt not in collection:
                                        collection.append(cnt)
                                        collected += 1
                                        if collected >= 5000:
                                            break
                    except Exception:
                        pass
                    insert_data = {'user_id': cl_usr.id, 'chain': collection}
                    await ev.db[ev.db.db_nam].MarkovChains.delete_one({'user_id': cl_usr.id})
                    await ev.db[ev.db.db_nam].MarkovChains.insert_one(insert_data)
                    await ev.db.cache.del_cache(cl_usr.id)
                    await notify_target(cl_ath, cl_usr, cl_chn, collected, collection)
                    current_user_collecting = None
                    ev.log.info(f'Collected a chain for {cl_usr.name}#{cl_usr.discriminator} [{cl_usr.id}]')
        await asyncio.sleep(1)
