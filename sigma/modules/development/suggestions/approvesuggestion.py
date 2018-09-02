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
import json

import aiohttp
import discord
from sigma.core.mechanics.command import SigmaCommand


def parse_approval(args: list):
    suggestion_token = args[0].lower()
    suggestion_details = ' '.join(args[1:])
    suggestion_title, suggestion_description = suggestion_details.split('; ')
    return suggestion_token, suggestion_title, suggestion_description


def make_gl_suggestion(tkn: str, dsc: str, sugg: dict):
    sugg_txt = sugg.get("suggestion", {}).get("text")
    sugg_uid = sugg.get("user", {}).get('id')
    sugg_unam = sugg.get('user', {}).get('name')
    return f'{dsc}\n\n> {sugg_txt}\n\nSuggestion `{tkn}` by `{sugg_unam} [{sugg_uid}]`.'


async def submit_gl_issue(tkn: str, prj: str, ttl: str, dsc: str):
    api_url = f'https://gitlab.com/api/v4/projects/{prj}/issues'
    req_body = {'title': ttl, 'description': dsc, 'labels': 'Suggestion'}
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers={'PRIVATE-TOKEN': tkn}, data=req_body) as response:
            data = json.loads(await response.read())
    return data.get('web_url')


async def approvesuggestion(cmd: SigmaCommand, message: discord.Message, args: list):
    if len(args) >= 3:
        token, title, description = parse_approval(args)
        suggestion = await cmd.db[cmd.db.db_nam].Suggestions.find_one({'suggestion.id': token})
        if suggestion:
            gl_token = cmd.cfg.get('token')
            gl_project = cmd.cfg.get('project')
            gl_issue_url = gl_desc = None
            if gl_token and gl_project:
                gl_desc = make_gl_suggestion(token, description, suggestion)
                gl_issue_url = await submit_gl_issue(gl_token, gl_project, title, gl_desc)
            athr = discord.utils.find(lambda u: u.id == suggestion.get('user', {}).get('id'), cmd.bot.get_all_members())
            if athr:
                to_user_title = f'✅ Suggestion {token} approved by {message.author.display_name}.'
                to_user = discord.Embed(color=0x77B255, title=to_user_title)
                if gl_issue_url:
                    to_user_desc = f'Your suggestion was approved, you can view its status and details [here]'
                    to_user_desc += f'({gl_issue_url}). If you need info, the support server is in the help command.'
                else:
                    to_user_desc = f'```md\n{gl_desc}\n```'
                to_user.description = to_user_desc
                try:
                    await athr.send(embed=to_user)
                except (discord.Forbidden, discord.NotFound):
                    pass
            response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {token} approved.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No suggestion entry with that ID was found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    await message.channel.send(embed=response)
