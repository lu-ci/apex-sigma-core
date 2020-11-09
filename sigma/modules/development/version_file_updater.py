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

import json

import arrow
import yaml


async def version_file_updater(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    if ev.bot.cfg.pref.dev_mode:
        with open('info/version.yml', 'r') as version_file:
            current_version_data = yaml.safe_load(version_file)
        beta = current_version_data['beta']
        build_date = arrow.utcnow().int_timestamp
        patch = current_version_data['version']['patch'] + 1
        minor = patch // 20
        major = current_version_data['version']['major']
        codename = current_version_data['codename']
        data_out = {
            'beta': beta,
            'build_date': build_date,
            'version': {
                'major': major,
                'minor': minor,
                'patch': patch
            },
            'codename': codename
        }
        with open('info/version.yml', 'w') as version_out:
            yaml.dump(data_out, version_out, default_flow_style=False)
        ev.log.info('Updated Version File.')

        with open('info/version.json', 'w') as version_out:
            json.dump({"version": f'{codename}'}, version_out)
