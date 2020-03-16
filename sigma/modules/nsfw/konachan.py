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

from sigma.core.utilities.generic_responses import not_found, error
from sigma.modules.nsfw.mech.core import konachan_client


async def konachan(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    client = konachan_client(cmd.db.cache, cmd.bot.user.id)
    tags = client.remove_lines_breaks(pld.args)
    if not len(tags) > 6:
        post = await client.randpost(pld.args)
        if post:
            post_url = client.post_url + str(post.get('id'))
            footer_text = f'Score: {post.get("score")} | Size: {post.get("width")}x{post.get("height")}'
            footer_text += f' | Uploaded By: {post.get("author")}'
            response = discord.Embed(color=0x473a47)
            response.set_author(name='Konachan', url=post_url, icon_url=client.icon_url)
            response.set_image(url=post.get('file_url'))
            response.set_footer(text=footer_text)
        else:
            response = not_found('No results.')
    else:
        response = error('You can only search up to 6 tags.')
    await pld.msg.channel.send(embed=response)
