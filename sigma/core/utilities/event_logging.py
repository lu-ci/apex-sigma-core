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


async def log_event(bot, settings, response, event):
    """
    Logs an event in the set logging channel for the event type.
    :type bot: sigma.core.sigma.ApexSigma
    :type settings: dict
    :type response: discord.Embed
    :type event: str
    """
    log_channel_id, log_event_active = settings.get(f'{event}_channel'), settings.get(event)
    if log_channel_id and log_event_active:
        log_channel = await bot.get_channel(log_channel_id, True)
        if log_channel:
            # noinspection PyBroadException
            try:
                await log_channel.send(embed=response)
            except Exception:
                pass
