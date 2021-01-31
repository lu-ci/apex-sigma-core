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


async def invite(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
    if 'text' in ' '.join(pld.args).lower():
        invite_text = f'Click the following link to invite me: <{invite_url}>'
        await pld.msg.channel.send(invite_text)
    else:
        inv_title = 'Click here to invite me.'
        sigma_image = 'https://i.imgur.com/DM8fIy6.png'
        response = discord.Embed(color=0x1B6F5F).set_author(name=inv_title, icon_url=sigma_image, url=invite_url)
        await pld.msg.channel.send(embed=response)
