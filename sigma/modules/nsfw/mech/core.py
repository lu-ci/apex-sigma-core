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

import json
import secrets

import aiohttp
from lxml import html


def danbooru_client(cache, user_agent):
    """
    Returns an GalleryClient instance with E621 data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'danbooru_',
        'client_url': 'https://danbooru.donmai.us/posts.json?tags=',
        'post_url': 'https://danbooru.donmai.us/posts/',
        'icon_url': 'https://i.imgur.com/ytMyEyr.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def e621_client(cache, user_agent):
    """
    Returns an GalleryClient instance with E621 data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'e621_',
        'client_url': 'https://e621.net/posts.json?tags=',
        'post_url': 'https://e621.net/post/show/',
        'icon_url': 'https://i.imgur.com/UveWhWm.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def gelbooru_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Gelbooru data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'gelbooru_',
        'client_url': 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'https://gelbooru.com/index.php?page=post&s=view&id=',
        'icon_url': 'https://i.imgur.com/dr1bUWK.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def konachan_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Konachan data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'konachan_',
        'client_url': 'https://konachan.com/post.json?limit=100&tags=',
        'post_url': 'http://konachan.com/post/show/',
        'icon_url': 'https://i.imgur.com/utGEFiD.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def rule34_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Rule 34 data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'rule34_',
        'client_url': 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'https://rule34.xxx/index.php?page=post&s=view&id=',
        'icon_url': 'https://i.imgur.com/GrEg8Oz.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def xbooru_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Xbooru data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'xbooru_',
        'client_url': 'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'http://xbooru.com/index.php?page=post&s=view&id=',
        'icon_url': 'https://i.imgur.com/mBuaF9Y.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def yandere_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Yande.re data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :param user_agent: The core client's user agent.
    :type user_agent: dict
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'yandere_',
        'client_url': 'https://yande.re/post.json?limit=100&tags=',
        'post_url': 'https://yande.re/post/show/',
        'icon_url': 'https://i.imgur.com/CxshkK8.png'
    }
    return GalleryClient(client_data, cache, user_agent)


class GalleryClient(object):
    def __init__(self, client_data, cache, user_agent):
        """
        :param client_data: The gallery client's data.
        :type client_data: dict
        :param cache: The cache configuration class.
        :type cache: sigma.core.mechanics.caching.Cacher
        :param user_agent: The core client's user agent.
        :type user_agent: dict
        """
        self.cache = cache
        self.as_json = client_data.get('as_json')
        self.cache_key = client_data.get('cache_key')
        self.client_url = client_data.get('client_url')
        self.post_url = client_data.get('post_url')
        self.icon_url = client_data.get('icon_url')
        self.headers = user_agent
        self.tags = None

    @staticmethod
    def remove_lines_breaks(tags):
        """
        Removes line breaks from a list of tags.
        :param tags: The list of tags to parse
        :type tags: list[str]
        :return:
        :rtype: list[str]
        """
        new_tags = []
        for tag in tags:
            new_tags.extend(tag.split('\n'))
        return new_tags

    async def _get_posts(self):
        """
        Fetches posts from the client.
        :return:
        :rtype: list[dict]
        """
        async with aiohttp.ClientSession() as aio_client:
            async with aio_client.get(self.client_url + self.tags, headers=self.headers) as aio_session:
                data = await aio_session.read()
                if self.as_json:
                    try:
                        posts = json.loads(data)
                    except json.JSONDecodeError:
                        posts = []
                else:
                    posts = html.fromstring(data)
        return self._filter_posts(posts)

    def _filter_posts(self, posts):
        """
        Filters posts based on if they include a file_url field.
        :param posts: The posts to filter.
        :type posts: dict or list[lxml.html.HtmlElement]
        :return:
        :rtype: list[dict]
        """
        if self.as_json:
            if self.cache_key.startswith('e621_'):
                posts = posts.get('posts')
                posts = [ps for ps in posts if ps.get('file').get('url')]
            else:
                posts = [ps for ps in posts if ps.get('file_url')]
        else:
            posts = [dict(ps.attrib) for ps in posts if ps.attrib.get('file_url')]
        return posts

    async def randpost(self, tags):
        """
        Fetches a random post from the client.
        :param tags: The tags to search for.
        :type tags: list[str]
        :return:
        :rtype: dict
        """
        sorted_tags = sorted([tag.lower() for tag in tags])
        self.tags = '+'.join(sorted_tags) if tags else 'nude'
        self.cache_key += self.tags
        posts = await self.cache.get_cache(self.cache_key)
        if not posts:
            posts = await self._get_posts()
            await self.cache.set_cache(self.cache_key, posts)
        return secrets.choice(posts) if posts else None
