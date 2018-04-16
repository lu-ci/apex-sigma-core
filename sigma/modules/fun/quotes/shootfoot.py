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


import secrets

import discord
import yaml

from sigma.core.mechanics.command import SigmaCommand

feet_data = None


async def shootfoot(cmd: SigmaCommand, message: discord.Message, args: list):
    global feet_data
    if not feet_data:
        with open(cmd.resource('feets.yml')) as footfile:
            feet_data = yaml.safe_load(footfile)
    if args:
        foot_lang = None
        foot_lang_search = args[0].lower()
        for foot_key in feet_data.keys():
            if foot_key.lower() == foot_lang_search:
                foot_lang = foot_key
        if foot_lang:
            joke_list = feet_data.get(foot_lang)
        else:
            joke_list = None
    else:
        foot_lang = secrets.choice(list(feet_data.keys()))
        joke_list = feet_data.get(foot_lang)
    if joke_list:
        joke = secrets.choice(joke_list)
        response = discord.Embed(color=0xbf6952, title=f'🔫 How to shoot yourself in the foot with {foot_lang}...')
        response.description = joke
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 I don\'t know how to do it with {foot_lang_search}.')
    await message.channel.send(embed=response)
