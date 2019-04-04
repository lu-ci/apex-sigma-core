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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.sigma import ApexSigma
from sigma.core.utilities.generic_responses import error, ok


def parse_approval(args: list):
    """

    :param args:
    :type args:
    :return:
    :rtype:
    """
    suggestion_token = args[0].lower()
    suggestion_details = ' '.join(args[1:])
    suggestion_title, suggestion_description = suggestion_details.split('; ')
    return suggestion_token, suggestion_title, suggestion_description


def make_gl_suggestion(tkn: str, dsc: str, sugg: dict):
    """

    :param tkn:
    :type tkn:
    :param dsc:
    :type dsc:
    :param sugg:
    :type sugg:
    :return:
    :rtype:
    """
    sugg_txt = sugg.get("suggestion", {}).get("text")
    sugg_uid = sugg.get("user", {}).get('id')
    sugg_unam = sugg.get('user', {}).get('name')
    return f'{dsc}\n\n> {sugg_txt}\n\nSuggestion `{tkn}` by `{sugg_unam} [{sugg_uid}]`.'


async def submit_gl_issue(tkn: str, prj: str, ttl: str, dsc: str):
    """

    :param tkn:
    :type tkn:
    :param prj:
    :type prj:
    :param ttl:
    :type ttl:
    :param dsc:
    :type dsc:
    :return:
    :rtype:
    """
    api_url = f'https://gitlab.com/api/v4/projects/{prj}/issues'
    req_body = {'title': ttl, 'description': dsc, 'labels': 'Suggestion'}
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers={'PRIVATE-TOKEN': tkn}, data=req_body) as response:
            data = json.loads(await response.read())
    return data.get('web_url')


async def react_to_suggestion(bot: ApexSigma, suggestion: dict, reaction: str, delete: bool):
    """

    :param bot:
    :type bot:
    :param suggestion:
    :type suggestion:
    :param reaction:
    :type reaction:
    :param delete:
    :type delete:
    """
    sugg_cmd = bot.modules.commands.get('botsuggest')
    if sugg_cmd:
        if sugg_cmd.cfg.channel:
            sugg_chn = await bot.get_channel(sugg_cmd.cfg.channel, True)
            if sugg_chn:
                try:
                    smsg = await sugg_chn.fetch_message(suggestion.get('message'))
                    if smsg:
                        if delete:
                            await smsg.delete()
                        else:
                            await smsg.add_reaction(reaction)
                except (discord.Forbidden, discord.NotFound):
                    pass


async def approvesuggestion(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.args) >= 3:
        token, title, description = parse_approval(pld.args)
        suggestion = await cmd.db[cmd.db.db_nam].Suggestions.find_one({'suggestion.id': token})
        if suggestion:
            await react_to_suggestion(cmd.bot, suggestion, '✅', False)
            gl_issue_url = gl_desc = None
            if cmd.cfg.token and cmd.cfg.project:
                gl_desc = make_gl_suggestion(token, description, suggestion)
                gl_issue_url = await submit_gl_issue(cmd.cfg.token, cmd.cfg.project, title, gl_desc)
            athr = await cmd.bot.get_user(suggestion.get('user', {}).get('id'))
            if athr:
                to_user = ok(f'Suggestion {token} approved by {pld.msg.author.display_name}.')
                if gl_issue_url:
                    to_user_desc = 'Your suggestion was approved, you can view its status and details [here]'
                    to_user_desc += f'({gl_issue_url}). If you need info, the support server is in the help command.'
                else:
                    to_user_desc = f'```md\n{gl_desc}\n```'
                to_user.description = to_user_desc
                try:
                    await athr.send(embed=to_user)
                    response = ok(f'Suggestion {token} approved.')
                except (discord.Forbidden, discord.NotFound):
                    response = ok(f'Suggestion {token} approved, but delivery to author failed.')
            else:
                response = ok(f'Suggestion {token} approved, but the author was not found.')
        else:
            response = error('No suggestion entry with that ID was found.')
    else:
        response = error('Not enough arguments.')
    await pld.msg.channel.send(embed=response)
