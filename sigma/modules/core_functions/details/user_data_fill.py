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
    mem_data = {
        'Name': member.name,
        'Nickname': member.display_name,
        'Discriminator': member.discriminator,
        'UserID': member.id,
        'ServerID': member.guild.id,
        'Avatar': await clean_avatar(member),
        'Color': str(member.color)
    }
    return mem_data


async def user_data_fill(ev):
    ev.log.info('Filling member details...')
    threads = ThreadPoolExecutor(2)
    start_stamp = arrow.utcnow().float_timestamp
    ev.bot.cool_down.set_cooldown(ev.name, 'member_details', 3600)
    mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
    mem_coll.drop()
    for x in range(0, ev.bot.shard_count):
        shard_start = arrow.utcnow().float_timestamp
        member_list = []
        for guild in ev.bot.guilds:
            if guild.shard_id == x:
                for member in guild.members:
                    mem_data = await generate_member_data(member)
                    member_list.append(mem_data)
        task = functools.partial(mem_coll.insert, member_list)
        await ev.bot.loop.run_in_executor(threads, task)
        shard_end = arrow.utcnow().float_timestamp
        shard_diff = round(shard_end - shard_start, 3)
        ev.log.info(f'Filled Shard #{x} Members in {shard_diff}s.')
    end_stamp = arrow.utcnow().float_timestamp
    diff = round(end_stamp - start_stamp, 3)
    ev.log.info(f'Member detail filler finished in {diff}s.')
