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

import discord
import wolframalpha as wa_wrapper

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.minigames.quiz.mathgame import ongoing_list as math_chs


async def wolframalpha(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.channel.id not in math_chs:
        if 'app_id' in cmd.cfg:
            if not args:
                response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
            else:
                wa_q = ' '.join(args)
                wac = wa_wrapper.Client(cmd.cfg['app_id'])
                results = wac.query(wa_q)
                # noinspection PyBroadException
                try:
                    response = discord.Embed(type='rich', color=0x66cc66, title='✅ Processing Done')
                    for res in results.results:
                        if int(res['@numsubpods']) == 1:
                            output = res['subpod']['plaintext'][:500]
                        else:
                            output = res['subpod'][0]['img']['@title'][:500]
                        response.add_field(name=res['@title'], value='```\n' + output + '\n```')
                except Exception:
                    title = '❗ We were unable to process that.'
                    response = discord.Embed(color=0xBE1931, title=title)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Wolfram can\'t be used during an ongoing math game.')
    await message.channel.send(embed=response)
