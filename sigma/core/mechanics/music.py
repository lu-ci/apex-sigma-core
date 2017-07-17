import hashlib
import asyncio
import discord
import functools
import youtube_dl
from concurrent.futures import ThreadPoolExecutor

ytdl_prefs = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


class MusicController(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        self.queues = {}
        self.bindings = {}
        self.repeaters = []
        self.ytdl = youtube_dl.YoutubeDL(ytdl_prefs)
        self.threads = ThreadPoolExecutor(max_workers=2)

    def get_queue(self, guild):
        if guild.id in self.queues:
            queue = self.queues[guild.id]
        else:
            queue = asyncio.Queue()
        return queue

    async def get_from_queue(self, guild):
        queue = self.get_queue(guild)
        if not queue.empty():
            item = await queue.get()
        else:
            item = None
        return item

    async def add_to_queue(self, guild, item):
        queue = self.get_queue(guild)
        await queue.put(item)
        self.queues.update({guild.id: queue})

    async def del_from_queue(self, guild, order):
        queue = self.get_queue(guild)
        if not queue.empty():
            item_list = []
            while not queue.empty():
                item = await queue.get()
                item_list.append(item)
            item_list.remove(item_list[order])
            for item in item_list:
                await queue.put(item)
            self.queues.update({guild.id: queue})

    @staticmethod
    def generate_token(url_id):
        crypt = hashlib.new('md5')
        crypt.update(url_id.encode('utf-8'))
        final = crypt.hexdigest()
        return final

    async def get_song_info(self, url):
        info = await self.bot.loop.run_in_executor(self.threads, functools.partial(self.ytdl.extract_info, url,
                                                                                   download=False))
        return info

    async def download_yt_item(self, item):
        token = self.generate_token(item['url'])
        location = f'cache/yt_{token}'
        self.ytdl.params['outtmpl'] = location
        await self.bot.loop.run_in_executor(self.threads, functools.partial(self.ytdl.extract_info, item['url']))
        return location

    async def play(self, guild, item):
        item_location = await self.download_yt_item(item)
        item_info = await self.get_song_info(item['url'])
        item.update({'info': item_info})
        source = discord.FFmpegPCMAudio(item_location)
        guild.voice_client.play(source)
        return item
