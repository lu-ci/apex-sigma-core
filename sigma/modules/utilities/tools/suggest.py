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


import discord
import secrets
import aiohttp
from sigma.core.mechanics.command import SigmaCommand


def create_body(msg: discord.Message, args: list, token: str):
    content = f'# Suggestion {token}\n\n## Submitter'
    content += f'\n\nSubmitted by **{msg.author.name}**#{msg.author.discriminator} [{msg.author.id}]'
    content += f'from **{msg.guild.name}** [{msg.guild.id}].'
    content += f'\n\n## Content\n\n> {" ".join(args)}'
    return content


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
                await session.post(repo_url, json=issue_data)
            response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {sugg_token} submitted.')
            sugg_chn_id = cmd.cfg.get('channel')
            if sugg_chn_id:
                sugg_chn = discord.utils.find(lambda x: x.id == sugg_chn_id, cmd.bot.get_all_channels())
                if sugg_chn:
                    try:
                        sugg_msg = await sugg_chn.send(f'```md\n{body}\n```')
                        await sugg_msg.add_reaction('⬆')
                        await sugg_msg.add_reaction('⬇')
                    except Exception:
                        pass
        else:
            response = discord.Embed(title='❗ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='❗ Missing GitHub confirguation.', color=0xBE1931)
    await message.channel.send(embed=response)
