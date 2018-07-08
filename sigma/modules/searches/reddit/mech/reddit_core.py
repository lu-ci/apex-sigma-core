# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import aiohttp
import arrow

reddit_base = 'https://www.reddit.com/r'
reddit_auth = 'https://www.reddit.com/api/v1/access_token?grant_type=client_credentials'


class RedditPost(object):
    def __init__(self, data: dict):
        self.raw = data
        for key in self.raw:
            setattr(self, key, self.raw.get(key))


class RedditSub(object):
    def __init__(self, data: dict):
        self.private = data.get('reason') == 'private'
        self.banned = data.get('reason') == 'banned'
        self.raw = data.get('data', {})
        if not self.private and not self.banned:
            for key in self.raw:
                setattr(self, key, self.raw.get(key))


class RedditClient(object):
    def __init__(self, client_id: str, client_secret: str, bot_client_id: int):
        self.headers = {'User-Agent': f'Apex Sigma Derivate {bot_client_id}'}
        self.authorization = aiohttp.BasicAuth(client_id, client_secret)
        self.token = None
        self.expires = 0

    async def boot(self):
        no_token = self.token is None
        expired = self.expires <= arrow.utcnow().timestamp
        if no_token or expired:
            await self.__create()

    async def __create(self):
        async with aiohttp.ClientSession() as session:
            response = await session.post(reddit_auth, auth=self.authorization, headers=self.headers)
            login_data = json.loads(await response.read())
            self.token = login_data.get('token')
            self.expires = arrow.utcnow().timestamp + login_data.get('expires_in')

    async def __get_data(self, url: str):
        await self.boot()
        url = f'{url}?token={self.token}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as data_response:
                data = json.loads(await data_response.read())
        return data

    async def get_subreddit(self, subreddit: str):
        sub_about_url = f'{reddit_base}/{subreddit}/about.json'
        sub_about_data = await self.__get_data(sub_about_url)
        return RedditSub(sub_about_data)

    async def get_posts(self, subreddit: str, listing: str):
        await self.boot()
        sub_listing_url = f'{reddit_base}/{subreddit}/{listing}.json'
        sub_listing_data = await self.__get_data(sub_listing_url)
        sub_listing_list = sub_listing_data.get('data', {}).get('children', [])
        posts = [RedditPost(post.get('data')) for post in sub_listing_list]
        return posts
