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

import discord

from sigma.core.utilities.generic_responses import error, not_found


def get_perm_names(gld: discord.Guild):
    """

    :param gld:
    :type gld:
    :return:
    :rtype:
    """
    return [x[0].replace('_', ' ').title() for x in gld.roles[0].permissions]


def check_perm_validity(gld: discord.Guild, requested: list):
    """

    :param gld:
    :type gld:
    :param requested:
    :type requested:
    :return:
    :rtype:
    """
    invalid_perms = []
    for req in requested:
        valid = False
        for perm in gld.roles[0].permissions:
            if perm[0].replace('_', ' ').lower() == req.lower():
                valid = True
                break
        if not valid:
            invalid_perms.append(req)
    return invalid_perms


async def roleswithpermission(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = pld.args if pld.args else None
    if lookup is not None:
        args, negative = (pld.args[:-1], True) if pld.args[-1].lower() == '--negative' else (pld.args, False)
        perms = [x.strip() for x in ' '.join(args).split(';')] if args else None
        invalid_perms = check_perm_validity(pld.msg.guild, perms)
        if len(invalid_perms) == 0:
            matched_roles = []
            for role in pld.msg.guild.roles:
                valid = True
                for perm in perms:
                    for role_perm in role.permissions:
                        if role_perm[0].replace('_', ' ').lower() == perm.lower():
                            if (role_perm[1] is True and negative) or (role_perm[1] is False and not negative):
                                valid = False
                if valid:
                    matched_roles.append(role)
            if len(matched_roles) != 0:
                response = discord.Embed(color=0xF9F9F9, title=f'📃 Found {len(matched_roles)} roles.')
                response.description = ', '.join([r.name for r in matched_roles])
            else:
                response = not_found('No roles match that search.')
        else:
            ender = 'is' if len(invalid_perms) == 1 else 'are'
            response = error('Unrecognized permissions.')
            response.description = f'I don\'t know what {", ".join(invalid_perms)} {ender}.'
            response.description += f'\nThe available permissions are: {", ".join(get_perm_names(pld.msg.guild))}'
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
