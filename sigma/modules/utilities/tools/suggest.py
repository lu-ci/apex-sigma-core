# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import json
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


def create_body(msg: discord.Message, args: list, token: str):
    content = f'# Suggestion {token}\n\n## Submitter'
    content += f'\n\nSubmitted by **{msg.author.name}**#{msg.author.discriminator} [{msg.author.id}]'
    content += f' from **{msg.guild.name}** [{msg.guild.id}].'
    content += f'\n\n## Content\n\n> {" ".join(args)}'
    return content


def make_sugg_embed(msg: discord.Message, args: list, token: str, issue: str):
    sugg_embed = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
    sugg_embed.description = " ".join(args)
    author_name = f'{msg.author.name}#{msg.author.discriminator}'
    sugg_embed.set_author(name=author_name, icon_url=user_avatar(msg.author), url=issue)
    sugg_embed.set_footer(icon_url=msg.guild.icon_url, text=f'[{token}] From {msg.guild.name}.')
    return sugg_embed


async def suggest(cmd: SigmaCommand, message: discord.Message, args: list):
    sugg_ghu = cmd.cfg.get('user')
    sugg_ghr = cmd.cfg.get('repo')
    sugg_ght = cmd.cfg.get('token')
    if sugg_ght and sugg_ghr and sugg_ghu:
        if args:
            auth = aiohttp.BasicAuth(sugg_ghu, sugg_ght)
            sugg_token = secrets.token_hex(4)
            body = create_body(message, args, sugg_token)
            issue_data = {'title': f'Suggestion {sugg_token}', 'body': body}
            repo_url = f'https://api.github.com/repos/{sugg_ghr}/issues'
            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.post(repo_url, json=issue_data) as api_resp:
                    issue_url = json.loads(await api_resp.read()).get('html_url')
            response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {sugg_token} submitted.')
            sugg_chn_id = cmd.cfg.get('channel')
            if sugg_chn_id:
                sugg_chn = discord.utils.find(lambda x: x.id == sugg_chn_id, cmd.bot.get_all_channels())
                if sugg_chn:
                    try:
                        sugg_msg = await sugg_chn.send(embed=make_sugg_embed(message, args, sugg_token, issue_url))
                        await sugg_msg.add_reaction('⬆')
                        await sugg_msg.add_reaction('⬇')
                    except Exception:
                        pass
        else:
            response = discord.Embed(title='❗ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='❗ Missing GitHub confirguation.', color=0xBE1931)
    await message.channel.send(embed=response)
