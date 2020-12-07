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

from sigma.modules.nsfw.mech.core import safebooru_client

usagi_icon = 'https://i.imgur.com/DWZLtAk.jpg'
posts = []
titles = [
    'Touch fluffy ears~', '>:3',
    '乀^｀・´^／', '(ミ`ω´ミ)', '◝(´◝ω◜｀)◜'
]


async def usagimimi(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    client = safebooru_client(cmd.db.cache, cmd.bot.get_agent())
    global posts
    if not posts:
        wait_text = f'🦊 One moment, filling {cmd.bot.user.name} with bunnies...'
        wait_embed = discord.Embed(color=0xEEEEEE, title=wait_text)
        working_msg = await pld.msg.channel.send(embed=wait_embed)
        posts = await client.randpost(['bunny_ears'], True)
        working_done = discord.Embed(color=0xEEEEEE, title=f'🦊 We added {len(posts)} bunnies!')
        try:
            await working_msg.edit(embed=working_done)
        except discord.NotFound:
            pass
    post = posts.pop(secrets.randbelow(len(posts)))
    img_url = post.get('file_url')
    if not img_url.startswith('http'):
        img_url = f"https:{img_url}"
    post_url = client.post_url + str(post.get('id'))
    score_text = f'Score: {post.get("score")}'
    size_text = f'Size: {post.get("width")}x{post.get("height")}'
    response = discord.Embed(color=0xad3d3d)
    response.set_author(name=secrets.choice(titles), url=post_url, icon_url=client.icon_url)
    response.set_image(url=img_url)
    response.set_footer(text=f'{score_text} | {size_text}')
    await pld.msg.channel.send(embed=response)


