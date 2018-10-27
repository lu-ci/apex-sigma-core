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


async def colorme(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if not message.guild.me.top_role.position <= message.author.top_role.position:
        enabled = pld.settings.get('color_roles')
        if enabled:
            if args:
                bad_hex = False
                hex_req = args[0].lower().strip('#')
                if len(hex_req) == 3:
                    hex_req = hex_req * 2
                if len(hex_req) != 6:
                    bad_hex = True
                if not bad_hex:
                    role_name = f'SCR-{hex_req.upper()}'
                    role_posi = message.author.top_role.position + 1
                    role_objc = discord.utils.find(lambda role: role.name == role_name, message.guild.roles)
                    if not role_objc:
                        color_int = int(f'0x{hex_req}', 16)
                        role_color = discord.Color(color_int)
                        role_objc = await message.guild.create_role(name=role_name, color=role_color)
                        await role_objc.edit(position=role_posi)
                    for member_role in message.author.roles:
                        if member_role.name.startswith('SCR-'):
                            await message.author.remove_roles(member_role, reason='Assigning new color role.')
                    await message.author.add_roles(role_objc, reason='Assigned color role.')
                    addition_title = f'✅ {role_objc.name} has been added to you, {message.author.name}.'
                    response = discord.Embed(color=0x77B255, title=addition_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid HEX color code.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No color HEX provided.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'⛔ Color roles are not enabled.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ I can\'t make a color role with my current role position.')
    await message.channel.send(embed=response)
