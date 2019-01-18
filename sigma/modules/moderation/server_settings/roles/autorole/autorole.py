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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, ok, error, not_found


async def autorole(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            lookup = ' '.join(pld.args)
            if lookup.lower() != 'disable':
                target_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), pld.msg.guild.roles)
                if target_role:
                    role_bellow = bool(target_role.position < pld.msg.guild.me.top_role.position)
                    if role_bellow:
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'auto_role', target_role.id)
                        response = ok(f'{target_role.name} is now the autorole.')
                    else:
                        response = error('This role is above my highest role.')
                else:
                    response = not_found(f'{lookup} not found.')
            else:
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'auto_role', None)
                response = ok('Autorole has been disabled.')
        else:
            curr_role_id = pld.settings.get('auto_role')
            if curr_role_id:
                curr_role = pld.msg.guild.get_role(curr_role_id)
                if curr_role:
                    response = discord.Embed(color=0xF9F9F9, title=f'📇 The current autorole is **{curr_role}**.')
                else:
                    response = error('An autorole is set but was not found.')
            else:
                response = discord.Embed(color=0xF9F9F9, title='📇 No autorole set.')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)
