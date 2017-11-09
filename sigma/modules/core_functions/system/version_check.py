import json

import aiohttp


async def version_check(ev):
    version_url = 'https://api.lucia.moe/data/version'
    async with aiohttp.ClientSession() as session:
        async with session.get(version_url) as version_data:
            data = await version_data.read()
            data = json.loads(data)
    official_stamp = data['build_date']
    current_stamp = ev.bot.info.version.timestamp
    if official_stamp > current_stamp:
        current = f'{ev.bot.info.version.major}.{ev.bot.info.version.minor}.{ev.bot.info.version.patch}'
        current += f' {ev.bot.info.version.codename}'
        latest = f'{data["version"]["major"]}.{data["version"]["minor"]}.{data["version"]["patch"]}'
        latest += f' {data["codename"]}'
        ev.log.warning('---------------------------------')
        ev.log.warning('Your Sigma version is outdated.')
        ev.log.warning(f'CURRENT: {current}')
        ev.log.warning(f'LATEST:  {latest}')
        ev.log.warning('Updating is strongly suggested.')
        ev.log.warning('---------------------------------')
