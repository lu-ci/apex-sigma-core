import secrets

from sigma.core.utilities.stats_processing import add_special_stats


async def table_unflipper(ev, message):
    if '(╯°□°）╯︵ ┻━┻'.replace(' ', '') in message.content.replace(' ', ''):
        if message.guild:
            flip_settings = await ev.db.get_guild_settings(message.guild.id, 'Unflip')
            if flip_settings is None:
                unflip = False
            else:
                unflip = flip_settings
        else:
            unflip = True
        if unflip:
            await add_special_stats(ev.db, 'tables_fixed')
            table = ['┬─┬ ノ( ^_^ノ)',
                     '┬─┬ ﾉ(° -°ﾉ)',
                     '┬─┬ ノ(゜-゜ノ)',
                     '┬─┬ ノ(ಠ\_ಠノ)',
                     '┻━┻~~~~  ╯(°□° ╯)',
                     '┻━┻====  ╯(°□° ╯)',
                     ' ┬──┬﻿ ¯\_(ツ)',
                     '(ヘ･_･)ヘ┳━┳',
                     'ヘ(´° □°)ヘ┳━┳']
            table_resp = secrets.choice(table)
            await message.channel.send(table_resp)
