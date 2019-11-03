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


async def temproom_checker(_ev, pld):
    """
    :param _ev: The main event instance referenced.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.VoiceStateUpdatePayload
    """
    b = pld.before
    if b:
        if b.channel:
            if b.channel.name.startswith('[Σ]'):
                try:
                    members = len([m for m in b.channel.members if not m.bot])
                    if not members:
                        await b.channel.delete(reason='Temporary Voice Channel Emptied')
                    await asyncio.sleep(.25)
                    category = b.channel.category
                    if category:
                        custom_cat_id = pld.settings.get('temp_channel_category')
                        custom_cat = category.guild.get_channel(custom_cat_id)
                        if custom_cat:
                            if category.id == custom_cat.id:
                                return
                        if category.name.startswith('[Σ]'):
                            if len(category.channels) == 0:
                                await category.delete(reason='Temporary VC Category Emptied')
                except (discord.NotFound, discord.Forbidden):
                    pass
