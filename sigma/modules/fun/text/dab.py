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

import secrets

import discord

dab_imgs = [
    'https://i.ytimg.com/vi/6VatNMm6ac4/maxresdefault.jpg',
    'https://pa1.narvii.com/6724/6683da02ba2ee1ccce786c0f6b78117f666ab04c_hq.gif',
    'https://pbs.twimg.com/media/DNJj8ucUQAAmw9n.png'
]


async def dab(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    dab_img = secrets.choice(dab_imgs)
    await pld.msg.channel.send(embed=discord.Embed().set_image(url=dab_img))
