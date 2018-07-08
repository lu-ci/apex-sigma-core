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
from sigma.modules.searches.reddit.mech.reddit_core import RedditClient

reddit_client = None
reddit_icon = 'https://i.imgur.com/5w7eJ5A.png'


async def grab_post(subreddit, argument):
    filters = ['tophot', 'randomhot', 'topnew', 'randomnew', 'toptop', 'randomtop']
    if argument in filters:
        posts = await reddit_client.get_posts(subreddit, argument[-3:])
        post = posts[0] if argument.startswith('top') else secrets.choice(posts)
    else:
        post = secrets.choice(await reddit_client.get_posts(subreddit, 'hot'))
    return post


def add_post_image(post, response):
    if hasattr(post, 'preview'):
        images = post.preview.get('images')
        if images:
            sources = images[0].get('variants', {})
            variant_data = sources.get('gif', sources.get('png', sources.get('jpg', {}))) or images[0]
            prev_img = variant_data.get('source', {}).get('url')
            if prev_img:
                response.set_image(url=prev_img)


async def reddit(cmd: SigmaCommand, message: discord.Message, args: list):
    global reddit_client
    client_id = cmd.cfg.get('client_id')
    client_secret = cmd.cfg.get('client_secret')
    if client_id and client_secret:
        if args:
            if reddit_client is None:
                reddit_client = RedditClient(client_id, client_secret, cmd.bot.user.id)
                await reddit_client.boot()
            subreddit = args[0]
            argument = args[-1].lower()
            subreddit = await reddit_client.get_subreddit(subreddit)
            if not subreddit.private and not subreddit.banned:
                if subreddit:
                    post = await grab_post(subreddit.display_name, argument)
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
                        response = discord.Embed(color=0xBE1931, title='❗ No such subreddit.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ No such subreddit.')
            else:
                reason = 'banned' if subreddit.banned else 'private'
                response = discord.Embed(color=0xBE1931, title=f'❗ That subreddit is {reason}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
