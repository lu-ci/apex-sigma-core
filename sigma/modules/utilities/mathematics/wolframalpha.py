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
from urllib.parse import quote as escape

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

wolfram_icon = 'https://i.imgur.com/sGKq1A6.png'
wolfram_url = 'http://www.wolframalpha.com/input/?i='
api_url = 'http://api.wolframalpha.com/v2/query?output=JSON&format=image,plaintext&input='


class WolframResult(object):
    def __init__(self, data):
        """
        :type data: dict
        """
        self.pods = [Pod(p) for p in data.get('pods', [])]
        try:
            self.primary_pod = list(filter(lambda x: x.is_primary, self.pods))[0] if self.pods else []
        except IndexError:
            self.primary_pod = None
        self.success = data.get('success') and bool(self.primary_pod)


class Pod(object):
    def __init__(self, data):
        """
        :type data: dict
        """
        self.title = data.get('title', '').strip()
        self.subpods = [SubPod(p) for p in data.get('subpods')]
        self.is_primary = data.get('primary')


class SubPod(object):
    def __init__(self, data):
        """
        :type data: dict
        """
        self.text = data.get('plaintext', '').strip()
        self.image = data.get('img', {}).get('src') or None


def make_safe_query(query):
    """
    Creates a URL safe string by escaping reserved characters.
    :type query: list
    :rtype: str
    """
    safe = r'`~!@$^*()[]{}\|:;"\'<>,.'
    query_list = list(' '.join(query))
    safe_query = ''
    while query_list:
        char = query_list.pop(0).lower()
        safe_query += escape(char, safe=safe)
    return safe_query


async def send_response(message, init, response):
    """
    Edits the initial command response to display the results.
    Sends a new message if `init` or if the original isn't found.
    :type message: discord.Message
    :type init: discord.Message or None
    :type response: discord.Embed
    """
    await init.edit(embed=response) if init else await message.channel.send(embed=response)


async def wolframalpha(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    init_message = None
    if cmd.cfg.app_id:
        if not Ongoing.is_ongoing('mathgame', pld.msg.channel.id):
            if pld.args:
                full_results = False
                if len(pld.args) and pld.args[-1].lower() == '--full':
                    pld.args.pop(-1)
                    full_results = True
                query = make_safe_query(pld.args)
                url = f'{api_url}{query}&appid={cmd.cfg.app_id}'
                init_response = discord.Embed(color=0xff7e00)
                init_response.set_author(name='Processing request...', icon_url=wolfram_icon)
                init_message = await pld.msg.channel.send(embed=init_response)
                results = await aioget(url, as_json=True)
                results = WolframResult(results.get('queryresult'))
                if results.success:
                    try:
                        response = discord.Embed(color=0xff7e00)
                        response.set_author(name='Wolfram|Alpha', icon_url=wolfram_icon, url=wolfram_url + query)
                        if full_results:
                            image_set = False
                            for i, pod in enumerate(results.pods):
                                values = []
                                for subpod in pod.subpods:
                                    if subpod.text:
                                        values.append(f'```\n{subpod.text}\n```')
                                    elif subpod.image:
                                        if not image_set:
                                            values.append('(See embedded image)')
                                            response.set_image(url=subpod.image)
                                            image_set = True
                                        else:
                                            values.append(f'[Click to view image]({subpod.image})')
                                if values:
                                    values = '\n'.join(values)
                                    response.add_field(name=f'{i + 1}. {pod.title}', value=values, inline=False)
                            response.set_footer(text='View the results online by clicking the embed title.')
                        else:
                            subpod = results.primary_pod.subpods[0]
                            if subpod.text:
                                response.description = f'```\n{subpod.text}\n```'
                            else:
                                response.set_image(url=subpod.image)
                            response.set_footer(text='Add "--full" to the end to see the full result.')
                            await send_response(pld.msg, init_message, response)
                            return
                    except discord.HTTPException:
                        response = GenericResponse('Results too long to display.').error()
                        response.description = f'You can view them directly [here]({wolfram_url + query}).'
                        await send_response(pld.msg, init_message, response)
                        return
                else:
                    response = GenericResponse('No results.').not_found()
            else:
                response = GenericResponse('Nothing inputted.').error()
        else:
            response = GenericResponse('Wolfram can\'t be used during an ongoing math game.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await send_response(pld.msg, init_message, response)
