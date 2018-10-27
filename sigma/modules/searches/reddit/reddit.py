# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import secrets

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.searches.reddit.mech.reddit_core import RedditClient

reddit_client = None
reddit_icon = 'https://i.imgur.com/5w7eJ5A.png'


async def grab_post(subreddit, argument):
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


async def reddit(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    global reddit_client
    if args:
        if reddit_client is None:
            reddit_client = RedditClient(cmd.bot.user.id)
        subreddit = args[0]
        argument = args[-1].lower()
        subreddit = await reddit_client.get_subreddit(subreddit)
        if not subreddit.private and not subreddit.banned:
            post = await grab_post(subreddit, argument)
            if subreddit.exists:
                if post:
                    if not post.over_18 or message.channel.is_nsfw():
                        post_desc = f'Author: {post.author if post.author else "Anonymous"}'
                        post_desc += f' | Karma Score: {post.score}'
                        author = f'https://www.reddit.com{post.permalink}'
                        response = discord.Embed(color=0xcee3f8, timestamp=arrow.get(post.created_utc).datetime)
                        response.set_author(name=f'r/{subreddit.display_name}', url=author, icon_url=reddit_icon)
                        response.description = post.title
                        response.set_footer(text=post_desc)
                        add_post_image(post, response)
                    else:
                        nsfw_warning = '❗ NSFW Subreddits and posts are not allowed here.'
                        response = discord.Embed(color=0xBE1931, title=nsfw_warning)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ That subreddit has no posts.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No such subreddit.')
        else:
            reason = 'banned' if subreddit.banned else 'private'
            response = discord.Embed(color=0xBE1931, title=f'❗ That subreddit is {reason}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
