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

from sigma.modules.moderation.server_settings.collectionjar.collection_watcher import clean_word


def match_trigger(text, trigger):
    """
    Compares text content for a trigger's presence.
    :param text: The text to check.
    :type text: str
    :param trigger: The trigger to search for.
    :type trigger: str
    :return:
    :rtype: bool
    """
    text_pieces = clean_word(text).split()
    trigger_pieces = clean_word(trigger).split()
    matching_trigger = False
    if len(text_pieces) >= len(trigger_pieces):
        piece_location = None
        for piece_index, piece_text in enumerate(text_pieces):
            if piece_text == trigger_pieces[0]:
                piece_location = piece_index
                break
        if piece_location is not None:
            missmatch = False
            for trigger_index, trigger_piece in enumerate(trigger_pieces):
                if text_pieces[piece_location + trigger_index] != trigger_piece:
                    missmatch = True
                    break
            if not missmatch:
                matching_trigger = True
    return matching_trigger


async def auto_reactor(ev, pld):
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
                triggers = pld.settings.get('reactor_triggers') or {}
                # sort triggers by word count to avoid longer ones never triggering
                triggers = sorted(triggers.items(), key=lambda x: len(x[0].split()), reverse=True)
                for trigger, reaction in triggers:
                    match = match_trigger(pld.msg.content, trigger)
                    if match:
                        # noinspection PyBroadException
                        try:
                            await pld.msg.add_reaction(reaction)
                        except Exception:
                            pass
                        break
