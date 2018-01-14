import discord

from .nodes.upgrades import upgrade_list


def calculate_upgrade(up_id, level):
    up_table = {
        'stamina': {
            'amount': -(60 - (int(60 - ((60 / 100) * (level * 0.5))))),
            'end': 'Seconds'
        },
        'luck': {
            'amount': 100 - (level * 0.5),
            'end': '% Range'
        },
        'storage': {
            'amount': 64 + (level * 8),
            'end': 'Spaces'
        },
        'oven': {
            'amount': -(3600 - (int(3600 - ((3600 / 100) * (level * 0.2))))),
            'end': 'Seconds'
        },
        'casino': {
            'amount': -(60 - (int(60 - ((60 / 100) * (level * 0.5))))),
            'end': 'Seconds'
        }
    }
    return up_table[up_id]


async def upgrades(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': target.id})
    if upgrade_file is None:
        await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one({'UserID': target.id})
        upgrade_file = {}
    upgrade_text = ''
    upgrade_index = 0
    for upgrade in upgrade_list:
        upgrade_index += 1
        upgrade_id = upgrade['id']
        if upgrade_id in upgrade_file:
            upgrade_level = upgrade_file[upgrade_id]
        else:
            upgrade_level = 0
        up_data = calculate_upgrade(upgrade_id, upgrade_level)
        upgrade_text += f'\n**Level {upgrade_level}** {upgrade["name"]}: **{up_data["amount"]} {up_data["end"]}**'
    upgrade_list_embed = discord.Embed(color=0xF9F9F9, title=f'🛍 {target.display_name}\'s Sigma Upgrades')
    upgrade_list_embed.description = upgrade_text
    await message.channel.send(embed=upgrade_list_embed)
