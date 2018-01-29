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
import asyncio
import functools
import hashlib
import os
from asyncio.queues import Queue
from concurrent.futures import ThreadPoolExecutor

import discord
import youtube_dl

ytdl_params = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


class QueueItem(object):
    def __init__(self, requester, item_info):
        self.requester = requester
        self.item_info = item_info
        self.url = self.item_info.get('webpage_url')
        self.video_id = self.item_info.get('id') or self.url
        self.uploader = self.item_info.get('uploader') or 'Unknown'
        self.title = self.item_info['title']
        if 'thumbnail' in self.item_info:
            thumb = self.item_info.get('thumbnail')
            if thumb:
                self.thumbnail = thumb
            else:
                self.thumbnail = 'https://i.imgur.com/CGPNJDT.png'
        else:
            self.thumbnail = 'https://i.imgur.com/CGPNJDT.png'
        self.duration = int(self.item_info.get('duration') or 0)
        self.downloaded = False
        self.loop = asyncio.get_event_loop()
        self.threads = ThreadPoolExecutor()
        self.ytdl_params = ytdl_params
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_params)
        self.token = self.tokenize()
        self.location = None

    def tokenize(self):
        name = 'yt_' + self.video_id
        crypt = hashlib.new('md5')
        crypt.update(name.encode('utf-8'))
        final = crypt.hexdigest()
        return final

    async def download(self):
        if self.url:
            out_location = f'cache/{self.token}'
            if not os.path.exists(out_location):
                self.ytdl.params['outtmpl'] = out_location
                task = functools.partial(self.ytdl.extract_info, self.url)
                await self.loop.run_in_executor(self.threads, task)
                self.downloaded = True
            self.location = out_location

    async def create_player(self, voice_client):
        await self.download()
        if self.location:
            audio_source = discord.FFmpegPCMAudio(self.location)
            if not voice_client.is_playing():
                voice_client.play(audio_source)


class MusicCore(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.loop = asyncio.get_event_loop()
        self.threads = ThreadPoolExecutor()
        self.queues = {}
        self.currents = {}
        self.repeaters = []
        self.ytdl_params = ytdl_params
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_params)

    async def extract_info(self, url):
        task = functools.partial(self.ytdl.extract_info, url, False)
        information = await self.loop.run_in_executor(self.threads, task)
        return information

    def get_queue(self, guild_id):
        if guild_id in self.queues:
            queue = self.queues[guild_id]
        else:
            queue = Queue()
            self.queues.update({guild_id: queue})
        return queue

    @staticmethod
    async def listify_queue(queue):
        item_list = []
        while not queue.empty():
            item = await queue.get()
            item_list.append(item)
        for item in item_list:
            await queue.put(item)
        return item_list
