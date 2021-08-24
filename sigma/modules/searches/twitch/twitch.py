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

import discord
import twitchio

from sigma.core.utilities.generic_responses import GenericResponse


async def twitch(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        username = pld.args[0]
        twt = twitchio.Client(cmd.cfg.get('token'))
        users = await twt.fetch_users([username])
        if users:
            user = users[0]
            channels = await twt.search_channels(user.name)
            channel = None
            for result in channels:
                if result.id == user.id:
                    channel = result
                    break
            if channel:
                channel_url = f'https://www.twitch.tv/{channel.name}'
                color = 0x91_47_ff if channel.live else 0x69_69_69
                response = discord.Embed(color=color)
                response.set_author(name=user.name, icon_url=user.profile_image, url=channel_url)
                if channel.live:
                    games = await twt.fetch_games([int(channel.game_id)])
                    game = games[0]
                    response.description = channel.title
                    response.set_thumbnail(url=game.art_url(144, 192))
                else:
                    response.description = f'{user.name} is currently offline.'
            else:
                response = GenericResponse('Found the user, but not their channel... somehow.').error()
        else:
            response = GenericResponse('I couldn\'t find that user.').not_found()
    else:
        response = GenericResponse('Please specify a Twitch username.').error()
    await pld.msg.channel.send(embed=response)
