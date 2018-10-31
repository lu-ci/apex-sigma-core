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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload
from sigma.modules.fun.auto_response.auto_responder import clean_word
from sigma.modules.moderation.server_settings.collectionjar.viewcollectionjar import CollectionJar


async def add_to_jar(ev: SigmaEvent, message: discord.Message, jar: dict):
    jar = CollectionJar(jar, message)
    jar.raw.update({'total': jar.total + 1})
    jar.channels.update({str(message.channel.id): jar.channel + 1})
    jar.user.update({str(message.channel.id): jar.user_channel + 1})
    jar.users.update({str(message.author.id): jar.user})
    await ev.db.set_guild_settings(message.guild.id, 'collection_jar', jar.raw)


async def collection_watcher(ev: SigmaEvent, pld: MessagePayload):
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
