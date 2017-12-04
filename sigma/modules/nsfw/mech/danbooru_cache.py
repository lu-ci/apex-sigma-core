import secrets
import json
import aiohttp

links = {}


async def get_dan_post(tag):
    file_url_base = 'https://danbooru.donmai.us'
    if tag not in links:
        need_filling = True
    else:
        if len(links[tag]) == 0:
            need_filling = True
        else:
            need_filling = False
    if need_filling:
        resource = 'https://danbooru.donmai.us/post/index.json?&tags=' + tag
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
                data = json.loads(data)
        temp_list = []
        for post in data:
            if 'file_url' in post:
                temp_list.append(post['file_url'])
        links.update({tag: temp_list})
    item_count = len(links[tag])
    if item_count:
        rand_num = secrets.randbelow(item_count)
        img_url = links[tag].pop(rand_num)
        full_url = file_url_base + img_url
    else:
        full_url = None
    return full_url
