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

import asyncio
import hashlib
import os
from asyncio.queues import Queue

import discord
import yt_dlp

ytdl_params = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'opus',
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
    """
    An item wrapping the information of a queued music item.
    """

    __slots__ = (
        "bot", "requester", "item_info", "url", "video_id", "uploader",
        "title", "thumbnail", "duration", "downloaded", "loop",
        "threads", "ytdl_params", "ytdl", "token", "location"
    )

    def __init__(self, bot, requester, item_info):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :type requester: discord.Member
        :type item_info: dict
        """
        self.bot = bot
        self.requester = requester
        self.item_info = item_info
        self.url = self.item_info.get('webpage_url')
        self.video_id = self.item_info.get('id', self.url)
        self.uploader = self.item_info.get('uploader', 'Unknown')
        self.title = self.item_info.get('title')
        self.thumbnail = self.item_info.get('thumbnail', 'https://i.imgur.com/CGPNJDT.png')
        self.duration = int(self.item_info.get('duration', 0))
        self.downloaded = False
        self.loop = asyncio.get_event_loop()
        self.ytdl_params = ytdl_params
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_params)
        self.token = self.tokenize()
        self.location = None

    def tokenize(self):
        """
        Generates a token identifier for
        a queued item for cache storage.
        :rtype: str
        """
        name = 'yt_' + self.video_id
        crypt = hashlib.new('md5')
        crypt.update(name.encode('utf-8'))
        final = crypt.hexdigest()
        return final

    async def download(self):
        """
        Downloads a queued item
        """
        if self.url:
            out_location = f'cache/{self.token}'
            if not os.path.exists(out_location):
                outtmpl = self.ytdl.params.get('outtmpl')
                outtmpl.update({'default': out_location})
                self.ytdl.params.update(outtmpl)
                await self.bot.threader.execute(self.ytdl.extract_info, (self.url,))
                self.downloaded = True
            self.location = out_location

    async def create_player(self, voice_client):
        """
        Creates a player instance for a voice client
        to deliver the item's music data to.
        :type voice_client: discord.VoiceClient
        """
        await self.download()
        if self.location:
            audio_source = discord.FFmpegOpusAudio(self.location)
            if voice_client:
                if not voice_client.is_playing():
                    await self.bot.threader.execute(voice_client.play, (audio_source,))


class MusicCore(object):
    """
    The core class for handling music
    queuing, storage and handling.
    """

    __slots__ = (
        "bot", "db", "loop", "queues",
        "currents", "repeaters", "ytdl_params",
        "ytdl"
    )

    def __init__(self, bot):
        """
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.db = bot.db
        self.loop = None
        self.queues = {}
        self.currents = {}
        self.repeaters = []
        self.ytdl_params = ytdl_params
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_params)

    async def init(self, loop):
        """
        Sets the event loop.
        :type loop: asyncio.AbstractEventLoop
        """
        self.loop = loop

    async def extract_info(self, url):
        """
        Grabs the information of a downloadable URL
        or one that's parse-able by YTDL.
        :type url: str
        :rtype: dict
        """
        return self.ytdl.extract_info(url, False)

    def get_queue(self, guild_id):
        """
        Gets a guild's queue.
        If the guild doesn't have one, it'll be generated.
        :type guild_id: int
        :rtype: asyncio.Queue
        """
        queue = self.queues.get(guild_id, Queue())
        self.queues.update({guild_id: queue})
        return queue

    @staticmethod
    async def listify_queue(queue):
        """
        Due to the asynchronous nature of the queue
        this is for making a standard list out of a queue item.
        :type queue: asyncio.Queue
        :rtype: list
        """
        item_list = []
        while not queue.empty():
            item = await queue.get()
            item_list.append(item)
        for item in item_list:
            await queue.put(item)
        return item_list
