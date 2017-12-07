import discord

from sigma.core.utilities.data_processing import user_avatar


def count_all_commands(db, user):
    cmd_items = db[db.db_cfg.database]['CommandStats'].aggregate(
        [
            {'$match': {
                'author': user.id
            }},
            {"$group": {
                "_id": {
                    "command": "$command.name",
                },
                "count": {"$sum": 1}
            }}
        ]
    )
    output = {}
    total = 0
    for x in cmd_items:
        output.update({x['_id']['command']: x['count']})
        total += x['count']
    return output, total


async def profile(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    commands, total_commands = count_all_commands(cmd.db, target)
    exp = await cmd.db.get_experience(target, message.guild)
    global_level = int((exp['global'] // ((((exp['global'] // 690) * 0.0125) + 1) * 690)))
    top_cmd = {'cmd': None, 'val': 0}
    for command in commands:
        if commands[command] > top_cmd['val']:
            top_cmd = {'cmd': command, 'val': commands[command]}
    if total_commands != 0:
        cmd_percentage = int((top_cmd['val'] / total_commands) * 100)
    else:
        cmd_percentage = 0
    cmd_stats = f'Level: {global_level}'
    cmd_stats += f'\nMost Used: {top_cmd["cmd"]}'
    cmd_stats += f'\nCount: {top_cmd["val"]} ({cmd_percentage}%)'
    cmd_stats += f'\nTotal: {total_commands} Commands'
    response = discord.Embed(color=target.color)
    response.set_thumbnail(url=avatar)
    response.add_field(name=f'{target.display_name}\'s Profile', value=cmd_stats)
    await message.channel.send(embed=response)
