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
import discord

from sigma.core.utilities.data_processing import user_avatar


async def command_logger(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.CommandEventPayload
    """
    if pld.msg.guild:
        log_title = f'{pld.msg.author.name}#{pld.msg.author.discriminator}\'s used {pld.cmd.name.upper()}.'
        arguments = ' '.join(pld.args) if pld.args else 'No Arguments'
        log_embed = discord.Embed(color=0x1B6F5F, timestamp=arrow.utcnow().datetime)
        log_embed.set_author(name=log_title, icon_url=user_avatar(pld.msg.author))
        log_embed.description = f'Location: {pld.msg.channel.mention}\nArguments: {arguments}'
        log_embed.set_footer(text=f'Message ID: {pld.msg.id}')
        log_channel_id = pld.settings.get('log_modules_channel')
        logged_modules = pld.settings.get('logged_modules') or []
        log_event_active = pld.cmd.category.lower() in logged_modules
        if log_channel_id and log_event_active:
            log_channel = await ev.bot.get_channel(log_channel_id, True)
            if log_channel:
                # noinspection PyBroadException
                try:
                    await log_channel.send(embed=log_embed)
                except Exception:
                    pass
