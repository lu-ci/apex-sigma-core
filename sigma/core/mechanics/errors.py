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


async def make_error_embed(error_file):
    response = discord.Embed(color=0xBE1931, title=f'🚨 Error: `{error_file["token"]}`')
    cmd_text = f'Command: **{error_file["message"]["command"]}**'
    cmd_text += f'\nID: **{error_file["message"]["id"]}**'
    cmd_text += f'\nArguments: **{" ".join(error_file["message"]["arguments"]) or "None"}**'
    orgn_text = f'Author: **{error_file["author"]["name"]}**'
    orgn_text += f'\nAuthor ID: **{error_file["author"]["id"]}**'
    orgn_text += f'\nChannel: **{error_file["channel"]["name"]}**'
    orgn_text += f'\nChannel ID: **{error_file["channel"]["id"]}**'
    orgn_text += f'\nGuild: **{error_file["guild"]["name"]}**'
    orgn_text += f'\nGuild ID: **{error_file["guild"]["id"]}**'
    trace_text = f'Trace Class:\n**{error_file["traceback"]["class"]}**'
    trace_text += f'\nTrace Details:\n```py\n{error_file["traceback"]["details"][:1800]}\n```'
    response.add_field(name='Command', value=cmd_text)
    response.add_field(name='Origin', value=orgn_text)
    return response, trace_text


async def send_error_embed(error_chn, error_data):
    if error_chn:
        response, trace = await make_error_embed(error_data)
        await error_chn.send(embed=response)
        if trace:
            await error_chn.send(trace)
