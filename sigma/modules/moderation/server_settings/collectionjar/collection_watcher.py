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

import string

from sigma.modules.moderation.server_settings.collectionjar.viewcollectionjar import CollectionJar


def clean_word(text):
    """
    Removes punctuation from a string.
    :type text: str
    :rtype: str
    """
    output = ''
    for char in text:
        if char.lower() not in string.punctuation:
            output += char.lower()
    return output


async def add_to_jar(ev, message, jar):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type message: discord.Message
    :type jar: dict
    """
    jar = CollectionJar(jar, message, message.author)
    jar.channels.update({str(message.channel.id): jar.channel + 1})
    jar.user.update({str(message.channel.id): jar.user_channel + 1})
    jar.users.update({str(message.author.id): jar.user})
    jar.raw.update({'total': jar.total + 1, 'channels': jar.channels, 'users': jar.users})
    await ev.db.set_guild_settings(message.guild.id, 'collection_jar', jar.raw)


async def collection_watcher(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.guild:
        if pld.msg.content:
            pfx = ev.db.get_prefix(pld.settings)
            if not pld.msg.content.startswith(pfx):
                jar_doc = pld.settings.get('collection_jar', {})
                trigger = jar_doc.get('trigger')
                if trigger:
                    content = clean_word(pld.msg.content)
                    if trigger.lower() in content:
                        if not await ev.bot.cool_down.on_cooldown(ev.name, pld.msg.author):
                            await ev.bot.cool_down.set_cooldown(ev.name, pld.msg.author, 60)
                            await add_to_jar(ev, pld.msg, jar_doc)
