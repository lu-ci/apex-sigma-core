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
import secrets

import discord
import twitchio

partner_monitor_running = False
live_constant = False
twitch_icon = 'https://static.twitchcdn.net/assets/favicon-32-e29e246c157142c94346.png'


def is_live():
    return live_constant


async def partner_monitor(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global partner_monitor_running
    if not partner_monitor_running:
        partner_monitor_running = True
        ev.bot.loop.create_task(cycler(ev))


def shuffle(items):
    new = []
    copy = [i for i in items]
    while len(copy) > 0:
        new.append(copy.pop(secrets.randbelow(len(copy))))
    return new


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global live_constant
    cfg = ev.bot.modules.commands.get('twitch').cfg
    cfg_args = ['token', 'partners']
    if all([bool(getattr(cfg, arg)) for arg in cfg_args]):
        twt = twitchio.Client(cfg.get('token'))
        while True:
            live_constant = False
            for partner_name in shuffle(cfg.get('partners')):
                channels = await twt.search_channels(partner_name)
                channel = None
                for result in channels:
                    if result.name.lower() == partner_name.lower():
                        channel = result
                        break
                if channel:
                    if channel.live:
                        live_constant = True
                        # noinspection PyBroadException
                        try:
                            ev.log.info(f'Hosting {channel.name} as a partner stream.')
                            await ev.bot.change_presence(activity=discord.Streaming(
                                platform='twitch',
                                name=f'a friend: {channel.name}',
                                url=f'https://www.twitch.tv/{channel.name}',
                                twitch_name=channel.name
                            ))
                            break
                        except SyntaxError:
                            pass
            await asyncio.sleep(300)
