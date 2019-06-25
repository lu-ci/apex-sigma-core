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

REPO_URL = 'https://gitlab.com/lu-ci/sigma/apex-sigma'
REPO_ICON = 'https://framablog.org/wp-content/uploads/2016/01/gitlab.png'
REPO_TITLE = 'Apex Sigma: The Database Giant'


async def repository(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if '--text' in pld.args:
        response_embed = None
        response_text = REPO_URL
    else:
        response_text = None
        response_embed = discord.Embed(color=0xF7682D)
        response_embed.set_author(name=REPO_TITLE, icon_url=REPO_ICON, url=REPO_URL)
    await pld.msg.channel.send(response_text, embed=response_embed)
