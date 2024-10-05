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

import discord


class CollectionJar(object):
    def __init__(self, jar, message, target):
        """
        :type jar: dict
        :type message: discord.Message
        :type target: discord.Member
        """
        self.raw = jar
        self.total = self.raw.get('total', 0)
        self.channels = self.raw.get('channels', {})
        self.channel = self.channels.get(str(message.channel.id), 0)
        self.users = self.raw.get('users', {})
        self.user = self.users.get(str(target.id), {})
        self.user_channel = self.user.get(str(message.channel.id), 0)

    @property
    def user_total(self):
        """
        :rtype: int
        """
        contributions = 0
        for chn, amount in self.user.items():
            contributions += amount
        return contributions


async def viewcollectionjar(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    jar_doc = pld.settings.get('collection_jar') or {}
    if jar_doc:
        target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
        starters = ['Their', 'Them'] if pld.msg.mentions else ['Your', 'You']
        jar = CollectionJar(jar_doc, pld.msg, target)
        response = discord.Embed(color=0xf9ca55, title='🫙 Collection Jar')
        contents = f'Total: **{jar.total}**\n'
        contents += f'This Channel: **{jar.channel}**\n'
        contents += f'{starters[0]} Contributions: **{jar.user_total}**\n'
        contents += f'{starters[1]} In This Channel: **{jar.user_channel}**'
        response.add_field(name='Contents', value=contents, inline=False)
        response.add_field(name='Trigger', value=jar_doc.get('trigger', '<unset>'), inline=False)
    else:
        response = discord.Embed(color=0xf9ca55, title='🫙 Totally empty...')
    await pld.msg.channel.send(embed=response)
