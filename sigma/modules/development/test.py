import copy


async def test(cmd, message, args):
    coll = cmd.db.aurora.CommandStats
    all_cmds = coll.find({})
    total = await all_cmds.count()
    all_cmds = await all_cmds.to_list(None)
    current = 0
    for item in all_cmds:
        current += 1
        if not isinstance(item['command'], str):
            cmd_name = item['command']['name']
            new = copy.deepcopy(item)
            new.update({'command': cmd_name})
            coll.update_one(item, {'$set': new})
    await message.channel.send('All good!')
