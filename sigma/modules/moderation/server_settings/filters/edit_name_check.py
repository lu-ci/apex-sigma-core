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

import string


def is_invalid(name):
    """

    :param name:
    :type name: str
    :return:
    :rtype: bool
    """
    invalid = False
    for char in name:
        if char not in string.printable:
            invalid = True
            break
    return invalid


def clean_name(name, default):
    """

    :param name:
    :type name: str
    :param default:
    :type default: str
    :return:
    :rtype: str
    """
    end_name = ''
    for char in str(name):
        if char in string.printable:
            end_name += char
    if not end_name:
        end_name = default
    return end_name.strip()


async def edit_name_check(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MemberUpdatePayload
    """
    if pld.after.guild:
        is_owner = pld.after.id in ev.bot.cfg.dsc.owners
        if not any([pld.after.guild_permissions.administrator, is_owner]):
            if pld.before.display_name != pld.after.display_name:
                active = pld.settings.get('ascii_only_names')
                if active:
                    if is_invalid(pld.after.display_name):
                        # noinspection PyBroadException
                        try:
                            temp_name = pld.settings.get('ascii_temp_name', '<Change My Name>')
                            new_name = clean_name(pld.after.display_name, temp_name)
                            await pld.after.edit(nick=new_name, reason='ASCII name enforcement.')
                        except Exception:
                            pass
