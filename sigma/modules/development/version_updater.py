import json

import arrow
import yaml


async def version_updater(ev):
    if ev.bot.cfg.pref.dev_mode:
        with open('info/version.yml', 'r') as version_file:
            current_version_data = yaml.safe_load(version_file)
        beta = current_version_data['beta']
        build_date = arrow.utcnow().timestamp
        major = current_version_data['version']['major']
        minor = current_version_data['version']['minor']
        patch = current_version_data['version']['patch'] + 1
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
            json.dump({"version": f'{major}.{minor}.{patch}'}, version_out)
