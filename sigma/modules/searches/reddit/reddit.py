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

import arrow
import discord

from sigma.core.utilities.generic_responses import error
from sigma.modules.searches.reddit.mech.reddit_core import RedditClient

reddit_client = None
reddit_icon = 'https://i.imgur.com/5w7eJ5A.png'


async def grab_post(subreddit, argument):
    """

    :param subreddit:
    :type subreddit:
    :param argument:
    :type argument:
    :return:
    :rtype:
    """
    try:
        subreddit_name = subreddit.display_name
    except AttributeError:
        subreddit_name = None
    filters = ['tophot', 'randomhot', 'topnew', 'randomnew', 'toptop', 'randomtop']
    if subreddit_name:
        try:
            if argument in filters:
                posts = await reddit_client.get_posts(subreddit_name, argument[-3:])
                post = posts[0] if argument.startswith('top') else secrets.choice(posts)
            else:
                post = secrets.choice(await reddit_client.get_posts(subreddit_name, 'hot'))
        except IndexError:
            post = None
        setattr(subreddit, 'exists', True)
    else:
        post = None
        setattr(subreddit, 'exists', False)
    return post


def add_post_image(post, response):
    """

    :param post:
    :type post:
    :param response:
    :type response:
    """
    if post.url.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif']:
        response.set_image(url=post.url)
    elif hasattr(post, 'preview'):
        images = post.preview.get('images')
        if images:
            sources = images[0].get('variants', {})
            variant_data = sources.get('gif', sources.get('png', sources.get('jpg', {}))) or images[0]
            prev_img = variant_data.get('source', {}).get('url')
            if prev_img:
                response.set_image(url=prev_img)


async def reddit(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    global reddit_client
    if pld.args:
        if reddit_client is None:
            reddit_client = RedditClient(cmd.bot.user.id)
        subreddit = pld.args[0]
        argument = pld.args[-1].lower()
        subreddit = await reddit_client.get_subreddit(subreddit)
        if not subreddit.private and not subreddit.banned:
            post = await grab_post(subreddit, argument)
            if subreddit.exists:
                if post:
                    if not post.over_18 or pld.msg.channel.is_nsfw():
                        post_desc = f'Author: {post.author if post.author else "Anonymous"}'
                        post_desc += f' | Karma Score: {post.score}'
                        author = f'https://www.reddit.com{post.permalink}'
                        response = discord.Embed(color=0xcee3f8, timestamp=arrow.get(post.created_utc).datetime)
                        response.set_author(name=f'r/{subreddit.display_name}', url=author, icon_url=reddit_icon)
                        response.description = post.title
                        response.set_footer(text=post_desc)
                        add_post_image(post, response)
                    else:
                        response = error('NSFW Subreddits and posts are not allowed here.')
                else:
                    response = error('That subreddit has no posts.')
            else:
                response = error('No such subreddit.')
        else:
            reason = 'banned' if subreddit.banned else 'private'
            response = error(f'That subreddit is {reason}.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
