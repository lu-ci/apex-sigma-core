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

import re

from sigma.core.utilities.data_processing import command_message_parser


async def auto_responder(ev, pld):
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
                triggers = pld.settings.get('responder_triggers') or {}
                # sort triggers by word count to avoid longer ones never triggering
                triggers = sorted(triggers.items(), key=lambda x: len(x[0].split()), reverse=True)
                for trigger, response in triggers:
                    # matches <string-start|non-word-char><trigger><string-end|non-word-char>
                    match = re.search(r'(^|\W)' + trigger + r'($|\W)', pld.msg.content)
                    if match:
                        response = command_message_parser(pld.msg, response)
                        await pld.msg.channel.send(response)
                        break
