import asyncio
import functools
import hashlib
import os
from multiprocessing.pool import ThreadPool
from asyncio.queues import Queue

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
        self.video_id = self.item_info['id']
        if 'uploader' in self.item_info:
            self.uploader = self.item_info['uploader']
        else:
            self.uploader = 'Unknown'
        self.title = self.item_info['title']
        if 'thumbnail' in self.item_info:
            self.thumbnail = self.item_info['thumbnail']
        else:
            self.thumbnail = 'https://i.imgur.com/CGPNJDT.png'
        self.duration = int(self.item_info['duration'])
        self.downloaded = False
        self.loop = asyncio.get_event_loop()
        self.pool = ThreadPool(1)
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
                async_download = self.pool.apply_async(task)
                async_download.get()
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
        self.pool = ThreadPool(1)
        self.queues = {}
        self.currents = {}
        self.repeaters = []
        self.ytdl_params = ytdl_params
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_params)

    async def extract_info(self, url):
        task = functools.partial(self.ytdl.extract_info, url, False)
        async_extract = self.pool.apply_async(task)
        information = async_extract.get()
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
