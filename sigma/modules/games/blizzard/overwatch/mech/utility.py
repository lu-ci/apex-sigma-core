import asyncio

from overwatch_api.core import AsyncOWAPI

ow_cli = AsyncOWAPI(request_timeout=60)
ow_icon = 'https://i.imgur.com/YZ4w2ey.png'
region_convert = {
    'europe': 'eu',
    'korea': 'kr',
    'na': 'us',
    'americas': 'us',
    'america': 'us',
    'china': 'cn',
    'japan': 'jp'
}


def clean_numbers(stats: dict):
    for key in stats:
        try:
            int_value = int(stats.get(key))
            if int_value != stats.get(key):
                int_value = round(stats.get(key), 2)
            stats.update({key: int_value})
        except ValueError:
            pass
        except TypeError:
            pass
    return stats


async def get_profile(battletag: str, region: str):
    profile = None
    timeout = False
    failed = False
    try:
        profile = await ow_cli.get_profile(battletag, regions=region)
    except asyncio.TimeoutError:
        timeout = True
    except Exception:
        failed = True
    return profile, timeout, failed
