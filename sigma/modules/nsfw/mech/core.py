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

import aiohttp
import secrets
from lxml import html


def e621_client(cache):
    """
    Returns an GalleryClient instance with E621 data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'e621_',
        'client_url': 'https://e621.net/post/index.json?tags=',
        'post_url': 'https://e621.net/post/show/',
        'icon_url': 'https://e621.net/favicon.ico',
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    }
    return GalleryClient(client_data, cache)


def gelbooru_client(cache):
    """
    Returns an GalleryClient instance with Gelbooru data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'gelbooru_',
        'client_url': 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'https://gelbooru.com/index.php?page=post&s=view&id=',
        'icon_url': 'https://gelbooru.com/favicon.png'
    }
    return GalleryClient(client_data, cache)


def konachan_client(cache):
    """
    Returns an GalleryClient instance with Konachan data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'konachan_',
        'client_url': 'https://konachan.com/post.json?limit=100&tags=',
        'post_url': 'http://konachan.com/post/show/',
        'icon_url': 'https://i.imgur.com/qc4awFL.png'
    }
    return GalleryClient(client_data, cache)


def rule34_client(cache):
    """
    Returns an GalleryClient instance with Rule 34 data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'rule34_',
        'client_url': 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'https://rule34.xxx/index.php?page=post&s=view&id=',
        'icon_url': 'https://i.imgur.com/63GGrmG.png'
    }
    return GalleryClient(client_data, cache)


def xbooru_client(cache):
    """
    Returns an GalleryClient instance with Xbooru data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': False,
        'cache_key': 'xbooru_',
        'client_url': 'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags=',
        'post_url': 'http://xbooru.com/index.php?page=post&s=view&id=',
        'icon_url': 'http://xbooru.com/apple-touch-icon-152x152-precomposed.png'
    }
    return GalleryClient(client_data, cache)


def yandere_client(cache):
    """
    Returns an GalleryClient instance with Yande.re data.
    :param cache: The cache configuration class.
    :type cache: sigma.core.mechanics.caching.Cacher
    :return:
    :rtype: sigma.modules.nsfw.mech.core.GalleryClient
    """
    client_data = {
        'as_json': True,
        'cache_key': 'yandere_',
        'client_url': 'https://yande.re/post.json?limit=100&tags=',
        'post_url': 'https://yande.re/post/show/',
        'icon_url': 'https://i.imgur.com/vgJwau2.png'
    }
    return GalleryClient(client_data, cache)


class GalleryClient(object):
    def __init__(self, client_data, cache):
        """
        :param client_data: The gallery client's data.
        :type client_data: dict
        :param cache: The cache configuration class.
        :type cache: sigma.core.mechanics.caching.Cacher
        """
        self.cache = cache
        self.as_json = client_data.get('as_json')
        self.cache_key = client_data.get('cache_key')
        self.client_url = client_data.get('client_url')
        self.post_url = client_data.get('post_url')
        self.icon_url = client_data.get('icon_url')
        self.headers = client_data.get('headers')
        self.tags = None

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
