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

import arrow

stats = {}
start_stamp = arrow.utcnow().int_timestamp
end_stamp = start_stamp + 86400


def update_stat(guild_id, stat):
    """
    :type guild_id: int
    :type stat: str
    """
    gld_stats = stats.get(guild_id, {})
    count = gld_stats.get(stat, 0)
    gld_stats.update({stat: count + 1})
    stats.update({guild_id: gld_stats})


async def guild_watcher(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    global start_stamp, end_stamp
    if pld.msg.guild:
        now = arrow.utcnow().int_timestamp
        if now > end_stamp:
            stats.clear()
            start_stamp, end_stamp = now, now + 86400
        update_stat(pld.msg.guild.id, 'messages')
        prefix = ev.db.get_prefix(pld.settings)
        if pld.msg.content.startswith(prefix):
            if pld.msg.content != prefix and not pld.msg.content.startswith(prefix + ' '):
                cmd = pld.msg.content[len(prefix):].lower().split()[0]
                if cmd in ev.bot.modules.commands or cmd in ev.bot.modules.alts:
                    update_stat(pld.msg.guild.id, 'commands')
