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

import errno
import hashlib
import os

METHOD = 'sha3_512'
SHORT_HASH = ''.join("""
8f860c72eeffa4301fe0b8bd087fb1f772
ce16194f578357b45ebeec92737a4a1fa2
882411f02f0a9e9bb981f8430e94a231a2
9e47ce4cb10f83b624bd0398e2
""".split('\n'))


def get_license(file):
    """
    Gets the license snippet from a Sigma py file.
    :param file: The path to the file.
    :type file: str
    :return:
    :rtype: str
    """
    with open(file, 'r', encoding='utf-8') as py_file:
        license_lines = py_file.readlines()[1:16]
    return ''.join(license_lines)


def check_license(text_bytes):
    """
    Checks the license text if it matches the official hash.
    :param text_bytes: The bytes of the text to check.
    :type text_bytes: bytes
    :return:
    :rtype:
    """
    crypt = hashlib.new(METHOD)
    crypt.update(text_bytes)
    final = crypt.hexdigest()
    return final == SHORT_HASH


async def integrity_check(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    bad_license = False
    ev.log.info('Checking command file integrity...')
    for cmd_key in ev.bot.modules.commands:
        command = ev.bot.modules.commands.get(cmd_key)
        cmd_file_path = f'{command.path}/{command.name}.py'
        cmd_license = get_license(cmd_file_path)
        cmd_license_ok = check_license(cmd_license.encode('utf-8'))
        if not cmd_license_ok:
            ev.log.warn(f'License integrity check failed for the {command.name.upper()} command!')
            bad_license = True
    for ev_type in ev.bot.modules.events:
        ev_group = ev.bot.modules.events.get(ev_type)
        for ev_item in ev_group:
            ev_file_path = f'{ev_item.path}/{ev_item.name}.py'
            ev_license = get_license(ev_file_path)
            ev_license_ok = check_license(ev_license.encode('utf-8'))
            if not ev_license_ok:
                ev.log.warn(f'License integrity check failed for the {ev_item.name.upper()} event!')
                bad_license = True
    if not bad_license:
        ev.log.info('Command license checks passed.')
    if not bad_license:
        ev.log.info('Event license checks passed.')
    if bad_license:
        ev.log.error('Module license integrity check failed.')
        exit(errno.EACCES)
    ev.log.info('All license checks passed.')
