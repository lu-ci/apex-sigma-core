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

import aiohttp
import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def setavatar(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args or pld.msg.attachments:
        image_url = pld.msg.attachments[0].url if pld.msg.attachments else pld.args[0]
        try:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as image_response:
                        img_data = await image_response.read()
                await cmd.bot.user.edit(avatar=img_data)
                response = GenericResponse('My avatar has been changed.').ok()
            except aiohttp.InvalidURL:
                response = GenericResponse('Invalid URL.').error()
        except discord.Forbidden:
            response = GenericResponse('I was unable to change my avatar.').error()
    else:
        response = GenericResponse('Give me a link or attach an image, please.').error()
    await pld.msg.channel.send(embed=response)
