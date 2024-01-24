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


def safebooru_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Safebooru data.
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
    """
    client_data = {
        'cache_key': 'safebooru_',
        'client_url': 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=rating:safe+',
        'post_url': 'http://safebooru.org/index.php?page=post&s=view&id=',
        'icon_url': 'https://i.imgur.com/vEJ67ko.png'
    }
    return GalleryClient(client_data, cache, user_agent)


def danbooru_client(cache, user_agent):
    """
    Returns an GalleryClient instance with Danbooru data.
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
    :type cache: sigma.core.mechanics.caching.Cacher
    :type user_agent: dict
    :rtype: GalleryClient
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
        :type client_data: dict
        :type cache: sigma.core.mechanics.caching.Cacher
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
        :type tags: list
        :rtype: list
        """
        new_tags = []
        for tag in tags:
            new_tags.extend(tag.split('\n'))
        return new_tags

    @staticmethod
    def xml_to_json(root):
        posts = []
        for post in root:
            _post = {}
            for elem in post.getchildren():
                _post.update({elem.tag: elem.text})
            posts.append(_post)
        return posts

    async def _get_posts(self):
        """
        Fetches posts from the client.
        :rtype: list
        """
        async with aiohttp.ClientSession() as aio_client:
            async with aio_client.get(self.client_url + self.tags, headers=self.headers) as aio_session:
                data = await aio_session.read()
                if self.as_json:
                    try:
                        posts = json.loads(data)
                    except json.JSONDecodeError:
                        posts = {}
                else:
                    posts = html.fromstring(data)
        return self._ensure_source(posts)

    def _ensure_source(self, posts):
        """
        Filters posts based on if they include a file_url field.
        :type posts: dict or list
        :rtype: list
        """
        if self.as_json:
            if self.cache_key.startswith('e621_'):
                posts = posts.get('posts')
                posts = [ps for ps in posts if ps.get('file').get('url')]
            else:
                posts = [ps for ps in posts if ps.get('file_url')]
        else:
            if self.cache_key.startswith('gelbooru_'):
                posts = [ps for ps in self.xml_to_json(posts) if ps.get('file_url')]
            else:
                posts = [dict(ps.attrib) for ps in posts if ps.attrib.get('file_url')]
        return self._ensure_size(posts)

    def _ensure_size(self, posts):
        """
        Filters posts based on their dimensions.
        :type posts: dict or list
        :rtype: list
        """
        valid_posts = []
        for post in posts:
            if self.cache_key.startswith('e621_'):
                file = post.get('file')
                width, height = file.get('width'), file.get('height')
            elif self.cache_key.startswith('danbooru_'):
                width, height = post.get('image_width'), post.get('image_height')
            else:
                width, height = post.get('width'), post.get('height')
            if int(width) <= 2000 and int(height) <= 2000:
                valid_posts.append(post)
        return valid_posts

    async def randpost(self, tags, return_all=False):
        """
        Fetches a random post from the client.
        :type tags: list
        :type return_all: bool
        :rtype: dict
        """
        sorted_tags = sorted([tag.lower() for tag in tags])
        self.tags = '+'.join(sorted_tags) if tags else 'nude'
        self.cache_key += self.tags
        posts = await self.cache.get_cache(self.cache_key)
        if not posts:
            posts = await self._get_posts()
            await self.cache.set_cache(self.cache_key, posts)
        if return_all:
            return posts
        return secrets.choice(posts) if posts else None
