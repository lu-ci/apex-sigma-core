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

import re

from sigma.core.utilities.generic_responses import GenericResponse


def check_field(field, value):
    """
    :type field: str
    :type value: str
    :rtype: re.Match
    """
    if field == 'color':
        try:
            int_value = int(value, 16)
            return int_value <= 16777215
        except ValueError:
            return False
    if field in ['thumbnail', 'image']:
        # matches a well-formed URL
        return re.match(r"^(?:http(s)?://)?[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#[\]@!$&'()*+,;=]+$", value)


async def greetembed(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        greet_embed = pld.settings.get('greet_embed') or {}
        embed_data = {
            'active': greet_embed.get('active'),
            'color': greet_embed.get('color'),
            'thumbnail': greet_embed.get('thumbnail'),
            'image': greet_embed.get('image')
        }
        if pld.args:
            queries = ' '.join(pld.args).split()
            qrys = [(f, d, v) for f, d, v in [qry.partition(':') for qry in queries]]
            fields = ['color', 'thumbnail', 'image']
            results = []
            for qry in qrys:
                if qry[1]:
                    field, value = qry[0].lower(), qry[2]
                    if field in fields:
                        if value.lower() == 'remove':
                            embed_data.update({field: None})
                            res = 'Removed'
                        elif check_field(field, value):
                            if field == 'color':
                                value = int(value, 16)
                            embed_data.update({field: value})
                            res = 'Set'
                        else:
                            res = 'Invalid Value'
                    else:
                        res = 'Invalid Field'
                    res_line = f'{field.title()}: {res}'
                    results.append(res_line)
                else:
                    response = GenericResponse('Separate fields and values with a colon.').error()
                    await pld.msg.channel.send(embed=response)
                    return
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'greet_embed', embed_data)
            response = GenericResponse('Greeting Embed updated.').ok()
            response.description = '\n'.join(results)
        else:
            if greet_embed.get('active'):
                state, ender = False, 'disabled'
            else:
                state, ender = True, 'enabled'
            embed_data.update({'active': state})
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'greet_embed', embed_data)
            response = GenericResponse(f'Greeting Embed {ender}.').ok()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
