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

from sigma.core.mechanics.payload import MessagePayload
from sigma.modules.core_functions.chatter_core.chatter_core_init import chatter_core, train


def set_session_info(pld: MessagePayload):
    """

    :param pld:
    :type pld:
    """
    chatter_core.setPredicate('hostname', pld.msg.guild.name, pld.msg.author.id)
    chatter_core.setPredicate('name', pld.msg.author.name, pld.msg.author.id)
    chatter_core.setPredicate('nickname', pld.msg.author.display_name, pld.msg.author.id)
    chatter_core.setBotPredicate('nickname', pld.msg.guild.me.display_name)


async def chatter_core_responder(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.content:
        start_one = pld.msg.content.startswith(f'<@{ev.bot.user.id}>')
        start_two = pld.msg.content.startswith(f'<@!{ev.bot.user.id}>')
        if start_one or start_two:
            clean_msg = ' '.join(pld.msg.content.split()[1:])
            if clean_msg:
                for mention in pld.msg.mentions:
                    clean_msg.replace(mention.mention, mention.display_name)
                active = pld.settings.get('chatterbot')
                if active:
                    async with pld.msg.channel.typing():
                        if not chatter_core.numCategories():
                            train(ev, chatter_core)
                        set_session_info(pld)
                        response_text = chatter_core.respond(clean_msg, pld.msg.author.id)
                        sleep_time = len(response_text) * 0.185
                        await asyncio.sleep(sleep_time)
                        await pld.msg.channel.send(f'{pld.msg.author.mention} {response_text}')
