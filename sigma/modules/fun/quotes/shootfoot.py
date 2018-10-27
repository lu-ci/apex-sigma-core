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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def shootfoot(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    lang = ' '.join(args).lower() if args else None
    if lang:
        joke_doc = await cmd.db[cmd.db.db_nam].ShootFootData.find_one({'lang_low': lang})
    else:
        all_docs = await cmd.db[cmd.db.db_nam].ShootFootData.find().to_list(None)
        joke_doc = secrets.choice(all_docs)
    if joke_doc:
        joke = secrets.choice(joke_doc.get('methods'))
        foot_lang = joke_doc.get('lang')
        response = discord.Embed(color=0xbf6952, title=f'🔫 How to shoot yourself in the foot with {foot_lang}...')
        response.description = joke
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 I don\'t know how to do it in {lang}.')
    await message.channel.send(embed=response)
