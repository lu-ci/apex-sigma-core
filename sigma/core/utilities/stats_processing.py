import arrow


async def add_cmd_stat(db, cmd, message, args, command_id):
    if not message.author.bot:
        if message.guild:
            channel_id = message.channel.id
            guild_id = message.guild.id
        else:
            channel_id = None
            guild_id = None
        stat_data = {
            'command': cmd.name,
            'args': args,
            'author': message.author.id,
            'channel': channel_id,
            'guild': guild_id,
            'timestamp': arrow.utcnow().float_timestamp,
            'id': command_id
        }
        db[db.db_cfg.database]['CommandStats'].insert_one(stat_data)


async def add_special_stats(db, stat_name):
    collection = 'SpecialStats'
    def_stat_data = {
        'name': stat_name,
        'count': 0
    }
    check = db[db.db_cfg.database][collection].find_one({"name": stat_name})
    if not check:
        db[db.db_cfg.database][collection].insert_one(def_stat_data)
        ev_count = 0
    else:
        ev_count = check['count']
    ev_count += 1
    updatetarget = {"name": stat_name}
    updatedata = {"$set": {'count': ev_count}}
    db[db.db_cfg.database][collection].update_one(updatetarget, updatedata)
