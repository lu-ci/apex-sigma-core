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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.nsfw.mech.core import safebooru_client


async def safebooru(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    client = safebooru_client(cmd.db.cache, cmd.bot.get_agent())
    post = await client.randpost(pld.args)
    if post:
        img_url = post.get('file_url')
        if not img_url.startswith('http'):
            img_url = f"https:{img_url}"
        post_url = client.post_url + str(post.get('id'))
        score_text = f'Score: {post.get("score")}'
        size_text = f'Size: {post.get("width")}x{post.get("height")}'
        response = discord.Embed(color=0xad3d3d)
        response.set_author(name='Safebooru', url=post_url, icon_url=client.icon_url)
        response.set_image(url=img_url)
        response.set_footer(text=f'{score_text} | {size_text}')
    else:
        response = GenericResponse('No results.').not_found()
    await pld.msg.channel.send(embed=response)
