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

import discord

invite_reporter_running = False


async def invite_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global invite_reporter_running
    if not invite_reporter_running:
        invite_reporter_running = True
        ev.bot.loop.create_task(invite_reporter_cycler(ev))


async def invite_reporter_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            invite_docs = await ev.db[ev.db.db_name].InviteQueue.find({'reported': False}).to_list(None)
            for invite_doc in invite_docs:
                guild = await ev.bot.get_guild(invite_doc.get('guild'))
                if guild:
                    try:
                        invites = await guild.invites()
                        error = False
                    except discord.Forbidden:
                        invites = []
                        if guild.me.guild_permissions.create_instant_invite:
                            for channel in guild.channels:
                                if isinstance(channel, discord.TextChannel):
                                    try:
                                        invites.append(await channel.create_invite())
                                        break
                                    except discord.Forbidden:
                                        pass
                        if len(invites) == 0:
                            error = True
                        else:
                            error = False
                    if not error:
                        if len(invites) != 0:
                            body = ''
                            for invite in invites[:10]:
                                body += f'\n[{invite.code}]({invite.url})'
                        else:
                            body = 'No invites found.'
                    else:
                        body = 'No access to invites.'
                    update_dict = {'$set': {'reported': True}}
                    await ev.db[ev.db.db_name].InviteQueue.update_one(invite_doc, update_dict)
                    data = {
                        'reported': False,
                        'title': f'👀 {guild.name} [{guild.id}] Invite Report',
                        'color': 0xf9f9f9,
                        'content': body
                    }
                    await ev.db[ev.db.db_name].SystemMessages.insert_one(data)
                    await asyncio.sleep(1)
        await asyncio.sleep(1)
