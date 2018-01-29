# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
import secrets

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
