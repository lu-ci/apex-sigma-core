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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


class CollectionJar(object):
    def __init__(self, jar, message):
        self.raw = jar
        self.total = self.raw.get('total', 0)
        self.channels = self.raw.get('channels', {})
        self.channel = self.channels.get(str(message.channel.id), 0)
        self.users = self.raw.get('users', {})
        self.user = self.users.get(str(message.author.id), {})
        self.user_channel = self.user.get(str(message.channel.id), 0)

    @property
    def user_total(self):
        contributions = 0
        for chn, amount in self.user.items():
            contributions += amount
        return contributions


async def viewcollectionjar(_cmd: SigmaCommand, pld: CommandPayload):
    jar_doc = pld.settings.get('collection_jar') or {}
    if jar_doc:
        jar = CollectionJar(jar_doc, pld.msg)
        response = discord.Embed(color=16636040, title='💰 Collection Jar')
        contents = f'Total: **{jar.total}**\n'
        contents += f'This Channel: **{jar.channel}**\n'
        contents += f'Your Contributions: **{jar.user_total}**\n'
        contents += f'You In This Channel: **{jar.user_channel}**'
        response.add_field(name='Contents', value=contents)
    else:
        response = discord.Embed(color=13034677, title='💸 Totally empty...')
    await pld.msg.channel.send(embed=response)
