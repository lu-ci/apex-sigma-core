import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

import arrow


async def clean_avatar(member):
    av_url = member.avatar_url or member.default_avatar
    av_url = av_url.split('?')[0]
    if member.avatar:
        if member.avatar.startswith('a_'):
            gif = True
        else:
            gif = False
    else:
        gif = False
    if gif:
        av_url = '.'.join(av_url.split('.')[:-1]) + '.gif'
    else:
        av_url = '.'.join(av_url.split('.')[:-1]) + '.png'
    return av_url


async def generate_member_data(member):
    if member:
        mem_data = {
            'Name': member.name,
            'Nickname': member.display_name,
            'Discriminator': member.discriminator,
            'UserID': member.id,
            'ServerID': member.guild.id,
            'Avatar': await clean_avatar(member),
            'Color': str(member.color)
        }
    else:
        mem_data = None
    return mem_data


async def push_to_database(ev, member_list):
    mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
    task = functools.partial(mem_coll.insert, member_list)
    with ThreadPoolExecutor() as threads:
        await ev.bot.loop.run_in_executor(threads, task)


async def user_data_fill(ev):
    ev.log.info('Filling member details...')
    start_stamp = arrow.utcnow().float_timestamp
    ev.bot.cool_down.set_cooldown(ev.name, 'member_details', 3600)
    mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
    mem_coll.drop()
    member_list = []
    for member in ev.bot.get_all_members():
        if member:
            mem_data = await generate_member_data(member)
            member_list.append(mem_data)
        if len(member_list) >= 500:
            await push_to_database(ev, member_list)
            member_list = []
            await asyncio.sleep(0.5)
    if member_list:
        await push_to_database(ev, member_list)
    end_stamp = arrow.utcnow().float_timestamp
    diff = round(end_stamp - start_stamp, 3)
    ev.log.info(f'Member detail filler finished in {diff}s.')
