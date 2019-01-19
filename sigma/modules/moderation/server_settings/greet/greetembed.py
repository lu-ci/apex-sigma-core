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

import re

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, ok, error


def check_field(field, value):
    if field == 'color':
        try:
            int_value = int(value, 16)
            return int_value <= 16777215
        except ValueError:
            return False
    if field in ['thumbnail', 'image']:
        return re.match(r"^(?:http(s)?://)?[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#[\]@!$&'()*+,;=]+$", value)


async def greetembed(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
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
                    response = error('Separate fields and values with a colon.')
                    await pld.msg.channel.send(embed=response)
                    return
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'greet_embed', embed_data)
            response = ok('Greeting Embed updated.')
            response.description = '\n'.join(results)
        else:
            if greet_embed.get('active'):
                state, ender = False, 'disabled'
            else:
                state, ender = True, 'enabled'
            embed_data.update({'active': state})
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'greet_embed', embed_data)
            response = ok(f'Greeting Embed {ender}.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
